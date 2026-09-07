# Techninis aprašymas

Skirta tam, kas prižiūrės puslapį toliau — žmogui arba AI sesijai.
Nereikia jokio ankstesnio konteksto: viskas, ką reikia žinoti, yra čia.

## Kas tai

Statinis vieno puslapio tinklalapis. **Jokio karkaso, jokio kompiliavimo,
jokio `npm install`.** Atsidarai `index.html` naršyklėje — ir jis veikia.
Tai sąmoningas sprendimas: puslapį turi galėti prižiūrėti bet kas, bet kada,
be priklausomybės nuo įrankių, kurie po kelerių metų nustos veikti.

Kalba: lietuvių. Kodo komentarai taip pat lietuviški.

## Failai

```
index.html              visas turinys ir struktūra
404.html                klaidos puslapis
favicon.svg             ikonėlė (firminis ženklas)
assets/css/style.css    visi stiliai; spalvos ir šriftai — :root bloke viršuje
assets/js/main.js       CONFIG blokas + meniu, animacijos, forma, nuotraukos
assets/img/             nuotraukos (žr. ADMIN.md dėl pavadinimų)
spauda/vizitine.html    vizitinių kortelių šablonas spaudai
spauda/FeelHarmonic-vizitine.pdf   sugeneruotas PDF
ADMIN.md                instrukcija savininkei (be programavimo)
TODO.md                 ko dar trūksta turinyje
```

## Dizaino sistema

Spalvos ir šriftai aprašyti kintamaisiais `assets/css/style.css` pradžioje.
Keičiant temą užtenka pataisyti `:root` bloką — visa kita paseks.

| Kintamasis | Reikšmė | Kur naudojama |
|---|---|---|
| `--teal` | `#0B3C41` | Meniu, hero, CTA juosta, poraštė |
| `--teal-deep` | `#072B2F` | Poraštė, tuščios nuotraukų vietos |
| `--gold` | `#CE8E34` | Dekoracijos, mygtukai, ženklas |
| `--gold-lt` | `#E2A94F` | Smulkus tekstas ant tamsaus fono |
| `--gold-ink` | `#8A5E18` | Tekstas ant šviesaus fono (kontrastui) |
| `--cream` / `--paper` | `#F6F1E6` / `#FCFAF4` | Šviesios juostos |

**Svarbu dėl kontrasto:** ryškus auksas ant kreminio fono duoda tik 2,4:1 —
neįskaitomas. Todėl tekstui šviesiame fone naudojamas `--gold-ink`, o ryškusis
paliktas dekoracijoms ir tamsiam fonui. Visos teksto poros patikrintos,
rezultatai 4,78–12,09:1 (WCAG AA). Keičiant spalvas tai reikia pertikrinti.

Šriftai: **Playfair Display** (antraštės) ir **Jost** (tekstas), iš Google Fonts.
Abu turi lietuviškas raides (latin-ext subsetas).

Firminis ženklas — inline SVG `<symbol id="mark">` failo `index.html` pradžioje.
Naudojamas per `<use href="#mark"/>` meniu, hero fone, skirtuke, poraštėje ir
tuščiose nuotraukų vietose.

## JavaScript

Vienas failas, be priklausomybių. Viršuje — `CONFIG` blokas (el. paštas ir
Formspree adresas), tai vienintelė vieta, kurią reikia redaguoti kasdienėje
priežiūroje.

Ką daro:
- mobilųjį meniu (burger),
- aktyvios sekcijos žymėjimą meniu (IntersectionObserver),
- turinio pasirodymą slenkant (`.reveal` klasė),
- užklausos formą: siunčia į Formspree, o jei jis nesukonfigūruotas —
  atidaro el. pašto programą su paruoštu laišku,
- **trūkstamų nuotraukų tvarkymą**: jei failo nėra, vietoje jo rodomas
  firminis ženklas; jei nėra nė vienos galerijos nuotraukos, visa galerijos
  skiltis ir nuoroda meniu paslepiamos; jei nėra „Apie“ nuotraukos, tekstas
  išsiplečia per visą plotį.

Puslapis veikia ir be JavaScript — tada tiesiog nėra animacijų ir mobiliojo
meniu. `.reveal` elementai paslepiami tik tada, kai JS įsikrauna (`.js` klasė
ant `<html>`), todėl be JS turinys matomas iš karto.

## Hostingas

GitHub Pages, šaka `main`, aplankas `/` (root).
Adresas: https://www.feelharmonic.lt/ (senasis
https://tomlebedev-cloud.github.io/feelharmonic/ persiunčia į jį).

Failas `.nojekyll` išjungia Jekyll apdorojimą.
Visos nuorodos reliatyvios, todėl puslapis vienodai veikia atidarytas iš failo,
GitHub Pages adresu arba bet kuriame kitame hostinge.

Įkėlus pakeitimą į `main`, puslapis persikuria automatiškai per ~1 min.

## Domenas

`feelharmonic.lt` nupirktas Hostingeryje 2026-09-07. Pagrindinis adresas —
`www.feelharmonic.lt`; šakninį domeną GitHub persiunčia pats.

- DNS Hostingerio zonoje: keturi A įrašai į `185.199.108–111.153` ir
  `CNAME www` į `tomlebedev-cloud.github.io.` MX ir TXT įrašai priklauso
  paštui — jų liesti negalima.
- Repozitorijos šaknyje `CNAME` su eilute `www.feelharmonic.lt`.
  **Trinti negalima.** Jei domenas įrašomas per GitHub sąsają, GitHub šį failą
  sukuria pats — tada prieš kitą `git push` būtinas `git pull`, kitaip
  pushinsi be jo ir domenas nustos veikti.
- GitHub → Settings → Pages → Custom domain, tada **Enforce HTTPS**.
- `og:image`, `canonical`, `robots.txt` ir `sitemap.xml` jau nurodo į
  `https://www.feelharmonic.lt/`.

## Vizitinės

`spauda/vizitine.html` — 85 × 55 mm su 3 mm nuopjova (failas 91 × 61 mm).
Kortelių fonai nupiešti SVG figūromis, ne CSS fonais, todėl spausdinami
visada, nepriklausomai nuo „Background graphics“ nustatymo.

PDF generuojamas taip:

```bash
chrome --headless=new --no-pdf-header-footer \
  --print-to-pdf=FeelHarmonic-vizitine.pdf spauda/vizitine.html
```

Rezultatas turi būti 2 puslapiai po 258 × 173 pt (= 91 × 61 mm).

## Paleisti lokaliai

Užtenka dukart spustelėti `index.html`. Jei nori tikro serverio:

```bash
python -m http.server 8000
```

## Ko šiame projekte NĖRA (ir kodėl)

- **Karkaso ar build žingsnio** — sąmoningai, kad puslapį galėtų prižiūrėti
  bet kas be įrankių diegimo.
- **CMS** — realiai keičiasi tik kainos, nuotraukos ir atsiliepimai, kelis
  kartus per metus. Jei prireiktų, tinkamiausias kelias: hostingą perkelti į
  Netlify (ta pati repozitorija, nemokamai) ir uždėti Decap CMS.
- **Tamsios temos** — dizainas sąmoningai vienspalvis, paimtas iš logotipo.

## Kas dar neužbaigta

Žr. [TODO.md](TODO.md).
