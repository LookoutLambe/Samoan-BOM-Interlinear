"""Feed a verse's walk output (from `gloss_corpus.py --debug`) straight into
simple_sentences and print each stage that changed something.
usage: python3 harness.py <debug.log> "<english prefix>" "<SS_TRACE phrase>" """
import sys, os, re, json, io, contextlib
sys.path.insert(0, "/Users/chrislambe/Desktop/O le Tusi a Mamona Interlinear/scripts")
log, prefix, phrase = sys.argv[1], sys.argv[2], sys.argv[3]
os.environ["SS_TRACE"] = phrase
import gloss_corpus as G
lines = open(log, errors="ignore").read().split("\n")
en = None; units = []
for i, l in enumerate(lines):
    if l.startswith("--- ") and prefix.lower() in l.lower():
        en = l.split(": ", 1)[1].strip()
        for m in lines[i + 1:]:
            mm = re.match(r"^\s+'(.*?)'\s+'(.*?)'\s+(\S+)", m)
            if not mm:
                break
            units.append((mm.group(1), mm.group(2)))
        break
assert en, "verse not found"
# the debug prints normalised keys; recover the tokens from the overrides file for exact forms
ov = json.load(open("/Users/chrislambe/Desktop/O le Tusi a Mamona Interlinear/O le Tusi a Mamona Interlinear/Resources/bom_overrides.json"))["verses"]
key = next(k for k, ws in ov.items() if k.startswith("1nephi|2|") and G.norm(" ".join(w["sm"] for w in ws)).split()[:6] == G.norm(" ".join(u[0] for u in units)).split()[:6]) if False else None
toks = []
for k, ws in ov.items():
    if not k.startswith("1nephi|"): continue
    flat = [G.norm(w["sm"]).strip(",;.:!?—") for w in ws]
    want = [t for u in units for t in u[0].split()]
    if flat == [w.strip(",;.:!?—") for w in want] or len(flat) == len(want) and sum(a == b for a, b in zip(flat, want)) > len(flat) * 0.9:
        toks = [w["sm"] for w in ws]; break
assert toks, "tokens not matched"
out = []; k = 0
for sm, en_u in units:
    n = len(sm.split())
    for j in range(n - 1):
        out.append({"sm": toks[k + j], "en": G.CONT})
    out.append({"sm": toks[k + n - 1], "en": en_u})
    k += n
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    G.simple_sentences(out, toks, en)
prev = None
for l in buf.getvalue().split("\n"):
    m = re.match(r"^\s+\[(.*?)\] (.*)$", l)
    if not m: continue
    if m.group(2) != prev:
        print(f"[{m.group(1)}] {m.group(2)}")
        prev = m.group(2)
print("FINAL:", " | ".join(f"{w['sm']}={w['en']}" for w in out if w["en"] != G.CONT))
