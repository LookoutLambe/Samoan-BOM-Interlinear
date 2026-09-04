#!/usr/bin/env python3
"""Content-word agreement with the curation. See score_against_curation.py."""
import json, pathlib, re, sys
from collections import Counter
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import english_register as ER
R = pathlib.Path(__file__).resolve().parent.parent / "O le Tusi a Mamona Interlinear" / "Resources"
SC = pathlib.Path("/private/tmp/claude-501/-Users-chrislambe-Desktop-untitled-folder"
                  "/613c68df-5949-46cb-8611-81201268d964/scratchpad")
new = json.loads((R/"bom_overrides.json").read_text())["verses"]
oldf = json.loads((SC/"bom_overrides.CURATED.json").read_text()); old = oldf["verses"]
curated = set(old) - set(oldf.get("generated", []))
FUNC = ER.FUNCTION_ONLY | {"be","been","being","was","were","is","are","did","do","does",
 "had","has","have","shall","will","would","should","may","might","can","there","it",
 "them","their","your","our","his","her","he","she","they","we","you","i","me","us",
 "him","who","which","what","when","then","than","if","because","so","as","yea"}
def bag(ws, c):
    o = Counter()
    for w in ws:
        g = w.get("en") or ""
        if g and g != "·":
            for x in re.findall(r"[a-z']+", g.lower()):
                if not c or x not in FUNC: o[x] += 1
    return o
for label, c in (("ALL", False), ("CONTENT", True)):
    k=m=sp=0
    for key in curated:
        n = new.get(key)
        if not n: continue
        bo, bn = bag(old[key], c), bag(n, c)
        i = sum((bo & bn).values()); k += i
        m += sum(bo.values()) - i; sp += sum(bn.values()) - i
    r=k/max(1,k+m); pr=k/max(1,k+sp)
    print("  %-8s recall %5.1f%%  precision %5.1f%%  F1 %5.1f%%" % (label,100*r,100*pr,100*2*r*pr/max(1e-9,r+pr)))
