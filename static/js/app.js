
const mobileBtn = document.getElementById('mobile-menu-btn');
const navRow = document.getElementById('nav-row');
if (mobileBtn && navRow) {
  mobileBtn.addEventListener('click', ()=>{
    navRow.style.display = navRow.style.display === 'block' ? 'none' : 'block';
  });
}
function showToast(text){
  const c = document.getElementById('toast-container');
  if(!c) return;
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = text;
  c.appendChild(el);
  setTimeout(()=> el.remove(), 2400);
}
document.querySelectorAll('[data-add-cart]').forEach(btn=>{
  btn.addEventListener('click', e=>{
    e.preventDefault();
    showToast("Mahsulot savatchaga qo'shildi");
  });
});
document.querySelectorAll('[data-qty]').forEach(box=>{
  const value = box.querySelector('span');
  box.querySelectorAll('button').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      let n = parseInt(value.textContent, 10);
      n += btn.dataset.act === 'plus' ? 1 : -1;
      if(n < 1) n = 1;
      value.textContent = n;
    });
  });
});
