/*----------------------------------------------

[Hero fire breath]

Just the flame — the dot-dragon body that used to live in this file
has been replaced by a 3D model (see dragon3d.js). This file keeps
the exact particle mechanics that were already tuned here: the same
soft sprite, the same spawn/fade/travel math, the same lifecycle
(pause off-screen, pause when the tab is hidden, a single still
frame for prefers-reduced-motion).

The 3D layer writes the mouth's current screen position into
window.__dragonMouth each frame; this file only spawns particles
once that mouth is marked active (the model has arrived and is
breathing), and reads wherever it currently is — so the flame
tracks the model through its flight-in without either file needing
to know the other's internals.

----------------------------------------------*/

(function () {
	'use strict';

	var canvas = document.querySelector('.sjh-dragon-canvas');
	if (!canvas || !canvas.getContext) { return; }
	var ctx = canvas.getContext('2d');
	if (!ctx) { return; }

	var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	var W = 0, H = 0, dpr = 1;

	function resize() {
		var box = canvas.parentNode.getBoundingClientRect();
		if (!box.width) { return; }
		dpr = Math.min(window.devicePixelRatio || 1, 1.25);
		W = Math.round(box.width);
		H = Math.round(box.height);
		canvas.width = W * dpr;
		canvas.height = H * dpr;
		canvas.style.width = W + 'px';
		canvas.style.height = H + 'px';
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
	}

	/* ---- flame particles -------------------------------------------
	   The soft blob is drawn once into an offscreen canvas and then
	   stamped with drawImage. Building a radial gradient for every
	   particle on every frame is what made this expensive. */
	var SPRITE = (function () {
		var c = document.createElement('canvas'), n = 64;
		c.width = c.height = n;
		var g2 = c.getContext('2d');
		var gr = g2.createRadialGradient(n / 2, n / 2, 0, n / 2, n / 2, n / 2);
		gr.addColorStop(0,    'rgba(255,231,166,0.95)');
		gr.addColorStop(0.35, 'rgba(255,150,40,0.55)');
		gr.addColorStop(1,    'rgba(255,59,31,0)');
		g2.fillStyle = gr;
		g2.fillRect(0, 0, n, n);
		return c;
	}());

	/* dirX/dirY: unit vector the mouth is currently pointing. The 3D layer
	   writes this every frame from the model's actual facing — currently
	   always straight left, since the dragon settles permanently once it
	   arrives, but this stays direction-aware rather than hardcoded so it
	   isn't wrong the day that changes. */
	var mouth = (window.__dragonMouth = window.__dragonMouth || { x: 0, y: 0, s: 1, active: false, dirX: -1, dirY: 0 });

	var MAX_FLAMES = 130;
	var flames = [];
	function spawn() {
		if (!mouth.active) { return; }
		if (flames.length >= MAX_FLAMES) { return; }
		var s = mouth.s || 1;
		var dx = typeof mouth.dirX === 'number' ? mouth.dirX : -1;
		var dy = typeof mouth.dirY === 'number' ? mouth.dirY : 0;
		var dmag = Math.hypot(dx, dy) || 1;
		dx /= dmag; dy /= dmag;
		/* perpendicular to the aim direction, for the little sideways jitter */
		var px = -dy, py = dx;
		var speed = 1.6 + Math.random() * 2.6;
		var jitter = (Math.random() - 0.5) * 0.5;
		flames.push({
			x: mouth.x + px * jitter * s * 0.12, y: mouth.y + py * jitter * s * 0.12,
			x0: mouth.x, y0: mouth.y,
			vx: dx * speed, vy: dy * speed + (Math.random() - 0.5) * 0.5,
			r: s * (0.012 + Math.random() * 0.024),
			life: 0,
			max: 460 + Math.random() * 260,
			travelMax: Math.max(s * 2.6, 500)
		});
	}

	/* ---- drawing --------------------------------------------------- */
	function draw() {
		ctx.clearRect(0, 0, W, H);
		var i, f, k;
		for (i = flames.length - 1; i >= 0; i--) {
			f = flames[i];
			k = f.life / f.max;
			/* how far it has travelled from the mouth, 0 there, 1 at the
			   far end of its run — direction-agnostic, since the aim can
			   now point either way */
			var dist = Math.hypot(f.x - f.x0, f.y - f.y0);
			var travel = Math.min(dist / f.travelMax, 1);
			var fade = 1 - travel * 0.88;
			/* fade in fast — a slow fade-in left new particles nearly
			   invisible while they drifted away from the mouth, reading
			   as the flame detaching from the dragon instead of leaving it */
			var a = (k < 0.02 ? k / 0.02 : (1 - k)) * 0.9 * fade;
			if (a <= 0.01) { continue; }
			var rr = f.r * (1 + k * 5.5);
			ctx.globalAlpha = a;
			ctx.drawImage(SPRITE, f.x - rr, f.y - rr, rr * 2, rr * 2);
		}
		ctx.globalAlpha = 1;
	}

	/* ---- loop ------------------------------------------------------ */
	var running = false, raf = 0, t = 0;

	function step() {
		t++;
		/* paint every other frame. At 60fps this fire looks identical and
		   costs half the main thread. */
		if (t % 2) { raf = requestAnimationFrame(step); return; }
		if (!reduce) {
			spawn();
			for (var i = flames.length - 1; i >= 0; i--) {
				var f = flames[i];
				f.x += f.vx; f.y += f.vy; f.vy -= 0.006; f.life++; /* embers rise a little regardless of aim */
				if (f.life > f.max || f.x < -80 || f.x > W + 80 || f.y < -80 || f.y > H + 80) { flames.splice(i, 1); }
			}
		}
		draw();
		raf = requestAnimationFrame(step);
	}

	function start() { if (!running) { running = true; raf = requestAnimationFrame(step); } }
	function stop()  { if (running)  { running = false; cancelAnimationFrame(raf); } }

	resize();
	if (reduce) {
		mouth.active = true;
		for (var n = 0; n < 140; n++) { spawn(); }
		for (var m = 0; m < 300; m++) {
			for (var j = 0; j < flames.length; j++) {
				flames[j].x += flames[j].vx; flames[j].y += flames[j].vy; flames[j].life++;
			}
		}
		draw();
	} else {
		start();
	}

	window.addEventListener('resize', function () { resize(); draw(); });

	document.addEventListener('visibilitychange', function () {
		if (document.hidden) { stop(); } else if (!reduce) { start(); }
	});

	if ('IntersectionObserver' in window) {
		new IntersectionObserver(function (es) {
			es.forEach(function (e) {
				if (e.isIntersecting) { if (!reduce) { start(); } }
				else { stop(); }
			});
		}, { threshold: 0.02 }).observe(canvas.parentNode);
	}
}());
