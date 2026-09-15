const $ = (selector) => document.querySelector(selector);
function render(data) {
  const host = $("#result");
  host.innerHTML = `<div class="summary"><span>SUMMARY</span><p></p></div><div class="sections"></div><div class="sources"><div class="subhead">SOURCES <small></small></div><div class="source-grid"></div></div><div class="trace"><div class="subhead">AGENT TRACE</div></div>`;
  host.querySelector(".summary p").textContent = data.summary;
  const sections = host.querySelector(".sections");
  data.sections.forEach((text, index) => { const el = document.createElement("article"); el.innerHTML = `<b>0${index + 1}</b><p></p>`; el.querySelector("p").textContent = text; sections.appendChild(el); });
  host.querySelector(".sources small").textContent = `${data.sources.length} cited items`;
  const cards = host.querySelector(".source-grid");
  data.sources.forEach((source) => { const card = document.createElement("article"); card.innerHTML = `<div><b></b><span></span></div><small></small><p></p><code></code>`; card.querySelector("b").textContent = source.title; card.querySelector("span").textContent = `${Math.round(source.relevance * 100)}%`; card.querySelector("small").textContent = `${source.publisher} · ${source.year}`; card.querySelector("p").textContent = source.excerpt; card.querySelector("code").textContent = `[${source.id}]`; cards.appendChild(card); });
  const trace = host.querySelector(".trace");
  data.trace.forEach((step) => { const row = document.createElement("div"); row.className = "trace-row"; row.innerHTML = `<b></b><span></span><small></small>`; row.querySelector("b").textContent = step.agent; row.querySelector("span").textContent = step.status; row.querySelector("small").textContent = step.detail; trace.appendChild(row); });
  $("#source-count").textContent = `${data.sources.length} SOURCES · ${data.mode}`;
}
async function research() {
  const button = $("#run"); button.disabled = true; button.innerHTML = "研究中…";
  try {
    const response = await fetch("/v1/research", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ topic: $("#topic").value, focus: $("#focus").value, max_sources: Number($("#max-sources").value) }) });
    const data = await response.json(); if (!response.ok) throw new Error(data.detail || "请求失败"); render(data);
  } catch (error) { $("#result").innerHTML = `<div class="error"></div>`; $("#result .error").textContent = error.message; }
  finally { button.disabled = false; button.innerHTML = "开始研究 <span>↗</span>"; }
}
$("#run").addEventListener("click", research); $("#topic").addEventListener("keydown", (event) => { if (event.key === "Enter") research(); });
