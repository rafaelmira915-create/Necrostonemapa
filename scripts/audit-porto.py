"""Audit published Porto snapshots without changing cemetery facts.

Run from any directory: python scripts/audit-porto.py
Structural checks are not documentary validation or an exhaustive inventory.
"""
import collections
import csv
import io
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/audits/porto-2026-10-29'
OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'data/distrito-porto/index.json').read_text())
documents=[json.loads((ROOT/f'data/distrito-porto/{slug}.json').read_text()) for slug in manifest]
assert len(documents)==18

def ring(point,points):
    x,y=point;result=False
    for a,b in zip(points,points[1:]+points[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
    return result

def inside(point,geometry):
    polygons=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
    return any(ring(point,p[0]) and not any(ring(point,h) for h in p[1:]) for p in polygons)

rows=[];parishes=[];municipalities=[];errors=[];unlocated=[]
for doc in documents:
    start=len(rows)
    for record in doc['records']:
        cs=record['cemeteries']
        parishes.append({'municipality':doc['municipality'],'parish':record['name'],'mappedCemeteries':len(cs),'geometryPresent':bool(record.get('feature')),'documentaryEvidenceRecords':sum(bool(c.get('evidence')) for c in cs),'inventoryCompleteness':'não demonstrada'})
        for pending in record.get('pendingCemeteries',[]):
            unlocated.append({'municipality':doc['municipality'],'parish':record['name'],**pending})
        for c in cs:
            xy=c.get('coordinates');valid=isinstance(xy,list) and len(xy)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) for v in xy) and -180<=xy[0]<=180 and -90<=xy[1]<=90
            in_parish=valid and bool(record.get('feature')) and inside(xy,record['feature']['geometry'])
            if not valid:errors.append(c['id']+': coordenadas inválidas')
            if not in_parish:errors.append(c['id']+': ponto fora da freguesia ou geometria em falta')
            pending_fields=[]
            if not c.get('named'):pending_fields.append('nome documental')
            if not c.get('officialCoordinates'):pending_fields.append('coordenadas oficiais')
            if c.get('areaM2') is None:pending_fields.append('área')
            if c.get('year') is None and not c.get('openingPeriod'):pending_fields.append('inauguração')
            if not c.get('summary') or c['summary'].startswith('Registo cartográfico'):pending_fields.append('descrição documental')
            if c.get('photo',{}).get('kind')!='ground':pending_fields.append('fotografia identificada')
            if not c.get('visit360Url') and not c.get('visita360Url'):pending_fields.append('visita 360° não identificada')
            rows.append({'municipality':doc['municipality'],'parish':record['name'],'id':c['id'],'name':c['name'],'coordinates':xy,'pointInsideStoredParish':in_parish,'officialCoordinates':c.get('officialCoordinates'),'address':c.get('address'),'areaM2':c.get('areaM2'),'year':c.get('year'),'openingPeriod':c.get('openingPeriod'),'photoKind':c.get('photo',{}).get('kind'),'photoUrl':c.get('photo',{}).get('url'),'visit360Url':c.get('visit360Url') or c.get('visita360Url'),'documentaryEvidenceAdded':bool(c.get('evidence')),'sourceUrl':c.get('sourceUrl'),'pending':pending_fields})
    local=rows[start:]
    municipalities.append({'municipality':doc['municipality'],'parishes':len(doc['records']),'cemeteries':len(local),'withEvidenceAdded':sum(r['documentaryEvidenceAdded'] for r in local),'namesPending':sum('nome documental' in r['pending'] for r in local),'areaPresent':sum(r['areaM2'] is not None for r in local),'openingPresent':sum(r['year'] is not None or bool(r['openingPeriod']) for r in local),'groundPhotos':sum(r['photoKind']=='ground' for r in local)})
ids=collections.Counter(r['id'] for r in rows)
errors.extend('ID duplicado: '+k for k,n in ids.items() if n>1)
summary={'reviewDate':'2026-10-29','status':'parcial — inventário e validação documental não concluídos','scope':'Revisão estrutural dos 425 registos existentes e das 275 fichas existentes; pesquisa documental dirigida. Não equivale a pesquisa documental individual de todos os cemitérios nem a prova de cobertura de todas as freguesias atuais.','totals':{'municipalities':len(documents),'storedParishes':len(parishes),'mappedCemeteries':len(rows),'documentaryEvidenceAdded':sum(r['documentaryEvidenceAdded'] for r in rows),'namesPending':sum('nome documental' in r['pending'] for r in rows),'areaPresent':sum(r['areaM2'] is not None for r in rows),'openingPresent':sum(r['year'] is not None or bool(r['openingPeriod']) for r in rows),'groundPhotos':sum(r['photoKind']=='ground' for r in rows),'visit360Identified':sum(bool(r['visit360Url']) for r in rows),'confirmedOmissionsAwaitingCoordinates':len(unlocated)},'structuralErrors':errors,'municipalities':municipalities,'confirmedOmissionsAwaitingCoordinates':unlocated,'limitations':['A área da freguesia nunca é tratada como área do cemitério.','Datas de ampliação, de projetos, de autorização e de bênção não são automaticamente datas de inauguração.','A ausência de visita 360° identificada não prova a inexistência de uma visita.','Satélite conservado como alternativa; a procura de fotografia não está concluída para todos os pontos.','Nomes e classificações previamente existentes foram preservados; campo preenchido não significa confirmação oficial.','A lista das 275 fichas ainda necessita de comparação integral com a divisão administrativa oficial atual.','Idães: dois cemitérios documentados, ainda sem pontos confirmados. Meixomil: correspondência com recinto Paços de Ferreira por esclarecer.']}
for name,value in [('summary.json',summary),('cemeteries.json',rows),('parishes.json',parishes)]:
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
buf=io.StringIO();w=csv.writer(buf);w.writerow(['Concelho','Freguesia','ID','Nome','Área m²','Inauguração','Imagem','Fonte','Por confirmar'])
for r in rows:w.writerow([r['municipality'],r['parish'],r['id'],r['name'],r['areaM2'],r['year'] or r['openingPeriod'],r['photoKind'],r['sourceUrl'],'; '.join(r['pending'])])
(OUT/'pendencias.csv').write_text(buf.getvalue())
lines=['# Distrito do Porto: revisão de 29 de outubro de 2026','','**Estado: parcial. O distrito não está documentalmente completo.**','',summary['scope'],'','Os registos com fontes acrescentadas não estão necessariamente completos em todos os campos. Os restantes conservam a informação anterior.','','## Cobertura dos ficheiros existentes','','| Concelho | Fichas | Cemitérios | Com fontes acrescentadas | Nomes por confirmar | Área preenchida | Inauguração/período | Fotografias |','|---|---:|---:|---:|---:|---:|---:|---:|']
for m in municipalities:lines.append('| '+' | '.join(str(m[k]) for k in ['municipality','parishes','cemeteries','withEvidenceAdded','namesPending','areaPresent','openingPresent','groundPhotos'])+' |')
lines+=['','## O que permanece por confirmar','']+['- '+s for s in summary['limitations']]+['','## Ficheiros de controlo','','- [Pendências por cemitério](pendencias.csv)','- [Resultados por freguesia](parishes.json)','- [Resumo e omissões confirmadas](summary.json)','','A verificação espacial testa os pontos contra os polígonos guardados. Não confirma no terreno os nomes, a gestão, os limites cadastrais ou a situação atual de cada recinto.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(summary['totals'],ensure_ascii=False));print('Erros estruturais:',len(errors))
assert not errors,errors
