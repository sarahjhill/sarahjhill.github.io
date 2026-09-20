# Project items

These are the 26 items `seed-project.sh` creates. If you would rather add them
by hand — or the GitHub CLI is being awkward — copy them from here.


## Storyboard


### SB-01 · The Judgement (hero)

Counter 3→0 over exactly three seconds while the headline sits blurred, then snaps sharp and the label reads 'they have decided'.
JOB: make the visitor feel the three seconds rather than read about them.
DONE WHEN: countdown, blur-resolve, replay button and scroll-progress handover all work, and reduce-motion skips to the resolved state.


### SB-02 · The Recognition (who it's for)

Three numbered lines: husband parking the van / on reception, love / nobody scrolled that far.
JOB: she stops reading a website and starts reading her own life.
DONE WHEN: lines stagger in and nudge right on hover.


### SB-03 · The Proof (the 3-second test)

Two electrician cards, a real three-second bar, three endings — picks B, picks A, or runs out of time.
JOB: the most important scene. Makes the argument happen to the reader instead of telling them.
DONE WHEN: all three verdicts fire correctly, keyboard-operable, result announced via aria-live.


### SB-04 · The Promise (manifesto)

Full-bleed flame. 'I say the thing everyone else softens. Your website should too.'
JOB: a breath after the test, and the moment the site states a character rather than a service.


### SB-05 · The Person (about)

Portrait in greyscale, flame frame offset behind, colour on hover. Career change, Code Institute, community work.
JOB: credibility by kinship — she's backing someone who's been in the same room.
DONE WHEN: a photograph of Sarah actually working replaces the current portrait.


### SB-06 · The Offer (what you get)

Five rows, each with a YOU GET payoff so nothing reads as a feature.
JOB: scannable in ten seconds, readable in two minutes.


### SB-07 · The Evidence (work)

Four live project tiles. JOB: the site doing what scene 06 just promised — leading with proof.
DONE WHEN: every tile links somewhere live and loads a real screenshot.


### SB-08 · The Product (Dragon Fire Process)

Counters 12/69/72/5, split for-the-client and for-the-studio, licence CTA.
JOB: the second revenue stream.
DONE WHEN: there is a price or a licence enquiry route, not just a demo link.


### SB-09 · The Voices (testimonials)

Three real quotes, deliberately unglamorous, placed so the free offer that follows feels earned.
DONE WHEN: there are five or more, each with a business name.


### SB-10 · The Hook (Doubt Audit)

'How many decide against you before they ring?' plus the honesty rows — no invented £47,000 figures.
JOB: a free, low-risk first step pitched at the fear rather than the service.


### SB-11 · The Ask (close)

'Let's get you taken seriously.' Two working days, honest answer, even if it's 'not me — try her instead'.
JOB: ends on the promise the site opened with.


## Build & deploy


### Create the redesign repo and turn Pages on

New public repo, upload the site, Settings → Pages → main / root.
DONE WHEN: live at sarahjhill.github.io/<repo>/ and deploy.sh pushes successfully.


### Show the redesign to five people before committing

Three tradeswomen if possible. Watch where they stop. Ask what they thought the business does.
DONE WHEN: five sets of notes exist and anything that confused people is fixed.


### Switch sarahjhill.com over to the new repo

CAREFUL: a custom domain can only point at one repo. Clear the domain from make-it-pop FIRST, then add CNAME here, then set the domain and enforce HTTPS.
BLOCKED BY: the five-person review above.


### Redesign website-audit.html to match

Its structure is already the model for the new homepage. Bring it into the new design language and rename it the Doubt Audit throughout.


### Redesign project-os.html to match

The Dragon Fire Process product page. Needs the licence offer made explicit, not just a demo link.


## Content


### Photograph of Sarah actually working

Would do more for the About and hero than anything else outstanding. Not a desk portrait — hands, tools, screen, real work.


### Collect five more testimonials

Ask every past client. One sentence is plenty. Business name and first name is enough attribution.


### Write one case study per audience

One tradeswoman, one Muslim-woman-owned business. Problem, what changed, what happened after. These become the trade landing pages later.


### Decide the name

Make It Pop sells the paint; this business sells the foundations. Currently running as Sarah J Hill with Dragon Fire Process as the product. Alternatives: Level, Underestimated, Plumb. See POSITIONING.md.


### Decide Cardiff, Birmingham, or both

The site says Cardiff & South Wales, the CV says Birmingham. Pick one deliberately — local SEO depends on it.


## Growth


### Set up a Google Business Profile

HIGHEST IMPACT ITEM ON THIS BOARD. For local search this outweighs every on-page change combined. Needs a service area, categories, photos and first reviews.


### Get listed on tradeswomen directories and networks

Those backlinks are worth more than any on-page tweak. Start with UK women-in-trade networks and local business groups.


### Build the tradeswomen directory

Searchable by trade and by town, free to join, free to search, no commission. Turns the studio from a supplier into a hub — and it's a local news story that isn't about web design.
DONE WHEN: twenty women are listed.


### One landing page per trade

/electricians, /plumbers, /joiners — once there's a case study for each. Specific pages rank; a general one doesn't.
BLOCKED BY: case studies.


### Fix the GitHub profile basics

Website field is empty on all nine repos, nothing is pinned, xcode-projects is an empty repo. Fifteen minutes, big difference. See GitHub-Polish-Checklist.
