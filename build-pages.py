#!/usr/bin/env python3
"""
Builds the inner pages from one shared shell, so the nav, footer, SEO
scaffolding and contact block can never drift apart between pages.

Run it after editing any page's content below:

    python3 build-pages.py

It writes the .html files beside itself. There is no build step in the
site itself — these are plain files once written.
"""

SITE = "https://sarahjhill.com"
EMAIL = "sarah@sarahjhill.com"
DEMO = "https://sarahjhill.com/project-os/app.html?guest=1"
PROJECT_OS = "https://sarahjhill.com/project-os/"
PORTFOLIO = "https://sarahjhill.com/portfolio/"
# The ember-store Cloudflare Worker (see ember-themes/delivery-worker). Paste the URL
# `npx wrangler deploy` prints, or a custom domain like https://store.sarahjhill.com
STORE_API = "https://ember-store.REPLACE-ME.workers.dev"

SHELL = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- ============ SEO ============ -->
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{site}/{url}">
  <meta name="author" content="Sarah J Hill">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#0a0a0c">

  <meta property="og:type" content="{ogtype}">
  <meta property="og:url" content="{site}/{url}">
  <meta property="og:site_name" content="Sarah J Hill">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{site}/assets/img/og-card.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="The Sarah J Hill homepage: &ldquo;That&rsquo;s how long they take to write you off.&rdquo;">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{ogtitle}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{site}/assets/img/og-card.jpg">

  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="{root}favicon-32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="{root}favicon-48.png">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <meta name="apple-mobile-web-app-title" content="Sarah J Hill">

  <!-- ============ STYLES ============ -->
  <link rel="stylesheet" href="{root}assets/css/01-tokens.css">
  <link rel="stylesheet" href="{root}assets/css/02-layout.css">
  <link rel="stylesheet" href="{root}assets/css/03-components.css">
  <link rel="stylesheet" href="{root}assets/css/06-globe.css">
  <link rel="stylesheet" href="{root}assets/css/04-motion.css">
{extracss}

  <!-- ============ STRUCTURED DATA ============ -->
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
<div id="tick" aria-hidden="true"></div>

<nav id="nav">
  <div class="wrap">
    <a class="brand" href="{root}index.html"><img class="brand-mark" src="{root}assets/img/logo-mark-160.png" alt="" width="38" height="38"><b>Sarah J <span>Hill</span><em>Dragon Fire Design</em></b></a>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navlinks">
      <span></span><span></span><span></span>
    </button>
    <div class="navlinks" id="navlinks">
      <a href="{root}index.html#work">Work</a>
      <a href="{root}process.html">How I work</a>
      <a href="{root}index.html#prices">Prices</a>
      <a href="{root}index.html#about">About</a>
      <a href="{root}blog/">Blog</a>
      <a class="navcta" href="{project_os}forms/intake.html" target="_blank" rel="noopener">Start a project</a>
    </div>
  </div>
</nav>

<header class="page-hero" id="top">
  <div class="wrap">
    <a class="backlink" href="{root}{backhref}">&larr; {backtext}</a>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
{herocta}
  </div>
</header>

<main id="main">
{body}
</main>

<!-- ============ CLOSE ============ -->
<section class="close" id="hello">
  <div class="wrap">
   <div class="globe-wrap">
    <div class="stand">
      <div class="sjh-globe" aria-hidden="true"><canvas class="sjh-globe-canvas"></canvas></div>
      <p class="sjh-globe-note">Wherever you are, it lands in Cardiff</p>
    </div>
   <div>
    <p class="eyebrow stand">Say hello</p>
    <h2 class="stand">Let's get you taken seriously.</h2>
    <p class="lead stand">Tell me what you do and what's driving you mad about it. Two working days,
      an honest answer &mdash; even if that answer is &ldquo;this isn't for you, and here's why&rdquo;.</p>
    <div class="cta-row stand" style="margin-top:32px;">
      <a class="btn btn-primary" href="{project_os}forms/intake.html" target="_blank" rel="noopener">Start a project &rarr;</a>
      <a class="btn btn-ghost" href="{root}process.html">How I work &rarr;</a>
    </div>
   </div>
   </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <span>&copy; <span id="yr">2026</span> Sarah J Hill &middot; Dragon Fire Design &middot; Built by hand, yours to own.</span>
    <span>Cardiff &amp; Birmingham &middot; <a href="mailto:{email}">{email}</a></span>
    <div class="footlinks" role="navigation" aria-label="More pages">
      <a href="{root}website-audit.html">Free website audit</a>
      <a href="{root}process.html">How I work</a>
      <a href="{root}index.html#answers">FAQs</a>
      <a href="{root}blog/">Blog</a>
      <a href="{root}web-design-cardiff.html">Web design Cardiff</a>
      <a href="{root}web-design-birmingham.html">Web design Birmingham</a>
      <a href="{root}project-os.html">The Dragon Fire Process</a>
    </div>
    <span class="footnote">Web design for women in business, female founders, charities, community groups
      and tradeswomen &mdash; Cardiff, South Wales, Birmingham, the West Midlands and remote across the UK.</span>
  </div>
</footer>

<script src="{root}assets/js/main.js" defer></script>
<script src="{root}assets/js/globe.js" defer></script>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8f936632609c48e5bc300dd47e8645ed"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""


def row(h3, p, label, payoff):
    return f"""      <div class="row stand">
        <div><h3>{h3}</h3>
          <p>{p}</p></div>
        <div class="payoff"><em>{label}</em><b>{payoff}</b></div>
      </div>
"""


def step(n, h3, p):
    return f"""      <div class="step stand"><span class="no">{n}</span>
        <div><h3>{h3}</h3><p>{p}</p></div></div>
"""


def stat(v, k, dark=True):
    bg = "" if dark else ' style="background:var(--paper);"'
    col = "" if dark else ' style="color:var(--flame)"'
    kc = "" if dark else ' style="color:var(--mute-dark)"'
    return (f'        <div class="stat stand"{bg}><div class="v" data-count="{v}"{col}>0</div>'
            f'<div class="k"{kc}>{k}</div></div>\n')


