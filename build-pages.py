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
  <link rel="canonical" href="{site}/{slug}">
  <meta name="author" content="Sarah J Hill">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#0a0a0c">

  <meta property="og:type" content="{ogtype}">
  <meta property="og:url" content="{site}/{slug}">
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

  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <meta name="apple-mobile-web-app-title" content="Sarah J Hill">

  <!-- ============ STYLES ============ -->
  <link rel="stylesheet" href="assets/css/01-tokens.css">
  <link rel="stylesheet" href="assets/css/02-layout.css">
  <link rel="stylesheet" href="assets/css/03-components.css">
  <link rel="stylesheet" href="assets/css/06-globe.css">
  <link rel="stylesheet" href="assets/css/04-motion.css">

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
    <a class="brand" href="index.html"><img class="brand-mark" src="assets/img/logo-mark-160.png" alt="" width="38" height="38"><b>Sarah J <span>Hill</span><em>Dragon Fire Design</em></b></a>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navlinks">
      <span></span><span></span><span></span>
    </button>
    <div class="navlinks" id="navlinks">
      <a href="index.html#you">Who it's for</a>
      <a href="index.html#test">The 3-second test</a>
      <a href="index.html#about">About me</a>
      <a href="project-os.html">Dragon Fire Process</a>
      <a href="{portfolio}">Portfolio</a>
      <a class="navcta" href="{project_os}forms/intake.html" target="_blank" rel="noopener">Brief me</a>
    </div>
  </div>
</nav>

<header class="page-hero" id="top">
  <div class="wrap">
    <a class="backlink" href="{backhref}">&larr; {backtext}</a>
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
      <a class="btn btn-primary" href="{project_os}forms/intake.html" target="_blank" rel="noopener">Brief me &rarr;</a>
      <a class="btn btn-ghost" href="{demo}" target="_blank" rel="noopener">See the process &rarr;</a>
    </div>
   </div>
   </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <span>&copy; <span id="yr">2026</span> Sarah J Hill &middot; Dragon Fire Design &middot; Built by hand, yours to own.</span>
    <span>Cardiff &amp; Birmingham &middot; <a href="mailto:{email}">{email}</a></span>
    <span class="footnote">Web design for electricians, plumbers, joiners, plasterers, mechanics and
      small businesses &mdash; Cardiff, South Wales, Birmingham and remote across the UK.</span>
  </div>
</footer>

<script src="assets/js/main.js" defer></script>
<script src="assets/js/globe.js" defer></script>
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
    title="The Doubt Audit — how many customers doubt you? | Sarah J Hill",
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

