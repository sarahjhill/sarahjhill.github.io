/*----------------------------------------------

[Comic dragon — the punchline]

A cameo appearance of the same 3D model from the hero section,
inside the knock-knock comic. It sits idle and invisible until
comic.js calls window.SJHComicDragon.torch(targetEl, callbacks) at
the end of the joke: it swoops in from off the right edge, hovers
just past the AI character breathing fire at it (using its own
instance of the same flame engine from dragon.js), then swoops back
out. comic.js is the one that actually removes/hides the AI — this
file just tells it, via callbacks.onImpact(), the moment the fire
has arrived so the melt can start in step with it.

Reuses the exact mesh-splitting technique from dragon3d.js (same
unrigged model, same wing/body-chain cuts) but with a much shorter,
snappier flight — this is a few-second cameo, not a permanent
fixture, so there's no hover-forever state and no idle body-chain
physics tuning beyond "looks right during a fast swoop".

----------------------------------------------*/

import * as THREE from 'three';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/DRACOLoader.js';

(function () {
	'use strict';

	var stage = document.getElementById('comicStage');
	if (!stage) { return; }

	/* no WebGL: give comic.js a no-op torch that still resolves, so the
	   loop doesn't hang waiting on a dragon that can never arrive */
	if (!window.WebGLRenderingContext) {
		window.SJHComicDragon = {
			torch: function (targetEl, callbacks) {
				callbacks = callbacks || {};
				if (callbacks.onImpact) { callbacks.onImpact(); }
				if (callbacks.onDone) { setTimeout(callbacks.onDone, 30); }
			}
		};
		return;
	}

	var caption = document.getElementById('comicCaption');

	var canvas3d = document.createElement('canvas');
	canvas3d.className = 'comic-dragon-3d';
	var fireCanvas = document.createElement('canvas');
	fireCanvas.className = 'comic-fire-canvas';
	/* both inserted ahead of the caption so the caption/spray text still
	   sits on top of them; fire ahead of the 3D canvas for the same
	   reason the hero scene does — flapping wings can otherwise sweep in
	   front of the mouth and cover the flame regardless of coordinates */
	stage.insertBefore(canvas3d, caption);
	stage.insertBefore(fireCanvas, caption);

	var fire = window.SJHFire.create(fireCanvas, { staticWhenReduced: false, maxFlames: 90 });
	var mouth = fire.mouth;

	/* ---- tunables --------------------------------------------------- */
	var MODEL_URL      = 'assets/models/dragon.glb';
	var FACE_YAW        = 2.623 + Math.PI; /* same model, same fix: local +Z forward -> world -X (left) */
	var WING_SPLIT_X     = 0.30;
	var MOUTH_OFFSET     = new THREE.Vector3(-0.033, 0.210, 0.605);
	var MOUTH_AIM        = new THREE.Vector3(-0.033, 0.210, 0.605 + 0.2);
	var BODY_CHAIN_Z     = [0.35, 0.05, -0.25, -0.55];
	var FLAP_PERIOD_MS   = 220;   /* faster than the hero's — an attack swoop, not a gentle hover */
	var FLAP_AMP         = 0.68;
	var FLY_MS           = 620;
	var BREATHE_MS       = 1500;
	var IMPACT_DELAY_MS  = 260;   /* how far into the breathe phase the fire visually reaches the target */
	var CHAIN_AMP        = [1.3, 1.5, 1.7, 1.9];
	var CHAIN_LAG        = [0.2, 0.16, 0.13, 0.1];

	var scene = new THREE.Scene();
	var camera = new THREE.OrthographicCamera(0, 1, 0, 1, -4000, 4000);
	var renderer = new THREE.WebGLRenderer({ canvas: canvas3d, alpha: true, antialias: true });
	renderer.setClearColor(0x000000, 0);

	scene.add(new THREE.HemisphereLight(0xfff2df, 0x2a1810, 2.2));
	var key = new THREE.DirectionalLight(0xffc98c, 3.2); key.position.set(-300, -200, 600); scene.add(key);
	var fill = new THREE.DirectionalLight(0xffe4c2, 1.4); fill.position.set(300, 400, 300); scene.add(fill);
	var rim = new THREE.DirectionalLight(0x88a8ff, 0.6); rim.position.set(400, 300, -400); scene.add(rim);
	var mouthGlow = new THREE.PointLight(0xff7a1a, 0, 900);
	scene.add(mouthGlow);

	var rig = new THREE.Group();
	rig.visible = false;
	scene.add(rig);

	var inner = null, wingL = null, wingR = null, chainPivots = [], chainAngles = [], modelMaxDim = 1;
	var loaded = false;
	var W = 0, H = 0, S = 1;

	function layout() {
		var box = stage.getBoundingClientRect();
		W = Math.max(1, Math.round(box.width));
		H = Math.max(1, Math.round(box.height));
		var dpr = Math.min(window.devicePixelRatio || 1, 2);
		renderer.setPixelRatio(dpr);
		renderer.setSize(W, H, false);
		camera.left = 0; camera.right = W; camera.top = 0; camera.bottom = H;
		camera.updateProjectionMatrix();
		S = Math.min(W * 0.5, H * 1.05);
		if (inner) { var s = S / modelMaxDim; inner.scale.set(s, -s, s); }
	}
	window.addEventListener('resize', layout);

	/* ---- identical mesh split to dragon3d.js — same model, same cuts --- */
	function splitWings(model) {
		var mesh = null;
		model.traverse(function (o) { if (o.isMesh) { mesh = o; } });
		if (!mesh) { return null; }

		var geom = mesh.geometry;
		var pos = geom.attributes.position;
		var norm = geom.attributes.normal;
		var uv = geom.attributes.uv;
		var idx = geom.index ? geom.index.array : null;
		var triCount = idx ? idx.length / 3 : pos.count / 3;

		function tri(t) { return idx ? [idx[t * 3], idx[t * 3 + 1], idx[t * 3 + 2]] : [t * 3, t * 3 + 1, t * 3 + 2]; }

		var segCount = BODY_CHAIN_Z.length + 1;
		var segTris = []; for (var s = 0; s < segCount; s++) { segTris.push([]); }
		var right = [], left = [];
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

		function bandPivot(zTarget, band) {
			var near = [];
			for (var i = 0; i < pos.count; i++) {
				if (Math.abs(pos.getZ(i) - zTarget) < band) { near.push(i); }
			}
			var s2 = new THREE.Vector3();
			(near.length ? near : [0]).forEach(function (i) { s2.x += pos.getX(i); s2.y += pos.getY(i); s2.z += pos.getZ(i); });
			s2.divideScalar(near.length || 1);
			return s2;
		}
		function edgePivot(xTarget) {
			var near = [];
			for (var i = 0; i < pos.count; i++) {
				if (Math.abs(pos.getX(i) - xTarget) < 0.05) { near.push(i); }
			}
			var s2 = new THREE.Vector3();
			(near.length ? near : [0]).forEach(function (i) { s2.x += pos.getX(i); s2.y += pos.getY(i); s2.z += pos.getZ(i); });
			s2.divideScalar(near.length || 1);
			return s2;
		}
		var pR = edgePivot(WING_SPLIT_X);
		var pL = edgePivot(-WING_SPLIT_X);
		var segPivotWorld = [new THREE.Vector3(0, 0, 0)];
		BODY_CHAIN_Z.forEach(function (z) { segPivotWorld.push(bandPivot(z, 0.05)); });

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
			if (N.length) { g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); }
			if (U.length) { g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); }
			if (!N.length) { g.computeVertexNormals(); }
			return g;
		}

		var mat = mesh.material;
		var bodyMesh = new THREE.Mesh(build(segTris[0], segPivotWorld[0]), mat);
		var rightMesh = new THREE.Mesh(build(right, pR), mat);
		var leftMesh = new THREE.Mesh(build(left, pL), mat);

		var rightPivot = new THREE.Group(); rightPivot.position.copy(pR); rightPivot.add(rightMesh);
		var leftPivot = new THREE.Group(); leftPivot.position.copy(pL); leftPivot.add(leftMesh);

		var chainPivotsLocal = [];
		var parent = bodyMesh;
		for (var seg = 1; seg < segCount; seg++) {
			var segMesh = new THREE.Mesh(build(segTris[seg], segPivotWorld[seg]), mat);
			var pivot = new THREE.Group();
			pivot.position.copy(segPivotWorld[seg].clone().sub(segPivotWorld[seg - 1]));
			pivot.add(segMesh);
			parent.add(pivot);
			chainPivotsLocal.push(pivot);
			parent = pivot;
		}

		var group = new THREE.Group();
		group.add(bodyMesh, rightPivot, leftPivot);

		mesh.parent.add(group);
		mesh.parent.remove(mesh);

		return { rightPivot: rightPivot, leftPivot: leftPivot, bodyMesh: bodyMesh, chainPivots: chainPivotsLocal };
	}

	var dracoLoader = new DRACOLoader();
	dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/draco/');
	var gltfLoader = new GLTFLoader();
	gltfLoader.setDRACOLoader(dracoLoader);

	gltfLoader.load(
		MODEL_URL,
		function (gltf) {
			var model = gltf.scene;
			var box = new THREE.Box3().setFromObject(model);
			var size = box.getSize(new THREE.Vector3());
			var center = box.getCenter(new THREE.Vector3());
			modelMaxDim = Math.max(size.x, size.y, size.z) || 1;

			model.traverse(function (o) {
				if (o.isMesh && o.material) {
					var mats = Array.isArray(o.material) ? o.material : [o.material];
					mats.forEach(function (m) { m.side = THREE.DoubleSide; });
				}
			});

			var wings = splitWings(model);
			if (wings) {
				wingR = wings.rightPivot; wingL = wings.leftPivot;
				chainPivots = wings.chainPivots;
				chainAngles = chainPivots.map(function () { return 0; });
			}

			inner = new THREE.Group();
			inner.add(model);
			model.position.sub(center);
			inner.rotation.y = FACE_YAW;
			rig.add(inner);

			layout();
			loaded = true;
		},
		undefined,
		function (err) { console.warn('[comic-dragon] failed to load model:', err); }
	);

	/* ---- torch sequence: idle -> flyIn -> breathe -> flyOut -> idle ---- */
	var state = 'idle';
	var stateStart = 0;
	var from = { x: 0, y: 0 }, to = { x: 0, y: 0 };
	var pending = null;
	var running = false, raf = 0;
	var bankAngle = 0;

	function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
	function easeInCubic(t) { return t * t * t; }

	function waitLoaded(cb) {
		if (loaded) { cb(); return; }
		var iv = setInterval(function () { if (loaded) { clearInterval(iv); cb(); } }, 60);
	}

	function torch(targetEl, callbacks) {
		callbacks = callbacks || {};
		waitLoaded(function () {
			layout();
			var stageRect = stage.getBoundingClientRect();
			var elRect = targetEl.getBoundingClientRect();
			var tx = elRect.left - stageRect.left + elRect.width * 0.5;
			var ty = elRect.top - stageRect.top + elRect.height * 0.32;

			to.x = tx + S * 0.42;
			to.y = ty;
			/* dives in from off the top-right corner, not level from the
			   side — a steeper, more dramatic entrance for the attack */
			from.x = W + S * 0.3;
			from.y = -H * 0.4;

			rig.visible = true;
			rig.position.set(from.x, from.y, 0);
			bankAngle = 0;

			pending = callbacks; pending.impactFired = false;
			state = 'flyIn';
			stateStart = performance.now();
			if (!running) { running = true; raf = requestAnimationFrame(frame); }
		});
	}

	window.SJHComicDragon = { torch: torch };

	function frame(now) {
		if (!loaded) { raf = requestAnimationFrame(frame); return; }

		var elapsed = now - stateStart;
		var flap = Math.sin(now / FLAP_PERIOD_MS * Math.PI * 2) * FLAP_AMP;
		if (wingR) { wingR.rotation.z = -flap; }
		if (wingL) { wingL.rotation.z = flap; }

		if (state === 'flyIn') {
			var t1 = Math.min(1, elapsed / FLY_MS);
			var e1 = easeOutCubic(t1);
			rig.position.x = from.x + (to.x - from.x) * e1;
			rig.position.y = from.y + (to.y - from.y) * e1;
			bankAngle = -0.22 * (1 - t1);
			if (t1 >= 1) {
				state = 'breathe'; stateStart = now;
				mouth.active = true;
				mouthGlow.intensity = 2.4;
			}
		} else if (state === 'breathe') {
			var bob = Math.sin(now / 260) * 3.5;
			rig.position.x = to.x;
			rig.position.y = to.y + bob;
			bankAngle += (0 - bankAngle) * 0.2;
			if (!pending.impactFired && elapsed > IMPACT_DELAY_MS) {
				pending.impactFired = true;
				if (pending.onImpact) { pending.onImpact(); }
			}
			if (elapsed > BREATHE_MS) {
				state = 'flyOut'; stateStart = now;
				mouth.active = false;
			}
		} else if (state === 'flyOut') {
			/* continues on off the left edge, chasing the same direction
			   it was already facing (and the same way I run off) rather
			   than doubling back the way it came in */
			var t2 = Math.min(1, elapsed / FLY_MS);
			var e2 = easeInCubic(t2);
			rig.position.x = to.x + (-(S * 0.6 + 200) - to.x) * e2;
			rig.position.y = to.y + t2 * H * 0.14;
			bankAngle = -0.3 * t2;
			if (t2 >= 1) {
				state = 'idle';
				rig.visible = false;
				mouthGlow.intensity = 0;
				var done = pending;
				pending = null;
				if (done && done.onDone) { done.onDone(); }
			}
		}

		rig.rotation.z = bankAngle;

		var chaseAngle = bankAngle;
		for (var ci = 0; ci < chainPivots.length; ci++) {
			var amp = CHAIN_AMP[Math.min(ci, CHAIN_AMP.length - 1)];
			var lag = CHAIN_LAG[Math.min(ci, CHAIN_LAG.length - 1)];
			chainAngles[ci] += (chaseAngle * amp - chainAngles[ci]) * lag;
			chainPivots[ci].rotation.z = chainAngles[ci] - chaseAngle;
			chaseAngle = chainAngles[ci];
		}

		rig.updateMatrixWorld(true);

		if (state === 'breathe' || (state === 'flyOut' && mouth.active)) {
			var m = MOUTH_OFFSET.clone().applyMatrix4(inner.matrixWorld);
			var mAim = MOUTH_AIM.clone().applyMatrix4(inner.matrixWorld);
			var dx = mAim.x - m.x, dy = mAim.y - m.y;
			var dmag = Math.hypot(dx, dy) || 1;
			mouth.x = m.x; mouth.y = m.y;
			mouth.dirX = dx / dmag; mouth.dirY = dy / dmag;
			mouth.s = S;
			mouthGlow.position.set(m.x, m.y, m.z + 60);
		}

		renderer.render(scene, camera);

		if (state !== 'idle') {
			raf = requestAnimationFrame(frame);
		} else {
			running = false;
		}
	}
}());
