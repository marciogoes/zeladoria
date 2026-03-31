import os, base64

d = os.path.dirname(os.path.abspath(__file__))

chunk_a = open(os.path.join(d, "_ca.b64")).read()
chunk_b = open(os.path.join(d, "_cb.b64")).read()
chunk_c = open(os.path.join(d, "_cc.b64")).read()

content = base64.b64decode(chunk_a + chunk_b + chunk_c).decode("utf-8")
out = os.path.join(d, "frontend", "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(content)
print(f"index.html escrito: {len(content)} chars")
print(f"  Sprint 17 paginacao: {'_totalPaginas' in content}")
print(f"  Sprint 17 timeline:  {'mostrarTimeline' in content}")
print(f"  Tempo medio:         {'stat-tempo-medio' in content}")
print(f"  Bugs corrigidos:     {'avaliacao: nota, comentario_avaliacao:' in content}")
print()
print("Pronto! Execute:")
print("  git add frontend\\index.html")
print("  git commit -m 'fix: sprint17 index.html'")
print("  git push")
for fn in ["_ca.b64", "_cb.b64", "_cc.b64", "_build_index.py"]:
    fp = os.path.join(d, fn)
    if os.path.exists(fp): os.remove(fp)
