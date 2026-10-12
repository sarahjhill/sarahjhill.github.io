"""
The blog and the Cardiff / Birmingham pages.

build-pages.py imports this file, so after editing anything here run:

    python3 build-pages.py

HOW TO ADD A BLOG POST
  1. Copy one of the post(...) blocks under "BLOG POSTS" below.
  2. Change the slug (the web address), title, description, date and body.
  3. Add it to POSTS at the bottom of that section, newest first.
  4. Run python3 build-pages.py. The blog index and sitemap update themselves.

Writing tips (these are what Google and AI tools reward):
  - Make the H2s the questions people actually type or ask.
  - Answer straight away in the first 1–3 sentences under each heading.
  - Real numbers, real names, real places. Link your sources.
"""
import html as _html
import json
import re

FREE_CHECK_URL = "https://dragonfire-seo-2d0179b090d6.herokuapp.com/free-check/"  # build-pages.py sets this
BLOG_CSS = '  <link rel="stylesheet" href="{root}assets/css/12-blog.css?v=20261013a">\n'
AUTHOR = {"@type": "Person", "name": "Sarah J Hill", "url": "https://sarahjhill.com/",
          "sameAs": ["https://github.com/sarahjhill",
                     "https://www.linkedin.com/in/sarah-hill-software-developer/"]}


def _plain(s):
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _words(body):
    return len(re.findall(r"\w+", _plain(body)))


def faq_html(items):
    out = '    <div class="faq">\n'
    for q, a in items:
        out += f"      <details><summary>{q}</summary><p>{a}</p></details>\n"
    return out + "    </div>\n"


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _plain(q), "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
        for q, a in items]}


