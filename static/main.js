// main.js - simple reorder with SortableJS

async function sendReorder(collectionSlug, order){
  await fetch(`/collections/${collectionSlug}/reorder`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order })
  });
}

if (window.Sortable){
  document.addEventListener('DOMContentLoaded', ()=>{
    const el = document.getElementById('links-list');
    if (!el) return;
    const slug = el.dataset.slug;
    const sortable = Sortable.create(el, {
      handle: '.drag-handle',
      onEnd: function(){
        const ids = Array.from(el.children).map(li=>parseInt(li.dataset.clid));
        sendReorder(slug, ids);
      }
    });
  });
}
