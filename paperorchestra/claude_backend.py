"""Route PaperOrchestra's LLM calls through the Claude Code CLI (`claude -p`).

PaperOrchestra sends every Gemini request through one function,
``utils.gemini_utils.call_gemini_with_contents``. That covers the outline,
literature search, section writing, refinement and PDF review. This module
swaps in a replacement that runs headless Claude Code, so inference uses the
login of whatever Claude Code is installed (a Pro/Max subscription on a
laptop, or the session's own credentials in a Claude Code cloud session).
No Anthropic, Gemini or OpenAI API key is needed.

How each Gemini feature is handled:
  * text parts             -> the prompt (sent on stdin)
  * system_instruction     -> --system-prompt-file (replaces Claude Code's default prompt)
  * google_search tool     -> the WebSearch tool, which runs on Anthropic's side
                              (WebFetch stays off, so the container's network allowlist is unchanged)
  * PDF / image parts      -> written to a temp dir that Claude reads with the Read tool;
                              PDFs also get their extracted text inlined
  * temperature, etc.      -> ignored (Claude Code exposes no sampling controls)
  * image generation       -> unsupported (only the plotting agent uses it; keep --use_plotting false)

Configuration (environment variables):
  PO_CLAUDE_MODEL          model for writer/reflection calls   (default: opus)
  PO_CLAUDE_FAST_MODEL     model for "flash" calls: search, parsing (default: sonnet)
  PO_CLAUDE_EFFORT         optional --effort level (low|medium|high|xhigh|max)
  PO_CLAUDE_CONCURRENCY    max simultaneous claude processes   (default: 3)
  PO_CLAUDE_TIMEOUT        seconds per call                    (default: 1800)
  PO_CLAUDE_BIN            path to the claude executable       (default: claude)
  PO_CLAUDE_LOG_DIR        if set, every prompt/response is saved there
"""

import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

DEFAULT_SYSTEM = (
    "You are an expert AI research scientist and technical writer. "
    "Follow the user's instructions exactly, including any required output format "
    "(for example fenced ```json or ```latex blocks). Answer directly."
)

_sem = threading.BoundedSemaphore(int(os.environ.get("PO_CLAUDE_CONCURRENCY", "3")))
_counter = 0
_counter_lock = threading.Lock()


def _resolve_model(model_name: str) -> str:
    name = (model_name or "").lower()
    if name.startswith("claude") or name in {"opus", "sonnet", "haiku", "fable"}:
        return model_name
    if "flash" in name or "lite" in name:
        return os.environ.get("PO_CLAUDE_FAST_MODEL", "sonnet")
    return os.environ.get("PO_CLAUDE_MODEL", "opus")


def _uses_search(configs) -> bool:
    for tool in (configs or {}).get("tools", []) or []:
        if getattr(tool, "google_search", None) is not None or "google_search" in str(tool):
            return True
    return False


def _pdf_text(path: Path) -> str:
    try:
        import pymupdf4llm

        return pymupdf4llm.to_markdown(str(path))
    except Exception as e:  # text extraction is a convenience; Read still works
        return f"[text extraction failed: {e}]"


def _render_contents(contents, workdir: Path):
    """Turn Gemini `contents` into (prompt_text, attached_file_paths)."""
    if not isinstance(contents, (list, tuple)):
        contents = [contents]
    chunks, files = [], []
    for item in contents:
        if isinstance(item, str):
            chunks.append(item)
            continue
        parts = getattr(item, "parts", None)
        for part in parts if parts else [item]:
            text = getattr(part, "text", None)
            blob = getattr(part, "inline_data", None)
            if text:
                chunks.append(text)
            elif blob is not None and getattr(blob, "data", None):
                mime = blob.mime_type or "application/octet-stream"
                ext = {"application/pdf": ".pdf", "image/png": ".png",
                       "image/jpeg": ".jpg"}.get(mime, ".bin")
                path = workdir / f"attachment_{len(files) + 1}{ext}"
                path.write_bytes(blob.data)
                files.append(path)
                if ext == ".pdf":
                    chunks.append(
                        f"[Attached PDF: {path}. Its extracted text follows; use the Read "
                        f"tool on the file to inspect layout, figures and rendering.]\n"
                        + _pdf_text(path)
                    )
                else:
                    chunks.append(f"[Attached image: {path}. View it with the Read tool.]")
            elif part is not None and not text:
                chunks.append(str(part))
    return "\n\n".join(chunks), files


def _log(prompt, system, result):
    log_dir = os.environ.get("PO_CLAUDE_LOG_DIR")
    if not log_dir:
        return
    global _counter
    with _counter_lock:
        _counter += 1
        n = _counter
    d = Path(log_dir)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{n:04d}.json").write_text(
        json.dumps({"system": system, "prompt": prompt, "result": result}, indent=1),
        encoding="utf-8",
    )


