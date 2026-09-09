#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeelHarmonic - puslapio generatorius
=====================================================================
Puslapio tekstai gyvena aplanke `turinys/` - po vieną JSON failą kiekvienai
kalbai (lt.json, en.json, it.json). Puslapio karkasas (HTML) aprašytas čia.

Paleidimas:

    python build.py

Perrašo tris failus:  index.html  (lietuviškas),  en/index.html,  it/index.html
ir atnaujina sitemap.xml.

TAISYKLE: index.html, en/index.html ir it/index.html RANKA neredaguojami -
juos perrašo šis skriptas. Teksta keisti turinys/*.json failuose, po to paleisti
skripta iš naujo.

JSON laukuose leidžiamas paprastas HTML (<em>, <b>, <span class="fill">...</span>),
todel tekstas neekranuojamas.
"""

import json
import pathlib
import datetime

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "turinys"

SITE = "https://www.feelharmonic.lt"
LANGS = ["lt", "en", "it"]
OUT = {"lt": ROOT / "index.html", "en": ROOT / "en" / "index.html", "it": ROOT / "it" / "index.html"}
HREF = {"lt": "/", "en": "/en/", "it": "/it/"}
BASE = {"lt": "", "en": "../", "it": "../"}
LOCALE = {"lt": "lt_LT", "en": "en_GB", "it": "it_IT"}
LANG_SHORT = {"lt": "LT", "en": "EN", "it": "IT"}
LANG_NAME = {"lt": "Lietuvių", "en": "English", "it": "Italiano"}

MARK = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="mark" viewBox="0 0 100 100">
    <g class="mark">
      <g class="ray">
        <line x1="50" y1="2"  x2="50" y2="98"/>
        <line x1="12" y1="50" x2="88" y2="50"/>
        <line x1="24" y1="24" x2="76" y2="76"/>
        <line x1="76" y1="24" x2="24" y2="76"/>
        <line x1="34" y1="14" x2="66" y2="86"/>
        <line x1="66" y1="14" x2="34" y2="86"/>
        <line x1="16" y1="34" x2="84" y2="66"/>
        <line x1="84" y1="34" x2="16" y2="66"/>
      </g>
      <path class="tri" d="M50 22 L76 74 L24 74 Z"/>
      <circle class="dot" cx="50" cy="50" r="6.4"/>
      <circle class="dot" cx="34" cy="22" r="2.6"/>
      <circle class="dot" cx="72" cy="34" r="1.8"/>
      <circle class="dot" cx="70" cy="70" r="2.4"/>
      <circle class="dot" cx="26" cy="60" r="1.6"/>
    </g>
  </symbol>
</svg>"""


def attr(text):
    """Ekranuoja teksta HTML atributui."""
    return (str(text).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def photo(base, src, alt, cls="shot", cap=None):
    fig = ['<figure class="%s" data-photo>' % cls,
           '  <svg class="ph-empty" viewBox="0 0 100 100" aria-hidden="true"><use href="#mark"/></svg>',
           '  <img src="%sassets/img/%s" alt="%s" data-optional>' % (base, src, attr(alt))]
    if cap:
        fig.append('  <figcaption>%s</figcaption>' % cap)
    fig.append('</figure>')
    return "\n      ".join(fig)


def langbar(lang, cls, aria):
    out = ['<div class="langs %s" role="group" aria-label="%s">' % (cls, attr(aria))]
    for code in LANGS:
        cur = ' class="is-current" aria-current="page"' if code == lang else ""
        out.append('  <a href="%s" hreflang="%s" lang="%s" title="%s"%s>%s</a>'
                   % (HREF[code], code, code, attr(LANG_NAME[code]), cur, LANG_SHORT[code]))
    out.append("</div>")
    return "\n    ".join(out)


def head(lang, c):
    b = BASE[lang]
    m = c["meta"]
    alts = "\n".join(
        '<link rel="alternate" hreflang="%s" href="%s%s">' % (code, SITE, HREF[code]) for code in LANGS)
    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>%(title)s</title>
<meta name="description" content="%(desc)s">

<link rel="canonical" href="%(site)s%(href)s">
%(alts)s
<link rel="alternate" hreflang="x-default" href="%(site)s/">
<meta property="og:url" content="%(site)s%(href)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="%(locale)s">
<meta property="og:site_name" content="FeelHarmonic">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(ogdesc)s">
<meta property="og:image" content="%(site)s/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B3C41">

<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="%(b)sfavicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,500;0,700;1,500&display=swap">
<link rel="stylesheet" href="%(b)sassets/css/style.css">
</head>
<body>
""" % {"lang": lang, "title": attr(m["title"]), "desc": attr(m["description"]),
       "ogdesc": attr(m["ogDescription"]), "site": SITE, "href": HREF[lang],
       "alts": alts, "locale": LOCALE[lang], "b": b}


def header(lang, c):
    nav = "\n      ".join('<a href="%s">%s</a>' % (i["href"], i["label"]) for i in c["nav"])
    mob = "\n  ".join('<a href="%s">%s</a>' % (i["href"], i["label"]) for i in c["mobileNav"])
    return """<a class="skip" href="#turinys">%(skip)s</a>

<!-- ženklo šablonas -->
%(mark)s

<header id="nav">
  <div class="in">
    <a class="brand" href="#top">
      <svg><use href="#mark"/></svg>
      <b>FeelHarmonic</b>
    </a>
    <nav class="main" aria-label="%(navaria)s">
      %(nav)s
      <a class="btn" href="#kontaktai">%(cta)s</a>
    </nav>
    %(langs)s
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="%(menuaria)s">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<nav class="mobile-nav" id="mobile-nav" aria-label="%(mobaria)s">
  %(mob)s
  <a class="btn solid" href="#kontaktai">%(cta)s</a>
  %(langsmob)s
</nav>
""" % {"skip": c["skip"], "mark": MARK, "nav": nav, "mob": mob, "cta": c["navCta"],
       "navaria": attr(c["navAria"]), "mobaria": attr(c["menuAria"]),
       "menuaria": attr(c["menuBtnAria"]),
       "langs": langbar(lang, "in-nav", c["langAria"]),
       "langsmob": langbar(lang, "in-mobile", c["langAria"])}


def hero(lang, c):
    h = c["hero"]
    facts = "\n        ".join("<span>%s</span>" % f for f in h["facts"])
    return """
<main id="top">
<span id="turinys"></span>

<!-- ---------- HERO ---------- -->
<div class="hero">
  <svg class="halo" aria-hidden="true"><use href="#mark"/></svg>
  <div class="in">
    <div>
      <p class="tagline">Let it come!</p>
      <h1>%(h1)s</h1>
      <p class="sub">%(sub)s</p>
      <div class="acts">
        <a class="btn solid" href="#kontaktai">%(cta1)s</a>
        <a class="btn" href="#programos">%(cta2)s</a>
      </div>
      <div class="hero-facts">
        %(facts)s
      </div>
    </div>

    <figure class="portrait" data-photo>
      <svg class="ph-empty" viewBox="0 0 100 100" aria-hidden="true"><use href="#mark"/></svg>
      <img src="%(b)sassets/img/elena.jpg" alt="%(alt)s" width="1000" height="1000" data-optional>
      <figcaption>
        <b>Elena Daunytė</b>
        <span>%(role)s</span>
      </figcaption>
    </figure>
  </div>
</div>
""" % {"h1": h["h1"], "sub": h["sub"], "cta1": h["ctaPrimary"], "cta2": h["ctaSecondary"],
       "facts": facts, "b": BASE[lang], "alt": attr(h["portraitAlt"]), "role": h["portraitRole"]}


def services(lang, c):
    s = c["services"]
    cards = []
    for it in s["items"]:
        tag = '<span class="tag-new">%s</span>' % it["tag"] if it.get("tag") else ""
        cards.append("""<article class="card">
        %(fig)s
        <div class="tx">
          <h3>%(h3)s%(tag)s</h3>
          <p>%(p)s</p>
          <a class="more" href="%(href)s">%(more)s</a>
        </div>
      </article>""" % {"fig": photo(BASE[lang], it["img"], it["alt"]), "h3": it["h3"],
                       "tag": tag, "p": it["p"], "href": it["moreHref"], "more": it["more"]})
    return """
<!-- ---------- PASLAUGOS ---------- -->
<section id="paslaugos" class="band-cream">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>

    <div class="grid3 reveal">
      %(cards)s
    </div>
  </div>
</section>
""" % {"eyebrow": s["eyebrow"], "h2": s["h2"], "lede": s["lede"],
       "cards": "\n\n      ".join(cards)}


def media(lang, c):
    m = c["media"]
    # Kai JSON faile atsiranda "videos" sąrašas, vietoj tuščių vietų rodomi
    # tikri YouTube įrašai. Kol sąrašas tuščias arba jo nėra — rodomos vietos.
    videos = m.get("videos") or []
    if videos:
        slots = "\n      ".join(
            '<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/%s" '
            'title="%s" loading="lazy" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"></iframe></div>'
            % (attr(v["id"]), attr(v["title"])) for v in videos)
    else:
        slots = "\n      ".join(
            '<div class="slot-dark"><strong>%s</strong><span>%s</span></div>' % (s["t"], s["d"])
            for s in m["slots"])
    return """
<!-- ---------- ĮRAŠAI ---------- -->
<section id="irasai" class="band-teal">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>

    <a class="media-card reveal" href="https://www.lrt.lt/mediateka/irasas/2000197212/klipvid-2021-elena-daunyte-ryto-ugnis" target="_blank" rel="noopener">
      <span class="media-play" aria-hidden="true">
        <svg viewBox="0 0 20 20" fill="currentColor"><path d="M6.5 4.2v11.6L16 10 6.5 4.2Z"/></svg>
      </span>
      <span class="media-body">
        <span class="media-label">%(label)s</span>
        <b>Elena Daunytė — „Ryto ugnis“</b>
        <span class="media-note">%(note)s</span>
      </span>
      <span class="media-go" aria-hidden="true">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h7v7M13 3 3.5 12.5"/></svg>
      </span>
    </a>

    <div class="video-slots reveal">
      <!-- ĮDĖTI: <div class="video"><iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe></div> -->
      %(slots)s
    </div>
  </div>
</section>
""" % {"eyebrow": m["eyebrow"], "h2": m["h2"], "lede": m["lede"],
       "label": m["cardLabel"], "note": m["cardNote"], "slots": slots}


def who(lang, c):
    items = "\n      ".join(
        """<div class="who">
        <span class="n">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </div>""" % (i["n"], i["h3"], i["p"]) for i in c["who"]["items"])
    return """
<!-- ---------- KAM SKIRTA ---------- -->
<section id="kam">
  <div class="in">
    <div class="div reveal"><span></span><svg aria-hidden="true"><use href="#mark"/></svg><span></span></div>
    <div class="who-grid reveal">
      %s
    </div>
  </div>
</section>
""" % items


def edu(lang, c):
    e = c["edu"]
    arts = []
    for a in e["items"]:
        facts = "\n          ".join(
            '<li><b>%s</b><span>%s</span></li>' % (f["k"], f["v"]) for f in a["facts"])
        arts.append("""<article>
        <h3>%(h3)s</h3>
        <p>%(p)s</p>
        <ul class="facts">
          %(facts)s
        </ul>
      </article>""" % {"h3": a["h3"], "p": a["p"], "facts": facts})
    notes = "\n    ".join('<p class="after-note reveal">%s</p>' % n for n in e["notes"])
    return """
<!-- ---------- EDUKACIJOS ---------- -->
<section id="edukacijos" class="band-cream">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>

    <div class="edu reveal">
      %(arts)s
    </div>

    %(notes)s
  </div>
</section>
""" % {"eyebrow": e["eyebrow"], "h2": e["h2"], "lede": e["lede"],
       "arts": "\n\n      ".join(arts), "notes": notes}


def programs(lang, c):
    p = c["programs"]
    arts = []
    for a in p["items"]:
        tag = '<span class="tag-new">%s</span>' % a["tag"] if a.get("tag") else ""
        specs = "\n          ".join(
            '<div><span class="k">%s</span><span class="v">%s</span></div>' % (s["k"], s["v"])
            for s in a["specs"])
        arts.append("""<article class="prog">
        <div>
          <h3>%(h3)s%(tag)s</h3>
          <p>%(p)s</p>
        </div>
        <div class="prog-specs">
          %(specs)s
        </div>
      </article>""" % {"h3": a["h3"], "tag": tag, "p": a["p"], "specs": specs})
    return """
<!-- ---------- PROGRAMOS ---------- -->
<section id="programos">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>

    <div class="programs reveal">
      %(arts)s
    </div>

    <p class="after-note reveal">%(note)s</p>
  </div>
</section>
""" % {"eyebrow": p["eyebrow"], "h2": p["h2"], "lede": p["lede"],
       "arts": "\n\n      ".join(arts), "note": p["note"]}


def studio(lang, c):
    s = c["studio"]
    pts = "\n          ".join("<li>%s</li>" % x for x in s["points"])
    return """
<!-- ---------- STUDIJA ---------- -->
<section id="studija" class="band-teal">
  <div class="in">
    <div class="two studio reveal">
      <div>
        <p class="eyebrow">%(eyebrow)s</p>
        <h2>%(h2)s</h2>
        <p class="lede">%(lede)s</p>
        <ul class="creds">
          %(pts)s
        </ul>
        <a class="btn" href="#kontaktai">%(cta)s</a>
      </div>
      <div class="about-photo" data-photo>
        <svg class="ph-empty" viewBox="0 0 100 100" aria-hidden="true"><use href="#mark"/></svg>
        <img src="%(b)sassets/img/studija.jpg" alt="%(alt)s" data-optional>
      </div>
    </div>
  </div>
</section>
""" % {"eyebrow": s["eyebrow"], "h2": s["h2"], "lede": s["lede"], "pts": pts,
       "cta": s["cta"], "b": BASE[lang], "alt": attr(s["alt"])}


def gallery(lang, c):
    g = c["gallery"]
    figs = "\n      ".join(photo(BASE[lang], i["img"], i["alt"], cap=i["cap"]) for i in g["items"])
    return """
<!-- ---------- GALERIJA ---------- -->
<section id="galerija" class="band-cream">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>

    <div class="gallery reveal">
      %(figs)s
    </div>
  </div>
</section>
""" % {"eyebrow": g["eyebrow"], "h2": g["h2"], "lede": g["lede"], "figs": figs}


def about(lang, c):
    a = c["about"]
    paras = "\n        ".join("<p>%s</p>" % x for x in a["paras"])
    creds = "\n          ".join("<li>%s</li>" % x for x in a["creds"])
    return """
<!-- ---------- APIE ---------- -->
<section id="apie">
  <div class="in">
    <div class="two about reveal">
      <div>
        <p class="eyebrow">%(eyebrow)s</p>
        <h2>%(h2)s</h2>
        %(paras)s

        <ul class="creds">
          %(creds)s
        </ul>

        <p>%(last)s</p>
        <a class="btn dark" href="#kontaktai">%(cta)s</a>
      </div>

      <div class="about-photo" data-photo>
        <svg class="ph-empty" viewBox="0 0 100 100" aria-hidden="true"><use href="#mark"/></svg>
        <img src="%(b)sassets/img/apie.jpg" alt="%(alt)s" data-optional>
      </div>
    </div>
  </div>
</section>
""" % {"eyebrow": a["eyebrow"], "h2": a["h2"], "paras": paras, "creds": creds,
       "last": a["closing"], "cta": a["cta"], "b": BASE[lang], "alt": attr(a["alt"])}


def quotes(lang, c):
    q = c["quotes"]
    slots = "\n      ".join(
        '<div class="slot"><strong>%s</strong><span>%s</span></div>' % (s["t"], s["d"])
        for s in q["slots"])
    return """
<!-- ---------- ATSILIEPIMAI ---------- -->
<section id="atsiliepimai" class="band-cream">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
      <p class="lede">%(lede)s</p>
    </div>
    <div class="quotes reveal">
      %(slots)s
    </div>
  </div>
</section>
""" % {"eyebrow": q["eyebrow"], "h2": q["h2"], "lede": q["lede"], "slots": slots}


def faq(lang, c):
    f = c["faq"]
    items = "\n      ".join(
        """<details>
        <summary>%s</summary>
        <div class="ans">%s</div>
      </details>""" % (i["q"], i["a"]) for i in f["items"])
    return """
<!-- ---------- DUK ---------- -->
<section id="duk">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
    </div>
    <div class="faq reveal">
      %(items)s
    </div>
  </div>
</section>
""" % {"eyebrow": f["eyebrow"], "h2": f["h2"], "items": items}


def cta(lang, c):
    x = c["cta"]
    return """
<!-- ---------- CTA ---------- -->
<section class="band-teal cta">
  <div class="in">
    <h2>%s</h2>
    <p class="lede">%s</p>
    <a class="btn solid" href="#kontaktai">%s</a>
  </div>
</section>
""" % (x["h2"], x["lede"], x["btn"])


def contact(lang, c):
    k = c["contact"]
    f = k["fields"]
    opts = "\n              ".join("<option>%s</option>" % o for o in k["options"])
    direct = []
    for d in k["direct"]:
        if d["type"] == "tel":
            v = '<a href="tel:+37067004184">+370 670 04184</a>'
        elif d["type"] == "email":
            v = '<a data-email href="mailto:elena.daunyte@feelharmonic.lt">elena.daunyte@feelharmonic.lt</a>'
        else:
            v = d["v"]
        direct.append("<dt>%s</dt>\n        <dd>%s</dd>" % (d["k"], v))
    js = c["js"]
    data = " ".join('data-%s="%s"' % (key, attr(val)) for key, val in js.items())
    return """
<!-- ---------- KONTAKTAI ---------- -->
<section id="kontaktai">
  <div class="in">
    <div class="head reveal">
      <p class="eyebrow">%(eyebrow)s</p>
      <h2>%(h2)s</h2>
    </div>

    <div class="two reveal">
      <form id="uzklausa" novalidate %(data)s>
        <div class="row2">
          <div class="field"><label for="v">%(f_name)s</label><input id="v" name="vardas" type="text" autocomplete="name" required></div>
          <div class="field"><label for="i">%(f_org)s</label><input id="i" name="istaiga" type="text" autocomplete="organization"></div>
        </div>
        <div class="row2">
          <div class="field"><label for="e">%(f_mail)s</label><input id="e" name="pastas" type="email" autocomplete="email" required></div>
          <div class="field"><label for="t">%(f_tel)s</label><input id="t" name="telefonas" type="tel" autocomplete="tel"></div>
        </div>
        <div class="row2">
          <div class="field">
            <label for="k">%(f_type)s</label>
            <select id="k" name="tipas">
              %(opts)s
            </select>
          </div>
          <div class="field"><label for="d">%(f_date)s</label><input id="d" name="data" type="text" placeholder="%(p_date)s"></div>
        </div>
        <div class="field"><label for="z">%(f_msg)s</label><textarea id="z" name="zinute" placeholder="%(p_msg)s"></textarea></div>

        <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">

        <button class="btn dark" type="submit">%(submit)s</button>
        <p class="form-msg" id="form-msg" role="status" aria-live="polite"></p>
      </form>

      <dl class="direct">
        %(direct)s
      </dl>
    </div>
  </div>
</section>
</main>
""" % {"eyebrow": k["eyebrow"], "h2": k["h2"], "data": data, "opts": opts,
       "f_name": f["name"], "f_org": f["org"], "f_mail": f["email"], "f_tel": f["phone"],
       "f_type": f["type"], "f_date": f["date"], "p_date": attr(f["datePlaceholder"]),
       "f_msg": f["message"], "p_msg": attr(f["messagePlaceholder"]),
       "submit": k["submit"], "direct": "\n        ".join(direct)}


def footer(lang, c):
    f = c["footer"]
    pages = "\n          ".join('<li><a href="%s">%s</a></li>' % (i["href"], i["label"])
                                for i in f["pages"])
    details = "\n          ".join("<li>%s</li>" % x for x in f["details"])
    return """
<!-- ---------- PORAŠTĖ ---------- -->
<footer>
  <div class="in">
    <div class="cols">
      <div>
        <div class="fbrand">
          <svg aria-hidden="true"><use href="#mark"/></svg>
          <div><b>FeelHarmonic</b><span class="tg">Let it come!</span></div>
        </div>
        <p style="max-width:34ch;margin:0 0 18px">%(about)s</p>
        %(langs)s
      </div>
      <div>
        <h4>%(colpages)s</h4>
        <ul>
          %(pages)s
        </ul>
      </div>
      <div>
        <h4>%(coldetails)s</h4>
        <ul>
          %(details)s
          <li><a data-email href="mailto:elena.daunyte@feelharmonic.lt">elena.daunyte@feelharmonic.lt</a></li>
          <li><a href="tel:+37067004184">+370 670 04184</a></li>
        </ul>
      </div>
    </div>
    <div class="fbot">
      <span>&copy; <span id="year">%(year)s</span> FeelHarmonic</span>
      <span>%(city)s</span>
    </div>
  </div>
</footer>
""" % {"about": f["about"], "colpages": f["colPages"], "pages": pages,
       "coldetails": f["colDetails"], "details": details, "city": f["city"],
       "year": datetime.date.today().year,
       "langs": langbar(lang, "in-footer", c["langAria"])}


def jsonld(lang, c):
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "name": "Elena Daunytė",
                "jobTitle": c["schema"]["jobTitle"],
                "url": SITE + HREF[lang],
                "email": "elena.daunyte@feelharmonic.lt",
                "telephone": "+370 670 04184",
                "worksFor": {"@type": "Organization", "name": "FeelHarmonic",
                             "slogan": "Let it come!", "url": SITE + "/"},
                "knowsLanguage": ["lt", "en", "it"],
                "knowsAbout": c["schema"]["knowsAbout"],
            },
            {
                "@type": "FAQPage",
                "inLanguage": lang,
                "mainEntity": [
                    {"@type": "Question", "name": q["q"],
                     "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                    for q in c["schema"]["faq"]
                ],
            },
        ],
    }
    return ('\n<script type="application/ld+json">\n%s\n</script>\n'
            % json.dumps(data, ensure_ascii=False, indent=2))


def page(lang, c):
    return "".join([
        head(lang, c), header(lang, c), hero(lang, c), services(lang, c), media(lang, c),
        who(lang, c), edu(lang, c), programs(lang, c), studio(lang, c), gallery(lang, c),
        about(lang, c), quotes(lang, c), faq(lang, c), cta(lang, c), contact(lang, c),
        footer(lang, c), jsonld(lang, c),
        '\n<script src="%sassets/js/main.js"></script>\n</body>\n</html>\n' % BASE[lang],
    ])


def sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for lang in LANGS:
        links = "\n".join(
            '    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (o, SITE, HREF[o])
            for o in LANGS)
        urls.append("""  <url>
    <loc>%s%s</loc>
%s
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>""" % (SITE, HREF[lang], links, today, "1.0" if lang == "lt" else "0.8"))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    for lang in LANGS:
        with open(CONTENT / ("%s.json" % lang), encoding="utf-8") as fh:
            c = json.load(fh)
        out = OUT[lang]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang, c), encoding="utf-8")
        print("parasyta  %s" % out.relative_to(ROOT))
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("parasyta  sitemap.xml")


if __name__ == "__main__":
    main()
