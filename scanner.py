#!/usr/bin/env python3
"""Build a catalog from explicitly configured public/authorized M3U sources."""
import json, re, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = "M3U-Playlist-Studio/1.0 (public playlist catalog)"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=35) as r:
        return r.read().decode("utf-8-sig", errors="replace")

def parse_m3u(text, country=""):
    result=[]; meta={}
    for raw in text.splitlines():
        line=raw.strip()
        if line.startswith("#EXTINF:"):
            comma=line.rfind(",")
            meta={"name": line[comma+1:].strip() if comma>=0 else "Pa emër",
                  "group": (re.search(r'group-title="([^"]*)"',line) or [None,"Të tjera"])[1],
                  "logo": (re.search(r'tvg-logo="([^"]*)"',line) or [None,""])[1]}
        elif line and not line.startswith("#") and meta:
            if line.startswith(("http://","https://")):
                result.append({**meta,"url":line,"country":country,"status":"Pa kontroll"})
            meta={}
    return result

def main():
    config=json.loads((ROOT/"sources.json").read_text(encoding="utf-8"))
    all_items=[]; errors=[]
    for source in config.get("sources",[]):
        if not source.get("enabled",True): continue
        try:
            entries=parse_m3u(fetch(source["url"]),source.get("country",""))
            all_items.extend(entries)
            print(f'OK {source["name"]}: {len(entries)}')
        except Exception as e:
            errors.append({"source":source.get("name","?"),"error":str(e)})
            print(f'ERROR {source.get("name")}: {e}')
    # Deduplicate by stream URL; preserve first occurrence.
    seen=set(); clean=[]
    for item in all_items:
        if item["url"] in seen: continue
        seen.add(item["url"]); clean.append(item)
    for i,item in enumerate(clean): item["id"]=f"ch{i+1}"
    data={"updated_at":datetime.now(timezone.utc).isoformat(),"source_count":len(config.get("sources",[])),
          "channel_count":len(clean),"channels":clean,"source_errors":errors}
    (ROOT/"catalog.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f'Catalog written: {len(clean)} unique entries; {len(errors)} source errors.')
if __name__=="__main__": main()
