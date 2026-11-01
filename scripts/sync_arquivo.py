"""Exporta os campos de apresentação do arquivo Necrostone para GitHub Pages.
Só executar com uma integração Notion autorizada para publicação pública.
"""
import os,json,time,urllib.request,urllib.error
from pathlib import Path
token=os.environ.get("NOTION_TOKEN")
database=os.environ.get("NOTION_DATABASE_ID")
if not token or not database:
    raise SystemExit("Configurar os secrets NOTION_TOKEN e NOTION_DATABASE_ID no GitHub.")
headers={"Authorization":"Bearer "+token,"Notion-Version":"2022-06-28","Content-Type":"application/json"}
def query(cursor=None):
    payload={"page_size":100}
    if cursor: payload["start_cursor"]=cursor
    req=urllib.request.Request("https://api.notion.com/v1/databases/"+database+"/query",data=json.dumps(payload).encode(),headers=headers,method="POST")
    with urllib.request.urlopen(req,timeout=45) as response: return json.load(response)
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
rows=[];cursor=None
while True:
    batch=query(cursor)
    for page in batch.get("results",[]):
        if page.get("archived"):continue
        p=page.get("properties",{})
        name=plain(p.get("Nome"))
        if not name:continue
        rows.append({"nome":name,"areas":multi(p.get("Área ")),"cemiterios":multi(p.get("Cemitério ")),"rotas":multi(p.get("Rota")),"nascimento":plain(p.get("Data de nascimento ")),"morte":plain(p.get("Data de morte")),"foto":""})
    if not batch.get("has_more"):break
    cursor=batch.get("next_cursor")
    time.sleep(.35)
path=Path("arquivo-prototipo/dados-publicos.json")
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(rows,ensure_ascii=False,indent=1),encoding="utf-8")
print("Exportados",len(rows),"registos")