# =====================================================================
PAGES = {}

# ---------------------------------------------------------------- audit
PAGES["website-audit.html"] = dict(
    title="Free website audit, Cardiff &amp; Birmingham | Sarah J Hill",
    desc=("A free website review that answers one question: how many customers doubt you before "
          "they ever ring? Two working days, nothing to pay, and no catch."),
    ogtitle="How many customers doubt you before they ring?",
    ogtype="website",
    backhref="index.html", backtext="Back to the start",
    eyebrow="Already got a website? &mdash; free, no catch",
    h1="You have a website <span class=\"hit\">but it does nothing for you.</span>",
    lead=("You'll never know how many people quietly left. There's no missed-call list for "
          "&ldquo;looked a bit unconvincing&rdquo;. So I'll go through your site the way your "
          "customers do &mdash; on a phone, in a hurry, hunting for a reason to say no &mdash; "
          "and tell you which bits have gone cold and which bits are still hot."),
    herocta=f"""    <div class="cta-row">
      <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Doubt%20Audit%20request">Get my free website review &rarr;</a>
      <a class="btn btn-ghost" href="#check">What I actually check</a>
    </div>
    <div class="chips">
      <span class="chip">3 minutes to ask</span>
      <span class="chip">Scored out of 100</span>
      <span class="chip">Report in 2 working days</span>
      <span class="chip">Nothing to pay</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "The Doubt Audit",
    "serviceType": "Website review",
    "provider": { "@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/" },
    "areaServed": { "@type": "Country", "name": "United Kingdom" },
    "description": "A free website review judged the way a doubtful customer judges it.",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "GBP" }
  }""",
    body=(
        """<!-- ============ THE LEAK ============ -->
<section class="band">
  <div class="wrap">
    <p class="eyebrow stand">The leak</p>
    <h2 class="stand">It takes about three seconds, and nobody tells you.</h2>
    <p class="lead stand">Here is exactly how you lose somebody who was ready to buy from you.</p>
    <div class="steps">
"""
        + step("01", "They tap your link",
               "Someone searches for what you do and taps through to your website. "
               "At this point you have already won the hard part.")
        + step("02", "They wait",
               "And wait. This is the moment it goes wrong, and it takes about three seconds. "
               "On a phone, on mobile data, standing in a car park.")
        + step("03", "They go back to Google",
               "Straight on to whoever loads faster &mdash; which is usually whoever is nearest you "
               "and no better at the job.")
        + step("04", "You never hear about it",
               "No missed-call list. No voicemail. No note through the door. It just quietly "
               "does not happen, week after week.")
        + """    </div>
  </div>
</section>

<!-- ============ THE NUMBERS ============ -->
<section class="dark">
  <div class="wrap">
    <p class="eyebrow stand">The averages</p>
    <h2 class="stand">Your site might beat these. It might be a great deal worse.</h2>
    <p class="lead stand">The only way to know is to measure it, which is what the audit is for.</p>
    <div class="stats">
"""
        + stat("9", "Average mobile load (s)")
        + stat("3", "What it should be under (s)")
        + stat("32", "More visitors lost by 3s (%)")
        + stat("2", "Working days to your report")
        + """    </div>
    <p class="source">Sources: HTTP Archive and Google mobile speed benchmarks; bounce-rate figures
      from Google's own research on mobile page speed.</p>
  </div>
</section>

<!-- ============ WHAT I CHECK ============ -->
<section class="band alt" id="check">
  <div class="wrap">
    <p class="eyebrow stand">What I actually check</p>
    <h2 class="stand">Some of it is a scan. The rest is me, on a phone, being your customer.</h2>
    <p class="lead stand">The scan is my own tool, Dragonfire: 35+ checks across speed, Google, local search
      and AI search, scored out of 100. Then I go through it by hand and tell you what actually matters.</p>
    <div class="rows">
"""
        + row("How fast it really is",
              "Measured on a phone on mobile data, not on a fast computer on office broadband. "
              "That difference is usually where the nasty surprise lives.",
              "You find out", "How many people never see your page at all.")
        + row("Whether it works on a phone",
              "Text you can read without pinching, buttons you can hit with a thumb, nothing running "
              "off the side of the screen. Most local searches happen on a phone, usually while the "
              "person is standing up.",
              "You find out", "What your busiest visitors are really looking at.")
        + row("Whether anyone can reach you",
              "I test your contact form and send a real message through it. I check your phone number "
              "is tappable and your address is right. A surprising number of forms have quietly been "
              "going nowhere for months.",
              "You find out", "Whether you've been losing enquiries you never knew existed.")
        + row("Whether Google can find you",
              "Your Google Business Profile, your opening hours, your reviews, and whether you turn up "
              "in the map results when somebody nearby searches for what you do. For a local business "
              "this is often worth more than the website itself.",
              "You find out", "Where you sit against the others near you.")
        + row("Whether AI can find and quote you",
              "More and more people ask ChatGPT, Gemini or Perplexity &ldquo;who&rsquo;s good near me?&rdquo; "
              "instead of Googling. I check whether those tools can read your site, understand what you do, "
              "and whether anything is quietly blocking them.",
              "You find out", "Whether you&rsquo;re in the running for the new front page.")
        + row("Whether the proof is where the doubt is",
              "Qualifications, insurance, reviews and real photographs of you doing the work &mdash; "
              "are they at the top where somebody is already looking for a reason to say no, or three "
              "scrolls down where nobody reaches?",
              "You find out", "What is making people hesitate.")
        + """    </div>
  </div>
</section>

<!-- ============ HONESTY ============ -->
<section class="dark">
  <div class="wrap">
    <p class="eyebrow stand">What I won't do</p>
    <h2 class="stand">I will not invent a number.</h2>
    <div class="rows">
"""
        + row("You have probably had the email",
              "&ldquo;Your website is losing you &pound;47,000 a year.&rdquo; Nobody who has never seen "
              "your books can possibly know that, and you were right to bin it.",
              "Instead", "Your figures, your sums, an honest range.")
        + row("You tell me three things you already know",
              "Roughly how many enquiries you get in a week, what an average customer is worth to you, "
              "and roughly how many of those enquiries you win. Put those next to what I measured and "
              "you get a sensible worst case and best case.",
              "You get", "A range with your own numbers behind it.")
        + row("And if your website is fine?",
              "If it is doing its job and the problem is somewhere else entirely, I will tell you that "
              "and we are done.",
              "You lose", "The time it took to send me the address.")
        + f"""    </div>
    <div class="cta-row stand" style="margin-top:32px;">
      <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Doubt%20Audit%20request">Get my free website review &rarr;</a>
    </div>
  </div>
</section>
"""
    ),
)


