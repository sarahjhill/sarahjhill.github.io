/* ============================================================
   Knock-knock comic — loops while scrolled into view, pausing
   automatically once it scrolls off. See assets/css/07-comic.css.

   Both characters walk in from the right and split apart for the
   joke — the AI settles on the right, me on the left. Once the
   punchline lands, we walk back together to meet in the middle,
   then the 3D dragon (comic-dragon.js) dives in from the top right
   and torches the AI, I run off to the left, and "Content is King"
   sprays up where the AI used to stand. Then it resets and loops.
   ============================================================ */
(function(){
  var stage = document.getElementById('comicStage');
  if(!stage) return;

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ai = document.getElementById('comicAi');
  var human = document.getElementById('comicHuman');
  var caption = document.getElementById('comicCaption');
  var spray = document.getElementById('comicSpray');
  var bubbles = {
    b1: document.getElementById('comicB1'),
    b2: document.getElementById('comicB2'),
    b3: document.getElementById('comicB3'),
    b4: document.getElementById('comicB4'),
    b5: document.getElementById('comicB5')
  };
  var inView = false;
  var running = false;
  var shownOnceForReduce = false;

  /* rest positions, as a fraction of stage width: the AI on the
     right, me on the left for the joke, then we both close in to
     meet in the middle before the dragon arrives */
  var REST_AI = 0.80;
  var REST_HUMAN = 0.10;
  var MEET_AI = 0.56;
  var MEET_HUMAN = 0.44;

  function wait(ms){ return new Promise(function(res){ setTimeout(res, ms); }); }

  function showFor(id, hold){
    bubbles[id].classList.add('show');
    return wait(hold).then(function(){ bubbles[id].classList.remove('show'); });
  }

  function animate(el, from, to, duration){
    return el.animate([{ left: from }, { left: to }], { duration: duration, easing: 'linear', fill: 'forwards' }).finished;
  }

  async function walkTo(el, from, to, duration){
    el.style.left = from;
    el.classList.add('walking');
    await animate(el, from, to, duration);
    el.classList.remove('walking');
  }

  function resetScene(){
    Object.keys(bubbles).forEach(function(k){ bubbles[k].classList.remove('show'); });
    caption.classList.remove('show');
    if(spray) spray.classList.remove('show');
    ai.classList.remove('walking', 'looking', 'melt');
    human.classList.remove('walking', 'looking', 'running');
  }

  async function playOnce(){
    var w = stage.clientWidth;
    var restAI = Math.round(w * REST_AI) + 'px';
    var restHuman = Math.round(w * REST_HUMAN) + 'px';
    var startAI = (w + 60) + 'px';
    var startHuman = (w + 260) + 'px';

    resetScene();
    ai.style.left = startAI; human.style.left = startHuman;

    /* walk in from off the right edge, splitting apart to opposite
       sides of the stage */
    await Promise.all([
      walkTo(ai, startAI, restAI, 1200),
      walkTo(human, startHuman, restHuman, 2600)
    ]);

    /* stop for the joke */
    await showFor('b1', 1300);   // Knock, knock.
    await wait(150);
    await showFor('b2', 1300);   // Who's there?
    await wait(150);
    await showFor('b3', 1400);   // Artificial intelligence.
    await wait(150);
    await showFor('b4', 1500);   // Artificial intelligence who?
    await wait(400);
    ai.classList.add('looking');
    await showFor('b5', 2800);   // Sorry, that was a mistake...
    ai.classList.remove('looking');
    await wait(400);

    /* the joke's over — we close the gap and meet in the middle */
    var meetAI = Math.round(w * MEET_AI) + 'px';
    var meetHuman = Math.round(w * MEET_HUMAN) + 'px';
    await Promise.all([
      walkTo(ai, restAI, meetAI, 900),
      walkTo(human, restHuman, meetHuman, 900)
    ]);
    await wait(300);

    /* the dragon dives in from the top right and torches the AI */
    await new Promise(function(resolve){
      if(window.SJHComicDragon){
        window.SJHComicDragon.torch(ai, {
          onImpact: function(){ ai.classList.add('melt'); },
          onDone: resolve
        });
      } else {
        ai.classList.add('melt');
        wait(700).then(resolve);
      }
    });

    /* I run off to the left, leaving the scorch mark behind */
    human.classList.add('running');
    await animate(human, meetHuman, '-200px', 900);
    human.classList.remove('running');

    /* the moral of the story sprays up where the AI used to stand */
    if(spray) spray.classList.add('show');
    await wait(2400);
  }

  async function runLoop(){
    if(running) return;
    running = true;
    while(inView){
      await playOnce();
      if(!inView) break;
      await wait(1400);
    }
    running = false;
  }

  function handleIntersect(entries){
    entries.forEach(function(entry){
      inView = entry.isIntersecting;
      if(reduce){
        if(inView && !shownOnceForReduce){
          shownOnceForReduce = true;
          var w = stage.clientWidth;
          ai.style.left = Math.round(w * REST_AI) + 'px';
          human.style.left = Math.round(w * REST_HUMAN) + 'px';
          caption.classList.add('show');
        }
        return;
      }
      if(inView) runLoop();
    });
  }

  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(handleIntersect, { threshold: 0.35 });
    io.observe(stage);
  } else if(!reduce){
    inView = true;
    runLoop();
  } else {
    caption.classList.add('show');
  }
})();
