/*----------------------------------------------

[The work — Dragon Quest]

Turns the plain project list in #work (.q-log) into a side-scrolling
flight. Scrolling the page moves a long "world" sideways under a
sticky stage; the dragon (quest-dragon.js, the same 3D model as the
hero) flies along a glowing ember line, and every project is a
treasure chest on that line. When the dragon reaches one it breathes
on it, the chest opens, and a game-style window pops out of it with
the real site inside — a full-length screenshot you can scroll — plus
what it was built with and why.

How scroll maps to the world: the journey is a list of segments,
"travel" (the world slides to the next chest) and "dwell" (the world
holds still while the window is open, so there's time to read and
scroll the screenshot). Each segment is worth some number of units;
one unit is a fixed number of pixels of page scroll. The page gets
exactly as tall as the journey needs.

Talks to quest-dragon.js through window.__questDragon (where the
dragon should be, which way it faces, whether it's breathing). If
WebGL or the model never arrives, everything here still works — you
just fly without a dragon.

Falls back to the plain list for reduced motion, for anyone who
presses "Skip it", and (because it's just HTML) with no JavaScript.

----------------------------------------------*/

(function () {
	'use strict';

	var root = document.getElementById('work');
	if (!root || !root.classList.contains('quest')) { return; }
	var track = root.querySelector('.q-track');
	var stage = root.querySelector('.q-stage');
	var log = root.querySelector('.q-log');
	if (!track || !stage || !log) { return; }

	var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	var LS_KEY = 'sjh_quest_list';

	/* ---- read the content ------------------------------------------------ */
	var levels = [].slice.call(log.querySelectorAll('.q-lvl')).map(function (sec, li) {
		return {
			n: li + 1,
			name: sec.getAttribute('data-name'),
			place: sec.getAttribute('data-place'),
			finale: sec.classList.contains('q-lvl--end'),
			items: [].slice.call(sec.querySelectorAll('.qi'))
		};
	});
	var stops = [];
	levels.forEach(function (lv) {
		lv.items.forEach(function (art) {
			var title = art.querySelector('.qi-title');
			stops.push({
				lv: lv,
				art: art,
				title: title ? title.childNodes[0].textContent.trim() : '',
				num: art.getAttribute('data-num'),
				locked: art.classList.contains('qi--locked'),
				finale: art.classList.contains('qi--finale')
			});
		});
	});
	var TREASURES = stops.filter(function (s) { return !s.finale; }).length;

	/* sky colours per world: [sky top, sky bottom, far hills, mid, near] */
	var PALETTE = [
		['#0a221d', '#1f5040', '#1a4537', '#0f2e26', '#09201a'],  /* the valleys */
		['#1a0b08', '#5a2312', '#40180c', '#2a0f08', '#1a0905'],  /* the forge */
		['#140f27', '#47295e', '#35224e', '#22163a', '#150e26'],  /* market town */
		['#08122a', '#22406e', '#1a3157', '#11223f', '#0a162b'],  /* the arena */
		['#1f0b0a', '#a2401a', '#5a2414', '#33130b', '#1c0a06']   /* the castle */
	];

	/* ---- modes ----------------------------------------------------------- */
	function storeGet() { try { return localStorage.getItem(LS_KEY); } catch (e) { return null; } }
	function storeSet(v) { try { localStorage.setItem(LS_KEY, v); } catch (e) { /* private mode */ } }

	var built = false;
	var flying = false;

	function setFlying(on, opts) {
		opts = opts || {};
		flying = !!on;
		root.classList.toggle('is-flying', flying);
		[].forEach.call(root.querySelectorAll('[data-quest="list"]'), function (b) { b.setAttribute('aria-pressed', String(!flying)); });
		if (flying) {
			if (!built) { build(); }
			layout();
			if (inView()) { startLoop(); }
		} else {
			stopLoop();
			closeWindow(true);
			publishDragon(false);
		}
		if (opts.remember) { storeSet(flying ? 'fly' : 'list'); }
		if (opts.scrollTo) {
			var el = flying ? track : log;
			window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset - (flying ? 0 : 80), behavior: reduce ? 'auto' : 'smooth' });
		}
	}

	root.classList.add('can-fly');
	root.addEventListener('click', function (e) {
		var b = e.target.closest('[data-quest]');
		if (!b) { return; }
		var what = b.getAttribute('data-quest');
		if (what === 'list') { e.preventDefault(); setFlying(false, { remember: true, scrollTo: true }); }
		if (what === 'up') {
			/* back up above the flight, to the section before it */
			e.preventDefault();
			closeWindow(true);
			var before = root.previousElementSibling;
			while (before && before.tagName !== 'SECTION') { before = before.previousElementSibling; }
			var upTop = before ? before.getBoundingClientRect().top + window.pageYOffset : root.getBoundingClientRect().top + window.pageYOffset - window.innerHeight;
			window.scrollTo({ top: Math.max(0, upTop - 60), behavior: 'instant' });
			if (before) { before.setAttribute('tabindex', '-1'); before.focus({ preventScroll: true }); }
			return;
		}
		if (what === 'exit') {
			/* jump straight past the flight — 'instant', or a smooth scroll
			   would replay the whole journey on the way down */
			e.preventDefault();
			closeWindow(true);
			var after = root.nextElementSibling;
			var top = after ? after.getBoundingClientRect().top + window.pageYOffset : root.getBoundingClientRect().bottom + window.pageYOffset;
			window.scrollTo({ top: top - 60, behavior: 'instant' });
			if (after) { after.setAttribute('tabindex', '-1'); after.focus({ preventScroll: true }); }
			return;
		}
				if (what === 'fly' || what === 'start') {
			e.preventDefault();
			if (!flying) { setFlying(true, { remember: true }); }
			window.scrollTo({ top: track.getBoundingClientRect().top + window.pageYOffset + 2, behavior: 'smooth' });
		}
	});

	/* ---- seeded random so the scenery is the same every visit ---------- */
	var seed = 7;
	function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

	/* ---- DOM bits -------------------------------------------------------- */
	var el = {};
	var SVGNS = 'http://www.w3.org/2000/svg';

	function mk(tag, cls, parent, html) {
		var n = document.createElement(tag);
		if (cls) { n.className = cls; }
		if (html != null) { n.innerHTML = html; }
		if (parent) { parent.appendChild(n); }
		return n;
	}

	var CHEST = '<svg class="chest" viewBox="0 0 64 56" aria-hidden="true">' +
		'<ellipse class="glow" cx="32" cy="22" rx="30" ry="20" fill="rgba(255,200,80,.55)"/>' +
		'<rect x="6" y="24" width="52" height="28" rx="3" fill="#7a4a1f" stroke="#2b1708" stroke-width="3"/>' +
		'<rect x="6" y="34" width="52" height="5" fill="#c98a12" stroke="#2b1708" stroke-width="2"/>' +
		'<rect x="27" y="30" width="10" height="13" fill="#ffcf4a" stroke="#2b1708" stroke-width="2"/>' +
		'<g class="lid"><path d="M6 24 Q6 8 32 8 Q58 8 58 24 Z" fill="#8f5a26" stroke="#2b1708" stroke-width="3"/>' +
		'<rect x="27" y="10" width="10" height="14" fill="#c98a12" stroke="#2b1708" stroke-width="2"/>' +
		'<circle class="gem" cx="32" cy="17" r="3" fill="#ff3b1f"/></g></svg>';

	var EGG_NODE = '<svg class="chest" viewBox="0 0 64 56" aria-hidden="true">' +
		'<ellipse class="glow" cx="32" cy="30" rx="28" ry="24" fill="rgba(255,140,40,.5)"/>' +
		'<path d="M32 4 C46 4 54 26 54 36 C54 48 44 54 32 54 C20 54 10 48 10 36 C10 26 18 4 32 4 Z" fill="#e9862a" stroke="#2b1708" stroke-width="3"/>' +
		'<circle class="gem" cx="25" cy="24" r="4" fill="#7a2e0f"/><circle cx="38" cy="38" r="5" fill="#7a2e0f"/></svg>';

	var CASTLE = '<svg class="chest" viewBox="0 0 120 110" aria-hidden="true">' +
		'<ellipse class="glow" cx="60" cy="60" rx="60" ry="50" fill="rgba(255,170,60,.45)"/>' +
		'<path d="M10 106 V46 h10 v-10 h8 v10 h8 v-10 h8 v10 h8 V30 h6 v-8 h6 v8 h6 v-8 h6 v8 h6 v16 h8 v-10 h8 v10 h8 v-10 h8 v10 h10 v60 Z" fill="#3a2414" stroke="#1d1209" stroke-width="3"/>' +
		'<path d="M50 106 v-24 a10 10 0 0 1 20 0 v24 Z" fill="#1d1209"/>' +
		'<rect x="24" y="60" width="8" height="12" fill="#ffcf4a"/><rect x="88" y="60" width="8" height="12" fill="#ffcf4a"/>' +
		'<rect x="56" y="38" width="8" height="10" fill="#ffcf4a"/>' +
		'<path d="M63 22 V2 l22 7 -22 7" fill="#ff3b1f" stroke="#1d1209" stroke-width="2"/></svg>';

	function build() {
		built = true;
		stage.innerHTML = '';
		el.stars = mk('div', 'q-stars', stage);
		el.moon = mk('div', 'q-moon', stage);
		el.far = mk('div', 'q-layer q-far', stage);
		el.mid = mk('div', 'q-layer q-mid', stage);
		el.near = mk('div', 'q-layer q-near', stage);
		el.embers = mk('div', 'q-embers', stage);
		for (var i = 0; i < 14; i++) {
			var e = mk('i', null, el.embers);
			e.style.left = (rnd() * 100) + '%';
			e.style.animationDelay = (-rnd() * 9) + 's';
			e.style.animationDuration = (7 + rnd() * 6) + 's';
		}
		el.world = mk('div', 'q-world', stage);
		el.fire = mk('canvas', 'q-fire', stage);
		el.dragon = mk('canvas', 'q-dragon-3d', stage);
		[el.stars, el.moon, el.far, el.mid, el.near, el.embers, el.fire, el.dragon].forEach(function (n) { n.setAttribute('aria-hidden', 'true'); });

		/* HUD */
		el.hud = mk('div', 'q-hud', stage);
		el.hudWorld = mk('div', 'world', el.hud);
		el.xp = mk('div', 'q-xp', el.hud, '<i></i>');
		el.xp.setAttribute('aria-hidden', 'true');
		el.xpFill = el.xp.firstChild;
		el.hudLoot = mk('div', 'loot', el.hud);
		el.hudLoot.setAttribute('aria-live', 'polite');
		el.listBtn = mk('button', null, el.hud, '&#9776; List');
		el.listBtn.type = 'button';
		el.listBtn.setAttribute('data-quest', 'list');
		el.listBtn.setAttribute('aria-label', 'Switch to the plain list of projects');

		el.rail = mk('div', 'q-rail', stage);
		el.rail.setAttribute('role', 'navigation');
		el.rail.setAttribute('aria-label', 'Leave the flight');
		el.upBtn = mk('button', 'q-rail-up', el.rail, '<span aria-hidden="true">&#9650;</span> Go back up');
		el.upBtn.type = 'button';
		el.upBtn.setAttribute('data-quest', 'up');
		el.upBtn.setAttribute('aria-label', 'Go back up the page, above the flight');
		el.downBtn = mk('button', 'q-rail-down', el.rail, 'Go down <span aria-hidden="true">&#9660;</span>');
		el.downBtn.type = 'button';
		el.downBtn.setAttribute('data-quest', 'exit');
		el.downBtn.setAttribute('aria-label', 'Go down the page, past the flight');

		el.help = mk('div', 'q-help', stage, 'Scroll to fly through my work &#9660;');
		el.help.setAttribute('aria-hidden', 'true');

		el.map = mk('div', 'q-map', stage);
		el.map.setAttribute('role', 'navigation');
		el.map.setAttribute('aria-label', 'Jump to a world');
		levels.forEach(function (lv) {
			var b = mk('button', null, el.map, lv.finale ? '&#9733;' : 'W' + lv.n);
			b.type = 'button';
			b.title = lv.finale ? 'Your quest' : 'World ' + lv.n + ': ' + lv.place;
			b.setAttribute('aria-label', b.title.replace(/&amp;/g, '&'));
			b.addEventListener('click', function () {
				var idx = stops.indexOf(stops.filter(function (s) { return s.lv === lv; })[0]);
				hopTo(idx);
			});
			lv.mapBtn = b;
		});

		/* the window */
		el.win = mk('div', 'q-win', stage);
		el.win.setAttribute('role', 'dialog');
		el.win.setAttribute('aria-modal', 'false');
		el.win.setAttribute('aria-labelledby', 'q-win-t');
		el.winBar = mk('div', 'q-win-bar', el.win);
		el.winT = mk('span', 't', el.winBar);
		el.winT.id = 'q-win-t';
		el.prev = mk('button', null, el.winBar, '&#9664;');
		el.prev.type = 'button'; el.prev.setAttribute('aria-label', 'Previous project');
		el.next = mk('button', null, el.winBar, '&#9654;');
		el.next.type = 'button'; el.next.setAttribute('aria-label', 'Next project');
		el.close = mk('button', null, el.winBar, '&#10005;');
		el.close.type = 'button'; el.close.setAttribute('aria-label', 'Close this window');
		el.winIn = mk('div', 'q-win-in', el.win);
		el.prev.addEventListener('click', function () { hopTo((current == null ? 0 : current) - 1); });
		el.next.addEventListener('click', function () { hopTo((current == null ? -1 : current) + 1); });
		el.close.addEventListener('click', function () { dismissed = current; closeWindow(); });

		/* chests + signs live in the world layer; built in layout() */
		stops.forEach(function (s, i) {
			var b = mk('button', 'q-node' + (s.locked ? ' q-node--locked' : '') + (s.finale ? ' q-node--castle' : ''), null,
				(s.finale ? CASTLE : s.locked ? EGG_NODE : CHEST) + '<span class="lbl">' + escapeHtml(s.title) + '</span>');
			b.type = 'button';
			b.setAttribute('aria-label', 'Fly to ' + s.title);
			b.addEventListener('click', function () { hopTo(i); });
			s.node = b;
		});
		levels.forEach(function (lv) {
			if (lv.finale) { return; }
			lv.sign = mk('div', 'q-sign', null,
				'<span class="board"><small>World ' + lv.n + ' &middot; ' + lv.place + '</small>' + lv.name + '</span><span class="post"></span>');
			lv.sign.setAttribute('aria-hidden', 'true');
		});
	}

	function escapeHtml(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

	/* ---- geometry -------------------------------------------------------- */
	var W = 0, H = 0, mobile = false;
	var dragonX = 0, nodeScreenX = 0, K = 1;
	var maxX = 1, worldW = 1;
	var segs = [], U = 0;
	var trackTop = 0;
	var signs = [];

	function pathY(x) {
		var base = mobile ? H * 0.3 : H * 0.8;
		var A = mobile ? H * 0.025 : H * 0.04;
		return base + A * Math.sin(x / (W * 0.62)) + A * 0.45 * Math.sin(x / (W * 0.23) + 1.3);
	}

	function layout() {
		if (!built) { return; }
		W = stage.clientWidth; H = stage.clientHeight;
		if (!W || !H) { return; }
		mobile = W < 761;
		dragonX = mobile ? W * 0.2 : W * 0.17;
		nodeScreenX = mobile ? W * 0.62 : W * 0.315;
		K = mobile ? H * 0.62 : H * 0.72;     /* px of page scroll per unit */

		/* lay the line out */
		var spacing = mobile ? W * 0.95 : Math.max(W * 0.85, 760);
		var cursor = W * 0.75;
		signs = [];
		levels.forEach(function (lv) {
			if (!lv.finale) {
				lv.signX = cursor + (mobile ? W * 0.1 : W * 0.05);
				cursor += mobile ? W * 0.75 : W * 0.5;
			} else {
				cursor += W * 0.2;
			}
			lv.startX = (lv.signX || cursor) - W * 0.4;
			lv.items.forEach(function () { /* counted below */ });
			stops.filter(function (s) { return s.lv === lv; }).forEach(function (s) {
				s.x = cursor;
				s.y = pathY(s.x);
				s.worldAt = s.x - nodeScreenX;  /* world offset that parks this chest at nodeScreenX */
				cursor += spacing;
			});
		});
		maxX = stops[stops.length - 1].worldAt;
		worldW = maxX + W * 1.2;

		/* segments: travel / dwell */
		segs = []; U = 0;
		var from = 0;
		stops.forEach(function (s, i) {
			var dist = s.worldAt - from;
			var tLen = Math.max(0.6, dist / (W * 0.9));
			segs.push({ type: 'travel', from: from, to: s.worldAt, u0: U, len: tLen, next: i });
			U += tLen;
			var dLen = s.finale ? 1.1 : 1.5;
			segs.push({ type: 'dwell', at: s.worldAt, u0: U, len: dLen, stop: i });
			U += dLen;
			from = s.worldAt;
		});
		U += 0.15;
		track.style.height = Math.round(U * K + H) + 'px';

		buildScenery();
		placeWorld();
		measure();
	}

	function measure() {
		trackTop = track.getBoundingClientRect().top + window.pageYOffset;
	}

	/* the ember line + chests + signs */
	function placeWorld() {
		el.world.innerHTML = '';
		el.world.style.width = worldW + 'px';
		var svg = document.createElementNS(SVGNS, 'svg');
		svg.setAttribute('class', 'q-path');
		svg.setAttribute('width', worldW); svg.setAttribute('height', H);
		svg.setAttribute('aria-hidden', 'true');
		var d = 'M0 ' + pathY(0).toFixed(1);
		for (var x = 30; x <= worldW; x += 30) { d += ' L' + x + ' ' + pathY(x).toFixed(1); }
		var rail = document.createElementNS(SVGNS, 'path');
		rail.setAttribute('class', 'rail'); rail.setAttribute('d', d);
		var defs = document.createElementNS(SVGNS, 'defs');
		var cp = document.createElementNS(SVGNS, 'clipPath'); cp.setAttribute('id', 'q-lit-clip');
		el.litRect = document.createElementNS(SVGNS, 'rect');
		el.litRect.setAttribute('x', 0); el.litRect.setAttribute('y', 0); el.litRect.setAttribute('height', H); el.litRect.setAttribute('width', 0);
		cp.appendChild(el.litRect); defs.appendChild(cp);
		var lit = document.createElementNS(SVGNS, 'path');
		lit.setAttribute('class', 'lit'); lit.setAttribute('d', d); lit.setAttribute('clip-path', 'url(#q-lit-clip)');
		svg.appendChild(defs); svg.appendChild(rail); svg.appendChild(lit);
		el.world.appendChild(svg);

		levels.forEach(function (lv) {
			if (!lv.sign) { return; }
			lv.sign.style.left = lv.signX + 'px';
			lv.sign.style.top = (pathY(lv.signX) - 6) + 'px';
			el.world.appendChild(lv.sign);
		});
		stops.forEach(function (s) {
			s.node.style.left = s.x + 'px';
			s.node.style.top = s.y + 'px';
			el.world.appendChild(s.node);
		});
	}

	/* ---- procedural scenery ---------------------------------------------
	   Three silhouette layers moving at different speeds. Each world gets
	   a landmark in the middle layer: a castle in the valleys, chimneys at
	   the forge, striped market stalls in town, an arena for the team
	   builds, and the final castle. */
	var FAR_F = 0.12, MID_F = 0.38, NEAR_F = 0.7;

	function svgLayer(host, width, inner) {
		host.innerHTML = '<svg width="' + Math.ceil(width) + '" height="' + H + '" viewBox="0 0 ' + Math.ceil(width) + ' ' + H + '" preserveAspectRatio="none">' + inner + '</svg>';
		host.style.width = Math.ceil(width) + 'px';
	}

	function ridge(width, baseY, amp, step, jag) {
		var d = 'M0 ' + H + ' L0 ' + baseY;
		for (var x = 0; x <= width + step; x += step) {
			var y = baseY - amp * (0.5 + 0.5 * Math.sin(x / (step * 2.7) + rnd() * jag)) - rnd() * amp * 0.35;
			d += ' L' + x + ' ' + y.toFixed(1);
		}
		return d + ' L' + (width + step) + ' ' + H + ' Z';
	}

	/* ---- real Cardiff landmarks, drawn as silhouettes -------------------
	   Coordinates are in "landmark units" (about a pixel on a 760px-tall
	   screen), y measured UP from the ground line, then scaled by s. */
	function P(cx, gy, s, pts) {     /* polygon from [x,y] pairs */
		return pts.map(function (p, i) { return (i ? 'L' : 'M') + (cx + p[0] * s).toFixed(1) + ' ' + (gy - p[1] * s).toFixed(1); }).join(' ') + 'Z';
	}

	/* Castell Coch: the red castle on the wooded hill above Tongwynlais —
	   three round towers with tall conical "witch's hat" roofs (the
	   Keep, Kitchen and Well towers), joined by curtain walls, sitting
	   in the beech woods. */
	function castellCoch(cx, gy, s) {
		var o = '';
		/* wooded hillside: a dome of tree crowns */
		var hill = [[-260, 0]];
		for (var x = -250; x <= 250; x += 18) {
			var h = 70 * Math.cos((x / 260) * Math.PI / 2) + (Math.sin(x * 0.37) + Math.sin(x * 0.11)) * 5;
			hill.push([x, Math.max(0, h)]);
		}
		hill.push([260, 0]);
		o += '<path class="lm" d="' + P(cx, gy, s, hill) + '"/>';
		var base = 62;
		/* curtain walls + gatehouse */
		o += '<path class="lm" d="' + P(cx, gy, s, [[-78, base], [-78, base + 52], [-28, base + 58], [-28, base], [30, base], [30, base + 56], [70, base + 50], [70, base]]) + '"/>';
		o += '<path class="lm" d="' + P(cx, gy, s, [[-28, base], [-28, base + 62], [30, base + 62], [30, base]]) + '"/>';
		/* towers: [centre x, radius, wall height, roof height] */
		[[-92, 22, 92, 74], [2, 30, 118, 92], [84, 19, 80, 62]].forEach(function (t, i) {
			var x0 = t[0] - t[1], x1 = t[0] + t[1], top = base + t[2];
			o += '<path class="lm" d="' + P(cx, gy, s, [[x0, base], [x0, top], [x1, top], [x1, base]]) + '"/>';
			/* the conical roof, slightly flared at the eaves */
			o += '<path class="lm roof" d="M' + (cx + (x0 - 5) * s).toFixed(1) + ' ' + (gy - top * s).toFixed(1) +
				' Q' + (cx + (t[0] - t[1] * 0.35) * s).toFixed(1) + ' ' + (gy - (top + t[3] * 0.45) * s).toFixed(1) +
				' ' + (cx + t[0] * s).toFixed(1) + ' ' + (gy - (top + t[3]) * s).toFixed(1) +
				' Q' + (cx + (t[0] + t[1] * 0.35) * s).toFixed(1) + ' ' + (gy - (top + t[3] * 0.45) * s).toFixed(1) +
				' ' + (cx + (x1 + 5) * s).toFixed(1) + ' ' + (gy - top * s).toFixed(1) + 'Z"/>';
			/* finial spike on top */
			o += '<path class="lm" d="' + P(cx, gy, s, [[t[0] - 1.5, top + t[3] - 2], [t[0], top + t[3] + 14], [t[0] + 1.5, top + t[3] - 2]]) + '"/>';
			/* lit windows */
			o += '<rect class="win-glow" x="' + (cx + (t[0] - 3) * s).toFixed(1) + '" y="' + (gy - (base + t[2] * 0.62) * s).toFixed(1) + '" width="' + (6 * s).toFixed(1) + '" height="' + (11 * s).toFixed(1) + '"/>';
			if (i === 1) { o += '<rect class="win-glow" x="' + (cx - 9 * s).toFixed(1) + '" y="' + (gy - (base + 40) * s).toFixed(1) + '" width="' + (5 * s).toFixed(1) + '" height="' + (9 * s).toFixed(1) + '"/><rect class="win-glow" x="' + (cx + 6 * s).toFixed(1) + '" y="' + (gy - (base + 40) * s).toFixed(1) + '" width="' + (5 * s).toFixed(1) + '" height="' + (9 * s).toFixed(1) + '"/>'; }
		});
		/* Keep tower's chimney stack */
		o += '<path class="lm" d="' + P(cx, gy, s, [[18, base + 160], [18, base + 186], [25, base + 186], [25, base + 150]]) + '"/>';
		/* a red banner, because it's the red castle */
		o += '<path class="lm" d="' + P(cx, gy, s, [[1, base + 222], [1, base + 250], [3, base + 250], [3, base + 222]]) + '"/>';
		o += '<path class="flag" d="' + P(cx, gy, s, [[3, base + 250], [24, base + 244], [3, base + 238]]) + '"/>';
		return o;
	}

	/* The Principality Stadium: the big oval bowl on the Taff with a
	   gently arched roof and four tall white masts at the corners, each
	   holding the roof up on cable stays. */
	function principality(cx, gy, s) {
		var o = '';
		var mast = function (x, top, lean, cls) {
			return '<line class="' + cls + '" x1="' + (cx + x * s).toFixed(1) + '" y1="' + gy.toFixed(1) + '" x2="' + (cx + (x + lean) * s).toFixed(1) + '" y2="' + (gy - top * s).toFixed(1) + '" stroke-width="' + (5 * s).toFixed(1) + '"/>';
		};
		var cable = function (x1, y1, x2, y2) {
			return '<line class="cable" x1="' + (cx + x1 * s).toFixed(1) + '" y1="' + (gy - y1 * s).toFixed(1) + '" x2="' + (cx + x2 * s).toFixed(1) + '" y2="' + (gy - y2 * s).toFixed(1) + '" stroke-width="' + (1.4 * s).toFixed(1) + '"/>';
		};
		/* back pair of masts first, so the bowl overlaps their feet */
		o += mast(-104, 196, -8, 'mast mast--back') + mast(104, 196, 8, 'mast mast--back');
		/* the bowl + arched roof */
		o += '<path class="lm stadium" d="M' + (cx - 190 * s).toFixed(1) + ' ' + gy.toFixed(1) +
			' L' + (cx - 172 * s).toFixed(1) + ' ' + (gy - 66 * s).toFixed(1) +
			' Q' + cx.toFixed(1) + ' ' + (gy - 122 * s).toFixed(1) + ' ' + (cx + 172 * s).toFixed(1) + ' ' + (gy - 66 * s).toFixed(1) +
			' L' + (cx + 190 * s).toFixed(1) + ' ' + gy.toFixed(1) + 'Z"/>';
		/* roof edge catching the floodlights */
		o += '<path class="rim" stroke-width="' + (2.5 * s).toFixed(1) + '" d="M' + (cx - 172 * s).toFixed(1) + ' ' + (gy - 66 * s).toFixed(1) +
			' Q' + cx.toFixed(1) + ' ' + (gy - 122 * s).toFixed(1) + ' ' + (cx + 172 * s).toFixed(1) + ' ' + (gy - 66 * s).toFixed(1) + '"/>';
		/* ribbed facade: the stadium's vertical ribs, plus two rows of lit
		   concourse windows */
		for (var k = -7; k <= 7; k++) {
			var rx = k * 23, rTop = 66 + (122 - 66) * 0.5 * (1 - Math.pow(rx / 172, 2));
			o += '<line class="rib" x1="' + (cx + rx * s).toFixed(1) + '" y1="' + (gy - 6 * s).toFixed(1) + '" x2="' + (cx + rx * 0.97 * s).toFixed(1) + '" y2="' + (gy - rTop * s).toFixed(1) + '" stroke-width="' + (1.6 * s).toFixed(1) + '"/>';
			if (k < 7) {
				o += '<rect class="win-glow" x="' + (cx + (rx + 6) * s).toFixed(1) + '" y="' + (gy - 58 * s).toFixed(1) + '" width="' + (11 * s).toFixed(1) + '" height="' + (6 * s).toFixed(1) + '"/>';
				o += '<rect class="win-glow dim" x="' + (cx + (rx + 6) * s).toFixed(1) + '" y="' + (gy - 36 * s).toFixed(1) + '" width="' + (11 * s).toFixed(1) + '" height="' + (6 * s).toFixed(1) + '"/>';
			}
		}
		/* front masts + cable stays down to the roof */
		o += mast(-150, 210, -14, 'mast') + mast(150, 210, 14, 'mast');
		[-1, 1].forEach(function (d) {
			var tx = d * 164, ty = 210;
			[[d * 120, 94], [d * 80, 106], [d * 40, 114]].forEach(function (pt) { o += cable(tx, ty, pt[0], pt[1]); });
		});
		/* floodlight bloom above the pitch */
		o += '<ellipse class="bloom" cx="' + cx.toFixed(1) + '" cy="' + (gy - 120 * s).toFixed(1) + '" rx="' + (150 * s).toFixed(1) + '" ry="' + (40 * s).toFixed(1) + '"/>';
		return o;
	}

	function landmark(kind, cx, groundY, s) {
		var o = '';
		var r = function (x, y, w, h, cls) { return '<rect class="' + (cls || 'lm') + '" x="' + (cx + x * s).toFixed(1) + '" y="' + (groundY - y * s).toFixed(1) + '" width="' + (w * s).toFixed(1) + '" height="' + (h * s).toFixed(1) + '"/>'; };
		if (kind === 1) {           /* the valleys: Castell Coch on its wooded hill */
			return castellCoch(cx, groundY, s * 0.85);
		} else if (kind === 2) {    /* forge */
			o += r(-90, 60, 180, 60) + r(-70, 140, 22, 140) + r(30, 170, 26, 170) + r(-20, 100, 18, 100);
			o += r(-50, 30, 16, 14, 'win-glow') + r(10, 30, 16, 14, 'win-glow') + r(50, 30, 16, 14, 'win-glow');
			o += '<circle class="smoke" cx="' + (cx - 59 * s) + '" cy="' + (groundY - 160 * s) + '" r="' + 14 * s + '"/>';
			o += '<circle class="smoke" cx="' + (cx + 43 * s) + '" cy="' + (groundY - 195 * s) + '" r="' + 18 * s + '" style="animation-delay:-2s"/>';
		} else if (kind === 3) {    /* market town */
			for (var k = 0; k < 5; k++) {
				var x0 = -125 + k * 52, h = 54 + (k % 2) * 26;
				o += r(x0, h, 44, h) + '<path class="lm" d="M' + (cx + (x0 - 4) * s) + ' ' + (groundY - h * s) + ' L' + (cx + (x0 + 22) * s) + ' ' + (groundY - (h + 26) * s) + ' L' + (cx + (x0 + 48) * s) + ' ' + (groundY - h * s) + 'Z"/>';
				o += r(x0 + 14, h - 14, 14, 12, 'win-glow');
			}
		} else if (kind === 4) {    /* the arena: the Principality Stadium */
			return principality(cx, groundY - 8 * s, s * 1.2);
		}
		return o;
	}

	function buildScenery() {
		seed = 11;
		var farW = W + maxX * FAR_F + 40, midW = W + maxX * MID_F + 40, nearW = W + maxX * NEAR_F + 40;
		var groundMid = mobile ? H * 0.5 : H * 0.84;
		svgLayer(el.far, farW, '<path d="' + ridge(farW, mobile ? H * 0.42 : H * 0.66, H * 0.2, 90, 3) + '"/>');
		var mid = '<path d="' + ridge(midW, groundMid, H * 0.06, 60, 2) + '"/>';
		var s = Math.max(0.6, Math.min(1.25, H / 760)) * (mobile ? 0.7 : 1);
		levels.forEach(function (lv, i) {
			if (lv.finale) {
				/* the final world: Castell Coch, big, on its hill behind
				   the dragon and the last chest, clear of the open window */
				var fin = stops[stops.length - 1];
				var atF = fin.worldAt * MID_F + (mobile ? W * 0.5 : W * 0.2);
				mid += castellCoch(atF, groundMid - H * 0.01, s * (mobile ? 1.15 : 1.45));
				return;
			}
			var at = (lv.signX - nodeScreenX + W * 0.75) * MID_F + W * 0.25;
			mid += landmark(i + 1, at, groundMid - H * 0.03, s);
		});
		svgLayer(el.mid, midW, mid);
		if (mobile) { el.near.innerHTML = ''; }
		else { svgLayer(el.near, nearW, '<path d="' + ridge(nearW, H * 0.97, H * 0.035, 40, 4) + '"/>'); }
	}

	/* ---- scroll -> world position ---------------------------------------- */
	function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

	var u = 0;
	function targetFromScroll() {
		u = -track.getBoundingClientRect().top / K;
		u = Math.max(0, Math.min(U, u));
		var res = { x: 0, stop: null, seg: null, t: 0 };
		for (var i = 0; i < segs.length; i++) {
			var sg = segs[i];
			if (u <= sg.u0 + sg.len || i === segs.length - 1) {
				var t = Math.max(0, Math.min(1, (u - sg.u0) / sg.len));
				res.seg = sg; res.t = t;
				if (sg.type === 'dwell') { res.x = sg.at; res.stop = sg.stop; }
				else {
					res.x = sg.from + (sg.to - sg.from) * ease(t);
					/* keep the window up a beat as you leave, and pop the
					   next one a beat before you land */
					if (t < 0.1 && sg.next > 0) { res.stop = sg.next - 1; }
					if (t > 0.94) { res.stop = sg.next; }
				}
				return res;
			}
		}
		return res;
	}

	function uForStop(i) {
		for (var k = 0; k < segs.length; k++) {
			if (segs[k].type === 'dwell' && segs[k].stop === i) { return segs[k].u0 + segs[k].len * 0.45; }
		}
		return 0;
	}

	function hopTo(i) {
		if (!flying) { return; }
		i = Math.max(0, Math.min(stops.length - 1, i));
		dismissed = null;
		window.scrollTo({ top: track.getBoundingClientRect().top + window.pageYOffset + uForStop(i) * K, behavior: reduce ? 'auto' : 'smooth' });
	}

	/* ---- window ---------------------------------------------------------- */
	var current = null, dismissed = null, autoRaf = 0, autoStop = false;

	function openWindow(i) {
		var s = stops[i];
		current = i;
		var clone = s.art.cloneNode(true);
		clone.removeAttribute('id');
		[].forEach.call(clone.querySelectorAll('[id]'), function (n) { n.removeAttribute('id'); });
		[].forEach.call(clone.querySelectorAll('img'), function (img) { img.loading = 'eager'; });
		var h = clone.querySelector('.qi-title');
		el.winIn.innerHTML = '';
		el.winIn.appendChild(clone);
		el.winT.innerHTML = (s.finale ? '&#9733; Final world' : '&#9670; Quest ' + s.num + '/' + TREASURES) + ' &middot; ' + s.lv.place;
		el.winT.setAttribute('aria-label', (h ? h.textContent : s.title));
		el.prev.disabled = i === 0;
		el.next.disabled = i === stops.length - 1;

		/* grow the window out of the chest it belongs to */
		var wr = el.win.getBoundingClientRect(), sr = stage.getBoundingClientRect();
		var ox = nodeScreenX - (wr.left - sr.left), oy = s.y - 40 - (wr.top - sr.top);
		el.win.style.transformOrigin = ox + 'px ' + oy + 'px';
		el.win.classList.add('is-open');

		startAutoScroll(clone);
	}

	function closeWindow(instant) {
		if (current == null && !instant) { return; }
		current = null;
		cancelAnimationFrame(autoRaf);
		if (el.win) { el.win.classList.remove('is-open'); }
	}

	/* the screenshot drifts down on its own so you see the whole site,
	   and stops for good the moment you touch it */
	function startAutoScroll(clone) {
		cancelAnimationFrame(autoRaf);
		var sc = clone.querySelector(mobile ? '.qi-phone .qi-scroll' : '.qi-browser .qi-scroll');
		if (!sc) { return; }
		var hint = document.createElement('div');
		hint.className = 'q-scrollhint';
		hint.textContent = '▼ Scroll the real site';
		hint.setAttribute('aria-hidden', 'true');
		(sc.closest('.qi-screens') || clone).appendChild(hint);
		autoStop = reduce;
		var stopIt = function () { autoStop = true; hint.classList.add('gone'); };
		['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (ev) { sc.addEventListener(ev, stopIt, { passive: true }); });
		sc.addEventListener('scroll', function () { if (sc.scrollTop > 40) { hint.classList.add('gone'); } }, { passive: true });
		var startAt = performance.now() + 1400, last = 0, pos = 0;
		function step(now) {
			if (autoStop) { return; }
			autoRaf = requestAnimationFrame(step);
			if (now < startAt) { last = now; return; }
			var dt = Math.min(50, now - last); last = now;
			pos += dt * (mobile ? 0.05 : 0.075);
			if (pos >= sc.scrollHeight - sc.clientHeight) { autoStop = true; return; }
			sc.scrollTop = pos;
		}
		autoRaf = requestAnimationFrame(step);
	}

	/* ---- treasure fx ----------------------------------------------------- */
	var found = {};
	var foundCount = 0;
	function celebrate(i) {
		var s = stops[i];
		s.node.classList.add('is-open');
		if (!found[i] && !s.finale) {
			found[i] = true; foundCount++;
			s.node.classList.add('is-found');
			if (!reduce) {
				for (var c = 0; c < 9; c++) {
					var coin = mk('span', 'q-coin', el.world);
					coin.style.left = (s.x - 7) + 'px';
					coin.style.top = (s.y - 40) + 'px';
					coin.style.setProperty('--dx', ((Math.random() - 0.5) * 140).toFixed(0) + 'px');
					coin.style.setProperty('--dy', (-60 - Math.random() * 90).toFixed(0) + 'px');
					coin.style.animationDelay = (c * 0.04) + 's';
					setTimeout(function (n) { n.remove(); }.bind(null, coin), 1500);
				}
				var plus = mk('span', 'q-plus', el.world, s.locked ? 'Egg found! Hatching soon' : '+1 Treasure');
				plus.style.left = s.x + 'px'; plus.style.top = (s.y - 92) + 'px';
				setTimeout(function () { plus.remove(); }, 1400);
			}
		}
	}

	/* ---- dragon bridge --------------------------------------------------- */
	var dragonState = window.__questDragon = window.__questDragon || {
		x: 0, y: 0, dir: 1, size: 200, breathe: false, visible: false, canvas: null, fireCanvas: null, speed: 0
	};
	function publishDragon(visible) { dragonState.visible = !!visible; if (!visible) { dragonState.breathe = false; } }

	/* ---- main loop ------------------------------------------------------- */
	var running = false, raf = 0;
	var curX = 0, prevX = 0, faceDir = 1, breatheUntil = 0;
	var lastLevel = null;

	function frame(now) {
		raf = requestAnimationFrame(frame);
		var tgt = targetFromScroll();
		curX += (tgt.x - curX) * (reduce || window.__questInstant ? 1 : 0.12);
		if (Math.abs(tgt.x - curX) < 0.3) { curX = tgt.x; }
		var vel = curX - prevX; prevX = curX;

		el.world.style.transform = 'translate3d(' + (-curX).toFixed(1) + 'px,0,0)';
		el.far.style.transform = 'translate3d(' + (-curX * FAR_F).toFixed(1) + 'px,0,0)';
		el.mid.style.transform = 'translate3d(' + (-curX * MID_F).toFixed(1) + 'px,0,0)';
		el.near.style.transform = 'translate3d(' + (-curX * NEAR_F).toFixed(1) + 'px,0,0)';
		el.stars.style.backgroundPosition = (-curX * 0.04).toFixed(1) + 'px 0';
		el.litRect.setAttribute('width', Math.max(0, curX + dragonX).toFixed(0));
		if (Math.abs(vel) > 2) { stage.classList.add('has-moved'); }

		/* which world are we in? blend the sky towards it */
		var li = 0;
		for (var k = 0; k < levels.length; k++) { if (curX + dragonX >= levels[k].startX) { li = k; } }
		var lv = levels[li];
		var nextLv = levels[li + 1];
		var blend = 0;
		if (nextLv) {
			var span = W * 0.6;
			blend = Math.max(0, Math.min(1, (curX + dragonX - (nextLv.startX - span)) / span));
		}
		setSky(li, blend);
		if (lv !== lastLevel) {
			lastLevel = lv;
			el.hudWorld.innerHTML = (lv.finale ? 'Final world &middot; <b>The Castle</b>' : 'World ' + lv.n + ' &middot; <b>' + lv.place + '</b>');
			levels.forEach(function (l) { l.mapBtn.setAttribute('aria-current', String(l === lv)); });
		}
		el.xpFill.style.width = 'calc(' + (Math.min(1, curX / maxX) * 100).toFixed(2) + '% - 4px)';
		var lootTxt = '&#9670; <b>' + foundCount + '</b>/' + TREASURES + '<span class="lt"> treasures</span>';
		if (lootTxt !== el.hudLoot._t) { el.hudLoot.innerHTML = lootTxt; el.hudLoot._t = lootTxt; }

		/* open / close windows */
		var want = tgt.stop;
		if (want !== null && Math.abs(stops[want].worldAt - curX) > W * 0.25) { want = null; }
		if (want !== current) {
			if (want === null || want === dismissed) { if (current !== null) { closeWindow(); } }
			else {
				if (current !== null) { closeWindow(); }
				openWindow(want);
				celebrate(want);
				breatheUntil = now + (stops[want].finale ? 2600 : 1300);
			}
		}
		if (want === null) { dismissed = null; }

		/* dragon */
		if (vel > 0.6) { faceDir = 1; } else if (vel < -0.6) { faceDir = -1; }
		else if (current !== null) { faceDir = 1; }
		var lag = Math.max(-W * 0.05, Math.min(W * 0.05, -vel * 3));
		var size = mobile ? Math.min(W * 0.36, H * 0.2) : Math.min(W * 0.2, H * 0.32);
		dragonState.x = dragonX + lag;
		dragonState.y = pathY(curX + dragonX) - size * (mobile ? 0.28 : 0.4);
		dragonState.dir = faceDir;
		dragonState.size = size;
		dragonState.speed = Math.abs(vel);
		dragonState.breathe = now < breatheUntil;
		dragonState.visible = true;
		dragonState.canvas = el.dragon;
		dragonState.fireCanvas = el.fire;
		dragonState.W = W; dragonState.H = H;
	}

	function hexMix(a, b, t) {
		var pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
		var r = Math.round(((pa >> 16) & 255) * (1 - t) + ((pb >> 16) & 255) * t);
		var g = Math.round(((pa >> 8) & 255) * (1 - t) + ((pb >> 8) & 255) * t);
		var bl = Math.round((pa & 255) * (1 - t) + (pb & 255) * t);
		return '#' + ((1 << 24) + (r << 16) + (g << 8) + bl).toString(16).slice(1);
	}
	var skyKey = '';
	function setSky(li, blend) {
		var key = li + ':' + blend.toFixed(2);
		if (key === skyKey) { return; }
		skyKey = key;
		var a = PALETTE[Math.min(li, PALETTE.length - 1)], b = PALETTE[Math.min(li + 1, PALETTE.length - 1)];
		var names = ['--sky-a', '--sky-b', '--far', '--mid', '--near'];
		for (var i = 0; i < 5; i++) { stage.style.setProperty(names[i], hexMix(a[i], b[i], blend)); }
	}

	function inView() {
		var r = track.getBoundingClientRect();
		return r.bottom > 0 && r.top < window.innerHeight;
	}
	function startLoop() { if (!running && flying) { running = true; raf = requestAnimationFrame(frame); } }
	function stopLoop() { if (running) { running = false; cancelAnimationFrame(raf); } publishDragon(false); }

	window.addEventListener('scroll', function () {
		if (!flying) { return; }
		if (inView()) { startLoop(); } else { stopLoop(); closeWindow(); }
	}, { passive: true });

	var rT = 0;
	window.addEventListener('resize', function () {
		clearTimeout(rT);
		rT = setTimeout(function () { if (flying) { var cur = current; closeWindow(true); layout(); current = null; if (cur != null) { dismissed = null; } } }, 150);
	});
	window.addEventListener('load', function () { if (flying) { measure(); } });
	document.addEventListener('visibilitychange', function () { if (document.hidden) { stopLoop(); } else if (flying && inView()) { startLoop(); } });

	/* keyboard: arrows hop between chests while the stage fills the screen */
	document.addEventListener('keydown', function (e) {
		if (!flying || e.altKey || e.ctrlKey || e.metaKey) { return; }
		if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') { return; }
		var tag = (e.target && e.target.tagName) || '';
		if (/INPUT|TEXTAREA|SELECT/.test(tag)) { return; }
		var r = track.getBoundingClientRect();
		if (r.top > 2 || r.bottom < window.innerHeight - 2) { return; }
		e.preventDefault();
		var base = current != null ? current : nearestStop();
		hopTo(base + (e.key === 'ArrowRight' ? 1 : -1));
	});
	function nearestStop() {
		var best = 0, bd = Infinity;
		stops.forEach(function (s, i) { var d = Math.abs(s.worldAt - curX); if (d < bd) { bd = d; best = i; } });
		return s0(best);
		function s0(b) { return stops[b].worldAt > curX ? b - 1 : b; }
	}

	/* ---- go -------------------------------------------------------------- */
	var pref = storeGet();
	if (reduce && pref !== 'fly') { setFlying(false); }
	else if (pref === 'list') { setFlying(false); }
	else { setFlying(true); }
}());