# --------------------------------------------------------------- process
def foru(text):
    return f'<span class="foru"><b>What it means for you:</b> {text}</span>'


PAGES["process.html"] = dict(
    title="How I work: the Dragon Fire Process | Sarah J Hill, Cardiff",
    desc=("The Dragon Fire Process: 12 phases and 69 checked tasks, with your own live project page. "
          "What happens at each step, what it means for you, and why it gets a better job delivered."),
    ogtitle="The Dragon Fire Process — a better job, delivered",
    ogtype="website",
    crumb="How I work",
    backhref="index.html", backtext="Back to the start",
    eyebrow="How I work &middot; the Dragon Fire Process",
    h1="The Dragon Fire Process. <span class=\"hit\">A better job, delivered.</span>",
    lead=("Most web designers send a proposal full of jargon, then go quiet until launch. My Dragon Fire "
          "Process is built so that never happens to you: 12 phases and 69 checked tasks, every one visible "
          "on your own live project page. Here&rsquo;s how it works, and what it means for you."),
    herocta=f"""    <div class="cta-row">
      <a class="btn btn-primary" href="{PROJECT_OS}forms/intake.html" target="_blank" rel="noopener">Start a project &rarr;</a>
      <a class="btn btn-ghost" href="#two-views">See it in action</a>
    </div>
    <div class="chips">
      <span class="chip">12 phases</span>
      <span class="chip">69 checked tasks</span>
      <span class="chip">Your own live project page</span>
      <span class="chip">Fixed price, real dates</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "The Dragon Fire Process: how a Sarah J Hill website gets built",
    "step": [
      { "@type": "HowToStep", "position": 1, "name": "The brief", "text": "Getting to know your business, your customers and your real value." },
      { "@type": "HowToStep", "position": 2, "name": "The plan", "text": "Every page mapped, with a fixed quote and real dates." },
      { "@type": "HowToStep", "position": 3, "name": "Built in the open", "text": "A working version you can click through, with every task visible on your own project page." },
      { "@type": "HowToStep", "position": 4, "name": "The design", "text": "Your colours, photos and voice brought to the working version." },
      { "@type": "HowToStep", "position": 5, "name": "Launch and connect", "text": "Tested, checked for Google and AI search, launched, and connected to other female-owned businesses." }
    ]
  }""",
    body=(
        """<!-- ============ THE STEPS ============ -->
<section class="band" id="steps">
  <div class="wrap">
    <p class="eyebrow stand">From hello to launch</p>
    <h2 class="stand">What happens, and what it means for you.</h2>
    <p class="lead stand">Five stages, in plain English. You always know where we are and what&rsquo;s next.</p>
    <div class="steps">
"""
        + step("01", "The brief: finding your real value",
               "We talk about what you do, who it&rsquo;s for and why you really need a website. I&rsquo;ll ask "
               "questions nobody else asks, and some might feel a bit uncomfortable. If it never gets a little "
               "awkward, I haven&rsquo;t dug deep enough. "
               + foru("a website that sells what&rsquo;s genuinely special about you, not a template with your name on it."))
        + step("02", "The plan: every page mapped",
               "Within two working days you get a fixed quote and a plan with real dates. I map every page: who "
               "it&rsquo;s for, what they need to see, and what you want them to do next. "
               + foru("you know the price and the dates before you commit. No padding, no surprise bills.") + ' ' + "<a class=\"baked\" href=\"" + PROJECT_OS + "app.html?guest=1\" target=\"_blank\" rel=\"noopener\">See a real plan I made earlier &rarr;</a>")
        + step("03", "Built in the open",
               "Instead of describing what I&rsquo;ll build and hoping you follow my jargon, I build a working "
               "version you can click through on your own phone, while every task ticks off on your project page. "
               + foru("you spot anything that&rsquo;s not right early, when it&rsquo;s quick to change, and you never have to chase me.") + ' ' + "<a class=\"baked\" href=\"#two-views\">Here&rsquo;s one I made earlier &rarr;</a>")
        + step("04", "The design: the fun bit",
               "The working version gets dressed in your brand: your colours, your photos, your voice. Hand-made, "
               "so it&rsquo;s fast and easy to use, not the usual bloated template. "
               + foru("a site that looks and sounds like you, loads fast, and you can edit yourself.") + ' ' + "<a class=\"baked\" href=\"index.html#work\">See finished sites &rarr;</a>")
        + step("05", "Launch and connect",
               "Tested on real phones and checked with Dragonfire, my own SEO tool. Then it goes live, I show you "
               "how to edit it, and I connect you with other female-owned businesses who&rsquo;ll share your work. "
               + foru("customers can find you on Google and in AI answers, and you&rsquo;re not doing it alone."))
        + """    </div>
  </div>
</section>

<!-- ============ TWO VIEWS ============ -->
<section class="dark" id="two-views">
  <div class="wrap">
    <p class="eyebrow stand">See it in action</p>
    <h2 class="stand">One project. Two views. Nothing hidden.</h2>
    <p class="lead stand">I run every project through the Dragon Fire Process. You get your own private page that
      shows the same project in plain English.</p>
    <div class="shots">
      <figure class="shot stand">
        <div class="shot-frame"><img src="assets/img/work/projectos-desk.webp" width="1000" height="1479" loading="lazy"
          alt="The Dragon Fire Process dashboard: overall progress, 12 phases with progress bars, and the next tasks"></div>
        <figcaption><b>My side.</b> All 12 phases and every task, so nothing gets missed and nothing depends on memory.</figcaption>
      </figure>
      <figure class="shot stand">
        <div class="shot-frame"><img src="assets/img/process/client-desk.webp" width="1000" height="1460" loading="lazy"
          alt="A client&rsquo;s project page: where things are, progress, what is needed from the client, key dates and shared files"></div>
        <figcaption><b>Your side.</b> Where things are, what I need from you, your key dates and your files. Private to you.</figcaption>
      </figure>
    </div>
    <p class="tiny-note stand">Screens show a demo project. Scroll inside each one.</p>
    <div class="cta-row stand" style="margin-top:22px;">
      <a class="btn btn-primary" href=\"""" + PROJECT_OS + """app.html?guest=1" target="_blank" rel="noopener">Look round a real demo &rarr;</a>
      <a class="btn btn-ghost" href="project-os.html">All 12 phases explained</a>
    </div>
  </div>
</section>

<!-- ============ COMMUNICATION ============ -->
<section class="band" id="talk">
  <div class="wrap">
    <p class="eyebrow stand">A better way to communicate</p>
    <h2 class="stand">No chasing. No &ldquo;any update?&rdquo; No lost emails.</h2>
    <p class="lead stand">Most projects go wrong in the gaps between messages. Your project page closes them.</p>
    <div class="talk-grid">
    <ul class="pticks stand">
      <li><b>Where things are, in plain English.</b> A short note from me at the top, updated as we go. No jargon.</li>
      <li><b>Exactly what I need from you, and by when.</b> Never a vague &ldquo;waiting on you&rdquo;. You tick it off and I see it.</li>
      <li><b>Real dates you can plan around.</b> Every milestone, marked done or coming up, so launch day doesn&rsquo;t drift.</li>
      <li><b>Every file in one place.</b> Logos, photos and words, not scattered across WhatsApp, email and texts.</li>
      <li><b>A human when you need one.</b> Questions get an answer from me, usually the same day.</li>
    </ul>
    <figure class="shot shot--phone stand">
      <div class="shot-frame"><img src="assets/img/process/client-phone.webp" width="480" height="2266"
        alt="The client project page on a phone"></div>
      <figcaption>Your project page on your phone. Check it in the queue at the shop.</figcaption>
    </figure>
    </div>
  </div>
</section>

<!-- ============ EXPERTISE ============ -->
<section class="dark" id="trained">
  <div class="wrap">
    <p class="eyebrow stand">Expertise</p>
    <h2 class="stand">Trained not to miss a single part.</h2>
    <p class="lead stand">I&rsquo;m a full-stack developer trained at Code Institute, and I&rsquo;ve studied how the
      best web agencies run their projects. The Dragon Fire Process turns that into a checklist I follow on
      every single build.</p>
    <ul class="pticks pticks--dark stand">
      <li><b>The same 69 checks, every time.</b> Quality doesn&rsquo;t depend on whether I&rsquo;m having a good day.</li>
      <li><b>Best practice built in.</b> Accessibility, speed on a cheap phone, security and clean code, checked before launch.</li>
      <li><b>Found, not just finished.</b> Every site goes through Dragonfire, my own SEO tool, for Google and AI search.</li>
      <li><b>One person who understands the whole build.</b> Words, design, front end and back end, so nothing gets lost in a hand-off.</li>
    </ul>
  </div>
</section>

<!-- ============ WHO I WORK WITH ============ -->
<section class="band" id="who">
  <div class="wrap">
    <p class="eyebrow stand">Who I work with</p>
    <h2 class="stand">Bold. Brave. <span style="color:var(--flame)">Ballsy.</span></h2>
    <p class="lead stand">I work with women who want to make a real difference: founders, tradeswomen, charities and
      community groups who do what they mean and mean what they say. If you&rsquo;re tired of being underestimated
      and ready to claim your space, we&rsquo;ll get on.</p>
    <p class="big-line stand">This is a woman&rsquo;s world. It&rsquo;s yours. Let&rsquo;s build it.</p>
    <div class="cta-row stand" style="margin-top:28px;">
      <a class="btn btn-primary" href=\"""" + PROJECT_OS + """forms/intake.html" target="_blank" rel="noopener">Start a project &rarr;</a>
      <a class="btn btn-ghost" href="index.html#prices">See prices</a>
    </div>
  </div>
</section>
"""
    ),
)

