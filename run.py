"""Token-free BETLOG updater bootstrap. Credentials remain in runner memory."""
import os,sys,io,json,urllib.request,urllib.parse,hashlib
EXPECTED_SHA256='c1dca5244b53828e39dd33e933f8de84eee2d78fd103bfa4cd4e01f50b828e4a'
origin=os.environ.get('BETLOG_SITE_URL','').rstrip('/')
token=os.environ.get('BETLOG_SITE_TOKEN','')
u=urllib.parse.urlparse(origin)
if u.scheme!='https' or not u.hostname or not u.hostname.endswith('.chatgpt.site') or u.path or u.query or u.fragment or u.username or u.password:
 raise SystemExit('Set BETLOG_SITE_URL to the private Site origin in repository secrets.')
if not token:raise SystemExit('Set BETLOG_SITE_TOKEN in repository secrets.')
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise RuntimeError('Cross-origin redirect refused')
try:
 request=urllib.request.Request(origin+'/automation/betlog-runner.py',headers={'OAI-Sites-Authorization':'Bearer '+token})
 with urllib.request.build_opener(NoRedirect()).open(request,timeout=30) as response:code=response.read(100000)
 if hashlib.sha256(code).hexdigest()!=EXPECTED_SHA256:raise RuntimeError('Updater integrity check failed; update the reviewed scheduler package.')
 sys.stdin=io.StringIO(json.dumps({'url':origin,'token':token,'scheduler':'github-actions'})+'\n')
 exec(compile(code,'verified-betlog-runner','exec'),{'__name__':'__main__'})
except Exception:
 # Never print request headers, environment values or credential-bearing exceptions.
 raise SystemExit('BETLOG update failed. Check the Site connection and the scheduler package; credentials were not logged.')
