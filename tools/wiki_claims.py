#!/usr/bin/env python3
"""Valida que las afirmaciones de openwiki/ y del README sigan respaldadas por el código.

Una afirmación es cualquier línea de un .md que enlaza a código con un ancla de
líneas, p. ej. [`detector.py:16`](../../src/x_vision/x_vision/detector.py#L16)
o #L11-L23. Este script guarda el hash de las líneas citadas en
openwiki/.claims/claims.json y luego avisa si cambiaron.

Uso:
  python tools/wiki_claims.py check              # falla (exit 1) si hay citas rotas, cambiadas o sin registrar
  python tools/wiki_claims.py check --fix-moved  # reescribe citas cuyo código solo se movió (sin ambigüedad)
  python tools/wiki_claims.py stamp              # registra los hashes; se niega si hay citas CAMBIADA/FALTA/FUERA
  python tools/wiki_claims.py stamp --revisado   # registra también las CAMBIADA, tras confirmar que siguen siendo ciertas
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
README = ROOT / "README.md"
CLAIMS = WIKI / ".claims" / "claims.json"
LINK = re.compile(r"\[([^\]]*)\]\(([^)#\s]+)#L(\d+)(?:-L(\d+))?\)")
BLOCKING = ("CAMBIADA", "FALTA", "FUERA", "ILEGIBLE")


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def read_lines(path):
    text = read_text(path)
    return None if text is None else text.replace("\r\n", "\n").split("\n")


def digest(lines):
    return hashlib.sha256("\n".join(l.rstrip() for l in lines).encode()).hexdigest()


def statement(line):
    text = LINK.sub(lambda m: m.group(1), line)
    return re.sub(r"\s+", " ", re.sub(r"^\s*(?:[-*]|\d+\.|\|)\s*", "", text)).strip()


def pages():
    return ([README] if README.exists() else []) + sorted(WIKI.rglob("*.md"))


def scan():
    """Devuelve (citas encontradas, páginas ilegibles)."""
    found, unreadable = [], []
    for md in pages():
        lines = read_lines(md)
        if lines is None:
            unreadable.append(md.relative_to(ROOT).as_posix())
            continue
        for n, line in enumerate(lines, 1):
            for m in LINK.finditer(line):
                target = (md.parent / m.group(2)).resolve()
                start = int(m.group(3))
                found.append({
                    "page": md.relative_to(ROOT).as_posix(),
                    "page_line": n,
                    "statement": statement(line),
                    "path": target.relative_to(ROOT).as_posix() if target.is_relative_to(ROOT) else str(target),
                    "lines": [start, int(m.group(4) or start)],
                    "link": m.group(0),
                })
    return found, unreadable


def key(c):
    return f'{c["page"]}|{c["path"]}#L{c["lines"][0]}-L{c["lines"][1]}|{c["statement"]}'


def relocate(src, old_hash, length):
    """Todas las posiciones (1-based) donde aparece el bloque citado."""
    return [(i + 1, i + length) for i in range(len(src) - length + 1) if digest(src[i:i + length]) == old_hash]


def head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_stored():
    stored = {}
    if CLAIMS.exists():
        for c in json.loads(CLAIMS.read_text(encoding="utf-8"))["claims"]:
            stored[(c["page"], c["evidence"]["path"], tuple(c["evidence"]["lines"]), c["statement"])] = c["evidence"]["sha256"]
    return stored


def audit():
    """Devuelve (citas, problemas) donde cada problema es (tipo, cita, mensaje, nueva_ubicación)."""
    stored = load_stored()
    claims, unreadable = scan()
    problems = [("ILEGIBLE", None, f"{p} no se puede leer como UTF-8", None) for p in unreadable]
    for c in claims:
        a, b = c["lines"]
        where = f'{c["page"]}:{c["page_line"]}'
        src = read_lines(ROOT / c["path"])
        if src is None:
            problems.append(("FALTA", c, f'{where}  {c["path"]} ya no existe', None))
            continue
        if b > len(src):
            problems.append(("FUERA", c, f'{where}  {c["path"]}#L{a}-L{b} pasa del final del archivo ({len(src)} líneas)', None))
            continue
        old = stored.get((c["page"], c["path"], (a, b), c["statement"]))
        if old is None:
            problems.append(("NUEVA", c, f'{where}  {c["path"]}#L{a}-L{b} sin registrar (revísala y corre stamp)', None))
        elif digest(src[a - 1:b]) != old:
            locs = relocate(src, old, b - a + 1)
            if len(locs) == 1:
                problems.append(("MOVIDA", c, f'{where}  {c["path"]}#L{a}-L{b} -> #L{locs[0][0]}-L{locs[0][1]}', locs[0]))
            elif locs:
                found = ", ".join(f"L{x}" for x, _ in locs)
                problems.append(("CAMBIADA", c, f'{where}  {c["path"]}#L{a}-L{b} se movió pero aparece en varias partes ({found}); elige a mano', None))
            else:
                problems.append(("CAMBIADA", c, f'{where}  {c["path"]}#L{a}-L{b}  «{c["statement"][:90]}»', None))
    return claims, problems


def fix_moved(moved):
    """Reescribe cada enlace en su línea exacta, todos a la vez, para no encadenar reemplazos."""
    targets = {(c["page"], c["page_line"], c["link"]): loc for c, loc in moved}
    for page in {c["page"] for c, _ in moved}:
        md = ROOT / page
        text = read_text(md)
        newline = "\r\n" if "\r\n" in text else "\n"

        def rewrite(m, n):
            loc = targets.get((page, n, m.group(0)))
            if not loc:
                return m.group(0)
            na, nb = loc
            rng = f"{na}" if na == nb else f"{na}-{nb}"
            label = re.sub(r":\d+(?:-\d+)?(`?)$", rf":{rng}\1", m.group(1))
            anchor = f"#L{na}" if na == nb else f"#L{na}-L{nb}"
            return f"[{label}]({m.group(2)}{anchor})"

        lines = text.replace("\r\n", "\n").split("\n")
        lines = [LINK.sub(lambda m, n=n: rewrite(m, n), line) for n, line in enumerate(lines, 1)]
        md.write_bytes(newline.join(lines).encode("utf-8"))
    print(f"{len(moved)} citas movidas reescritas; corre stamp para registrarlas.")


def stamp(args):
    claims, problems = audit()
    blocking = [p for p in problems if p[0] in BLOCKING and not (args.revisado and p[0] == "CAMBIADA")]
    if blocking:
        for kind, _, msg, _ in blocking:
            print(f"{kind:<9} {msg}")
        print("No se registró nada. Corrige la wiki o, si revisaste las CAMBIADA y siguen siendo ciertas, usa stamp --revisado.")
        return 1
    records = []
    for c in claims:
        a, b = c["lines"]
        src = read_lines(ROOT / c["path"])
        records.append({"id": hashlib.sha1(key(c).encode()).hexdigest()[:12], "page": c["page"], "statement": c["statement"],
                        "evidence": {"path": c["path"], "lines": [a, b], "sha256": digest(src[a - 1:b])}})
    CLAIMS.parent.mkdir(parents=True, exist_ok=True)
    CLAIMS.write_text(json.dumps({"schemaVersion": 1, "commit": head(), "claims": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(records)} afirmaciones registradas en {CLAIMS.relative_to(ROOT).as_posix()}")
    return 0


def check(args):
    _, problems = audit()
    for kind, _, msg, _ in problems:
        print(f"{kind:<9} {msg}")
    moved = [(c, loc) for kind, c, _, loc in problems if kind == "MOVIDA"]
    if args.fix_moved and moved:
        fix_moved(moved)
    print(f"{len(problems)} problema(s)" if problems else "Todas las afirmaciones siguen respaldadas por el código.")
    return 1 if problems else 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--fix-moved", action="store_true")
    s = sub.add_parser("stamp")
    s.add_argument("--revisado", action="store_true", help="registra también las citas CAMBIADA ya revisadas")
    args = ap.parse_args()
    sys.exit(check(args) if args.cmd == "check" else stamp(args))


if __name__ == "__main__":
    main()