# ------------------------------------------------------------- sjh process
PAGES["project-os.html"] = dict(
    title="The Dragon Fire Process — client portal | Sarah J Hill",
    desc=("Twelve phases, 69 guided tasks and 72 templates. Clients watch the build happen "
          "instead of chasing it, and other studios can licence the whole process for £39."),
    ogtitle="Nobody should have to type &ldquo;any update?&rdquo;",
    ogtype="website",
    backhref="index.html", backtext="Back to the start",
    eyebrow="The Dragon Fire Process &mdash; my custom client process",
    h1="Nobody should have to type <span class=\"hit\">&ldquo;any update?&rdquo;</span>",
    lead=("The industry standard is three weeks of silence and a hopeful email. I built my own "
          "custom client process instead &mdash; streamlined, transparent, and clean enough that "
          "you'll always know exactly where things stand. And you can own it too."),
    herocta=f"""    <div class="cta-row">
      <a class="btn btn-primary" href="{DEMO}" target="_blank" rel="noopener">Look round a real project &rarr;</a>
      <a class="btn btn-ghost" href="#studio">Licence it &mdash; &pound;39</a>
    </div>
    <div class="chips">
      <span class="chip">Installs to a phone</span>
      <span class="chip">Works with no signal</span>
      <span class="chip">Nothing that can rot</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "The Dragon Fire Process",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Any modern browser",
    "url": "https://sarahjhill.com/project-os/",
    "author": { "@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/" },
    "description": "A twelve-phase project delivery system with 69 guided tasks, 72 templates and a client sign-in.",
    "offers": { "@type": "Offer", "price": "39", "priceCurrency": "GBP" }
  }""",
    body=(
        """<!-- ============ CLIENT ============ -->
<section class="band alt" id="client">
  <div class="wrap">
    <p class="eyebrow stand">If you're a client</p>
    <h2 class="stand">You watch it happen. You don't wait to be told.</h2>
    <p class="lead stand">Everything below is what you see from the day we start.</p>
    <div class="rows">
"""
        + row("You get me. Not a ticket number.",
              "You also get the tool I wrote to run this studio. From the day we start, your project is "
              "a live page you sign in to &mdash; every phase, every task, ticking off in front of you as "
              "it actually happens. No weekly email saying &ldquo;good progress&rdquo;. You watch the real "
              "thing move.",
              "You get", "Every moment, as it unfolds.")
        + row("Everything you need is on that one page",
              "Your logo, your photos, your words, the plan, the invoice, the sign-off &mdash; uploaded and "
              "downloaded from the same place, whenever it suits you. No hunting back through an email chain "
              "for the file you sent in March.",
              "You get", "One page. Nothing lost, nothing attached.")
        + row("One thing at a time, and only when it's your turn",
              "Whatever I need from you is written there in plain English, one small step at a time, with a "
              "line saying why it matters. Nothing lands on you all at once and nothing arrives as a surprise.",
              "You get", "A short list you can actually finish.")
        + row("Sign in without another password to lose",
              "It emails you a link and that is the whole of it. It installs to your phone like an app, and "
              "it keeps working when the signal doesn't.",
              "You get", "Access from wherever you happen to be.")
        + row("Nobody has to chase anybody",
              "You always know what is happening, what is next, and whose turn it is. If it is mine, you can "
              "see it moving. If it is yours, it is already sitting there waiting. And I don't vanish the day "
              "after launch.",
              "You get", "Never having to ask again.")
        + f"""    </div>
    <div class="cta-row stand" style="margin-top:30px;">
      <a class="btn btn-primary" href="{DEMO}" target="_blank" rel="noopener">Look round a real project &rarr;</a>
      <a class="btn btn-ghost" href="{PROJECT_OS}forms/intake.html" target="_blank" rel="noopener">Start with my intake questionnaire &rarr;</a>
    </div>
    <p class="cta-note" style="margin-top:10px;">Left one's a working demo, loaded with a made-up client.
      Right one's the actual first template &mdash; nothing to sign up for either way.</p>
  </div>
</section>

<!-- ============ STUDIO ============ -->
<section class="band" id="studio">
  <div class="wrap">
    <div class="studio stand">
      <p class="split-label" style="margin-top:0;">The part that actually decides it</p>
      <h3 class="studio-h">My Dragon Fire Process.</h3>
      <p class="studio-p"><b>An AI can hand you a process document in ten seconds.</b> It has
        never once asked why your last three customers actually found you, or noticed you'd buried
        the best thing about your business in paragraph three.</p>

      <p class="studio-p">That's the concept gap &mdash; and it's exactly where a human earns their
        keep. I ask the second question, I read the room, and I build your strategy around what you
        actually know that nobody else does.</p>

      <p class="studio-p">The goal isn't &ldquo;good enough&rdquo;. It's <b>100% satisfaction, every
        time</b> &mdash; and you get to watch it happen, not take my word for it.</p>

      <div class="stats">
"""
        + stat("12", "Phases") + stat("69", "Guided tasks")
        + stat("72", "Templates") + stat("100", "% satisfaction, always")
        + f"""      </div>

      <div class="cta-row" style="margin-top:26px;">
        <a class="btn btn-primary" href="{DEMO}" target="_blank" rel="noopener">Watch today's project move &rarr;</a>
        <a class="btn btn-ghost" href="#hello">Start yours &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- ============ HOW IT IS BUILT ============ -->
<section class="dark">
  <div class="wrap">
    <p class="eyebrow stand">Under the bonnet</p>
    <h2 class="stand">Written by hand. Nothing that can rot.</h2>
    <div class="rows">
"""
        + row("No framework, no build step",
              "Plain HTML, CSS and JavaScript. Progress lives in the browser; accounts and client sharing run "
              "on Supabase, with database-level rules deciding who sees what rather than the interface politely "
              "hiding things.",
              "Which means", "No dependency that can break in two years.")
        + row("Clients see a snapshot, never the working project",
              "I choose what gets published. Every client form submits straight to me &mdash; nothing to download, "
              "nothing to attach, nothing to lose.",
              "Which means", "You share the right things and only those.")
        + row("The rigour is mine to carry",
              "Twelve phases and sixty-nine tasks exist so accessibility, testing and the fiddly bits never get "
              "quietly skipped the week everything runs late.",
              "Which means", "The careful version, every time.")
        + """    </div>
  </div>
</section>
"""
    ),
)



