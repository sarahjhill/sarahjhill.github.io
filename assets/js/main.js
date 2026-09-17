/* ============================================================
   Sarah J Hill — site behaviour
   No framework, no build step, no dependencies.
   ------------------------------------------------------------
   Index:
     1. Hero countdown        — the three seconds, then resolve
     2. Scroll handling       — sticky nav, progress bar, active link
     3. Cursor glow           — pointer-follow light in the hero
     4. Mobile menu           — burger toggle
     5. The concept gap        — ask-a-real-question interactive
     6. Counters & reveals    — IntersectionObserver
   Everything degrades safely when "reduce motion" is on.
   ============================================================ */

(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var num=document.getElementById('num'), lbl=document.getElementById('lbl'),
      tick=document.getElementById('tick'), nav=document.getElementById('nav'),
      timer=null, countdownDone=false;

  /* ---- hero countdown ---- */
  function runCountdown(){
    if(!num || !lbl || !tick){ countdownDone=true; return; }   /* inner pages have no countdown */
    if(reduce){ document.body.classList.add('resolved'); num.textContent='3'; countdownDone=true; return; }
    clearInterval(timer);
    countdownDone=false;
    document.body.classList.remove('resolved');
    tick.style.width=''; tick.classList.remove('run'); void tick.offsetWidth; tick.classList.add('run');
    var n=3; num.textContent=n; lbl.textContent='seconds to decide';
    timer=setInterval(function(){
      n--;
      if(n>0){ num.textContent=n; }
      else{ clearInterval(timer); num.textContent='0'; lbl.textContent='they have decided';
        document.body.classList.add('resolved');
        setTimeout(function(){ tick.classList.remove('run'); countdownDone=true; onScroll(); },400); }
    },1000);
  }

  /* ---- the bar becomes scroll progress once the countdown is done ---- */
  function onScroll(){
    var y=scrollY||document.documentElement.scrollTop;
    if(nav) nav.classList.toggle('stuck', y>40);
    if(countdownDone && tick){
      var h=document.documentElement.scrollHeight-innerHeight;
      tick.style.width=(h>0?(y/h)*100:0)+'%';
    }
    var best='';
    document.querySelectorAll('main section[id], header[id]').forEach(function(s){
      if(s.getBoundingClientRect().top<=140) best=s.id;
    });
    document.querySelectorAll('.navlinks a').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('href')==='#'+best && !a.classList.contains('navcta'));
    });
  }
  addEventListener('scroll', onScroll, {passive:true});

  /* ---- cursor glow ---- */
  var glow=document.getElementById('glow'), hero=document.querySelector('.hero');
  var layers=document.querySelectorAll('.scene .layer');
  if(hero && glow && !reduce && matchMedia('(hover:hover)').matches){
    hero.addEventListener('pointermove', function(e){
      var r=hero.getBoundingClientRect();
      var px=(e.clientX-r.left)/r.width;          /* 0 → 1 across the hero */
      glow.style.setProperty('--mx', (px*100)+'%');
      glow.style.setProperty('--my', ((e.clientY-r.top)/r.height*100)+'%');

      /* skyline parallax — nearer layers drift further, so the city
         has depth rather than being one flat sticker */
      layers.forEach(function(l){
        var d=+l.dataset.depth||0;
        l.style.transform='translateX('+((px-0.5)*-d)+'px)';
      });
    });
  }

  /* ---- mobile menu ---- */
  var burger=document.getElementById('burger');
  if(burger) burger.addEventListener('click', function(){
    var open=nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open?'true':'false');
  });
  document.querySelectorAll('.navlinks a').forEach(function(a){
    a.addEventListener('click', function(){ nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); });
  });

  /* ---- the concept gap ---- */
  var DEFAULT_Q='What makes my business different?',
      DEFAULT_A='My nan taught me the recipe in 1974, I still use her tin.';

  var aiTemplates=[
    "Great question! We pride ourselves on quality, professionalism, and outstanding customer service. Get in touch today to find out more.",
    "As a trusted local business, we are committed to excellence and customer satisfaction in everything we do. Contact us for a free quote.",
    "Thank you for your enquiry. We offer a wide range of services tailored to meet your needs, delivered to the highest standard. Reach out any time.",
    "We understand how important this is to you. That's why we go above and beyond to deliver results you can rely on. Speak to our team today."
  ];
  var humanTemplates=[
    "Before I answer that — what's the one thing your regulars say about you that you'd never think to put on a website?",
    "Good question. Can I ask why you actually started this? That's usually where the real answer is hiding.",
    "Tell me about the customer who came back a second time. What actually brought them back?",
    "Here's my real question: what do you do that the place down the road doesn't?",
    "Let's find out together — what's the story behind your last really good review?",
    "Can I ask you something first? What's the bit of the job you're quietly proudest of?"
  ];
  var aiFlatten=[
    "Got it — key takeaway: years of experience and a personal touch customers love.",
    "Thanks for sharing! In summary: a strong heritage and genuine passion for quality.",
    "To summarise: family tradition, decades of expertise, and real care in every detail.",
    "Noted — headline: proud history, trusted by generations, built on quality."
  ];

  var qInput=document.getElementById('qInput'), askBtn=document.getElementById('askBtn'),
      qInput2=document.getElementById('qInput2'), askBtn2=document.getElementById('askBtn2'),
      resetBtn=document.getElementById('resetBtn'),
      placeholderL=document.getElementById('placeholderL'), placeholderR=document.getElementById('placeholderR'),
      placeholderL2=document.getElementById('placeholderL2'), placeholderR2=document.getElementById('placeholderR2'),
      answerL=document.getElementById('answerL'), answerR=document.getElementById('answerR'),
      answerL2=document.getElementById('answerL2'), answerR2=document.getElementById('answerR2'),
      qechoL=document.getElementById('qechoL'),
      planks=document.querySelectorAll('.gap-plank'), embers=document.querySelectorAll('.gap-ember'),
      verdict=document.getElementById('verdict'), verdict2=document.getElementById('verdict2'),
      chasmlabel=document.getElementById('chasmlabel'), stage2wrap=document.getElementById('stage2wrap'),
      gapAsked1=false, gapAsked2=false;

  function gapPick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }
  function gapEscape(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function gapAsk1(){
    if(!askBtn || gapAsked1) return;
    var q=(qInput.value||'').trim()||DEFAULT_Q;
    gapAsked1=true;
    askBtn.disabled=true; qInput.disabled=true;

    qechoL.innerHTML='You asked: <b>&ldquo;'+gapEscape(q)+'&rdquo;</b>';
    placeholderL.style.display='none'; placeholderR.style.display='none';

    answerL.textContent=gapPick(aiTemplates);
    answerR.innerHTML=gapPick(humanTemplates);

    planks.forEach(function(p){ p.classList.add('on'); });
    embers.forEach(function(e){ e.classList.add('on'); });
    answerL.classList.add('on'); answerR.classList.add('on');
    chasmlabel.textContent='closed'; chasmlabel.classList.add('closed');
    verdict.classList.add('show');
    stage2wrap.classList.add('open');
  }

  function gapAsk2(){
    if(!askBtn2 || !gapAsked1 || gapAsked2) return;
    var a=(qInput2.value||'').trim()||DEFAULT_A;
    gapAsked2=true;
    askBtn2.disabled=true; qInput2.disabled=true;

    placeholderL2.style.display='none'; placeholderR2.style.display='none';
    answerL2.textContent=gapPick(aiFlatten);
    answerR2.innerHTML='&ldquo;'+gapEscape(a)+'&rdquo; — that\'s not a summary. That\'s the line. It goes on the site exactly like that.';

    answerL2.classList.add('on'); answerR2.classList.add('on');
    verdict2.classList.add('show');
    resetBtn.classList.add('show');
  }

  function gapReset(){
    gapAsked1=false; gapAsked2=false;
    askBtn.disabled=false; qInput.disabled=false; qInput.value='';
    askBtn2.disabled=false; qInput2.disabled=false; qInput2.value='';
    placeholderL.style.display=''; placeholderR.style.display='';
    placeholderL2.style.display=''; placeholderR2.style.display='';
    qechoL.innerHTML='';
    answerL.classList.remove('on'); answerL.textContent='';
    answerR.classList.remove('on'); answerR.textContent='';
    answerL2.classList.remove('on'); answerL2.textContent='';
    answerR2.classList.remove('on'); answerR2.textContent='';
    planks.forEach(function(p){ p.classList.remove('on'); });
    embers.forEach(function(e){ e.classList.remove('on'); });
    chasmlabel.textContent='the concept gap'; chasmlabel.classList.remove('closed');
    verdict.classList.remove('show'); verdict2.classList.remove('show');
    stage2wrap.classList.remove('open'); resetBtn.classList.remove('show');
  }

  if(askBtn){
    askBtn.addEventListener('click', gapAsk1);
    qInput.addEventListener('keydown', function(e){ if(e.key==='Enter') gapAsk1(); });
    askBtn2.addEventListener('click', gapAsk2);
    qInput2.addEventListener('keydown', function(e){ if(e.key==='Enter') gapAsk2(); });
    resetBtn.addEventListener('click', gapReset);
  }

  /* ---- counters + reveals ---- */
  function countUp(el){
    var target=+el.dataset.count, start=null, dur=1100;
    requestAnimationFrame(function step(ts){
      if(!start) start=ts;
      var p=Math.min((ts-start)/dur,1);
      el.textContent=Math.round(target*(1-Math.pow(1-p,3)));
      if(p<1) requestAnimationFrame(step);
    });
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      e.target.classList.add('in');
      var c=e.target.querySelector('[data-count]');
      if(c&&!c.dataset.done){ c.dataset.done=1; reduce?c.textContent=c.dataset.count:countUp(c); }
      io.unobserve(e.target);
    });
  },{threshold:.15, rootMargin:'0px 0px -50px 0px'});
  document.querySelectorAll('.stand').forEach(function(el,i){
    el.style.transitionDelay=((i%4)*70)+'ms'; io.observe(el);
  });

  var replay=document.getElementById('replay');
  if(replay) replay.addEventListener('click', runCountdown);
  var yr=document.getElementById('yr');
  if(yr) yr.textContent=new Date().getFullYear();
  runCountdown(); onScroll();
})();