# ------------------------------------------------------------- sjh process
PAGES["project-os.html"] = dict(
    title="The Dragon Fire Process — client portal and studio licence | Sarah J Hill",
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

# --------------------------------------------------------------- CCM
PAGES["cardiff-community-meals.html"] = dict(
    title="Cardiff Community Meals — case study | Sarah J Hill",
    desc=("Neighbours fund a meal, a Cardiff kitchen cooks it, and someone who needs it eats it "
          "— every step tracked to the penny. A community platform built by hand."),
    ogtitle="Cardiff Community Meals — a cwtch, delivered with dinner",
    ogtype="article",
    backhref="index.html#work", backtext="Back to the work",
    eyebrow="Community platform &mdash; working prototype",
    h1="A cwtch, <span class=\"hit\">delivered with dinner</span>.",
    lead=("Neighbours fund a meal. A local kitchen cooks it. Someone who needs it eats it, and every "
          "step is tracked to the door."),
    herocta="""    <div class="cta-row">
      <a class="btn btn-primary" href="https://sarahjhill.com" target="_blank" rel="noopener">See the live prototype &rarr;</a>
    </div>
    <div class="chips">
      <span class="chip">Caerdydd &middot; Cardiff</span>
      <span class="chip">Built and running</span>
      <span class="chip">Not-for-profit</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "Cardiff Community Meals",
    "creator": { "@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/" },
    "about": "A not-for-profit platform connecting Cardiff kitchens with neighbours who need a hot meal.",
    "inLanguage": ["en-GB", "cy"]
  }""",
    body=(
        """<!-- ============ WHERE IT STANDS ============ -->
<section class="band">
  <div class="wrap">
    <p class="eyebrow stand">Where it stands today</p>
    <h2 class="stand">Built, running, and honest about what it isn't yet.</h2>
    <p class="lead stand">Requests, donations, business applications, delivery tracking and the public
      impact record all work end to end. Payments are simulated and the kitchens listed are demonstration
      profiles &mdash; everything else is real working software waiting for real people behind it.</p>
    <div class="steps">
"""
        + step("01", "Anyone can ask, or ask on someone's behalf",
               "For themselves, or for a neighbour, relative or patient. A referral can come from a nurse "
               "as easily as from next door.")
        + step("02", "Every request is checked first",
               "Nothing appears publicly until it has been verified, and nobody is ever named without "
               "consenting to it.")
        + step("03", "Donors choose the meal and the kitchen",
               "Browse open requests, decide how many meals to fund, and pick which Cardiff kitchen cooks them.")
        + step("04", "Kitchens apply with their hygiene rating",
               "FSA rating and delivery capability on record. Bronze, Silver and Gold badges recognise the "
               "ones who do most.")
        + step("05", "Every meal is tracked to the door",
               "Confirmed delivery, counted in a public record that is the sum of real deliveries rather "
               "than a marketing number.")
        + """    </div>
  </div>
</section>

<!-- ============ WHY THIS SHAPE ============ -->
<section class="band alt">
  <div class="wrap">
    <p class="eyebrow stand">Why it works this way</p>
    <h2 class="stand">There are food banks, and they do essential work. This is a different shape on purpose.</h2>
    <div class="rows">
"""
        + row("The money stays in Cardiff",
              "Every meal funded is paid to a Cardiff kitchen &mdash; not a national chain, not a distribution "
              "centre in another county. The same pound feeds someone and keeps a local job.",
              "Which means", "The city gets two things back for every one it puts in.")
        + row("Dignity is designed in",
              "Nobody is named without consenting. Requests are verified before they go public. A referral can "
              "come from a neighbour or a nurse rather than requiring somebody to ask for themselves.",
              "Which means", "People who would never join a queue can still be fed.")
        + row("It is a proper meal",
              "Cooked food, delivered hot, from a kitchen with an FSA rating on record. Not a tin and a packet "
              "of pasta to take home to a flat with the electricity off.",
              "Which means", "It reaches people a parcel cannot help.")
        + row("Every meal is accounted for",
              "Donors see their meal tracked through to confirmed delivery, and the public totals are the sum "
              "of real deliveries.",
              "Which means", "Trust that does not rely on taking anyone's word for it.")
        + """    </div>
  </div>
</section>

<!-- ============ ASK ============ -->
<section class="dark">
  <div class="wrap">
    <p class="eyebrow stand">What it needs now</p>
    <h2 class="stand">Kitchens, referrers and a partner organisation.</h2>
    <p class="lead stand">The software is finished. What it needs is Cardiff kitchens willing to cook,
      people in a position to refer, and an organisation to stand behind it so the payments can be real.
      If that is you, or you know who it should be, I would like to hear from you.</p>
    <div class="cta-row stand" style="margin-top:30px;">
      <a class="btn btn-primary" href="#hello">Talk to me about it &rarr;</a>
    </div>
  </div>
</section>
"""
    ),
)

# ------------------------------------------------------------ emails/media
PAGES["emails-media.html"] = dict(
    title="Emails, posters and campaign media | Sarah J Hill, Cardiff",
    desc=("Campaign emails that survive Outlook, posters readable from three metres, and flyers "
          "and promo video for community organisations. One organisation, one look."),
    ogtitle="Emails, posters and media that look like one organisation",
    ogtype="article",
    backhref="index.html#work", backtext="Back to the work",
    eyebrow="Design work",
    h1="A website is <span class=\"hit\">rarely the whole job</span>.",
    lead=("The email that announces it, the poster for the shop window, the flyer for the school gate "
          "and the short video for social &mdash; all looking like the same organisation."),
    herocta="""    <div class="cta-row">
      <a class="btn btn-primary" href="#hello">Talk to me about a campaign &rarr;</a>
    </div>
    <div class="chips">
      <span class="chip">Design, print &amp; video</span>
      <span class="chip">Community &amp; education</span>
      <span class="chip">Files you can reuse</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Campaign design — email, print and video",
    "provider": { "@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/" },
    "areaServed": { "@type": "Country", "name": "United Kingdom" },
    "description": "Campaign emails, posters, flyers and promo video for community organisations, schools and small charities."
  }""",
    body=(
        """<!-- ============ THE BRIEF ============ -->
<section class="band">
  <div class="wrap">
    <p class="eyebrow stand">The brief</p>
    <h2 class="stand">Nobody here has a marketing department.</h2>
    <p class="lead stand">A community group launching something needs the email, the poster, the flyer
      and the video &mdash; and all of it needs to look like the same organisation. Nobody is briefing an
      agency. Somebody is doing this in the evening after everything else, and what they need is for it
      to be handled properly and to arrive on time.</p>
  </div>
</section>

<!-- ============ APPROACH ============ -->
<section class="band alt">
  <div class="wrap">
    <p class="eyebrow stand">The approach</p>
    <h2 class="stand">Start with where it will actually be seen.</h2>
    <p class="lead stand">A poster is read from three metres away by somebody walking past. An email is
      read on a phone, one-handed, in about four seconds. Those are different design problems, and
      pretending otherwise is how you end up with a poster nobody can read and an email everybody deletes.</p>
    <div class="rows">
"""
        + row("Emails built to survive Outlook",
              "Hand-coded HTML that holds together in Outlook, Gmail and on a phone &mdash; Outlook still "
              "breaks layouts that other tools take for granted.",
              "Which means", "It lands looking like you meant it to.")
        + row("One message per piece",
              "Nobody should have to work out what they are being asked to do. One thing, said once, with "
              "the next step obvious.",
              "Which means", "People act instead of squinting.")
        + row("Print and screen kept consistent",
              "The poster in the window and the email in the inbox read as one campaign rather than two "
              "unrelated efforts.",
              "Which means", "You look like an organisation, not a hobby.")
        + row("Files handed over in a form you can reuse",
              "You get the working files, in formats you can open, so the next flyer does not require "
              "coming back to me.",
              "You get", "Independence, not a subscription.")
        + """    </div>
  </div>
</section>

<!-- ============ WHAT IT COVERS ============ -->
<section class="dark">
  <div class="wrap">
    <p class="eyebrow stand">What this covers</p>
    <h2 class="stand">Four things that have to look like they came from the same place.</h2>
    <div class="rows">
"""
        + row("Campaign emails",
              "Hand-coded HTML that holds together in Outlook, Gmail and on a phone.",
              "Built for", "Inboxes, not previews.")
        + row("Posters and flyers",
              "Readable from three metres for a poster, readable in a hand for a flyer, print-ready either way.",
              "Built for", "Shop windows and school gates.")
        + row("Social graphics",
              "Sized properly for each place they go, so nothing important gets cropped off.",
              "Built for", "Feeds that scroll fast.")
        + row("Short promo video",
              "Enough to announce a thing and make somebody want to turn up.",
              "Built for", "Thirty seconds of attention.")
        + """    </div>
  </div>
</section>
"""
    ),
)

# --------------------------------------------------------- muslim bookers
PAGES["portfolio-project.html"] = dict(
    title="Muslim Bookers — halal travel booking | Sarah J Hill",
    desc=("Halal hotels and holidays in one place, with real reviews and honest prices, so nobody "
          "has to open six tabs to check whether somewhere is suitable."),
    ogtitle="Muslim Bookers — halal travel without six tabs open",
    ogtype="article",
    backhref="index.html#work", backtext="Back to the work",
    eyebrow="Travel booking",
    h1="Nobody should need <span class=\"hit\">six tabs</span> to book a holiday.",
    lead=("Halal hotels and holidays in one place, with real reviews and honest prices, so people stop "
          "giving up and booking something they settle for."),
    herocta="""    <div class="cta-row">
      <a class="btn btn-primary" href="#hello">Talk to me about a build &rarr;</a>
    </div>
    <div class="chips">
      <span class="chip">Web design &amp; build</span>
      <span class="chip">Responsive</span>
      <span class="chip">Booking &amp; reviews</span>
    </div>""",
    jsonld="""  {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "Muslim Bookers",
    "creator": { "@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/" },
    "about": "A halal travel booking site built around trust, reviews and honest pricing."
  }""",
    body=(
        """<!-- ============ THE BRIEF ============ -->
<section class="band">
  <div class="wrap">
    <p class="eyebrow stand">The brief</p>
    <h2 class="stand">A booking site lives or dies on whether you believe it.</h2>
    <p class="lead stand">Booking a halal-friendly holiday usually means six tabs open. One for the hotel,
      another to check whether it really is halal, a third for reviews you half trust, and a fourth to work
      out whether the price is any good. It is tiring, and it is why people give up and settle.</p>
    <p class="lead stand" style="margin-top:16px;">So the interesting problem was not the booking flow.
      It was trust &mdash; which meant reviews and recommendations had to sit beside the price rather than
      three clicks in, and the price had to be something you could sanity-check without leaving the page.</p>
  </div>
</section>

<!-- ============ APPROACH ============ -->
<section class="band alt">
  <div class="wrap">
    <p class="eyebrow stand">The approach</p>
    <h2 class="stand">Designed around how people browse, not how a database is organised.</h2>
    <div class="rows">
"""
        + row("The decision leads, the reassurance follows",
              "Where, when, how much &mdash; then the proof, right next to it. Somebody looking for a family "
              "holiday and somebody looking for a quiet week away want different things from the same page.",
              "Which means", "Fewer people bounce out to check elsewhere.")
        + row("Reviews sit beside the price",
              "Not buried three clicks in. If trust is the thing being sold, it belongs where the money "
              "decision is being made.",
              "Which means", "The doubt is answered at the moment it appears.")
        + row("Built from the phone up",
              "Most holiday browsing happens on a sofa, on a phone, half-watching something else.",
              "Which means", "It works where people actually are.")
        + row("Comparison made obvious",
              "Enough context on the page to feel confident without opening five more.",
              "Which means", "Nobody needs six tabs to feel safe.")
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
    title="Ember — a marketplace theme for Shopify &amp; WooCommerce | Sarah J Hill",
    desc=("Ember is a soft, British marketplace theme for Shopify and WooCommerce. Category bubbles, "
          "lightning deals, shop-by-budget and a mobile app bar. Edit everything visually. £59."),
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
def build():
    for slug, p in PAGES.items():
        html = SHELL.format(
            site=SITE, slug=slug, email=EMAIL, demo=DEMO, portfolio=PORTFOLIO, project_os=PROJECT_OS,
            title=p["title"], desc=p["desc"], ogtitle=p["ogtitle"], ogtype=p["ogtype"],
            backhref=p["backhref"], backtext=p["backtext"],
            eyebrow=p["eyebrow"], h1=p["h1"], lead=p["lead"],
            herocta=p["herocta"], jsonld=p["jsonld"], body=p["body"],
            robots=p.get("robots", "index, follow, max-image-preview:large"),
        )
        with open(slug, "w") as f:
            f.write(html)
        print(f"  wrote {slug}  ({len(html):,} bytes)")


if __name__ == "__main__":
    print("Building inner pages…")
    build()
    print("Done. No build step needed to view them — they are plain HTML.")