# --------------------------------------------------------------- THEMES
STORE_DIV = (f'<div id="store" data-store-api="{STORE_API}" '
             f'data-fallback="mailto:{EMAIL}?subject=Ember%20theme"></div>\n'
             '<script src="assets/js/store.js" defer></script>\n')


def plan(name, price, items, product, best=False, tag=""):
    li = "".join(f"<li>{i}</li>" for i in items)
    t = f'<span class="tag">{tag}</span>' if tag else ""
    return f"""      <div class="plan stand{' best' if best else ''}">
        {t}<h3>{name}</h3>
        <div class="price">&pound;{price}<small>one-off</small></div>
        <ul>{li}</ul>
        <a class="btn btn-primary" href="#buy" data-buy="{product}">Buy {name} &rarr;</a>
        <p class="buy-msg" aria-live="polite"></p>
      </div>
"""


IMG = "assets/img/ember/"


def feat(img, w, h, where, title, text, alt):
    return f"""      <div class="feat stand">
        <div class="shot{' shot--wide' if w / h > 2 else ''}"><img src="{IMG}{img}.webp" width="{w}" height="{h}" alt="{alt}" loading="lazy"></div>
        <span class="where">{where}</span>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>
"""


def page_btn(label, img, w, h, alt, pressed=False):
    return (f'<button type="button" data-target="desk-view" data-show-page="{IMG}{img}.webp" data-w="{w}" data-h="{h}" '
            f'data-alt="{alt}" aria-pressed="{"true" if pressed else "false"}">{label}</button>')