def claude_call(contents, model_name: str, generation_configs=None) -> str:
    configs = dict(generation_configs or {})
    model = _resolve_model(model_name)
    system = configs.get("system_instruction") or DEFAULT_SYSTEM
    if not isinstance(system, str):
        system = _render_contents(system, Path(tempfile.gettempdir()))[0]

    workdir = Path(tempfile.mkdtemp(prefix="po_claude_"))
    try:
        prompt, files = _render_contents(contents, workdir)
        tools = []
        if files:
            tools.append("Read")
        if _uses_search(configs):
            tools.append("WebSearch")
            system += (
                "\n\nYou have a WebSearch tool. Use it in place of Google Search to find "
                "and verify real papers. Never invent papers, titles, authors or years."
            )
        sys_file = workdir / "system_prompt.txt"
        sys_file.write_text(system, encoding="utf-8")

        cmd = [
            os.environ.get("PO_CLAUDE_BIN", "claude"), "-p",
            "--output-format", "json",
            "--model", model,
            "--system-prompt-file", str(sys_file),
            "--tools", ",".join(tools),
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--setting-sources", "user",
        ]
        if tools:
            cmd += ["--allowedTools", ",".join(tools), "--add-dir", str(workdir)]
        if os.environ.get("PO_CLAUDE_EFFORT"):
            cmd += ["--effort", os.environ["PO_CLAUDE_EFFORT"]]

        env = dict(os.environ)
        env.pop("CLAUDECODE", None)  # allow running inside a Claude Code session
        env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "64000")  # full-paper LaTeX outputs

        with _sem:
            proc = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, cwd=workdir, env=env,
                timeout=int(os.environ.get("PO_CLAUDE_TIMEOUT", "1800")),
            )
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"claude exited {proc.returncode}: {proc.stderr.strip()[:1000] or proc.stdout[:1000]}"
            )
        if out.get("is_error") or proc.returncode != 0:
            raise RuntimeError(f"claude error ({out.get('subtype')}): {str(out.get('result'))[:1000]}")
        result = out.get("result") or ""
        _log(prompt, system, result)
        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def call_claude_with_contents(
    contents,
    model_name: str,
    max_retries: int = 5,
    base_interval_sec: int = 5,
    result_parsing_func=None,
    generation_configs: dict = {},
    check_parsed_response_not_none: bool = True,
):
    """Drop-in replacement for utils.gemini_utils.call_gemini_with_contents."""
    from utils.gemini_utils import parse_gemini_json_results

    parse = result_parsing_func or parse_gemini_json_results
    raw = parsed = None
    for attempt in range(max_retries):
        try:
            raw = claude_call(contents, model_name, generation_configs)
            parsed = parse(raw)
            if check_parsed_response_not_none:
                assert parsed is not None, f"Parsed response is None. Raw response:\n{raw[:2000]}"
            return {"raw_response": raw, "parsed_response": parsed}
        except Exception as e:
            print(f"Warning: Claude Code call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(base_interval_sec * (2 ** attempt))
    return {"raw_response": raw, "parsed_response": parsed}


def _no_image_generation(*args, **kwargs):
    raise NotImplementedError(
        "Image generation is not available through Claude Code. Run with --use_plotting false."
    )


def install():
    """Patch every module that holds a reference to the Gemini call."""
    import importlib

    if shutil.which(os.environ.get("PO_CLAUDE_BIN", "claude")) is None:
        raise SystemExit("claude CLI not found; install Claude Code and log in (`claude` then /login).")

    modules = [
        "utils.gemini_utils",
        "utils.llm_backend_utils",
        "utils.content_parsing_utils",
        "utils.paper_banana_utils",
        "methods.agents.outline_agent",
        "methods.agents.literature_review_agent",
        "methods.agents.section_writing_agent",
        "methods.agents.content_refinement_agent",
        "methods.agents.plotting_agent",
    ]
    for name in modules:
        try:
            mod = importlib.import_module(name)
        except Exception as e:
            print(f"[claude_backend] skipped {name}: {e}")
            continue
        if hasattr(mod, "call_gemini_with_contents"):
            mod.call_gemini_with_contents = call_claude_with_contents
        if hasattr(mod, "generate_image_with_gemini"):
            mod.generate_image_with_gemini = _no_image_generation
    print(
        f"[claude_backend] LLM calls -> Claude Code CLI "
        f"(model={os.environ.get('PO_CLAUDE_MODEL', 'opus')}, "
        f"fast={os.environ.get('PO_CLAUDE_FAST_MODEL', 'sonnet')})"
    )
