"""Release metadata only. No private repository, user data or application source is read."""
import json,os,re,urllib.request,base64,hashlib
REPO=os.environ['GITHUB_REPOSITORY'];API='https://api.github.com/repos/'+REPO
HEADERS={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','User-Agent':'TRAPS-distribution'}
def request(path,method='GET',data=None,accept=None):
    h=dict(HEADERS)
    if accept:h['Accept']=accept
    if data is not None:data=json.dumps(data).encode();h['Content-Type']='application/json'
    with urllib.request.urlopen(urllib.request.Request(API+path,data=data,method=method,headers=h),timeout=30) as r:
        raw=r.read()
        if r.status==204:return None
        return raw if accept=='application/octet-stream' else json.loads(raw)
releases=[];page=1
while True:
    batch=request('/releases?per_page=100&page='+str(page));releases+=batch
    if len(batch)<100:break
    page+=1
apps={'traps':[],'jugement':[]};known=[]
for r in releases:
    if r.get('draft') or r.get('prerelease'):continue
    metadata=next((a for a in r['assets'] if a['name']=='release.json'),None)
    if not metadata:continue
    value=json.loads(request('/releases/assets/'+str(metadata['id']),accept='application/octet-stream'))
    app=value.get('app');build=value.get('build');name=value.get('file','');sha=value.get('sha256','')
    if app not in apps or type(build)is not int or build<=0 or not re.fullmatch('[a-f0-9]{64}',sha):raise ValueError('Métadonnées de version invalides')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+\.(apk|exe)',name):raise ValueError('Nom de téléchargement invalide')
    asset=next(a for a in r['assets'] if a['name']==name)
    digest=asset.get('digest')
    if digest and digest!='sha256:'+sha:raise ValueError('Empreinte différente du fichier GitHub')
    expected=('traps-' if app=='traps' else 'jugement-')+str(build)
    if r['tag_name']!=expected:raise ValueError('Tag et version différents')
    entry=dict(build=build,version=value['version'],url=asset['browser_download_url'],page=r['html_url'],sha256=sha,bytes=asset['size'],_release=r['id'])
    if app=='jugement' and 'installerProtocol' in value:
        if type(value['installerProtocol'])is not int or value['installerProtocol']!=1 or not re.fullmatch('[a-f0-9]{64}',value.get('licenseSha256','')):raise ValueError('Protocole ou licence de mise à jour invalide')
        entry.update(installerProtocol=1,licenseSha256=value['licenseSha256'])
    apps[app].append(entry)
# Publish a catalogue with ten entries first, before removing any superseded downloads.
catalog={'schema':1,'applications':{}}
old=[]
for app,items in apps.items():
    items.sort(key=lambda x:x['build'],reverse=True)
    if len({x['build'] for x in items})!=len(items):raise ValueError('Versions dupliquées')
    old+=items[10:];kept=[{k:v for k,v in x.items() if k!='_release'} for x in items[:10]]
    catalog['applications'][app]={'latest':kept[0] if kept else None,'releases':kept}
content=(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n').encode();current=request('/contents/catalog.json')
if base64.b64decode(current['content'])!=content:
    request('/contents/catalog.json','PUT',dict(message='Actualise les versions publiées',sha=current['sha'],content=base64.b64encode(content).decode()))
for item in old:request('/releases/'+str(item['_release']),'DELETE')
print('Catalogue publié ; dix versions maximum conservées par application.')