PAGES["themes.html"] = dict(
    title="Ember — Shopify &amp; WooCommerce theme | Sarah J Hill",
    desc=("Ember is a soft, British marketplace theme for Shopify and WooCommerce. Category bubbles, "
          "lightning deals, shop-by-budget. Edit it all visually. £59."),
    ogtitle="Ember: a marketplace theme with manners",
    ogtype="product",
    backhref="index.html", backtext="Back to the start",
    eyebrow="Ember &mdash; marketplace theme for Shopify &amp; WooCommerce",
    h1="All the buzz of a marketplace. <span class=\"hit\">None of the tat.</span>",
    lead=("Category bubbles, lightning deals, shop-by-budget and an app-style bar on phones. "
          "Wrapped in soft colours, a proper serif and a bit of British cheek. Install it tonight, "
          "then edit every word yourself."),
    herocta="""    <div class="cta-row">
      <a class="btn btn-primary" href="#buy">Get Ember &mdash; from &pound;59 &rarr;</a>
      <a class="btn btn-ghost" href="#look">Have a proper look</a>
    </div>
    <div class="platform-tag"><b>Shopify</b><b>WooCommerce</b><b>Instant download</b><b>No code</b></div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Ember marketplace theme",
    "image": "https://sarahjhill.com/assets/img/ember/desktop-home.webp",
    "brand": { "@type": "Brand", "name": "Sarah J Hill" },
    "description": "A soft, British marketplace theme for Shopify and WooCommerce, edited visually.",
    "offers": [
      { "@type": "Offer", "name": "Shopify", "price": "59", "priceCurrency": "GBP", "availability": "https://schema.org/InStock", "url": "https://sarahjhill.com/themes.html#buy" },
      { "@type": "Offer", "name": "WooCommerce", "price": "59", "priceCurrency": "GBP", "availability": "https://schema.org/InStock", "url": "https://sarahjhill.com/themes.html#buy" },
      { "@type": "Offer", "name": "Bundle", "price": "89", "priceCurrency": "GBP", "availability": "https://schema.org/InStock", "url": "https://sarahjhill.com/themes.html#buy" }
    ]
  }""",
    body=(
        f"""<!-- ============ HERO MOCK ============ -->
<section class="dark showcase" aria-label="Ember on a laptop and a phone">
  <div class="wrap">
    <div class="mock stand">
      <div class="browser">
        <div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>buntingandco.co.uk</span></div>
        <img src="{IMG}desktop-home.webp" width="1600" height="1000" alt="Ember home page: a pink welcome card reading Proper lovely things, sensible prices, beside lightning deals and new-in tiles" fetchpriority="high">
      </div>
      <div class="phone"><img src="{IMG}phone-home.webp" width="540" height="1168" alt="Ember on a phone, with a big search bar and an app-style bar along the bottom"></div>
    </div>
  </div>
</section>

<!-- ============ RESPONSIVE ============ -->
<section class="band" id="look">
  <div class="wrap">
    <p class="eyebrow stand">Every screen</p>
    <h2 class="stand">Built for phones first. Lovely everywhere else.</h2>
    <p class="lead stand">Most of your customers will meet you on a phone, mid-scroll, thumb hovering.
      So the search bar is huge, the basket is one tap away and the bottom bar feels like an app.</p>

    <div class="devices">
      <div class="device-tabs" role="tablist" aria-label="Choose a screen size">
        <button type="button" role="tab" id="tab-desk" aria-controls="panel-desk" aria-selected="true">Desktop</button>
        <button type="button" role="tab" id="tab-tab" aria-controls="panel-tab" aria-selected="false" tabindex="-1">Tablet</button>
        <button type="button" role="tab" id="tab-phone" aria-controls="panel-phone" aria-selected="false" tabindex="-1">Phone</button>
      </div>

      <div class="device-panel" id="panel-desk" role="tabpanel" aria-labelledby="tab-desk">
        <div class="browser">
          <div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>buntingandco.co.uk</span></div>
          <div class="scroller-view" id="desk-view" tabindex="0" aria-label="Scrollable screenshot">
            <img src="{IMG}desktop-home-full.webp" width="1200" height="3750" alt="The whole Ember home page, from welcome card to reviews" loading="lazy">
          </div>
        </div>
        <div class="page-thumbs">
          {page_btn("Home", "desktop-home-full", 1200, 3750, "The whole Ember home page, from welcome card to reviews", True)}
          {page_btn("Shop + filters", "desktop-shop", 1400, 875, "Shop page with price, category, rating and stock filters")}
          {page_btn("Product", "desktop-product", 1400, 875, "Product page with sale price, reviews and a delivery promise")}
          {page_btn("Deals page", "desktop-deals", 1400, 875, "Today’s deals page with a countdown to midnight")}
        </div>
        <p class="scroll-hint">Scroll inside the window to see the whole page.</p>
      </div>

      <div class="device-panel" id="panel-tab" role="tabpanel" aria-labelledby="tab-tab" hidden>
        <div class="tablet"><img src="{IMG}tablet-home.webp" width="820" height="1180" alt="Ember on a tablet, with the welcome card above two offer tiles" loading="lazy"></div>
      </div>

      <div class="device-panel" id="panel-phone" role="tabpanel" aria-labelledby="tab-phone" hidden>
        <div class="phones">
          <figure><div class="phone"><img src="{IMG}phone-home.webp" width="540" height="1168" alt="Home page on a phone" loading="lazy"></div><figcaption>Home</figcaption></figure>
          <figure><div class="phone"><img src="{IMG}phone-product.webp" width="540" height="1168" alt="Product page on a phone" loading="lazy"></div><figcaption>Product</figcaption></figure>
          <figure><div class="phone"><img src="{IMG}phone-cart.webp" width="540" height="1168" alt="Basket on a phone with a free delivery progress bar" loading="lazy"></div><figcaption>Basket</figcaption></figure>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============ FEATURES ============ -->
<section class="dark" id="features">
  <div class="wrap">
    <p class="eyebrow stand">What makes it a marketplace</p>
    <h2 class="stand">The bits that make people buy one more thing.</h2>
    <div class="feat-grid">
"""
        + feat("f-rail", 760, 235, "Home page", "Category bubbles",
               "A swipeable row of round pictures, like the apps people already use. One tap to an aisle.",
               "Round category pictures: kitchen, tea time, rainy days, garden and more")
        + feat("f-deals", 760, 126, "Home + deals page", "Lightning deals",
               "Sale items with a live countdown that resets at midnight. Urgency, without the shouting.",
               "Lightning deals heading with a countdown timer")
        + feat("f-card", 400, 737, "Every product grid", "Cards that do the selling",
               "Stars, the saving, the sale badge and a one-tap Add to basket. On Shopify: “Sold by” and “Only 3 left” too.",
               "A product card for a breakfast bowl with a sale badge, stars and a basket button")
        + feat("f-budget", 760, 117, "Home page", "Shop by budget",
               "Under £5, £10, £20. Straight into a filtered shop. Bargain hunters, sorted.",
               "Price chips: under five, ten, twenty and fifty pounds")
        + feat("f-delivery", 800, 270, "Product page", "Delivery promise",
               "“Order within 2h 30m and it ships today.” Counts down to your own dispatch cut-off.",
               "Delivery box: order now and it ships next working day, free UK delivery, 30-day returns")
        + feat("f-shipping", 700, 174, "Basket", "Free delivery nudge",
               "A progress bar that tells them how close they are, and updates as they add.",
               "Progress bar reading Free delivery, sorted")
        + feat("f-bottom-nav", 700, 114, "Phones", "App-style bottom bar",
               "Home, Shop, Deals, Account, Basket. Always under their thumb.",
               "Bottom bar with home, shop, deals, account and basket icons")
        + feat("f-filters", 360, 893, "Shop pages", "Proper filters",
               "Price slider, categories, ratings and stock. People find it, then they buy it.",
               "Filter panel with a price slider, categories, ratings and availability")
        + feat("f-header", 760, 121, "Every page", "Search front and centre",
               "A big, friendly search bar with live suggestions. The most-used box in any marketplace.",
               "Header with a large search bar, the menu and a Today’s deals link")
        + """    </div>
  </div>
</section>

<!-- ============ PLATFORMS ============ -->
<section class="band alt" id="platforms">
  <div class="wrap">
    <p class="eyebrow stand">Which one's for you</p>
    <h2 class="stand">Same look. Your platform.</h2>
    <p class="lead stand">Both versions share the design you can see above. Pick the one your shop
      runs on, or get both if you build for clients.</p>
    <div class="platforms">
      <div class="platform stand">
        <h3>Shopify</h3>
        <p class="for">For shops that want hosting, payments and security handled.</p>
        <dl>
          <dt>You edit in</dt><dd>Online Store &rarr; Customize. Drag, drop, click, type.</dd>
          <dt>Included</dt><dd>25 drag-in sections, 8 colour schemes, signature fonts or any Shopify font</dd>
          <dt>Marketplace</dt><dd>&ldquo;Sold by&rdquo; seller names, &ldquo;Only 3 left&rdquo;, deals countdown, budget chips, bottom bar</dd>
          <dt>Selling</dt><dd>Variants and swatches, subscriptions, gift cards, Shop Pay, Apple Pay, Markets</dd>
          <dt>You need</dt><dd>Any Shopify plan</dd>
        </dl>
        <a class="btn btn-primary" href="#buy" data-buy="ember-shopify">Buy for Shopify &mdash; &pound;59 &rarr;</a>
      </div>
      <div class="platform stand">
        <h3>WordPress + WooCommerce</h3>
        <p class="for">For shops that want to own everything, with no monthly theme fees.</p>
        <dl>
          <dt>You edit in</dt><dd>Appearance &rarr; Editor. Every page, header and footer, visually.</dd>
          <dt>Included</dt><dd>16 drag-in patterns, 5 one-click styles, a Deals page template</dd>
          <dt>Marketplace</dt><dd>Category bubbles, deals countdown, budget chips, delivery promise, bottom bar</dd>
          <dt>Selling</dt><dd>Everything WooCommerce does: Stripe, PayPal, Klarna, any shipping and tax rules</dd>
          <dt>You need</dt><dd>WordPress 6.5+, WooCommerce 8.5+</dd>
        </dl>
        <a class="btn btn-primary" href="#buy" data-buy="ember-woocommerce">Buy for WooCommerce &mdash; &pound;59 &rarr;</a>
      </div>
    </div>
    <p class="cta-note stand" style="margin-top:18px;">Screenshots are from the WooCommerce version with
      demo products. Your shop shows your own photos.</p>
  </div>
</section>

<!-- ============ BUY ============ -->
<section class="band" id="buy">
  <div class="wrap">
    <p class="eyebrow stand">Pay once</p>
    <h2 class="stand">Pick your platform.</h2>
    <p class="lead stand">One payment, instant download, free v1 updates. Secure checkout by Stripe.</p>
    <div class="plans">
"""
        + plan("Shopify", 59, ["Online Store 2.0 theme", "25 drag-in sections", "One store",
                               "Free v1 updates", "Email support"], "ember-shopify")
        + plan("Bundle", 89, ["Shopify <b>and</b> WooCommerce", "One store + one WordPress site",
                              "Free v1 updates", "Email support", "Save &pound;29"],
               "ember-bundle", best=True, tag="Best value")
        + plan("WooCommerce", 59, ["WordPress block theme", "16 patterns, 5 styles", "One site",
                                   "Free v1 updates", "Email support"], "ember-woocommerce")
        + """    </div>
  </div>
</section>

<!-- ============ DOCS / LICENCE ============ -->
<section class="band alt" id="docs">
  <div class="wrap">
    <p class="eyebrow stand">Before you buy</p>
    <h2 class="stand">The small print, in large print.</h2>
    <div class="rows">
"""
        + row("Installing",
              "<b>Shopify:</b> Online Store &rarr; Themes &rarr; Add theme &rarr; Upload zip file. "
              "<b>WooCommerce:</b> Appearance &rarr; Themes &rarr; Add New &rarr; Upload Theme. "
              "Upload the zip as it is. Don't unzip it.",
              "Takes", "About two minutes.")
        + row("The licence",
              "One store or site per licence. Build it for a client? Buy a licence for each client. "
              "The WooCommerce code is GPL like WordPress. The Shopify theme is licensed, not sold.",
              "In short", "One licence, one shop.")
        + row("Refunds",
              "It's a download, so once you've downloaded it the 14-day cooling-off period no longer "
              "applies. Checkout asks you to agree to that. But if it won't install and I can't fix it, "
              "you get your money back.",
              "Promise", "It works, or you're refunded.")
        + f"""    </div>
    <p class="cta-note stand" id="support" style="margin-top:22px;">Stuck? Email <a href="mailto:{EMAIL}">{EMAIL}</a>
      with your licence key. You'll get a human, usually the same day.</p>
  </div>
</section>
"""
        + STORE_DIV
    ),
)

