/* L3dgr website */

// ---- Google Play link ----------------------------------------------------
// When the Play listing goes live, set PLAY_LIVE to true. Every "Get the app" button then links to the store.
const PLAY_LIVE = false;
const PLAY_URL = 'https://play.google.com/store/apps/details?id=com.l3dgr.app';

document.querySelectorAll('[data-play]').forEach(a => {
  if (PLAY_LIVE) { a.href = PLAY_URL; a.rel = 'noopener'; }
  else a.href = '#get';
});

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---- nav turns solid after the top of the page ----------------------------
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('solid', scrollY > 24);
onScroll(); addEventListener('scroll', onScroll, { passive: true });

// ---- reveal on scroll -------------------------------------------------------
if ('IntersectionObserver' in window && !reduce) {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  document.querySelectorAll('.rv').forEach((el, i) => {
    // siblings in a grid come in one after another
    const sib = [...el.parentElement.children].filter(c => c.classList.contains('rv'));
    el.style.transitionDelay = Math.min(sib.indexOf(el), 4) * 80 + 'ms';
    io.observe(el);
  });
} else document.querySelectorAll('.rv').forEach(el => el.classList.add('in'));

// ---- "+$14.50 → Coffee → Done" plays step by step when it scrolls into view ----
const flow = document.getElementById('flow');
if (flow && !reduce && 'IntersectionObserver' in window) {
  const steps = [...flow.querySelectorAll('[data-step]')];
  let timer = null;
  const play = () => {
    steps.forEach(s => s.classList.remove('on'));
    steps.forEach((s, i) => setTimeout(() => s.classList.add('on'), 250 + i * 380));
  };
  new IntersectionObserver(([e]) => {
    clearInterval(timer);
    if (e.isIntersecting) { play(); timer = setInterval(play, 6000); }
  }, { threshold: 0.6 }).observe(flow);
} else if (flow) flow.classList.remove('anim');

// ---- monthly / yearly prices ------------------------------------------------
document.querySelectorAll('.toggle button').forEach(b => b.addEventListener('click', () => {
  const p = b.dataset.period === 'year' ? 'y' : 'm';
  document.querySelectorAll('.toggle button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  document.querySelectorAll('[data-m]').forEach(el => { el.textContent = el.dataset[p]; });
}));

// ---- the closing section's video loads only when it's near ------------------
const lateVid = document.querySelector('video[data-src]');
if (lateVid && !reduce && 'IntersectionObserver' in window) {
  new IntersectionObserver(([e], o) => {
    if (!e.isIntersecting) return;
    lateVid.src = matchMedia('(max-width: 760px)').matches ? lateVid.dataset.srcSm : lateVid.dataset.src; lateVid.play().catch(() => {}); o.disconnect();
  }, { rootMargin: '400px' }).observe(lateVid);
}
// pause the hero video for people who prefer less motion
if (reduce) document.querySelectorAll('video').forEach(v => { v.pause(); v.removeAttribute('autoplay'); });

document.querySelectorAll('[data-year]').forEach(s => { s.textContent = new Date().getFullYear(); });
