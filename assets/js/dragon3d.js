/*----------------------------------------------

[Hero dragon — 3D]

Replaces the old dot-matrix hero dragon with a real glTF model. It
flies in once from the right in slow, fluid motion, then settles in
the corner and stays there permanently, breathing fire at the
"Content is king" line — the same "always there" fixture the old
dot-dragon was, just arriving with a flight instead of simply being
present from page load. Wings flap and the body chain sways gently
the whole time it's parked. The fire itself is the exact flame
engine already in dragon.js, which reads the mouth's current screen
position from window.__dragonMouth every frame; this file never
touches the flame's own particle code, it only says where the mouth
is and when the dragon is close enough to breathe.

The model itself ships as one static, unrigged mesh (no skeleton,
no animations — checked the glTF JSON directly), so the wing flap
is faked here: the mesh is split into a body piece and two wing
pieces by X position at load time, each wing re-parented under its
own pivot at its root, then the pivots are rotated by hand every
frame. Everything else (position, scale, rotation) still applies to
the outer rig as one piece.

An orthographic camera is framed to exactly match the hero's pixel
box (left=0, right=width, top=0, bottom=height), so a model's world
position IS its screen position — no projection math needed to hand
the flame engine a coordinate it understands.

----------------------------------------------*/

import * as THREE from 'three';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/DRACOLoader.js';

