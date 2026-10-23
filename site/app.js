// Portada: todo sale de data.json y de content/*.md, que genera tools/build_site.mjs.
const $ = (sel) => document.querySelector(sel);

function stripFrontmatter(md) {
  return md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "");
}

function render(md, { dropTitle = false } = {}) {
  let body = stripFrontmatter(md).trimStart();
  if (dropTitle) body = body.replace(/^#\s.*\r?\n/, "");
  return DOMPurify.sanitize(marked.parse(body));
}

// Enlaces a otras páginas .md se abren en el lector; los de código van a GitHub en otra pestaña.
function wireLinks(container, basePath) {
  for (const a of container.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");
    if (/^https?:/.test(href)) {
      a.target = "_blank";
      a.rel = "noopener";
    } else if (href.endsWith(".md")) {
      const resolved = new URL(href, `https://x/${basePath}`).pathname.slice(1);
      a.addEventListener("click", (e) => {
        e.preventDefault();
        openPage(resolved);
      });
    } else if (href.endsWith("/")) {
      a.href = "wiki/";
    }
  }
}

async function loadInto(el, path, opts) {
  try {
    const res = await fetch(`content/${path}`);
    if (!res.ok) throw new Error(res.status);
    el.innerHTML = render(await res.text(), opts);
    wireLinks(el, path);
  } catch {
    el.innerHTML = `<p class="muted">No se pudo cargar <code>${path}</code>.</p>`;
  }
}

const pagesByPath = new Map();

async function openPage(path) {
  const dialog = $("#reader");
  $("#reader-title").textContent = pagesByPath.get(path)?.title || path;
  $("#reader-body").innerHTML = '<p class="muted">Cargando…</p>';
  if (!dialog.open) dialog.showModal();
  await loadInto($("#reader-body"), path);
  $("#reader-body").scrollTop = 0;
}

function renderDiagrams(diagrams) {
  const picker = $("#diagram-picker");
  const frame = $("#diagram-frame");
  const open = $("#diagram-open");
  if (!diagrams.length) {
    $("#arquitectura").hidden = true;
    return;
  }
  for (const d of diagrams) picker.add(new Option(d.title, d.file));
  picker.hidden = diagrams.length < 2;
  const show = (file) => {
    frame.src = file;
    open.href = file;
  };
  picker.addEventListener("change", () => show(picker.value));
  show(diagrams[0].file);
}

function renderPackages(packages) {
  const grid = $("#package-cards");
  for (const p of packages) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "card";
    card.innerHTML = `<span class="card-title"></span><span class="card-desc"></span><span class="card-link">Leer →</span>`;
    card.querySelector(".card-title").textContent = p.title || p.path;
    card.querySelector(".card-desc").textContent = p.description;
    card.addEventListener("click", () => openPage(p.path));
    grid.append(card);
  }
}

function renderStats(data) {
  $("#stat-packages").textContent = data.packages.length;
  $("#stat-claims").textContent = data.claimCount;
  $("#stat-diagrams").textContent = data.diagrams.length;
  const commit = data.lastUpdate?.commit;
  if (commit) {
    const short = commit.slice(0, 7);
    $("#stat-commit").innerHTML = data.repo.url
      ? `<a href="${data.repo.url}/commit/${commit}" target="_blank" rel="noopener"><code>${short}</code></a>`
      : `<code>${short}</code>`;
  }
  const built = new Date(data.builtAt).toLocaleString("es-MX", { dateStyle: "medium", timeStyle: "short" });
  $("#build-info").textContent = `Sitio construido el ${built} desde ${data.repo.slug || "el repo"} @ ${(data.repo.sha || "").slice(0, 7)}.`;
}

async function main() {
  const data = await (await fetch("data.json")).json();
  for (const p of data.pages) pagesByPath.set(p.path, p);
  renderStats(data);
  renderDiagrams(data.diagrams);
  renderPackages(data.packages);
  loadInto($("#estado-body"), "operations/estado.md", { dropTitle: true });
  loadInto($("#quickstart-body"), "quickstart.md", { dropTitle: true });

  for (const btn of document.querySelectorAll("[data-page]")) {
    btn.addEventListener("click", () => openPage(btn.dataset.page));
  }
  // El visor de OpenWiki toma el foco al cargar y arrastra el scroll de la página: se carga solo bajo demanda.
  $("#wiki-load").addEventListener("click", () => {
    const frame = document.createElement("iframe");
    frame.src = "wiki/";
    frame.title = "Visor de OpenWiki";
    $("#wiki-frame").replaceChildren(frame);
  });
  $("#reader-close").addEventListener("click", () => $("#reader").close());
  $("#reader").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) e.currentTarget.close();
  });
}

main();
