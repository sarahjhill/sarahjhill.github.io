/*----------------------------------------------

[Quest dragon — the guide through the work]

The same glTF dragon as the hero (and the comic cameo), flying the
portfolio flight in #work. quest.js owns all the game logic and just
publishes where the dragon should be through window.__questDragon:

  { x, y, size, dir (1 right / -1 left), speed, breathe, visible,
    canvas, fireCanvas, W, H }

This file eases the model towards that, turns it round when you
scroll backwards, flaps harder when it's moving fast, banks into
climbs and dives, and breathes fire (the shared SJHFire engine from
dragon.js) at each treasure as it lands.

Mesh splitting (wings + body chain) is the same technique as
dragon3d.js — see the long comments there for why it works this way.

----------------------------------------------*/

import * as THREE from 'three';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/DRACOLoader.js';

(function () {
	'use strict';

	if (!document.querySelector('#work.quest')) { return; }
	if (!window.WebGLRenderingContext) { return; }

	var MODEL_URL      = 'assets/models/dragon.glb';
	var FACE_RIGHT     = 0.95;             /* three-quarter view, snout to the right (2.623 shows its back; 1.57 is pure profile) */
	var WING_SPLIT_X   = 0.30;
	var MOUTH_OFFSET   = new THREE.Vector3(-0.033, 0.210, 0.605);
	var MOUTH_AIM      = new THREE.Vector3(-0.033, 0.210, 0.805);
	var BODY_CHAIN_Z   = [0.35, 0.05, -0.25, -0.55];
	var CHAIN_AMP      = [1.3, 1.5, 1.7, 1.9];
	var CHAIN_LAG      = [0.1, 0.075, 0.055, 0.04];

	var S = null;                 /* window.__questDragon, once quest.js has made it */
	var canvas = null, renderer = null, fire = null, mouth = null;
	var scene = new THREE.Scene();
	var camera = new THREE.OrthographicCamera(0, 1, 0, 1, -4000, 4000);

	scene.add(new THREE.HemisphereLight(0xfff2df, 0x2a1810, 2.7));
	var key = new THREE.DirectionalLight(0xffc98c, 3.0); key.position.set(-300, -200, 600); scene.add(key);
	var fill = new THREE.DirectionalLight(0xffe4c2, 1.3); fill.position.set(300, 400, 300); scene.add(fill);
	var rim = new THREE.DirectionalLight(0x88a8ff, 0.7); rim.position.set(400, 300, -400); scene.add(rim);
	var mouthGlow = new THREE.PointLight(0xff7a1a, 0, 900); scene.add(mouthGlow);

	var rig = new THREE.Group(); scene.add(rig);
	var turn = new THREE.Group(); rig.add(turn);      /* carries the left/right facing */
	var inner = null, wingL = null, wingR = null, chainPivots = [], chainAngles = [];
	var modelMaxDim = 1, loaded = false;

	function splitWings(model) {
		var mesh = null;
		model.traverse(function (o) { if (o.isMesh) { mesh = o; } });
		if (!mesh) { return null; }
		var geom = mesh.geometry, pos = geom.attributes.position, norm = geom.attributes.normal, uv = geom.attributes.uv;
		var idx = geom.index ? geom.index.array : null;
		var triCount = idx ? idx.length / 3 : pos.count / 3;
		function tri(t) { return idx ? [idx[t * 3], idx[t * 3 + 1], idx[t * 3 + 2]] : [t * 3, t * 3 + 1, t * 3 + 2]; }
		var segCount = BODY_CHAIN_Z.length + 1, segTris = [], right = [], left = [];
		for (var s = 0; s < segCount; s++) { segTris.push([]); }
		for (var t = 0; t < triCount; t++) {
			var tr = tri(t);
			var avgX = (pos.getX(tr[0]) + pos.getX(tr[1]) + pos.getX(tr[2])) / 3;
			var avgZ = (pos.getZ(tr[0]) + pos.getZ(tr[1]) + pos.getZ(tr[2])) / 3;
			if (avgX > WING_SPLIT_X) { right.push(tr); continue; }
			if (avgX < -WING_SPLIT_X) { left.push(tr); continue; }
			var si = 0;
			while (si < BODY_CHAIN_Z.length && avgZ < BODY_CHAIN_Z[si]) { si++; }
			segTris[si].push(tr);
		}
		function avgNear(test) {
			var v = new THREE.Vector3(), n = 0;
			for (var i = 0; i < pos.count; i++) { if (test(i)) { v.x += pos.getX(i); v.y += pos.getY(i); v.z += pos.getZ(i); n++; } }
			return n ? v.divideScalar(n) : v;
		}
		var pR = avgNear(function (i) { return Math.abs(pos.getX(i) - WING_SPLIT_X) < 0.05; });
		var pL = avgNear(function (i) { return Math.abs(pos.getX(i) + WING_SPLIT_X) < 0.05; });
		var segPivot = [new THREE.Vector3()];
		BODY_CHAIN_Z.forEach(function (z) { segPivot.push(avgNear(function (i) { return Math.abs(pos.getZ(i) - z) < 0.05; })); });
		function build(list, pivot) {
			var P = [], N = [], U = [];
			list.forEach(function (tr) {
				tr.forEach(function (i) {
					P.push(pos.getX(i) - pivot.x, pos.getY(i) - pivot.y, pos.getZ(i) - pivot.z);
					if (norm) { N.push(norm.getX(i), norm.getY(i), norm.getZ(i)); }
					if (uv) { U.push(uv.getX(i), uv.getY(i)); }
				});
			});
			var g = new THREE.BufferGeometry();
			g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
			if (N.length) { g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); } else { g.computeVertexNormals(); }
			if (U.length) { g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); }
			return g;
		}
		var mat = mesh.material;
		var body = new THREE.Mesh(build(segTris[0], segPivot[0]), mat);
		var rP = new THREE.Group(); rP.position.copy(pR); rP.add(new THREE.Mesh(build(right, pR), mat));
		var lP = new THREE.Group(); lP.position.copy(pL); lP.add(new THREE.Mesh(build(left, pL), mat));
		var chain = [], parent = body;
		for (var seg = 1; seg < segCount; seg++) {
			var pv = new THREE.Group();
			pv.position.copy(segPivot[seg].clone().sub(segPivot[seg - 1]));
			pv.add(new THREE.Mesh(build(segTris[seg], segPivot[seg]), mat));
			parent.add(pv); chain.push(pv); parent = pv;
		}
		var group = new THREE.Group(); group.add(body, rP, lP);
		mesh.parent.add(group); mesh.parent.remove(mesh);
		return { r: rP, l: lP, chain: chain };
	}

	var draco = new DRACOLoader();
	draco.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/draco/');
	var loader = new GLTFLoader(); loader.setDRACOLoader(draco);

	/* don't fetch anything until the work section is close */
	function loadModel() {
		loader.load(MODEL_URL, function (gltf) {
			var model = gltf.scene;
			var box = new THREE.Box3().setFromObject(model);
			var size = box.getSize(new THREE.Vector3()), center = box.getCenter(new THREE.Vector3());
			modelMaxDim = Math.max(size.x, size.y, size.z) || 1;
			model.traverse(function (o) {
				if (o.isMesh && o.material) { (Array.isArray(o.material) ? o.material : [o.material]).forEach(function (m) { m.side = THREE.DoubleSide; }); }
			});
			var parts = splitWings(model);
			if (parts) { wingR = parts.r; wingL = parts.l; chainPivots = parts.chain; chainAngles = chainPivots.map(function () { return 0; }); }
			inner = new THREE.Group(); inner.add(model); model.position.sub(center);
			inner.rotation.y = FACE_RIGHT;
			turn.add(inner);
			loaded = true;
		}, undefined, function (err) { console.warn('[quest-dragon] model failed to load:', err); });
	}

	function attach() {
		S = window.__questDragon;
		if (!S || !S.canvas) { return false; }
		if (canvas === S.canvas) { return true; }
		canvas = S.canvas;
		renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
		renderer.setClearColor(0x000000, 0);
		if (window.SJHFire && S.fireCanvas) {
			fire = window.SJHFire.create(S.fireCanvas, { staticWhenReduced: false, maxFlames: 120 });
			mouth = fire && fire.mouth;
		}
		return true;
	}

	var lw = 0, lh = 0;
	function size() {
		var W = S.W || canvas.clientWidth, H = S.H || canvas.clientHeight;
		if (W === lw && H === lh) { return; }
		lw = W; lh = H;
		renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
		renderer.setSize(W, H, false);
		camera.left = 0; camera.right = W; camera.top = 0; camera.bottom = H;
		camera.updateProjectionMatrix();
		if (fire) { fire.resize(); }
	}

	var px = null, py = 0, yaw = 0, bank = 0, flapPhase = 0, lastNow = 0;

	function frame(now) {
		requestAnimationFrame(frame);
		if (!S && !attach()) { return; }
		if (S.canvas !== canvas) { attach(); }
		if (!renderer) { return; }
		if (!S.visible) { if (mouth) { mouth.active = false; } return; }
		if (!loaded) { return; }
		size();
		var dt = Math.min(50, now - (lastNow || now)); lastNow = now;
		var t = now / 1000;

		/* ease towards where quest.js wants us, with a little life on top */
		var hoverBob = Math.sin(t * 1.5) * S.size * 0.05 + Math.sin(t * 3.7 + 1) * S.size * 0.015;
		var tx = S.x, ty = S.y + hoverBob;
		if (px === null) { px = tx; py = ty; }
		var vx = (tx - px) * 0.18, vy = (ty - py) * 0.18;
		px += vx; py += vy;
		rig.position.set(px, py, 0);
		var sc = S.size / modelMaxDim;
		if (inner) { inner.scale.set(sc, -sc, sc); }

		/* face the way we're travelling: a half-turn about Y, eased */
		var wantYaw = S.dir < 0 ? -FACE_RIGHT * 2 : 0;   /* turn through facing-camera, not away */
		yaw += (wantYaw - yaw) * 0.09;
		turn.rotation.y = yaw + Math.sin(t * 1.6) * 0.08;

		/* bank into climbs and dives, more when moving fast */
		var tilt = Math.max(-0.45, Math.min(0.45, -vy * 0.03 * (S.dir < 0 ? -1 : 1)));
		bank += (tilt - bank) * 0.12;
		rig.rotation.z = bank + Math.min(0.18, S.speed * 0.004) * -S.dir * 0.4;

		/* flap: faster when the world is rushing past */
		var rate = 1 / 1.45 + Math.min(1.6, S.speed * 0.05);
		flapPhase += dt / 1000 * rate * Math.PI * 2;
		var amp = 0.5 + Math.min(0.25, S.speed * 0.01);
		var flap = Math.sin(flapPhase) * amp - amp * 0.15;
		if (wingR) { wingR.rotation.z = -flap; }
		if (wingL) { wingL.rotation.z = flap; }

		var chase = bank;
		for (var ci = 0; ci < chainPivots.length; ci++) {
			chainAngles[ci] += (chase * CHAIN_AMP[ci] - chainAngles[ci]) * CHAIN_LAG[ci];
			chainPivots[ci].rotation.z = chainAngles[ci] - chase;
			chase = chainAngles[ci];
		}

		rig.updateMatrixWorld(true);

		if (mouth) {
			var m = MOUTH_OFFSET.clone().applyMatrix4(inner.matrixWorld);
			var a = MOUTH_AIM.clone().applyMatrix4(inner.matrixWorld);
			var dx = a.x - m.x, dy = a.y - m.y, d = Math.hypot(dx, dy) || 1;
			mouth.x = m.x; mouth.y = m.y; mouth.dirX = dx / d; mouth.dirY = dy / d;
			mouth.s = S.size * 0.8;
			mouth.active = !!S.breathe;
			mouthGlow.position.set(m.x, m.y, m.z + 60);
			mouthGlow.intensity += ((S.breathe ? 2.6 : 0.2) - mouthGlow.intensity) * 0.15;
		}
		renderer.render(scene, camera);
	}

	/* start loading when the section is a screen or so away */
	var work = document.getElementById('work');
	var started = false;
	function go() { if (started) { return; } started = true; loadModel(); requestAnimationFrame(frame); }
	if ('IntersectionObserver' in window) {
		var io = new IntersectionObserver(function (es) {
			if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); go(); }
		}, { rootMargin: '150% 0px' });
		io.observe(work);
	} else { go(); }
}());
