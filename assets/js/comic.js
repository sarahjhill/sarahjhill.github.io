/* ============================================================
   Knock-knock comic — loops while scrolled into view, pausing
   automatically once it scrolls off. See assets/css/07-comic.css.
   ============================================================ */
(function(){
  var stage = document.getElementById('comicStage');
  if(!stage) return;

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ai = document.getElementById('comicAi');
  var human = document.getElementById('comicHuman');
  var caption = document.getElementById('comicCaption');
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

  function wait(ms){ return new Promise(function(res){ setTimeout(res, ms); }); }

  function showFor(id, hold){
    bubbles[id].classList.add('show');
    return wait(hold).then(function(){ bubbles[id].classList.remove('show'); });
  }

  function animate(el, from, to, duration){
    return el.animate([{ left: from }, { left: to }], { duration: duration, easing: 'linear', fill: 'forwards' }).finished;
  }

  function resetScene(){
    Object.keys(bubbles).forEach(function(k){ bubbles[k].classList.remove('show'); });
    caption.classList.remove('show');
    ai.classList.remove('walking', 'looking');
    human.classList.remove('walking', 'looking');
  }

  async function playOnce(){
    var w = stage.clientWidth;
    var pauseAI = Math.round(w*0.15 + 50) + 'px';
    var pauseHuman = Math.round(w*0.15 - 110) + 'px';
    var endAI = (w + 160) + 'px';
    var endHuman = (w + 20) + 'px';

    resetScene();
    ai.style.left = '-160px'; human.style.left = '-320px';

    /* walk in from fully off-page */
    ai.classList.add('walking'); human.classList.add('walking');
    await Promise.all([ animate(ai, '-160px', pauseAI, 3400), animate(human, '-320px', pauseHuman, 3400) ]);

    /* stop for the joke */
    ai.classList.remove('walking'); human.classList.remove('walking');
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
    await wait(500);

    /* walk out, fully off-page the other side */
    ai.classList.add('walking'); human.classList.add('walking');
    var walkOut = Promise.all([ animate(ai, pauseAI, endAI, 7800), animate(human, pauseHuman, endHuman, 7800) ]);
    await wait(5600);
    caption.classList.add('show');
    await walkOut;
    ai.classList.remove('walking'); human.classList.remove('walking');
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
          ai.style.left = Math.round(w*0.15 + 50) + 'px';
          human.style.left = Math.round(w*0.15 - 110) + 'px';
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
