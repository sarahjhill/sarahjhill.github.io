/*----------------------------------------------
[Price slider — "you get what you pay for"]
Five stops on a range input. Each stop swaps the price, name, what you
get, what it opens up for you, and moves two meters that both climb:
how much it grows your business and how much time it gives you back.
Deliberately positive all the way up — every tier is a real step forward,
the higher ones just do more of the work for you.
Edit the TIERS list below to change prices or wording.
----------------------------------------------*/
(function () {
	'use strict';
	var box = document.querySelector('[data-price]');
	if (!box) { return; }

	var TIERS = [
		{ amount: '£300', name: 'The pretty postcard',
		  tag: 'A neat little online card that says you’re open for business. A lovely first step.',
		  get: ['A clean, simple page with your name up in lights', 'Who you are, what you do, how to reach you', 'Looks smart on a phone'],
		  later: ['Somewhere to send people when they ask “have you got a website?”', 'A first foothold online you can build on'],
		  grow: 15, time: 5 },
		{ amount: '£600', name: 'Done right first time',
		  tag: 'A proper little site built around your business, with words that make people pick up the phone.',
		  get: ['A simple site built around YOUR business', 'Clear words that tell people what you do', 'Works beautifully on any phone', 'A contact form that lands in your inbox'],
		  later: ['Enquiries from people who already “get” you', 'Easy to add pages as you grow'],
		  grow: 30, time: 20 },
		{ amount: '£1,200', name: 'The shop window',
		  tag: 'Your own design, words that sell, and set up to be found on Google.',
		  get: ['Design that fits YOU — not a template', 'Words that say what you do in the first line', 'Fast on any phone, set up for Google', 'Contact form straight to your inbox'],
		  later: ['New customers finding you on Google', 'Ready for bookings, payments or tools when you are'],
		  grow: 50, time: 40 },
		{ amount: '£2,500', name: 'The business builder',
		  tag: 'Built to bring the work in, and easy for you to keep fresh.',
		  get: ['Everything in the shop window', 'Proof up top: reviews, results, real photos', 'Online bookings or enquiries that sort themselves', 'An editor so you change it yourself', 'Simple stats so you know what’s working'],
		  later: ['A steady stream of the right customers', 'Confidence to raise your prices'],
		  grow: 75, time: 70 },
		{ amount: '£4,500+', name: 'Breathes fire',
		  tag: 'A fully working site plus the tools that run your business for you.',
		  get: ['Everything in the business builder', 'Custom tools: rotas, bookings, payments, dashboards', 'The spreadsheet and group chat, replaced', 'Hours back every week', 'A site that grows your business while you sleep'],
		  later: ['Evenings and weekends back', 'Room to grow without hiring yet'],
		  grow: 100, time: 100 }
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
		el('pr-time').style.width = t.time + '%';
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
