// main.js — client-side renderer for the static wiki

let DATA = null;

async function loadData(){
  const res = await fetch('/data/content.json');
  DATA = await res.json();
}

function q(selector, parent=document){ return parent.querySelector(selector); }

function renderIndex(filter=''){
  const app = q('#app');
  app.innerHTML = '';
  const h = document.createElement('h1'); h.textContent = 'Collections'; app.appendChild(h);
  const row = document.createElement('div'); row.className = 'row';
  DATA.collections.forEach(col=>{
    // filter
    const text = (col.title + ' ' + (col.description||'') + ' ' + (col.links||[]).map(l=>l.title+' '+(l.description||'')).join(' ')).toLowerCase();
    if (filter && !text.includes(filter.toLowerCase())) return;
    const div = document.createElement('div'); div.className='col-12 collection-card';
    div.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title"><a href="#/collection/${encodeURIComponent(col.slug)}">${escapeHtml(col.title)}</a></h5>
          <p class="card-text text-muted">${escapeHtml(col.description||'')}</p>
          <p><small class="text-muted">${col.links.length} links</small></p>
        </div>
      </div>
    `;
    row.appendChild(div);
  });
  if (!row.children.length){
    app.innerHTML += '<div class="alert alert-secondary">No collections found.</div>';
  } else app.appendChild(row);
}

function renderCollection(slug, filter=''){
  const col = DATA.collections.find(c=>c.slug===slug);
  if (!col) { document.getElementById('app').innerHTML = '<div class="alert alert-danger">Collection not found</div>'; return; }
  const app = q('#app'); app.innerHTML = '';
  const hdr = document.createElement('div'); hdr.innerHTML = `<h1>${escapeHtml(col.title)}</h1><p class="text-muted">${escapeHtml(col.description||'')}</p>`;
  app.appendChild(hdr);
  const list = document.createElement('ul'); list.className='collection-links';
  col.links.forEach(l=>{
    const text = (l.title + ' ' + (l.description||'') + ' ' + (l.tags||[]).join(' ')).toLowerCase();
    if (filter && !text.includes(filter.toLowerCase())) return;
    const li = document.createElement('li');
    li.innerHTML = `
      <div>
        <a href="${escapeAttr(l.url)}" target="_blank"><strong>${escapeHtml(l.title)}</strong></a>
        <p class="mb-1 text-muted">${escapeHtml(l.description||'')}</p>
        <div>${(l.tags||[]).map(t=>`<span class="tag">${escapeHtml(t)}</span>`).join('')}</div>
      </div>
    `;
    list.appendChild(li);
  });
  if (!list.children.length) app.innerHTML += '<div class="alert alert-secondary">No links found.</div>';
  app.appendChild(list);
}

function router(){
  const hash = location.hash || '#/';
  const parts = hash.slice(2).split('/');
  const filter = q('#searchInput')?.value || '';
  if (parts[0]==='collection' && parts[1]){
    renderCollection(decodeURIComponent(parts[1]), filter);
  } else {
    renderIndex(filter);
  }
}

function escapeHtml(s){ if(!s) return ''; return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }
function escapeAttr(s){ return escapeHtml(s).replaceAll('\"','&quot;'); }

window.addEventListener('hashchange', router);

window.addEventListener('DOMContentLoaded', async ()=>{
  await loadData();
  q('#loading').style.display='none';
  q('#searchInput').addEventListener('input', ()=>router());
  router();
});
