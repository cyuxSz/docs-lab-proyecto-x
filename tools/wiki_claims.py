#!/usr/bin/env python3
"""Valida que las afirmaciones de openwiki/ sigan respaldadas por el código.

Una afirmación es cualquier línea de un .md en openwiki/ que enlaza a código
con un ancla de líneas, p. ej. [`detector.py:16`](../../src/x_vision/x_vision/detector.py#L16)
o #L11-L23. Este script guarda el hash de las líneas citadas en
openwiki/.claims/claims.json y luego avisa si cambiaron.

Uso:
  python tools/wiki_claims.py check        # falla (exit 1) si hay citas rotas o cambiadas
  python tools/wiki_claims.py check --fix-moved   # reescribe citas cuyo código solo se movió
  python tools/wiki_claims.py stamp        # registra los hashes actuales (tras revisar la wiki)
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "openwiki"
CLAIMS = WIKI / ".claims" / "claims.json"
LINK = re.compile(r"\[([^\]]*)\]\(([^)#\s]+)#L(\d+)(?:-L(\d+))?\)")


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    except (OSError, UnicodeDecodeError):
        return None


def digest(lines):
    return hashlib.sha256("\n".join(l.rstrip() for l in lines).encode()).hexdigest()


def statement(line):
    text = LINK.sub(lambda m: m.group(1), line)
    return re.sub(r"\s+", " ", re.sub(r"^\s*(?:[-*]|\d+\.|\|)\s*", "", text)).strip()


def scan():
    """Devuelve una lista de citas encontradas en la wiki."""
    found = []
    for md in sorted(WIKI.rglob("*.md")):
        for n, line in enumerate(read_lines(md), 1):
            for m in LINK.finditer(line):
                target = (md.parent / m.group(2)).resolve()
                start = int(m.group(3))
                end = int(m.group(4) or start)
                found.append({
                    "page": md.relative_to(ROOT).as_posix(),
                    "page_line": n,
                    "statement": statement(line),
                    "path": target.relative_to(ROOT).as_posix() if target.is_relative_to(ROOT) else str(target),
                    "lines": [start, end],
                    "link": m.group(0),
                })
    return found


def key(c):
    return f'{c["page"]}|{c["path"]}#L{c["lines"][0]}-L{c["lines"][1]}|{c["statement"]}'


def relocate(src, old_hash, length):
    for i in range(len(src) - length + 1):
        if digest(src[i:i + length]) == old_hash:
            return i + 1, i + length
    return None


def head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def stamp(_args):
    claims = []
    for c in scan():
        src = read_lines(ROOT / c["path"])
        a, b = c["lines"]
        if src is None or b > len(src):
            sys.exit(f'No se puede registrar {c["link"]} en {c["page"]}:{c["page_line"]}: archivo o líneas inexistentes')
        claims.append({"id": hashlib.sha1(key(c).encode()).hexdigest()[:12], "page": c["page"], "statement": c["statement"],
                       "evidence": {"path": c["path"], "lines": [a, b], "sha256": digest(src[a - 1:b])}})
    CLAIMS.parent.mkdir(parents=True, exist_ok=True)
    CLAIMS.write_text(json.dumps({"schemaVersion": 1, "commit": head(), "claims": claims}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(claims)} afirmaciones registradas en {CLAIMS.relative_to(ROOT).as_posix()}")


def check(args):
    stored = {}
    if CLAIMS.exists():
        for c in json.loads(CLAIMS.read_text(encoding="utf-8"))["claims"]:
            stored[(c["page"], c["evidence"]["path"], tuple(c["evidence"]["lines"]), c["statement"])] = c["evidence"]["sha256"]

    problems, moved = [], []
    for c in scan():
        a, b = c["lines"]
        where = f'{c["page"]}:{c["page_line"]}'
        src = read_lines(ROOT / c["path"])
        if src is None:
            problems.append(f'FALTA     {where}  {c["path"]} ya no existe')
            continue
        if b > len(src):
            problems.append(f'FUERA     {where}  {c["path"]}#L{a}-L{b} pasa del final del archivo ({len(src)} líneas)')
            continue
        old = stored.get((c["page"], c["path"], (a, b), c["statement"]))
        if old is None:
            problems.append(f'NUEVA     {where}  {c["path"]}#L{a}-L{b} sin registrar (revísala y corre stamp)')
        elif digest(src[a - 1:b]) != old:
            loc = relocate(src, old, b - a + 1)
            if loc:
                moved.append((c, loc))
                problems.append(f'MOVIDA    {where}  {c["path"]}#L{a}-L{b} -> #L{loc[0]}-L{loc[1]}')
            else:
                problems.append(f'CAMBIADA  {where}  {c["path"]}#L{a}-L{b}  «{c["statement"][:90]}»')

    if args.fix_moved and moved:
        # Reescribe cada enlace en su línea exacta, todos a la vez, para no encadenar reemplazos.
        targets = {(c["page"], c["page_line"], c["link"]): loc for c, loc in moved}
        for page in {c["page"] for c, _ in moved}:
            md = ROOT / page
            lines = read_lines(md)

            def rewrite(m, n):
                loc = targets.get((page, n, m.group(0)))
                if not loc:
                    return m.group(0)
                na, nb = loc
                rng = f"{na}" if na == nb else f"{na}-{nb}"
                text = re.sub(r":\d+(?:-\d+)?(`?)$", rf":{rng}\1", m.group(1))
                anchor = f"#L{na}" if na == nb else f"#L{na}-L{nb}"
                return f"[{text}]({m.group(2)}{anchor})"

            lines = [LINK.sub(lambda m, n=n: rewrite(m, n), line) for n, line in enumerate(lines, 1)]
            md.write_text("\n".join(lines), encoding="utf-8")
        print(f"{len(moved)} citas movidas reescritas; corre stamp para registrarlas.")

    for p in problems:
        print(p)
    print(f"{len(problems)} problema(s)" if problems else "Todas las afirmaciones siguen respaldadas por el código.")
    return 1 if problems else 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--fix-moved", action="store_true")
    sub.add_parser("stamp")
    args = ap.parse_args()
    sys.exit(check(args) if args.cmd == "check" else stamp(args))


if __name__ == "__main__":
    main()