PAGES["themes-thanks.html"] = dict(
    title="Your download — Ember | Sarah J Hill",
    desc="Download your Ember theme.",
    ogtitle="Your Ember download",
    ogtype="website",
    robots="noindex, nofollow",
    backhref="themes.html", backtext="Back to Ember",
    eyebrow="Your order",
    h1="Done. <span class=\"hit\">Go and build something.</span>",
    lead="Your download is below. It's also in your inbox, so you can come back to it any time.",
    herocta="",
    jsonld='  { "@context": "https://schema.org", "@type": "WebPage", "name": "Ember order" }',
    body=(
        """<section class="dark">
  <div class="wrap">
    <div class="order" id="order" aria-live="polite">
      <h2>Finding your order&hellip;</h2>
      <p>This takes a couple of seconds after payment.</p>
    </div>
  </div>
</section>
"""
        + STORE_DIV
    ),
)


# =====================================================================
# Blog posts + Cardiff/Birmingham pages live in content_pages.py
import sys
sys.dont_write_bytecode = True   # no __pycache__ folder ending up on the live site
from content_pages import add_pages
add_pages(PAGES, SITE, EMAIL, PROJECT_OS)

import json
import os

UPDATED = "2026-10-12"   # bump when you change a page; goes into dateModified


def crumbs(slug, p):
    """Home › (Blog ›) This page — as BreadcrumbList schema."""
    items = [("Home", f"{SITE}/")]
    if slug.startswith("blog/") and slug != "blog/index.html":
        items.append(("Blog", f"{SITE}/blog/"))
    items.append((p.get("crumb") or p["ogtitle"].split("—")[0].strip(), f"{SITE}/{public_url(slug)}"))
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n.replace("&amp;", "&"), "item": u}
        for i, (n, u) in enumerate(items)]}


