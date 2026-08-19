import re,html,sys
page=open('/Users/michelleegle/hustle/portfolio/bench02/index.html',encoding='utf-8').read()
qs=re.findall(r'<q>(.*?)</q>', page, flags=re.S)
def norm(s):
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    for a,b in [('’',"'"),('‘',"'"),('“','"'),('”','"'),('—','-'),('–','-')]:
        s=s.replace(a,b)
    return re.sub(r'\s+',' ',s).strip().strip('"')
srcs={}
for name,f in [('TNW','/tmp/tnw.txt'),('REGISTER','/tmp/reg.txt')]:
    srcs[name]=norm(open(f,encoding='utf-8').read())
print("quoted strings on page:",len(qs))
bad=0
for q in qs:
    n=norm(q).rstrip(',.')
    where=[k for k,v in srcs.items() if n in v]
    if not where: bad+=1
    print(("  OK  ["+where[0]+"]" if where else "  FAIL     "), n[:100])
print("\nFAILURES:",bad)
sys.exit(1 if bad else 0)
