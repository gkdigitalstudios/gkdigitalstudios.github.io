// Mobile nav
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) toggle.addEventListener('click', () => links.classList.toggle('show'));

// Reveal-on-scroll
const revealEls = document.querySelectorAll('.reveal');
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('show'); });
},{ threshold: 0.12 });
revealEls.forEach(el => io.observe(el));

// Animated counters
function animateCount(el){
  const target = +el.dataset.count;
  let cur = 0;
  const step = Math.max(1, Math.floor(target/120));
  const iv = setInterval(() => {
    cur += step;
    if (cur >= target){ cur = target; clearInterval(iv); }
    el.textContent = cur;
  }, 16);
}
document.querySelectorAll('[data-count]').forEach(el=>{
  const o = new IntersectionObserver(([e])=>{
    if (e.isIntersecting){ animateCount(el); o.disconnect(); }
  },{threshold:.3});
  o.observe(el);
});

// Back to top
const backTop = document.querySelector('.back-to-top');
window.addEventListener('scroll', ()=>{
  if (window.scrollY > 600) backTop.classList.add('show'); else backTop.classList.remove('show');
});
if (backTop) backTop.addEventListener('click', ()=> window.scrollTo({top:0, behavior:'smooth'}));

// Year in footer
const y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

// Portfolio filters
const chips = document.querySelectorAll('.chip');
const items = document.querySelectorAll('.g-item');
chips.forEach(ch=>{
  ch.addEventListener('click', ()=>{
    chips.forEach(c=>c.classList.remove('active'));
    ch.classList.add('active');
    const f = ch.dataset.filter;
    items.forEach(it=>{
      const show = f==='all' || it.dataset.category===f;
      it.style.display = show ? '' : 'none';
    });
  });
});

// Lightbox (supports portfolio images and any element with .lightboxable)
const lightbox = document.querySelector('.lightbox');
const lightImg = document.querySelector('.lightbox-img');
const lightClose = document.querySelector('.lightbox-close');

function openLightbox(src, alt=''){
  if (!lightbox || !lightImg) return;
  lightImg.src = src;
  lightImg.alt = alt;
  lightbox.classList.add('show');
  document.body.style.overflow = 'hidden';
}

// Attach to portfolio items + poster image
document.querySelectorAll('.g-item img, .lightboxable').forEach(img=>{
  img.addEventListener('click', ()=>{
    openLightbox(img.src, img.alt || '');
  });
});

if (lightClose && lightbox) {
  lightClose.addEventListener('click', ()=>{
    lightbox.classList.remove('show');
    document.body.style.overflow = '';
  });
  lightbox.addEventListener('click', (e)=>{
    if (e.target === lightbox) {
      lightbox.classList.remove('show');
      document.body.style.overflow = '';
    }
  });
}