def public_url(slug):
    return slug[: -len("index.html")] if slug.endswith("index.html") else slug


def build():
    for slug, p in PAGES.items():
        root = "../" * slug.count("/")
        page_ld = json.loads(p["jsonld"]) if p.get("jsonld") else None
        if page_ld is None:
            graph = []
        elif "@graph" in page_ld:
            graph = page_ld["@graph"]
        else:
            graph = [page_ld]
        for node in graph:
            node.pop("@context", None)
            node.setdefault("dateModified", p.get("updated", UPDATED))
        graph.append(crumbs(slug, p))
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                            ensure_ascii=False, indent=2)
        html = SHELL.format(
            site=SITE, slug=slug, url=public_url(slug), root=root,
            email=EMAIL, demo=DEMO, portfolio=PORTFOLIO, project_os=PROJECT_OS,
            title=p["title"], desc=p["desc"], ogtitle=p["ogtitle"], ogtype=p["ogtype"],
            backhref=p["backhref"], backtext=p["backtext"],
            eyebrow=p["eyebrow"], h1=p["h1"], lead=p["lead"],
            herocta=p["herocta"], jsonld=jsonld, body=p["body"],
            extracss=p.get("extracss", "").format(root=root),
            robots=p.get("robots", "index, follow, max-image-preview:large"),
        )
        os.makedirs(os.path.dirname(slug) or ".", exist_ok=True)
        with open(slug, "w") as f:
            f.write(html)
        print(f"  wrote {slug}  ({len(html):,} bytes)")
    write_sitemap()


def write_sitemap():
    """sitemap.xml = the homepage + every page above that isn't noindex."""
    urls = [("", "1.0")]
    for slug, p in PAGES.items():
        if "noindex" in p.get("robots", ""):
            continue
        prio = "0.9" if slug in ("website-audit.html", "web-design-cardiff.html", "web-design-birmingham.html",
                                 "blog/index.html", "process.html") else "0.7"
        urls.append((public_url(slug), prio))
    rows = "".join(f"""  <url>
    <loc>{SITE}/{u}</loc>
    <lastmod>{UPDATED}</lastmod>
    <priority>{pr}</priority>
  </url>
""" for u, pr in urls)
    with open("sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "</urlset>\n")
    print(f"  wrote sitemap.xml  ({len(urls)} URLs)")


if __name__ == "__main__":
    print("Building inner pages…")
    build()
    print("Done. No build step needed to view them — they are plain HTML.")
