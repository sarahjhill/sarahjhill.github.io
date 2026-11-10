/*----------------------------------------------

[The work — phone view]

On phones the project list (#q-log) is a sideways row of cards you swipe
through. This adds what makes that easy to use:

  - world chips above the row (Charity, Tools, Business, Team builds,
    Yours). Tap one to jump straight to that world. The chip for the
    card you're looking at lights up.
  - a bar under the row with back / next buttons and "3 / 12", so you
    always know where you are and never have to swipe blind.
  - a one-off "scroll inside the phone" hint on the first screenshot.

Only runs at phone width, and only while the list is showing (not
while the dragon is flying). Does nothing without JavaScript: the row
still swipes on its own.

----------------------------------------------*/
(function () {
	'use strict';

	var root = document.getElementById('work');
	var log = root && root.querySelector('.q-log');
	if (!log) { return; }
	var cards = [].slice.call(log.querySelectorAll('.qi'));
	if (!cards.length) { return; }
	var mq = window.matchMedia('(max-width: 760px)');

	/* short names for the chips, keyed by world number */
	var SHORT = { 1: 'Charity', 2: 'Tools', 3: 'Business', 4: 'Team builds', 5: 'Yours' };
	var worlds = [].slice.call(log.querySelectorAll('.q-lvl')).map(function (sec) {
		var n = sec.getAttribute('data-lvl');
		return { n: n, label: SHORT[n] || sec.getAttribute('data-name'), first: sec.querySelector('.qi'), sec: sec };
	}).filter(function (w) { return w.first; });

	/* ---- build the chips and the bar --------------------------------- */
	var nav = document.createElement('div');
	nav.setAttribute('role', 'navigation');
	nav.className = 'qm-chips';
	nav.setAttribute('aria-label', 'Jump to a world');
	worlds.forEach(function (w) {
		var b = document.createElement('button');
		b.type = 'button';
		b.className = 'qm-chip';
		b.textContent = w.label;
		b.setAttribute('data-w', w.n);
		b.addEventListener('click', function () { go(cards.indexOf(w.first)); });
		nav.appendChild(b);
	});

	var bar = document.createElement('div');
	bar.className = 'qm-bar';
	bar.innerHTML =
		'<button type="button" class="qm-arrow" data-d="-1" aria-label="Previous project">&larr;</button>' +
		'<p class="qm-count" aria-live="polite"><b>1</b> / ' + cards.length + '<span></span></p>' +
		'<button type="button" class="qm-arrow" data-d="1" aria-label="Next project">&rarr;</button>';
	var countN = bar.querySelector('b');
	var countName = bar.querySelector('span');
	[].forEach.call(bar.querySelectorAll('.qm-arrow'), function (b) {
		b.addEventListener('click', function () { go(current + Number(b.getAttribute('data-d'))); });
	});

	log.parentNode.insertBefore(nav, log);
	log.parentNode.insertBefore(bar, log.nextSibling);

	/* one-off hint on the first phone screenshot */
	var firstPhone = log.querySelector('.qi-phone');
	if (firstPhone) {
		var hint = document.createElement('span');
		hint.className = 'qm-hint';
		hint.setAttribute('aria-hidden', 'true');
		hint.textContent = 'Scroll inside ↕';
		firstPhone.appendChild(hint);
		var sc = firstPhone.querySelector('.qi-scroll');
		var hide = function () { hint.classList.add('is-gone'); };
		if (sc) { sc.addEventListener('scroll', hide, { once: true, passive: true }); }
		firstPhone.addEventListener('touchstart', hide, { once: true, passive: true });
	}

	/* ---- moving and tracking ----------------------------------------- */
	var current = 0;
	function go(i) {
		i = Math.max(0, Math.min(cards.length - 1, i));
		var c = cards[i];
		log.scrollTo({ left: c.offsetLeft - (log.clientWidth - c.offsetWidth) / 2, behavior: smooth() });
		set(i);
	}
	function smooth() {
		return window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
	}
	function set(i) {
		if (i === current && countN.textContent === String(i + 1)) { return; }
		current = i;
		countN.textContent = String(i + 1);
		var t = cards[i].querySelector('.qi-title');
		countName.textContent = t ? t.firstChild.textContent.trim() : '';
		var lvl = cards[i].closest('.q-lvl');
		var n = lvl ? lvl.getAttribute('data-lvl') : '';
		[].forEach.call(nav.children, function (b) {
			var on = b.getAttribute('data-w') === n;
			b.classList.toggle('is-on', on);
			b.setAttribute('aria-current', on ? 'true' : 'false');
			if (on && mq.matches) {
				nav.scrollTo({ left: b.offsetLeft - 16, behavior: smooth() });
			}
		});
		bar.querySelector('[data-d="-1"]').disabled = i === 0;
		bar.querySelector('[data-d="1"]').disabled = i === cards.length - 1;
	}
	/* which card is in the middle of the row */
	var raf = 0;
	log.addEventListener('scroll', function () {
		if (raf) { return; }
		raf = requestAnimationFrame(function () {
			raf = 0;
			var mid = log.scrollLeft + log.clientWidth / 2, best = 0, bd = Infinity;
			cards.forEach(function (c, i) {
				var d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid);
				if (d < bd) { bd = d; best = i; }
			});
			set(best);
		});
	}, { passive: true });

	/* arrow keys while the row has focus */
	log.addEventListener('keydown', function (e) {
		if (!mq.matches) { return; }
		if (e.target !== log) { return; }
		if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
		if (e.key === 'ArrowLeft') { e.preventDefault(); go(current - 1); }
	});

	current = -1;
	set(0);
}());
