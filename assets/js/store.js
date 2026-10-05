/* ============================================================
   STORE — buy buttons on themes.html, order page on themes-thanks.html.
   Talks to the ember-store Cloudflare Worker, whose address is in
   data-store-api on #store (set by STORE_API in build-pages.py).
   No card details ever touch this site: Stripe's own page takes payment.
   ============================================================ */
/* ---------- showcase: device tabs + page buttons (themes.html) ---------- */
(() => {
  const tabs = document.querySelectorAll('.device-tabs [role="tab"]');
  tabs.forEach((tab, i) => {
    const select = () => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
    };
    tab.addEventListener('click', select);
    tab.addEventListener('keydown', (e) => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      const next = tabs[(i + d + tabs.length) % tabs.length];
      next.focus(); next.click();
    });
  });
  document.querySelectorAll('[data-show-page]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const view = document.getElementById(btn.dataset.target);
      const img = view.querySelector('img');
      img.src = btn.dataset.showPage;
      img.alt = btn.dataset.alt;
      img.width = btn.dataset.w; img.height = btn.dataset.h;
      view.scrollTop = 0;
      document.querySelectorAll(`[data-target="${btn.dataset.target}"]`).forEach((b) => b.setAttribute('aria-pressed', b === btn));
    });
  });
})();

(() => {
  const root = document.getElementById('store');
  if (!root) return;
  const API = root.dataset.storeApi.replace(/\/$/, '');
  const fallback = root.dataset.fallback;

  /* ---------- buy buttons ---------- */
  document.querySelectorAll('[data-buy]').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const msg = btn.closest('.plan, .cta-row')?.querySelector('.buy-msg');
      const label = btn.innerHTML;
      btn.setAttribute('aria-busy', 'true');
      btn.innerHTML = 'Opening secure checkout&hellip;';
      try {
        const res = await fetch(`${API}/checkout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product: btn.dataset.buy }),
        });
        const data = await res.json();
        if (!res.ok || !data.url) throw new Error(data.error || 'Checkout unavailable');
        window.location.href = data.url;
      } catch (err) {
        btn.innerHTML = label;
        btn.removeAttribute('aria-busy');
        if (msg) msg.innerHTML = `Checkout didn't open. Try again, or <a href="${fallback}">email me</a> and I'll send an invoice.`;
      }
    });
  });

  /* ---------- order page ---------- */
  const order = document.getElementById('order');
  if (!order) return;
  const sid = new URLSearchParams(location.search).get('session_id');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  if (!sid) {
    order.innerHTML = `<h2>No order reference.</h2><p>Open the link in your receipt email, or <a href="${fallback}">email me</a> and I'll resend it.</p>`;
    return;
  }

  let tries = 0;
  async function load() {
    try {
      const res = await fetch(`${API}/order?session_id=${encodeURIComponent(sid)}`);
      const data = await res.json();
      if (res.status === 202 && tries++ < 10) { setTimeout(load, 1500); return; }
      if (!res.ok) throw new Error(data.error || 'Order not found');
      render(data);
    } catch (err) {
      order.innerHTML = `<h2>We couldn't load that order.</h2><p>${esc(err.message)}. Your payment is safe &mdash; <a href="${fallback}">email me</a> with your receipt and I'll sort it the same day.</p>`;
    }
  }

  function render(d) {
    const isShopify = d.downloads.some((x) => /shopify/i.test(x.label));
    const isWoo = d.downloads.some((x) => /woo/i.test(x.label));
    order.innerHTML = `
      <p class="eyebrow" style="color:var(--flame)">Paid &mdash; thank you</p>
      <h2>${esc(d.product)}</h2>
      <p>Receipt sent to <b>${esc(d.email)}</b>. Keep that email: its link brings you back here for fresh downloads.</p>
      <div class="dl">${d.downloads.map((x) => `<a class="btn btn-primary" href="${esc(x.url)}">${esc(x.label)} <span aria-hidden="true">&darr;</span></a>`).join('')}</div>
      <p style="margin-bottom:8px"><b>Your licence key</b></p>
      <div class="licence-key"><span id="lic">${esc(d.license)}</span><button type="button" id="copy">Copy</button></div>
      ${isShopify ? `<p style="margin-top:24px"><b>Shopify:</b></p><ol>
        <li>Shopify admin &rarr; <b>Online Store &rarr; Themes</b></li>
        <li><b>Add theme &rarr; Upload zip file</b> &mdash; upload the zip as it is, don't unzip it</li>
        <li>Click <b>Customize</b>. Everything is drag, drop and click from there.</li></ol>` : ''}
      ${isWoo ? `<p style="margin-top:24px"><b>WooCommerce:</b></p><ol>
        <li>WordPress admin &rarr; <b>Appearance &rarr; Themes &rarr; Add New &rarr; Upload Theme</b></li>
        <li>Choose the zip, <b>Install Now</b>, <b>Activate</b></li>
        <li><b>Appearance &rarr; Editor</b> to edit every page visually.</li></ol>` : ''}
      <p class="fine">Links work until ${new Date(d.expires).toLocaleDateString('en-GB', { day: 'numeric', month: 'long' })}
        and you've used ${d.downloadsUsed} of ${d.downloadsAllowed} downloads. Full guide: <a href="themes.html#docs">themes.html#docs</a>.</p>`;
    document.getElementById('copy').addEventListener('click', (e) => {
      navigator.clipboard?.writeText(d.license).then(() => { e.target.textContent = 'Copied'; });
    });
  }
  load();
})();
