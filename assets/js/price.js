/*----------------------------------------------
[Price slider — "you get what you pay for"]
Four stops on a range input. Each stop swaps the price, name, what you
get, what it costs you later, and moves two meters: how much it grows
your business vs how much you'll spend fixing it later.
Edit the TIERS list below to change prices or wording.
----------------------------------------------*/
(function () {
	'use strict';
	var box = document.querySelector('[data-price]');
	if (!box) { return; }

	var TIERS = [
		{ amount: '£300', name: 'The pretty postcard',
		  tag: 'A template whipped up in a day. Looks a little pretty. Does nothing for you.',
		  get: ['A template that looks like everyone else’s', 'A few pages of “welcome to our website”', 'Your logo, somewhere'],
		  later: ['Rewriting the words so people actually ring', 'Paying again to be found on Google', 'Needs fixing — or a full rebrand — soon to come'],
		  grow: 8, fix: 95 },
		{ amount: '£1,200', name: 'The shop window',
		  tag: 'Your own design, words that sell, and found on Google. A solid start.',
		  get: ['Design that fits YOU — not a template', 'Words that say what you do in the first line', 'Fast on any phone, set up for Google', 'Contact form straight to your inbox'],
		  later: ['Online bookings, payments or tools as you grow', 'More pages when you add services'],
		  grow: 40, fix: 55 },
		{ amount: '£2,500', name: 'The business builder',
		  tag: 'Built to bring the work in, and easy for you to keep fresh.',
		  get: ['Everything in the shop window', 'Proof up top: reviews, results, real photos', 'Online bookings or enquiries that sort themselves', 'An editor so you change it yourself', 'Know what’s working with simple stats'],
		  later: ['Not much — it’s built to grow with you'],
		  grow: 75, fix: 20 },
		{ amount: '£4,500+', name: 'Breathes fire',
		  tag: 'A fully working site plus the tools that run your business for you.',
		  get: ['Everything in the business builder', 'Custom tools: rotas, bookings, payments, dashboards', 'The spreadsheet and group chat, replaced', 'Hours back every week', 'A site that grows your business while you sleep'],
		  later: ['Nothing to fix — just more customers to look after'],
		  grow: 100, fix: 4 }
	];

	var range = box.querySelector('#pr-range');
	var el = function (id) { return box.querySelector('#' + id); };
	function li(list, items) {
		list.innerHTML = '';
		items.forEach(function (t) { var n = document.createElement('li'); n.textContent = t; list.appendChild(n); });
	}
	function render() {
		var i = +range.value, t = TIERS[i];
		el('pr-amount').textContent = t.amount;
		el('pr-name').textContent = t.name;
		el('pr-tag').textContent = t.tag;
		li(el('pr-get'), t.get);
		li(el('pr-later'), t.later);
		el('pr-grow').style.width = t.grow + '%';
		el('pr-fix').style.width = t.fix + '%';
		range.setAttribute('aria-valuetext', t.amount + ', ' + t.name);
		range.style.setProperty('--pct', (i / (TIERS.length - 1) * 100) + '%');
		box.setAttribute('data-tier', i);
	}
	range.addEventListener('input', render);
	box.querySelectorAll('.pr-ticks span').forEach(function (s, i) {
		s.addEventListener('click', function () { range.value = i; render(); });
	});
	render();
}());
