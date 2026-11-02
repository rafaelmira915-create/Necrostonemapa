"""Exporta os campos de apresentação do arquivo Necrostone para GitHub Pages.
Só executar com uma integração Notion autorizada para publicação pública.
"""
import os,json,time,urllib.request,urllib.error,hashlib,re,unicodedata
from pathlib import Path
token=os.environ.get("NOTION_TOKEN")
database=os.environ.get("NOTION_DATABASE_ID","")
if not token:
    raise SystemExit("Configurar o secret NOTION_TOKEN no GitHub.")
headers={"Authorization":"Bearer "+token,"Notion-Version":"2025-09-03","Content-Type":"application/json"}
def resolve_data_source():
    # Find the actual API data source ID; connector collection IDs are not API IDs.
    payload=json.dumps({"query":"Arquivo Necrostone","page_size":100}).encode()
    req=urllib.request.Request("https://api.notion.com/v1/search",data=payload,headers=headers,method="POST")
    with urllib.request.urlopen(req,timeout=45) as response:
        found=json.load(response)
    matches=[]
    for item in found.get("results",[]):
        if item.get("object")!="data_source": continue
        title="".join(t.get("plain_text","") for t in item.get("title",[]))
        if title.strip().casefold()=="arquivo necrostone":
            matches.append(item["id"])
    if len(matches)!=1:
        raise SystemExit(f"Encontradas {len(matches)} fontes com o nome Arquivo Necrostone. Verificar acesso ou duplicados.")
    return matches[0]
data_source=database or resolve_data_source()
def query(cursor=None):
    payload={"page_size":100}
    if cursor: payload["start_cursor"]=cursor
    req=urllib.request.Request("https://api.notion.com/v1/data_sources/"+data_source+"/query",data=json.dumps(payload).encode(),headers=headers,method="POST")
    try:
        with urllib.request.urlopen(req,timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body=exc.read().decode("utf-8",errors="replace")
        try:
            detail=json.loads(body)
            # Never log tokens or request headers.
            code=detail.get("code","unknown")
            message=detail.get("message","")
            raise SystemExit(f"Notion API HTTP {exc.code} ({code}): {message}")
        except (ValueError,TypeError):
            raise SystemExit(f"Notion API HTTP {exc.code}: resposta inválida")

def plain(prop):
    if not prop:return ""
    kind=prop.get("type","")
    if kind in ("title","rich_text"):return "".join(x.get("plain_text","") for x in prop.get(kind,[]))
    if kind=="date":return (prop.get("date") or {}).get("start") or ""
    return ""
def multi(prop):
    if not prop:return []
    kind=prop.get("type")
    if kind=="multi_select":return [x["name"] for x in prop.get("multi_select",[])]
    if kind=="select":return [prop["select"]["name"]] if prop.get("select") else []
    return []
def photo_items(properties):
    for key,value in properties.items():
        normalized="".join(ch for ch in unicodedata.normalize("NFD",key.casefold()) if unicodedata.category(ch)!="Mn")
        if "foto" not in normalized and "imagem" not in normalized and "retrato" not in normalized:
            continue
        if value.get("type")=="files":
            for item in value.get("files",[]):
                url=(item.get("file") or item.get("external") or {}).get("url","")
                if url.startswith("https://"): yield url
        elif value.get("type") in ("url","rich_text"):
            url=value.get("url") if value.get("type")=="url" else plain(value)
            if url and url.startswith("https://"): yield url

images_dir=Path("arquivo-prototipo/fotos")
images_dir.mkdir(parents=True,exist_ok=True)
new_images=0
def store_photo(page,properties):
    global new_images
    candidates=list(photo_items(properties))
    if not candidates:return ""
    stem=re.sub(r"[^a-f0-9]","",page["id"].lower())
    for ext in (".jpg",".png",".webp"):
        existing=images_dir/(stem+ext)
        if existing.exists():return "fotos/"+existing.name
    # Avoid oversized Git commits; subsequent scheduled syncs continue the import.
    if new_images>=250:return ""
    for url in candidates[:1]:
        try:
            request=urllib.request.Request(url,headers={"User-Agent":"NecrostoneArchiveSync/1.0"})
            with urllib.request.urlopen(request,timeout=20) as response:
                typ=response.headers.get("Content-Type","").split(";")[0].lower()
                ext={ "image/jpeg":".jpg","image/png":".png","image/webp":".webp"}.get(typ)
                if not ext:continue
                content=response.read(3_000_001)
                if len(content)>3_000_000:continue
            (images_dir/(stem+ext)).write_bytes(content)
            new_images+=1
            return "fotos/"+stem+ext
        except (OSError,urllib.error.URLError,TimeoutError):
            continue
    return ""

rows=[];cursor=None
while True:
    batch=query(cursor)
    for page in batch.get("results",[]):
        if page.get("archived"):continue
        p=page.get("properties",{})
        name=plain(p.get("Nome"))
        if not name:continue
        rows.append({"nome":name,"areas":multi(p.get("Área ")),"cemiterios":multi(p.get("Cemitério ")),"rotas":multi(p.get("Rota")),"nascimento":plain(p.get("Data de nascimento ")),"morte":plain(p.get("Data de morte")),"foto":store_photo(page,p)})
    if not batch.get("has_more"):break
    cursor=batch.get("next_cursor")
    time.sleep(.35)
path=Path("arquivo-prototipo/dados-publicos.json")
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(rows,ensure_ascii=False,indent=1),encoding="utf-8")
print("Exportados",len(rows),"registos; novas fotografias:",new_images)
