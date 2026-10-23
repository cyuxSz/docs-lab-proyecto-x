#!/usr/bin/env node
// Construye el sitio de documentación en dist/ a partir de lo que ya está en el repo:
//   openwiki/        -> visor de OpenWiki en /wiki/ y páginas Markdown en /content/
//   docs/arch/*.html -> diagramas de Archify en /arch/
//   site/            -> portada personalizada en /
// No llama a ningún LLM: para actualizar el sitio basta con actualizar openwiki/ o docs/arch/ y hacer push.
import { execFileSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, posix, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DIST = join(ROOT, "dist");
const STAGE = join(ROOT, ".site-build");
const OPENWIKI_VERSION = "0.7.2";

function git(...args) {
  try {
    return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

function repoInfo() {
  const env = process.env;
  let slug = env.VERCEL_GIT_REPO_OWNER && env.VERCEL_GIT_REPO_SLUG ? `${env.VERCEL_GIT_REPO_OWNER}/${env.VERCEL_GIT_REPO_SLUG}` : "";
  if (!slug) {
    const m = git("remote", "get-url", "origin").match(/github\.com[:/](.+?)(?:\.git)?$/);
    slug = m ? m[1] : "";
  }
  const sha = env.VERCEL_GIT_COMMIT_SHA || git("rev-parse", "HEAD");
  return { slug, sha, url: slug ? `https://github.com/${slug}` : "" };
}

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

function frontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fields = {};
  if (m) for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (kv) fields[kv[1]] = kv[2].replace(/^["']|["']$/g, "");
  }
  return fields;
}

// Los enlaces relativos a código (../../src/x.py#L3) no existen en el sitio: apuntan a GitHub en el commit construido.
function rewriteCodeLinks(text, mdPath, repo) {
  if (!repo.url) return text;
  return text.replace(/\]\((?!https?:|#)([^)\s]+?)(#L\d+(?:-L\d+)?)?\)/g, (all, target, anchor = "") => {
    if (target.endsWith(".md") || target.endsWith("/")) return all;
    const abs = relative(ROOT, join(dirname(mdPath), target)).split(sep).join(posix.sep);
    if (abs.startsWith("..")) return all;
    return `](${repo.url}/blob/${repo.sha}/${abs}${anchor})`;
  });
}

const repo = repoInfo();
rmSync(DIST, { recursive: true, force: true });
rmSync(STAGE, { recursive: true, force: true });
mkdirSync(DIST, { recursive: true });

// 1. Copia de openwiki/ con enlaces a código reescritos.
const pages = [];
for (const file of walk(join(ROOT, "openwiki"))) {
  const rel = relative(join(ROOT, "openwiki"), file).split(sep).join(posix.sep);
  if (rel.startsWith(".")) continue;
  const dest = join(STAGE, "openwiki", rel);
  mkdirSync(dirname(dest), { recursive: true });
  if (!rel.endsWith(".md")) {
    cpSync(file, dest);
    continue;
  }
  const text = rewriteCodeLinks(readFileSync(file, "utf8"), file, repo);
  writeFileSync(dest, text);
  const fm = frontmatter(text);
  pages.push({ path: rel, title: fm.title || "", description: fm.description || "", type: fm.type || "" });
}
cpSync(join(STAGE, "openwiki"), join(DIST, "content"), { recursive: true });

// 2. Visor de OpenWiki (solo lee Markdown, no usa modelo).
execFileSync("npx", ["--yes", `openwiki@${OPENWIKI_VERSION}`, "visualize", join(STAGE, "openwiki"), "--export", join(DIST, "wiki")], {
  cwd: ROOT,
  stdio: "inherit",
  shell: process.platform === "win32",
});

// 3. Diagramas de Archify: cualquier HTML en docs/arch/ aparece en la portada.
const diagrams = [];
const archDir = join(ROOT, "docs", "arch");
if (existsSync(archDir)) {
  mkdirSync(join(DIST, "arch"), { recursive: true });
  for (const name of readdirSync(archDir).filter((n) => n.endsWith(".html"))) {
    const html = readFileSync(join(archDir, name), "utf8");
    const title = (html.match(/<title>([^<]*)<\/title>/) || [])[1] || name;
    cpSync(join(archDir, name), join(DIST, "arch", name));
    diagrams.push({ file: `arch/${name}`, title: title.replace(/\s*·\s*Diagrama$/, "") });
  }
}

// 4. Datos para la portada.
const readJson = (p) => (existsSync(p) ? JSON.parse(readFileSync(p, "utf8")) : null);
const claims = readJson(join(ROOT, "openwiki", ".claims", "claims.json"));
const lastUpdate = readJson(join(ROOT, "openwiki", ".last-update.json"));
const data = {
  repo,
  builtAt: new Date().toISOString(),
  claimCount: claims ? claims.claims.length : 0,
  lastUpdate,
  pages,
  packages: pages.filter((p) => p.path.startsWith("packages/") && !p.path.endsWith("index.md")),
  diagrams,
};
writeFileSync(join(DIST, "data.json"), JSON.stringify(data, null, 2));

// 5. Portada.
cpSync(join(ROOT, "site"), DIST, { recursive: true });
rmSync(STAGE, { recursive: true, force: true });
console.log(`Sitio listo en dist/: ${pages.length} páginas, ${diagrams.length} diagrama(s), ${data.claimCount} afirmaciones.`);