(function () {
	'use strict';

	var scene_el = document.querySelector('.scene');
	if (!scene_el) { return; }
	if (!window.WebGLRenderingContext) { return; }

	var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	var canvas = document.createElement('canvas');
	canvas.className = 'sjh-dragon-3d';
	/* insertBefore, not appendChild — the flame is a separate 2D canvas
	   that must stay ON TOP of this one, or the wings (which sweep back
	   and forth in front of the mouth as they flap) periodically cover
	   the fire regardless of how accurate the mouth coordinate is */
	scene_el.insertBefore(canvas, scene_el.firstChild);

	var mouth = (window.__dragonMouth = window.__dragonMouth || { x: 0, y: 0, s: 1, active: false });

	/* ---- tunables ---------------------------------------------------
	   MOUTH_OFFSET is in the model's own native units (its loaded
	   bounding box is roughly ±1), applied through the model's own
	   world matrix — so it scales correctly with the model at any
	   viewport size instead of needing to be re-tuned per size. */
	var MODEL_URL      = 'assets/models/dragon.glb'; /* Draco-compressed — 2MB, was 68MB */
	/* rotate.y so local +Z (the body's own forward axis) maps to world -X —
	   i.e. head-first into the direction of travel. The +π here fixed a
	   real bug: without it, the head pointed toward +X (backwards, since
	   the dragon travels right-to-left) the whole time. */
	var FACE_YAW       = 2.623 + Math.PI;
	var WING_SPLIT_X   = 0.30;            /* native units either side of centre */
	/* the open mouth itself, identified by eye in an isolated viewer of
	   the body mesh alone (front-on, camera at +Z, teeth clearly visible)
	   and confirmed by raycasting several points on it — not guessed */
	var MOUTH_OFFSET   = new THREE.Vector3(-0.033, 0.210, 0.605);
	/* a bit further out along the snout's own forward axis (+Z, same
	   direction the head faces) — paired with MOUTH_OFFSET each frame to
	   read off the mouth's current aim, not just its position */
	var MOUTH_AIM      = new THREE.Vector3(-0.033, 0.210, 0.605 + 0.2);
	var DUR            = { enter: 2600 };
	var BOB_PERIOD_MS  = 4200;
	var BOB_AMP_PX     = 10;
	var FLAP_PERIOD_MS = 1450;
	var FLAP_AMP       = 0.55;            /* radians */
	var BANK_MAX       = 0.48;            /* radians, how far it leans into vertical motion */
	var YAW_WAG_AMP    = 0.09;            /* radians, gentle side-to-side snake-like wag */

	var scene = new THREE.Scene();
	var camera = new THREE.OrthographicCamera(0, 1, 0, 1, -4000, 4000);
	var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
	renderer.setClearColor(0x000000, 0);

	scene.add(new THREE.HemisphereLight(0xfff2df, 0x2a1810, 2.2));
	var key = new THREE.DirectionalLight(0xffc98c, 3.2);
	key.position.set(-300, -200, 600);
	scene.add(key);
	var fill = new THREE.DirectionalLight(0xffe4c2, 1.4);
	fill.position.set(300, 400, 300);
	scene.add(fill);
	var rim = new THREE.DirectionalLight(0x88a8ff, 0.6);
	rim.position.set(400, 300, -400);
	scene.add(rim);
	var mouthGlow = new THREE.PointLight(0xff7a1a, 0, 900);
	scene.add(mouthGlow);

	var rig = new THREE.Group();
	scene.add(rig);

	var inner = null;        /* holds the model, carries norm scale + yaw */
	var wingL = null, wingR = null; /* pivot groups, rotated each frame to flap */
	var chainPivots = [];   /* body chain, head-to-tail, each nested in the last */
	var chainAngles = [];   /* this frame's lagged angle for each chain pivot */
	var modelMaxDim = 1;

	var W = 0, H = 0;
	function layout() {
		var box = scene_el.getBoundingClientRect();
		W = Math.max(1, Math.round(box.width));
		H = Math.max(1, Math.round(box.height));
		var dpr = Math.min(window.devicePixelRatio || 1, 2);
		renderer.setPixelRatio(dpr);
		renderer.setSize(W, H, false);
		/* top=0,bottom=H flips the camera to match screen coordinates
		   (y grows downward), so world position == screen pixel position */
		camera.left = 0; camera.right = W; camera.top = 0; camera.bottom = H;
		camera.updateProjectionMatrix();

		/* corner box clear of the headline — same footprint the old
		   dot-dragon used */
		var S = Math.min(W * 0.34, H * 0.52);
		var ox = W - S * 1.0;
		var oy = H - S * 0.74 - H * 0.02;
		target.x = ox + S * 0.5;
		target.y = oy + S * 0.35;

		if (inner) { var s = S / modelMaxDim; inner.scale.set(s, -s, s); }
	}

	/* ---- split the static mesh into flappable wings + a full-length
	   body chain ----------------------------------------------------------
	   The model ships as one fused, unrigged mesh, so there's no skeleton
	   to animate — there's no way to bend it the way Project33 bends its
	   30-point chain. What we CAN do: cut the body itself (excluding the
	   wings, which are split off separately by X and hinged for flapping)
	   into several slices along its own front-back axis (local Z — head
	   sits at high +Z, tail at low -Z) and nest each slice's pivot inside
	   the previous one's, head to tail. Then in the render loop each
	   pivot's rotation lags the one ahead of it — exactly the "each link
	   eases toward the one ahead, with its own delay" rule the SVG chain
	   runs on, just four hinges standing in for thirty position-linked
	   points. Segment 0 (the head end) stays rigid — no lag — so the
	   camera-facing pose and the mouth offset stay exactly where they
	   were tuned; segments 1..N-1 carry the whip. */
	var BODY_CHAIN_Z = [0.35, 0.05, -0.25, -0.55]; /* native Z cut points, head-to-tail */

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
		/* segment 0 has no pivot of its own (it's rigid — no lag applied),
		   so its geometry stays in native coordinates; each later segment
		   pivots at its own cut point */
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

		/* nest each later segment's pivot inside the previous one's — a
		   lag rotation on link i then carries automatically into every
		   link after it, same as a lag on one chain point drags the rest */
		var chainPivots = [];
		var parent = bodyMesh;
		for (var seg = 1; seg < segCount; seg++) {
			var segMesh = new THREE.Mesh(build(segTris[seg], segPivotWorld[seg]), mat);
			var pivot = new THREE.Group();
			pivot.position.copy(segPivotWorld[seg].clone().sub(segPivotWorld[seg - 1]));
			pivot.add(segMesh);
			parent.add(pivot);
			chainPivots.push(pivot);
			parent = pivot;
		}

		var group = new THREE.Group();
		group.add(bodyMesh, rightPivot, leftPivot);

		mesh.parent.add(group);
		mesh.parent.remove(mesh);

		return { rightPivot: rightPivot, leftPivot: leftPivot, bodyMesh: bodyMesh, chainPivots: chainPivots };
	}

	var loaded = false;
	var target = { x: 0, y: 0 };
	var start = { x: 0, y: 0 };

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
			/* screen Y grows downward, so the model's own up (+Y) needs
			   inverting; a Y-scale flip does only that, leaving FACE_YAW
			   free to independently pick which way it faces */
			inner.rotation.y = FACE_YAW;
			rig.add(inner);

			layout();
			loaded = true;
			beginFlight(performance.now());
		},
		undefined,
		function (err) { console.warn('[dragon3d] failed to load model:', err); }
	);

	window.addEventListener('resize', layout);

	/* ---- flight state: idle -> enter -> hover (permanent) --------------- */
	var phase = 'idle';
	var phaseStart = 0;
	var flightGlobalStart = 0; /* one continuous clock for the whole flight,
	                               not reset per phase, so the idle wobble
	                               never jumps at a phase boundary */

	function easeInOutSine(t) { return -(Math.cos(Math.PI * t) - 1) / 2; }

	function beginFlight(now) {
		phase = 'enter';
		phaseStart = now;
		flightGlobalStart = now;
		var edge = Math.min(W * 0.34, H * 0.52);
		start.x = W + edge;
		start.y = H * 0.4;
	}

	/* ---- render loop --------------------------------------------------- */
	var running = false, raf = 0;
	var prevX = 0, prevY = 0, bankAngle = 0, yawWag = 0;
	/* per-link lag: how much each successive chain link amplifies the
	   angle it's chasing, and how slowly (lower = laggier) it chases it —
	   both grow toward the tail, the same way Project33's per-segment
	   gap shrinks toward its tail so the whip builds link over link */
	var CHAIN_AMP = [1.3, 1.5, 1.7, 1.9];
	var CHAIN_LAG = [0.1, 0.075, 0.055, 0.04];

	function frame(now) {
		raf = requestAnimationFrame(frame);
		if (!loaded) { return; }

		var elapsed = now - phaseStart;
		var flightT = (now - flightGlobalStart) / 1000;
		/* two sine waves at different frequencies, not one — a single sine
		   repeats so evenly it reads as mechanical; this is what gave the
		   SVG prototype its less predictable, organic drift */
		var wobble = Math.sin(flightT * 0.9) * (H * 0.02) + Math.sin(flightT * 2.3 + 1.1) * (H * 0.008);

		var flap = Math.sin(now / FLAP_PERIOD_MS * Math.PI * 2) * FLAP_AMP - FLAP_AMP * 0.15;
		if (wingR) { wingR.rotation.z = -flap; }
		if (wingL) { wingL.rotation.z = flap; }

		if (phase === 'enter') {
			var t = Math.min(1, elapsed / DUR.enter);
			var e = easeInOutSine(t);
			rig.position.x = start.x + (target.x - start.x) * e;
			rig.position.y = start.y + (target.y - start.y) * e + wobble;
			if (t >= 1) {
				phase = 'hover'; phaseStart = now;
				mouthGlow.intensity = 2.2;
			}
		} else if (phase === 'hover') {
			/* settles here permanently once it arrives — no exit, no loop,
			   the same "always there" fixture the old dot-dragon was */
			var bob = Math.sin(now / BOB_PERIOD_MS * Math.PI * 2) * BOB_AMP_PX;
			var sway = Math.sin(now / (BOB_PERIOD_MS * 1.7) * Math.PI * 2) * (BOB_AMP_PX * 0.4);
			rig.position.x = target.x + sway;
			rig.position.y = target.y + bob + wobble * 0.3;
		}

		/* bank off the actual atan2 direction of travel, exactly the
		   technique the SVG prototype uses — and, like that prototype,
		   settle to level (0°) instead of chasing atan2 noise once the
		   speed drops near zero (hover), rather than a prescribed curve */
		var vx = rig.position.x - prevX, vy = rig.position.y - prevY;
		prevX = rig.position.x; prevY = rig.position.y;
		var speed = Math.hypot(vx, vy);
		var targetBank = 0;
		if (speed > 0.4) {
			targetBank = Math.max(-BANK_MAX, Math.min(BANK_MAX, Math.atan2(-vy, -vx)));
		}
		bankAngle += (targetBank - bankAngle) * 0.16;
		yawWag = Math.sin(flightT * 1.6) * YAW_WAG_AMP;
		rig.rotation.z = bankAngle;
		rig.rotation.y = yawWag;

		/* each body-chain link chases the one ahead of it with its own
		   amplified lag — exactly the cascading-delay rule the Project33
		   chain runs, just walked over four hinges instead of thirty
		   position-linked points. Each pivot's LOCAL rotation is the
		   difference between its own lagged angle and its parent's (its
		   parent's rotation already carries through automatically since
		   the pivots are nested), so the whip visibly builds toward the
		   tail instead of the whole chain swinging as one rigid fan. */
		var chaseAngle = bankAngle;
		for (var ci = 0; ci < chainPivots.length; ci++) {
			var amp = CHAIN_AMP[Math.min(ci, CHAIN_AMP.length - 1)];
			var lag = CHAIN_LAG[Math.min(ci, CHAIN_LAG.length - 1)];
			chainAngles[ci] += (chaseAngle * amp - chainAngles[ci]) * lag;
			chainPivots[ci].rotation.z = chainAngles[ci] - chaseAngle;
			chaseAngle = chainAngles[ci];
		}

		/* matrixWorld is only refreshed inside renderer.render() below, so
		   without this the mouth position read one frame behind wherever
		   the model actually is — a one-frame lag is what made the flame
		   look like it was detaching from the mouth during real motion */
		rig.updateMatrixWorld(true);

		if (phase === 'hover') {
			mouth.active = true;
			var m = MOUTH_OFFSET.clone().applyMatrix4(inner.matrixWorld);
			/* a second point a little further out along the snout's own
			   forward axis, transformed the same way — the vector between
			   the two IS the direction the mouth is currently aimed, so
			   the fire keeps shooting out the front of the mouth even as
			   it sways gently while parked */
			var mAim = MOUTH_AIM.clone().applyMatrix4(inner.matrixWorld);
			var dx = mAim.x - m.x, dy = mAim.y - m.y;
			var dmag = Math.hypot(dx, dy) || 1;
			mouth.x = m.x; mouth.y = m.y;
			mouth.dirX = dx / dmag; mouth.dirY = dy / dmag;
			mouth.s = Math.min(W * 0.34, H * 0.52);
			mouthGlow.position.set(m.x, m.y, m.z + 60);
		}

		renderer.render(scene, camera);
	}

	function start_() { if (!running) { running = true; raf = requestAnimationFrame(frame); } }
	function stop() { if (running) { running = false; cancelAnimationFrame(raf); } }

	if (reduce) {
		/* skip the flight, land already settled and breathing */
		var settle = function () {
			if (!loaded) { requestAnimationFrame(settle); return; }
			layout();
			rig.position.x = target.x; rig.position.y = target.y;
			rig.updateMatrixWorld(true);
			mouth.active = true;
			var m = MOUTH_OFFSET.clone().applyMatrix4(inner.matrixWorld);
			var mAim = MOUTH_AIM.clone().applyMatrix4(inner.matrixWorld);
			var dmag = Math.hypot(mAim.x - m.x, mAim.y - m.y) || 1;
			mouth.x = m.x; mouth.y = m.y;
			mouth.dirX = (mAim.x - m.x) / dmag; mouth.dirY = (mAim.y - m.y) / dmag;
			mouth.s = Math.min(W * 0.34, H * 0.52);
			mouthGlow.intensity = 2.2;
			mouthGlow.position.set(m.x, m.y, m.z + 60);
			renderer.render(scene, camera);
		};
		settle();
	} else {
		start_();
	}

	document.addEventListener('visibilitychange', function () {
		if (document.hidden) { stop(); } else if (!reduce) { start_(); }
	});

	if ('IntersectionObserver' in window) {
		new IntersectionObserver(function (es) {
			es.forEach(function (e) {
				if (e.isIntersecting) { if (!reduce) { start_(); } }
				else { stop(); }
			});
		}, { threshold: 0.02 }).observe(scene_el);
	}
}());