def add_pages(PAGES, SITE, EMAIL, PROJECT_OS):
    intake = f"{PROJECT_OS}forms/intake.html"

    # ================================================================ #
    # LOCATION PAGES
    # ================================================================ #
    cardiff_faq = [
        ("How much does a website cost in Cardiff?",
         "Anywhere from about £300 for a simple one-pager to £4,500+ for a site with bookings, payments "
         "and custom tools. Whatever you pick, you get a fixed quote before anything starts, and no monthly rent."),
        ("Do you build bilingual Welsh and English websites?",
         "Yes. Cardiff Community Meals is Cymraeg first, with English one tap away, because it&rsquo;s Cardiff&rsquo;s. "
         "If your community speaks Welsh, your website should too."),
        ("Do you work with charities and community groups?",
         "Yes, and gladly. Charity and community work is the first world on my homepage for a reason. "
         "I&rsquo;ll be straight about what your budget can do, and what it can&rsquo;t."),
        ("How long does a website take?",
         "It depends on the brief. Within two days of your enquiry you get a plan with real dates, "
         "and you can watch the build happen live in your own client page."),
        ("I&rsquo;m not techy. Is that a problem?",
         "None at all. Plain English, one small step at a time, and only when it&rsquo;s your turn."),
    ]
    PAGES["web-design-cardiff.html"] = dict(
        title="Web design Cardiff for women in business | Sarah J Hill",
        desc=("Websites for women in business, charities and community groups in Cardiff and the Valleys. "
              "Bilingual when it matters. Fixed price, yours to own."),
        ogtitle="Web design in Cardiff — for women who won&rsquo;t be written off",
        crumb="Web design Cardiff",
        ogtype="website",
        backhref="index.html", backtext="Back to the start",
        eyebrow="Web design &middot; Cardiff &amp; the Valleys",
        h1="Web design in Cardiff, for women who <span class=\"hit\">won&rsquo;t be written off.</span>",
        lead=("Founders, charities, community groups and tradeswomen across Cardiff. A fixed-price website "
              "that does the believing for you, built by a woman who knows exactly what being underestimated feels like."),
        herocta=f"""    <div class="cta-row">
      <a class="btn btn-primary" href="{intake}" target="_blank" rel="noopener">Start a project enquiry &rarr;</a>
      <a class="btn btn-ghost" href="website-audit.html">Take the Doubt Test</a>
    </div>""",
        extracss=BLOG_CSS,
        jsonld=json.dumps({"@context": "https://schema.org", "@graph": [
            {"@type": "Service", "name": "Web design in Cardiff", "serviceType": "Web design",
             "provider": {"@type": "ProfessionalService", "name": "Sarah J Hill", "url": f"{SITE}/"},
             "areaServed": {"@type": "City", "name": "Cardiff",
                            "containedInPlace": {"@type": "AdministrativeArea", "name": "Wales"}},
             "audience": {"@type": "Audience", "audienceType": "Women in business, charities and community groups"},
             "offers": {"@type": "AggregateOffer", "lowPrice": "300", "highPrice": "4500", "priceCurrency": "GBP"}},
            faq_ld(cardiff_faq)]}),
        body=f"""<section class="read">
  <div class="wrap">
    <div class="post">
      <p class="answer">I build websites for <b>women in business, charities and community groups in Cardiff</b>:
        fixed price, yours to own, and built so the right people trust you in the first three seconds.</p>

      <h2>Who is this for?</h2>
      <p>You, if any of this sounds familiar:</p>
      <ul>
        <li><strong>You&rsquo;ve started something</strong> and your website still looks like a placeholder.</li>
        <li><strong>You run a charity, CIC or community group</strong> and need people to donate, volunteer or turn up.</li>
        <li><strong>You&rsquo;re a tradeswoman</strong> and you&rsquo;re tired of being asked when &ldquo;the man&rdquo; is coming.</li>
        <li><strong>You&rsquo;ve got that something</strong> &mdash; a voice, a cause, a way of doing things &mdash; and a template flattens it.</li>
      </ul>

      <h2>What makes a Cardiff website different?</h2>
      <p>Cardiff is a city that looks after its own. People here buy from people they trust, and they
        notice when you&rsquo;ve bothered. So:</p>
      <ul>
        <li><strong>Bilingual when it matters.</strong> Cymraeg first or English first, your call, done properly.</li>
        <li><strong>Local proof up front.</strong> Where you work, who you&rsquo;ve helped, real photos of you.</li>
        <li><strong>Found on the map.</strong> Set up for Google so people nearby can find you when they search.</li>
      </ul>

      <h2>Can I see work you&rsquo;ve done in Cardiff?</h2>
      <p><b>Cardiff Community Meals</b>: neighbours fund a meal,
        a local kitchen cooks it, and someone having a hard time gets fed without being made to feel like a
        charity case. Bilingual, fast on a cheap phone, and every penny tracked.
        <a href="https://sarahjhill.com/cardiff-community-meals/" target="_blank" rel="noopener">See the live site</a>.</p>

      <div class="callout">
        <strong>Already got a website?</strong> I&rsquo;ll go through it the way your customers do &mdash; on a phone,
        in a hurry &mdash; and tell you what&rsquo;s working and what isn&rsquo;t. Free, two working days.<br>
        <a class="btn btn-primary" href="website-audit.html">Take the Doubt Test &rarr;</a>
      </div>

      <h2>Questions people in Cardiff ask</h2>
{faq_html(cardiff_faq)}
    </div>
  </div>
</section>
""",
    )

    brum_faq = [
        ("Do you work with businesses in Birmingham?",
         "Yes, Birmingham and across the West Midlands. Most of the work happens on screen anyway: you get your "
         "own client page where you can watch your site being built, so you&rsquo;re never chasing me for an update."),
        ("How much does a website cost in Birmingham?",
         "From about £300 for a simple one-pager to £4,500+ for bookings, payments and custom tools. "
         "It&rsquo;s a fixed quote agreed before anything starts, with no monthly rent."),
        ("Do you work with charities and community groups?",
         "Yes. Charity and community websites are a big part of what I do, with honest advice about what your budget will stretch to."),
        ("What if I already have a website?",
         "Start with the Doubt Test. I&rsquo;ll tell you what&rsquo;s worth keeping, and if your site is fine "
         "I&rsquo;ll say so."),
    ]
    PAGES["web-design-birmingham.html"] = dict(
        title="Web design Birmingham for women in business | Sarah J Hill",
        desc=("Websites for women in business, female founders, charities and community groups in Birmingham "
              "and the West Midlands. Fixed price, yours to own."),
        ogtitle="Web design in Birmingham &amp; the West Midlands",
        crumb="Web design Birmingham",
        ogtype="website",
        backhref="index.html", backtext="Back to the start",
        eyebrow="Web design &middot; Birmingham &amp; the West Midlands, UK",
        h1="Web design in Birmingham for women <span class=\"hit\">with something to say.</span>",
        lead=("Founders, side-hustlers, charities and community groups across Birmingham and the West Midlands. "
              "A website with your personality in it, at a fixed price, that you own outright."),
        herocta=f"""    <div class="cta-row">
      <a class="btn btn-primary" href="{intake}" target="_blank" rel="noopener">Start a project enquiry &rarr;</a>
      <a class="btn btn-ghost" href="website-audit.html">Take the Doubt Test</a>
    </div>""",
        extracss=BLOG_CSS,
        jsonld=json.dumps({"@context": "https://schema.org", "@graph": [
            {"@type": "Service", "name": "Web design in Birmingham", "serviceType": "Web design",
             "provider": {"@type": "ProfessionalService", "name": "Sarah J Hill", "url": f"{SITE}/"},
             "areaServed": {"@type": "City", "name": "Birmingham",
                            "containedInPlace": {"@type": "AdministrativeArea", "name": "West Midlands, England"}},
             "audience": {"@type": "Audience", "audienceType": "Women in business, charities and community groups"},
             "offers": {"@type": "AggregateOffer", "lowPrice": "300", "highPrice": "4500", "priceCurrency": "GBP"}},
            faq_ld(brum_faq)]}),
        body=f"""<section class="read">
  <div class="wrap">
    <div class="post">
      <p class="answer">I build websites for <b>women in business, charities and community groups in Birmingham
        and the West Midlands</b>: fixed price, yours to own, and built so nobody writes you off before you&rsquo;ve said a word.</p>

      <h2>Who is this for?</h2>
      <ul>
        <li><strong>Female founders</strong> whose website is the last thing still looking &ldquo;temporary&rdquo;.</li>
        <li><strong>Charities and community groups</strong> who need donors, volunteers and bums on seats.</li>
        <li><strong>Women in the trades</strong> who want to be booked for their skill, not questioned about it.</li>
        <li><strong>Anyone with that je ne sais quoi</strong> who refuses to look like everyone else.</li>
      </ul>

      <h2>How does it work if we&rsquo;re not in the same room?</h2>
      <p>Really well, honestly. Within two days of your enquiry you get a plan with real dates. Then you
        get your own <a href="project-os.html">client page</a>: upload your logo and photos, see what&rsquo;s done
        and what&rsquo;s next, and never have to type &ldquo;any update?&rdquo;.</p>

      <h2>What will my website actually do for me?</h2>
      <ul>
        <li><strong>Say what you do in the first line</strong>, in the words your customers use.</li>
        <li><strong>Put your proof where the doubt is</strong>: reviews, results, real photos.</li>
        <li><strong>Get found in Birmingham searches</strong>, on Google and in AI answers.</li>
        <li><strong>Work beautifully on a phone</strong>, because that&rsquo;s where people find you.</li>
      </ul>

      <div class="callout">
        <strong>Not sure where to start?</strong> Send me your current site, or your Instagram if that&rsquo;s all you&rsquo;ve
        got, and I&rsquo;ll tell you honestly what I&rsquo;d do first.<br>
        <a class="btn btn-primary" href="website-audit.html">Take the Doubt Test &rarr;</a>
      </div>

      <h2>Questions people in Birmingham ask</h2>
{faq_html(brum_faq)}
    </div>
  </div>
</section>
""",
    )

    # ================================================================ #
    # BLOG POSTS
    # ================================================================ #
    def post(slug, title, desc, h1, lead, tag, date, body, sources):
        words = _words(body)
        mins = max(2, round(words / 220))
        src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in sources)
        srcblock = f'<div class="sources"><strong>Sources</strong><ol>{src}</ol></div>' if sources else ""
        from urllib.parse import quote as _q
        _u = _q(f"{SITE}/blog/{slug}.html", safe=""); _t = _q(_plain(h1), safe="")
        share = f"""      <div class="share" aria-label="Share this post">
        <p class="share-h">Found this useful? Pass it on.</p>
        <div class="share-row">
          <button type="button" class="share-native" hidden>Share&hellip;</button>
          <a href="https://wa.me/?text={_t}%20{_u}" target="_blank" rel="noopener">WhatsApp</a>
          <a href="https://www.facebook.com/sharer/sharer.php?u={_u}" target="_blank" rel="noopener">Facebook</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={_u}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://twitter.com/intent/tweet?url={_u}&amp;text={_t}" target="_blank" rel="noopener">X</a>
          <a href="mailto:?subject={_t}&amp;body={_u}">Email</a>
          <button type="button" class="share-copy" data-url="{SITE}/blog/{slug}.html">Copy link</button>
        </div>
      </div>
      <script>
      (function(){{
        var c=document.querySelector('.share-copy'), n=document.querySelector('.share-native');
        if(c) c.addEventListener('click',function(){{
          var u=c.getAttribute('data-url');
          (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{c.textContent='Link copied';}})
            .catch(function(){{window.prompt('Copy this link:',u);}});
        }});
        if(n && navigator.share){{ n.hidden=false; n.addEventListener('click',function(){{
          navigator.share({{title:document.title,url:c.getAttribute('data-url')}}).catch(function(){{}});
        }}); }}
      }})();
      </script>
"""
        PAGES[f"blog/{slug}.html"] = dict(
            title=title, desc=desc, ogtitle=_plain(h1), crumb=tag, ogtype="article",
            backhref="blog/", backtext="All posts",
            eyebrow=f"Blog &middot; {tag}", h1=h1, lead=lead,
            herocta=f'    <p class="post-meta"><span>By <b>Sarah J Hill</b></span><span><time datetime="{date}">'
                    f'{_date(date)}</time></span><span>{mins} min read</span></p>',
            extracss=BLOG_CSS, updated=date,
            ogimage=f"{SITE}/assets/img/blog/{slug}.jpg", ogalt=_plain(h1).replace('"', "&quot;"),
            jsonld=json.dumps({"@context": "https://schema.org", "@type": "BlogPosting",
                               "headline": _plain(h1), "description": _plain(desc),
                               "datePublished": date, "dateModified": date,
                               "author": AUTHOR, "publisher": {"@type": "Organization", "name": "Sarah J Hill",
                                                               "logo": f"{SITE}/assets/img/logo-mark-512.png"},
                               "mainEntityOfPage": f"{SITE}/blog/{slug}.html",
                               "image": f"{SITE}/assets/img/blog/{slug}.jpg", "articleSection": _plain(tag), "wordCount": words,
                               "inLanguage": "en-GB"}),
            body=f"""<section class="read">
  <div class="wrap">
    <article class="post">
{body}
{share}      <div class="callout">
        <strong>Does your website make people doubt you?</strong> Get your free score out of 100. I&rsquo;ll check it the
        way a doubtful customer would and tell you straight. Free, no catch.<br>
        <a class="btn btn-primary" href="{FREE_CHECK_URL}">Take the Doubt Test &rarr;</a>
      </div>
      {srcblock}
    </article>
      <aside class="fs-box" id="fs-box" hidden aria-labelledby="fs-box-h">
        <button type="button" class="fs-x" aria-label="Close">&times;</button>
        <h2 id="fs-box-h">Does your website make people doubt you?</h2>
        <p>Take the Doubt Test. Free score out of 100 in 30 seconds, plus the three things to fix first.</p>
        <a class="btn btn-primary" href="{FREE_CHECK_URL}">Take the Doubt Test &rarr;</a>
      </aside>
      <script>
      (function(){{
        var box=document.getElementById('fs-box'), art=document.querySelector('article.post');
        if(!box||!art) return;
        var KEY='fsBoxHidden', DAYS=14;
        try{{ var t=+localStorage.getItem(KEY); if(t && Date.now()-t < DAYS*864e5) return; }}catch(e){{}}
        var shown=false;
        function close(){{ box.classList.remove('is-in'); setTimeout(function(){{box.hidden=true;}},350);
          try{{ localStorage.setItem(KEY, String(Date.now())); }}catch(e){{}}
          window.removeEventListener('scroll', check); }}
        function check(){{
          if(shown) return;
          var r=art.getBoundingClientRect(), read=(window.innerHeight - r.top)/r.height;
          if(read > .5){{ shown=true; box.hidden=false; requestAnimationFrame(function(){{box.classList.add('is-in');}}); }}
        }}
        box.querySelector('.fs-x').addEventListener('click', close);
        box.querySelector('.btn').addEventListener('click', function(){{ try{{ localStorage.setItem(KEY, String(Date.now())); }}catch(e){{}} }});
        document.addEventListener('keydown', function(e){{ if(e.key==='Escape' && shown && !box.hidden) close(); }});
        window.addEventListener('scroll', check, {{passive:true}});
      }})();
      </script>
  </div>
</section>
""",
            _card=dict(slug=slug, tag=tag, date=date, mins=mins, h1=_plain(h1), desc=desc),
        )

    # ---------------------------------------------------------------- 1
    post(
        slug="tradeswoman-in-midlife",
        title="Tradeswoman in midlife: is it too late? | Sarah J Hill",
        desc=("Retraining as an electrician, plumber or gas engineer at 40 or 50? Real stories, the real numbers, "
              "and how to get started without being written off."),
        h1="Becoming a tradeswoman in midlife: <span class=\"hit\">is it too late?</span>",
        lead="Short answer: no. Longer answer: you might be better placed than the 18-year-olds.",
        tag="Women in business",
        date="2026-10-11",
        sources=[
            ("Stylist — 8 women on the realities of working in skilled trades",
             "https://www.stylist.co.uk/life/careers/women-working-in-skilled-trades/1099379"),
            ("Electrical Times — shortfall of over 29,000 female electricians in the UK (metals4U research, March 2024)",
             "https://www.electricaltimes.co.uk/?p=25344"),
            ("Wikipedia — Hattie Hasan, founder of Stopcocks Women Plumbers",
             "https://en.wikipedia.org/wiki/Hattie_Hasan"),
        ],
        body="""      <!-- TODO Sarah: add the Daily Mail story here — one line + link, e.g.
           <p>This week the Daily Mail ran <a href="LINK">a story about ...</a>.</p> -->
      <p class="answer">It isn&rsquo;t too late. Women regularly retrain as <b>electricians, plumbers and gas engineers
        in their late thirties, forties and beyond</b>, and the trades badly need them: women are fewer
        than 1 in 50 UK electricians.</p>

      <h2>Do women really switch to a trade later in life?</h2>
      <p>All the time. They just don&rsquo;t get much airtime.</p>
      <ul>
        <li><strong>Karen Matthews</strong> spent 20 years in advertising, then started a plumbing course at 36. She&rsquo;s now a heating engineer and plumber.</li>
        <li><strong>Amy Lister</strong> managed a Co-op store for 14 years before qualifying as an electrician at 36.</li>
        <li><strong>Olha Kulyk</strong> was a training manager at Costa Coffee until she was made redundant. She retrained as an electrician.</li>
        <li><strong>Hattie Hasan</strong> taught in inner-city schools for eight years, became a plumber, and went on to found Stopcocks Women Plumbers. She now has an MBE.</li>
      </ul>
      <blockquote>&ldquo;You are never too old to learn.&rdquo;<cite>Olha Kulyk, electrician, speaking to Stylist</cite></blockquote>

      <h2>How few women are in the trades?</h2>
      <p>Very few, which is exactly the opportunity.</p>
      <div class="facts">
        <div class="fact"><div class="v">1.7%</div><div class="k">of UK electricians are women (around 3,574)</div></div>
        <div class="fact"><div class="v">2%</div><div class="k">of plumbers are women</div></div>
        <div class="fact"><div class="v">1.1%</div><div class="k">of carpenters and joiners are women</div></div>
        <div class="fact"><div class="v">29,448</div><div class="k">&ldquo;missing&rdquo; female electricians, by one estimate</div></div>
      </div>
      <p>Those figures come from research by metals4U, reported by Electrical Times in 2024. However you count it,
        the gap is huge, and plenty of customers would genuinely rather open the door to a woman.</p>

      <h2>What does midlife give you that a teenager doesn&rsquo;t have?</h2>
      <p>More than you think. Running a trade is half skill, half everything else, and you&rsquo;ve probably spent
        twenty years practising the everything else:</p>
      <ul>
        <li><strong>Talking to customers</strong> &mdash; calmly, clearly, without the jargon.</li>
        <li><strong>Managing money</strong>, quotes and the awkward &ldquo;that&rsquo;ll be extra&rdquo; conversation.</li>
        <li><strong>Turning up when you said you would.</strong> Rarer than it should be, and people talk about it.</li>
        <li><strong>Knowing who you are.</strong> Useful when someone asks if your husband&rsquo;s parking the van.</li>
      </ul>

      <h2>What&rsquo;s actually hard about it?</h2>
      <p>Let&rsquo;s not pretend. The women who&rsquo;ve done it are honest about two things.</p>
      <p><strong>It&rsquo;s physical.</strong> Karen Matthews puts it plainly: the work can be demanding, especially as
        you get older. Look after your knees, your back and your tools, in that order.</p>
      <p><strong>Being taken seriously takes a while.</strong> When Olha Kulyk started, she says almost no one took her
        seriously &mdash; &ldquo;neither men nor women&rdquo;. That gets better with every job you finish. It also
        gets better faster when your first impression does some of the convincing for you.</p>

      <h2>How do you get started?</h2>
      <ol>
        <li><strong>Pick the trade, not the course.</strong> Talk to people who do it. Shadow someone for a day if you can.</li>
        <li><strong>Choose training that leads to a recognised qualification and real site experience.</strong>
          Be wary of short &ldquo;fast-track&rdquo; courses that promise everything in a few weeks.</li>
        <li><strong>Look at apprenticeships too.</strong> Adults do them, and you earn while you learn.</li>
        <li><strong>Find your people.</strong> Women-in-trades groups and networks are full of women who&rsquo;ve been exactly where you are.</li>
      </ol>

      <h2>When you go out on your own, how do you look the part online?</h2>
      <p>This is where I come in. When a customer searches for an electrician and finds you, they decide
        in about three seconds. Put these where they&rsquo;ll see them first:</p>
      <ul>
        <li>A <strong>real photo of you</strong>, at work, in your kit.</li>
        <li>Your <strong>qualifications and insurance</strong>, up top, not buried in a footer.</li>
        <li><strong>Reviews</strong> from real customers, with their first name and area.</li>
        <li>A <strong>free Google Business Profile</strong>, so you turn up on the map.</li>
      </ul>
      <p>More on this in <a href="present-yourself-online.html">how to present yourself online so people take you seriously</a>.</p>
""",
    )

    # ---------------------------------------------------------------- 2
    post(
        slug="women-in-business-uk-facts",
        title="Women in business in the UK: the facts (2026) | Sarah J Hill",
        desc=("How many women run businesses in the UK, how much funding they get, how Wales and the West Midlands "
              "compare, and what it means for your website."),
        h1="Women in business in the UK: <span class=\"hit\">the facts.</span>",
        lead="The numbers behind the pep talks, and what they mean if you&rsquo;re the one doing it.",
        tag="Women in business",
        date="2026-10-11",
        sources=[
            ("Prowess — Rose Review progress check (DBT and British Business Bank figures)",
             "https://prowess.org.uk/rose-review-progress-check/"),
            ("Prowess — UK women in business statistics",
             "https://prowess.org.uk/?p=4"),
            ("GOV.UK — Landmark review sparks action to boost number of female entrepreneurs (Rose Review, 2019)",
             "https://www.gov.uk/government/news/landmark-review-sparks-action-to-boost-number-of-female-entrepreneurs"),
            ("Greater Birmingham Chambers of Commerce — Women in Business",
             "https://www.greaterbirminghamchambers.com/support/women-in-business.html"),
        ],
        body="""      <p class="answer">There are now around <b>1.6 million women-led businesses</b> in the UK, up from about
        1.1 million in 2019. But women still make up only about <b>1 in 3</b> UK entrepreneurs, and female-founded
        companies got just <b>5.2%</b> of equity investment in 2024.</p>

      <h2>How many women run businesses in the UK?</h2>
      <p>About 1.6 million, according to Department for Business and Trade figures for 2025. That&rsquo;s roughly
        half a million more than when the government&rsquo;s Rose Review was published in 2019.</p>
      <div class="facts">
        <div class="fact"><div class="v">1.6m</div><div class="k">women-led businesses in the UK (2025)</div></div>
        <div class="fact"><div class="v">1 in 3</div><div class="k">UK entrepreneurs is a woman</div></div>
        <div class="fact"><div class="v">£250bn</div><div class="k">extra value if women started and scaled businesses at the rate men do</div></div>
        <div class="fact"><div class="v">5.2%</div><div class="k">of equity investment went to female-founded companies (2024)</div></div>
      </div>

      <h2>Do women-led businesses get less funding?</h2>
      <p>Yes, by a distance. Female-founded companies received 5.2% of all equity investment in 2024
        (British Business Bank). That&rsquo;s up from 2.3% in 2019, but it&rsquo;s still small change.</p>
      <p>Loans tell the same story. In 2022, the average approved loan for a women-led business was about
        £174,000, against £507,000 for a male-led one (Investing in Women Code). And around a third of women
        say funding is the biggest barrier to starting at all.</p>
      <p><strong>What that means in real life:</strong> most of us are building on our own money, so every pound
        we spend has to work hard, the website included.</p>

      <h2>Is it different in Wales and the West Midlands?</h2>
      <p>A bit. The 2025 Global Entrepreneurship Monitor found that women&rsquo;s early-stage business activity in
        Wales and the North East trailed London by more than three percentage points. Fewer women are starting
        out here, which makes the ones who do more visible, and more worth backing.</p>
      <p>In Birmingham, the <a href="https://www.greaterbirminghamchambers.com/support/women-in-business.html"
        target="_blank" rel="noopener">Greater Birmingham Chambers of Commerce</a> runs a Women in Business network.
        In Wales, Business Wales offers free start-up advice. Use them. That&rsquo;s what they&rsquo;re for.</p>

      <h2>So what does this mean for your website?</h2>
      <p>If you&rsquo;re more likely to be self-funded, more likely to be underestimated, and less likely to have
        a marketing team, your website has to do three jobs at once:</p>
      <ol>
        <li><strong>Be believed in three seconds.</strong> Real photo, clear words, proof up top.</li>
        <li><strong>Be found without an ad budget.</strong> Google, the map pack, and now AI answers.</li>
        <li><strong>Save you time.</strong> Enquiries, bookings and the boring questions, handled while you work.</li>
      </ol>
      <p>None of that needs a big budget. It needs the right things in the right order.
        <a href="present-yourself-online.html">Here are seven to start with</a>.</p>
""",
    )

    # ---------------------------------------------------------------- 3
    post(
        slug="present-yourself-online",
        title="How to present yourself online and be taken seriously",
        desc=("Seven practical fixes for women in business, charities and tradeswomen: what to put at the top of your "
              "site, how to be found on Google, and how to look as good as you are."),
        h1="How to present yourself online so people <span class=\"hit\">take you seriously.</span>",
        lead="Seven fixes. Most cost nothing but an afternoon.",
        tag="Your online presence",
        date="2026-10-11",
        sources=[
            ("Google Business Profile — create or claim your profile",
             "https://www.google.com/business/"),
            ("Google Search Central — creating helpful, reliable, people-first content",
             "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"),
        ],
        body="""      <p class="answer">People decide whether to trust you in about three seconds. To pass that test,
        <b>show your face, say what you do in one line, and put your proof at the top</b>. Then make sure
        Google can find you.</p>

      <h2>1. Should I put my photo on my website?</h2>
      <p>Yes. A real one. People buy from people, and a stock photo of a smiling stranger tells them nothing.
        It doesn&rsquo;t need to be a studio shoot &mdash; a good phone photo of you doing the work, in decent light, beats
        anything from a picture library.</p>

      <h2>2. What should go at the top of my homepage?</h2>
      <p>One line that says what you do, who for, and where. In your customer&rsquo;s words, not yours.</p>
      <ul>
        <li>Not this: <em>&ldquo;Delivering innovative solutions for a changing world.&rdquo;</em></li>
        <li>This: <em>&ldquo;Electrician in Cardiff. Rewires, EV chargers and safety checks.&rdquo;</em></li>
      </ul>

      <h2>3. Where should my reviews and qualifications go?</h2>
      <p>Where the doubt is: near the top. If someone is hunting for a reason to say no, don&rsquo;t make them scroll
        past it to find your reasons for yes. Qualifications, insurance, a couple of short reviews with real first names.</p>

      <h2>4. How do I show up on Google Maps?</h2>
      <p>Claim your free <a href="https://www.google.com/business/" target="_blank" rel="noopener">Google Business Profile</a>.
        It&rsquo;s what puts you in the map results when someone nearby searches for what you do. If you work from home,
        you can hide your address and just show the areas you cover. Then ask your last five happy customers for a review.</p>

      <h2>5. Does my website need to work on a phone?</h2>
      <p>It&rsquo;s the main event. Most people will find you on a phone, often standing up, often in a hurry.
        Open your own site on your phone, on mobile data, and time it. If you&rsquo;re drumming your fingers, so are they.</p>

      <h2>6. How easy is it to contact me?</h2>
      <p>Test it today. Tap your phone number &mdash; does it dial? Send yourself a message through your contact
        form &mdash; does it arrive? A surprising number of forms have quietly been going nowhere for months.</p>

      <h2>7. What should I write about?</h2>
      <p>The questions customers ask you every week. How much does it cost? How long does it take? What happens
        first? Answer them plainly on your site. It saves you time, it builds trust, and it&rsquo;s exactly what Google
        and AI assistants look for when they decide who to recommend.</p>

      <hr>
      <p><strong>Got that something?</strong> Good. Don&rsquo;t sand it off to look like everyone else. The point of all this
        isn&rsquo;t to look corporate. It&rsquo;s to make sure the real you comes across before anyone has the chance to doubt it.</p>
""",
    )

    # ---------------------------------------------------------------- 4
    post(
        slug="website-in-a-day",
        title="Why I won&rsquo;t build you a website in a day | Sarah J Hill",
        desc=("One-day websites look quick and cheap. Here&rsquo;s what you actually get, the mistakes they bake in, "
              "and seven questions to ask before you pay anyone for a website."),
        h1="Why I won&rsquo;t build you a website <span class=\"hit\">in a day.</span>",
        lead="Because a website knocked up in a day says exactly that about your business.",
        tag="Your online presence",
        date="2026-10-12",
        sources=[
            ("W3C — How to meet WCAG (quick reference)", "https://www.w3.org/WAI/WCAG22/quickref/"),
            ("web.dev — Web Vitals: what Google measures about speed and stability", "https://web.dev/articles/vitals"),
            ("GOV.UK — Accessibility requirements for public sector websites and apps",
             "https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps"),
        ],
        body="""      <p class="answer">A website built in a day is a template with your logo dropped in. It skips the bits that actually
        win you customers: knowing who it&rsquo;s for, what they need to hear, and what proves you&rsquo;re worth it.
        That isn&rsquo;t a website. It&rsquo;s a placeholder with a price tag.</p>

      <h2>What do you actually get from a one-day website?</h2>
      <p>Usually a theme someone bought once and sells fifty times, stock photos of people who&rsquo;ve never heard of you,
        and words written in a rush by someone who&rsquo;s known your business for an hour. &ldquo;Welcome to my
        website.&rdquo; &ldquo;Quality service at affordable prices.&rdquo; Sound familiar? It should. It&rsquo;s on
        thousands of other sites.</p>
      <p>None of that is a crime. None of it sells you, either.</p>

      <h2>What does generic design cost women in business?</h2>
      <p>More than it costs anyone else. If you&rsquo;re a woman running a business, you already get second-guessed: by
        suppliers, by customers, by the bloke who asks to &ldquo;speak to the owner&rdquo;. A generic site doesn&rsquo;t
        challenge that doubt. It confirms it. It looks like everyone else, says nothing specific and proves nothing, so
        people fill the gaps with their own assumptions. Those are rarely generous.</p>
      <p>Your website is the one place you control the first impression completely. Wasting it on a template is like
        turning up to a pitch in someone else&rsquo;s clothes.</p>

      <h2>What actually works?</h2>
      <ul>
        <li><strong>Words first, design second.</strong> Decide what the site needs to say before anyone picks a colour.
          Design built around real words looks better and sells harder.</li>
        <li><strong>Say who it&rsquo;s for in the first line.</strong> &ldquo;Electrician in Cardiff for homeowners who want
          it done right&rdquo; beats &ldquo;Welcome&rdquo; every single time.</li>
        <li><strong>Proof near the top.</strong> Reviews with real first names, qualifications, and photos of you and your
          actual work. Not stock.</li>
        <li><strong>One clear next step per page.</strong> Call, book or enquire. Pick one. Three competing buttons is how
          you get none.</li>
        <li><strong>Built for a phone first.</strong> That&rsquo;s where most people meet you, usually in a hurry. If it&rsquo;s
          slow or fiddly there, nothing else matters.</li>
        <li><strong>Accessible by default.</strong> Readable text, proper contrast, works with a keyboard and a screen reader.
          For public sector sites it&rsquo;s the law. For everyone else it&rsquo;s good manners and good business.</li>
      </ul>

      <h2>What are the mistakes I fix most often?</h2>
      <ul>
        <li>Stock photos where the owner should be. People buy from people.</li>
        <li>A lovely homepage, and a contact form that&rsquo;s been emailing nobody for months.</li>
        <li>Huge images that make the site crawl on mobile data.</li>
        <li>A sliding carousel of messages nobody waits around to read.</li>
        <li>No prices, not even a &ldquo;from&rdquo;. So people assume you&rsquo;re too expensive and don&rsquo;t ask.</li>
        <li>Apologetic words: &ldquo;just a small business&rdquo;, &ldquo;we&rsquo;ll try our best&rdquo;. Be proud, or be quiet.</li>
      </ul>

      <h2>What should I ask before I pay anyone for a website?</h2>
      <ol>
        <li>Who writes the words, and when?</li>
        <li>Is it built for my customers, or from a template?</li>
        <li>How fast will it load on a phone, on mobile data?</li>
        <li>Will I own it outright: the site, the domain and the words?</li>
        <li>Can I change it myself without ringing you?</li>
        <li>How will people find it on Google and in AI answers?</li>
        <li>What happens after launch if something breaks?</li>
      </ol>
      <p>If the answers are vague, so is the website.</p>

      <h2>So how long should a website take?</h2>
      <p>Long enough to do it properly. With my Dragon Fire Process you get a plan with real dates within two working days,
        and you watch every task tick off on your own project page. Not quick and nasty. Not slow and mysterious. Properly
        planned, researched and tested. <a href="../process.html">See how I work</a>.</p>

      <hr>
      <p><strong>Be bold. Be brave. Be ballsy.</strong> Your business isn&rsquo;t generic. Your website shouldn&rsquo;t be either.</p>
""",
    )

    # ---------------------------------------------------------------- 5
    post(
        slug="being-doubted",
        title="Your website isn&rsquo;t the problem. Being doubted is. | Sarah J Hill",
        desc=("Women in business get second-guessed before they say a word. How to make your website answer the doubt "
              "first: what to show, what to cut, and the five-second stranger test."),
        h1="Your website isn&rsquo;t the problem. <span class=\"hit\">Being doubted is.</span>",
        lead="Nobody tells you they doubted you. They just don&rsquo;t ring.",
        tag="Women in business",
        date="2026-10-12",
        sources=[],
        body="""      <p class="answer">Most small business websites don&rsquo;t fail because they&rsquo;re ugly. They fail because a stranger
        lands on them already half-doubting, and the site gives them nothing to change their mind. Your job is to answer the
        doubt before it&rsquo;s spoken: who you are, what you do, proof you&rsquo;re good at it, and how to get hold of you.</p>

      <h2>Why are women in business doubted more?</h2>
      <p>You know the moments. The customer who asks when your husband will be back. The supplier who explains your own trade
        to you. The networking do where someone assumes you&rsquo;re the assistant. That doubt doesn&rsquo;t switch off when
        people go online. It just goes quiet: a tab closed, a call never made.</p>
      <p>You can&rsquo;t control what people assume. You can control what they find.</p>

      <h2>What does a doubtful visitor look for first?</h2>
      <p>Four things, fast, usually on a phone:</p>
      <ol>
        <li>Who is this, and is it a real person?</li>
        <li>Do they do the thing I need, where I need it?</li>
        <li>Are they any good? Who says so?</li>
        <li>How do I get hold of them, right now?</li>
      </ol>
      <p>If any of those takes more than a scroll to find, you&rsquo;re relying on their patience. Doubtful people
        don&rsquo;t have much.</p>

      <h2>What actually works?</h2>
      <ul>
        <li><strong>Your face.</strong> A real photo of you, not a stock smile. It&rsquo;s the fastest trust signal there is.</li>
        <li><strong>Specifics, not adjectives.</strong> Your actual qualifications, the number of reviews you have, the
          towns you cover. &ldquo;Professional, friendly, reliable&rdquo; is what everyone types. Facts are what people believe.</li>
        <li><strong>Prices, or at least &ldquo;from&rdquo;.</strong> Hide your prices and people assume the worst, then leave
          without asking.</li>
        <li><strong>Reviews with names, near the top.</strong> Not on a separate page nobody clicks.</li>
        <li><strong>A way to contact you on every screen.</strong> Tap to call, a short form, or both.</li>
      </ul>

      <h2>What should I cut?</h2>
      <ul>
        <li>&ldquo;Welcome to my website.&rdquo; They know. They&rsquo;re on it.</li>
        <li>Apology words: <em>just</em>, <em>only</em>, <em>small</em>, <em>try</em>. You wouldn&rsquo;t say them to a
          customer&rsquo;s face. Don&rsquo;t write them on your homepage.</li>
        <li>Mission statements nobody asked for.</li>
        <li>Anything you&rsquo;d be embarrassed to read out loud across a counter.</li>
      </ul>
      <blockquote>&ldquo;If you wouldn&rsquo;t say it to a customer&rsquo;s face, don&rsquo;t put it on your homepage.&rdquo;
        <cite>My rule for every site I build</cite></blockquote>

      <h2>How do I test my own website?</h2>
      <p>The stranger test. Hand your phone to someone who&rsquo;s never heard of you. Give them five seconds on your
        homepage, take it back, and ask: What do I do? Who is it for? What would you do next? If they can&rsquo;t answer,
        the site isn&rsquo;t doing its job. No offence to the site.</p>

      <h2>Isn&rsquo;t this just about looking professional?</h2>
      <p>No. Professional is the minimum. This is about your worth showing up before you do. You&rsquo;ve done the training,
        the hours and the hard graft. Your website should make that obvious to a stranger in a hurry, so you never have to
        prove it from scratch on the phone again.</p>
      <p>Want a second pair of eyes? My <a href="../website-audit.html">Doubt Test</a> runs your site through exactly
        this, the way a doubtful customer would.</p>

      <hr>
      <p><strong>Be bold. Be brave. Be ballsy.</strong> This is a woman&rsquo;s world too. Make your website act like it.</p>
""",
    )

    # ---------------------------------------------------------------- 6
    post(
        slug="charity-website-mistakes",
        title="Charities: your donate button is in the wrong place | Sarah J Hill",
        desc=("What actually works on small charity and community group websites: where donate goes, how to show impact, "
              "Gift Aid, volunteers, and the mistakes that quietly cost you support."),
        h1="Charities: your donate button is <span class=\"hit\">in the wrong place.</span>",
        lead="And it&rsquo;s probably not the only thing quietly costing you support.",
        tag="Local &amp; community",
        date="2026-10-12",
        sources=[
            ("GOV.UK — Gift Aid: how it works for donors", "https://www.gov.uk/donating-to-charity/gift-aid"),
            ("W3C — Understanding contrast (minimum)", "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html"),
        ],
        body="""      <p class="answer">If someone has to hunt for how to give, they won&rsquo;t. On most small charity websites the donate
        button is tucked in a menu, missing on phones, or fighting five other buttons. Put one clear &ldquo;Donate&rdquo;
        in the top bar of every page, visible on a phone without opening a menu, and tell people exactly what their money does.</p>

      <h2>Where should the donate button go?</h2>
      <ul>
        <li><strong>In the header, on every page,</strong> and still visible on a phone. Not hidden inside the burger menu.</li>
        <li><strong>At the end of every story or update,</strong> when people are most moved to help.</li>
        <li><strong>Straight to a short, simple form.</strong> Every extra page between &ldquo;I want to give&rdquo; and
          &ldquo;done&rdquo; loses people.</li>
      </ul>

      <h2>How do I show what a donation actually does?</h2>
      <p>Turn money into something people can picture. &ldquo;&pound;5 pays for a hot meal&rdquo; (use your real numbers)
        works far harder than &ldquo;support our work&rdquo;. Show the people you help, with their consent. Tell one real
        story at a time, and keep it current. A news page last touched three years ago tells donors nobody&rsquo;s home.</p>
      <p>If you&rsquo;re a registered charity, remind UK taxpayers about
        <a href="https://www.gov.uk/donating-to-charity/gift-aid" target="_blank" rel="noopener">Gift Aid</a>: it adds
        25p to every &pound;1 they give, at no extra cost to them. Put the tick box where they can&rsquo;t miss it.</p>

      <h2>What do volunteers need from your website?</h2>
      <ul>
        <li>What the roles actually are, how much time they take, and where.</li>
        <li>A short sign-up form: name, how to reach them, what interests them. Ask the rest later.</li>
        <li>A named person who&rsquo;ll reply, and roughly when.</li>
      </ul>

      <h2>What are the most common mistakes?</h2>
      <ul>
        <li>The annual report as a PDF is the main content. Nobody reads PDFs on a phone.</li>
        <li>Three different donation platforms linked from different pages. Pick one.</li>
        <li>Sliding carousels. Nobody waits for slide four.</li>
        <li>Pale grey text on white. If people can&rsquo;t read it, they can&rsquo;t support it. The accessibility standard
          asks for a contrast ratio of at least 4.5:1 for normal text.</li>
        <li>English only, in a Welsh-speaking community. In Wales, offering Cymraeg says you belong.</li>
        <li>A free template that looks exactly like every other cause asking for the same money.</li>
      </ul>

      <h2>What does a generic charity template get wrong?</h2>
      <p>It treats your cause like a product category. The same photo of hands, the same &ldquo;Make a difference
        today&rdquo;, the same three icons. Donors scroll past dozens of those a week. What they don&rsquo;t see enough of is
        <em>you</em>: the specific people, the specific place, the specific difference. That&rsquo;s your edge, and generic
        design sands it right off.</p>

      <h2>Where do I start if money is tight?</h2>
      <ol>
        <li>Move donate into the header and test it on your own phone.</li>
        <li>Write one sentence on what &pound;10 does, with your real numbers.</li>
        <li>Swap one stock photo for a real one, with permission.</li>
        <li>Delete anything out of date.</li>
        <li>Ask a stranger to find how to volunteer. Time them.</li>
      </ol>
      <p>None of that needs a developer. When you&rsquo;re ready for more, <a href="../process.html">here&rsquo;s how I
        work</a>. Charity and community projects are the first world in my portfolio for a reason.</p>

      <hr>
      <p><strong>Be bold. Be brave. Be ballsy.</strong> Your cause deserves to be seen properly.</p>
""",
    )

    # ---------------------------------------------------------------- index
    cards = sorted((p["_card"] for p in PAGES.values() if "_card" in p), key=lambda c: c["date"], reverse=True)
    grid = "".join(f"""      <a class="card-post" href="{c['slug']}.html" data-cat="{_plain(c['tag'])}">
        <img class="card-img" src="../assets/img/blog/{c['slug']}.jpg" width="1200" height="630" loading="lazy" alt="">
        <span class="tag">{c['tag']}</span>
        <h2>{c['h1']}</h2>
        <p>{c['desc']}</p>
        <span class="more">Read &middot; {c['mins']} min &rarr;</span>
      </a>
""" for c in cards)
    PAGES["blog/index.html"] = dict(
        title="Blog: women in business &amp; community | Sarah J Hill",
        desc=("Straight-talking advice for women in business, charities and tradeswomen in Cardiff, Birmingham and "
              "beyond: facts, online presence, and backing local communities."),
        ogtitle="The blog — women in business, online presence and community",
        crumb="Blog", ogtype="website",
        backhref="index.html", backtext="Back to the start",
        eyebrow="The blog &middot; Be bold. Be brave. Be ballsy.",
        h1="Hot topics <span class=\"hit\">and making the changes for women.</span>",
        lead=("Straight talk, practical fixes and the people worth knowing &mdash; for founders, charities, community "
              "groups and tradeswomen in Cardiff, Birmingham and wherever you&rsquo;re reading."),
        heroscene='  <div class="scene" aria-hidden="true"><canvas class="sjh-dragon-canvas"></canvas></div>\n',
        extrajs=('<script src="{root}assets/js/dragon.js?v=20261012a" defer></script>\n'
                 '<script type="importmap">{{ "imports": {{ "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js" }} }}</script>\n'
                 '<script type="module" src="{root}assets/js/dragon3d.js?v=20261012a"></script>\n'),
        herocta="",
        extracss=BLOG_CSS + '  <link rel="stylesheet" href="{root}assets/css/05-scene.css?v=20261012a">\n',
        jsonld=json.dumps({"@context": "https://schema.org", "@type": "Blog", "name": "Sarah J Hill — Blog",
                           "url": f"{SITE}/blog/", "author": AUTHOR, "inLanguage": "en-GB"}),
        body=f"""<section class="read">
  <div class="wrap">
    <div class="cat-filter" role="group" aria-label="Show posts about">
      <button type="button" data-f="all" aria-pressed="true">All</button>
      <button type="button" data-f="Women in business" aria-pressed="false">Women in business</button>
      <button type="button" data-f="Your online presence" aria-pressed="false">Your online presence</button>
      <button type="button" data-f="Local &amp; community" aria-pressed="false">Local &amp; community</button>
    </div>
    <div class="posts">
{grid}    </div>
    <script>
    (function(){{
      var btns=document.querySelectorAll('.cat-filter button'), cards=document.querySelectorAll('.card-post');
      btns.forEach(function(b){{ b.addEventListener('click', function(){{
        var f=b.getAttribute('data-f');
        btns.forEach(function(x){{ x.setAttribute('aria-pressed', String(x===b)); }});
        cards.forEach(function(c){{ c.hidden = !(f==='all' || c.getAttribute('data-cat')===f); }});
      }}); }});
    }})();
    </script>
    <div class="topics-next">
      <p class="eyebrow">Coming next</p>
      <ul>
        <li>Starting out: what nobody tells new entrepreneurs</li>
        <li>Backing local: why community businesses matter in Cardiff &amp; Birmingham</li>
        <li>Bilingual websites: doing Welsh properly</li>
      </ul>
    </div>
  </div>
</section>
""",
    )
    for p in PAGES.values():
        p.pop("_card", None)


def _date(iso):
    import datetime as dt
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d:%B %Y}"
