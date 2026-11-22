import json,sys,glob,re
def load(path):
    s=open(path).read()
    i=s.find('{"ccr"'); j=s.rfind('</other-session')
    body=s[i:j].strip()
    return json.loads(body)['ccr']
if __name__=='__main__':
    for p in sys.argv[1:]:
        c=load(p); print(p[-30:], len(c['data']), c.get('first_id'), c.get('last_id'), c.get('has_more'))
