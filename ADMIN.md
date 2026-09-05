# Kaip pačiai keisti puslapį

Ši instrukcija skirta Elenai. Programuoti nereikia — viską galima padaryti
naršyklėje, GitHub svetainėje. Kompiuteryje nieko diegti nereikia.

Puslapis: **https://tomlebedev-cloud.github.io/feelharmonic/**
Kodas: **https://github.com/tomlebedev-cloud/feelharmonic**

---

## Pagrindinė taisyklė

Visas puslapio tekstas yra viename faile — **`index.html`**.
Kai jį pakeiti ir išsaugai, puslapis internete atsinaujina **per maždaug minutę**.

Kiekvienas išsaugojimas įsimenamas. Jei kas nors sugriūva, viską galima
atsukti atgal per 30 sekundžių — kaip tai padaryti, parašyta pačiame gale.

---

## 1. Pakeisti tekstą arba kainą

1. Atsidaryk https://github.com/tomlebedev-cloud/feelharmonic
2. Spustelėk failą **`index.html`**
3. Viršuje dešinėje spustelėk **pieštuko ikonėlę** (Edit this file)
4. Klaviatūra spausk `Ctrl + F` ir įrašyk žodį, kurį nori pakeisti
   (pavyzdžiui `Kalėdų vakaras`) — naršyklė nuves į tą vietą
5. Pakeisk tekstą. **Keisk tik žodžius tarp `>` ir `<`.**
   Pavyzdžiui čia keisti galima tik `55 min`:

   ```
   <span class="v">55 min</span>
   ```

6. Nuslink į apačią, spustelėk žalią **Commit changes**
7. Atsidariusiame lange dar kartą **Commit changes**

Po minutės atnaujink puslapį naršyklėje — pakeitimas jau ten.

### Kur ieškoti dažniausiai keičiamų dalykų

| Ką keisti | Ieškok žodžio |
|---|---|
| Programos kainos | `įrašyti €` |
| Edukacijos duomenys | `Kaip skamba emocija` |
| Telefonas | `+370 670 04184` |
| El. paštas | `daunyte.elena@gmail.com` |
| Individualios veiklos nr. | `Individuali veikla nr.` |
| Tekstas apie save | `Elena Daunytė — violončelininkė` |

Punktyriniu rėmeliu apvestos vietos puslapyje — tai dar neužpildyti duomenys.
Faile jos atrodo taip: `<span class="fill">įrašyti €</span>`.
Užpildant reikia ištrinti visą tą gabalą ir palikti tik skaičių, pavyzdžiui `120 €`.

---

## 2. Įkelti nuotrauką

Nuotraukos turi turėti **tikslų pavadinimą** — puslapis jų ieško pagal jį.

| Failo pavadinimas | Kur atsiras |
|---|---|
| `elena.jpg` | Pirmame ekrane, prie pavadinimo |
| `apie.jpg` | Skiltyje „Apie“ |
| `galerija-1.jpg` … `galerija-6.jpg` | Galerijoje |
| `paslauga-koncertai.jpg` | Kortelė „Koncertai“ |
| `paslauga-edukacijos.jpg` | Kortelė „Edukacijos“ |
| `paslauga-renginiai.jpg` | Kortelė „Renginiai“ |

Kaip įkelti:

1. Eik į https://github.com/tomlebedev-cloud/feelharmonic/tree/main/assets/img
2. Spustelėk **Add file → Upload files**
3. Nutempk nuotrauką (pavadinimas turi sutapti su lentele aukščiau)
4. Apačioje **Commit changes**

Nuotrauka atsiras pati, kode keisti nieko nereikia.

**Svarbu:** nuotrauka turi būti ne mažesnė kaip 1200 px pločio, bet ir ne
didesnė kaip ~500 KB, kitaip puslapis krausis lėtai. Suspausti nemokamai
galima čia: https://squoosh.app

Kol nuotraukų nėra, jų vietose rodomas firminis ženklas, o galerijos skiltis
tiesiog nerodoma. Puslapis nesugriūva.

---

## 3. Pridėti atsiliepimą

Faile `index.html` susirask `Ką sako užsakovai`. Po juo yra du blokai,
prasidedantys `<div class="slot">`. Pakeisk visą vieną tokį bloką šituo:

```html
<blockquote>
  <p>Čia įrašyk atsiliepimo tekstą.</p>
  <cite>Vardas Pavardė — įstaigos pavadinimas</cite>
</blockquote>
```

Visada prašyk leidimo skelbti. Nesugalvotų atsiliepimų nerašyti —
kultūros įstaigose žmonės pažįsta vieni kitus.

---

## 4. Įdėti vaizdo įrašą

Skiltyje „Įrašai“ susirask `slot-dark`. Pakeisk visą tą bloką šituo,
vietoj `VIDEO_ID` įrašydama savo YouTube įrašo kodą (jis matomas
adreso juostoje po `watch?v=`):

```html
<div class="video">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID"
          title="Koncerto ištrauka" loading="lazy"
          allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"
          allowfullscreen></iframe>
</div>
```

---

## 5. Kad užklausos ateitų į paštą

Dabar mygtukas „Siųsti užklausą“ atidaro el. pašto programą su paruoštu
laišku. Kad laiškai ateitų automatiškai:

1. Registruokis https://formspree.io (nemokamai — 50 užklausų per mėnesį)
2. Sukurk formą, nurodyk savo el. paštą
3. Nukopijuok gautą adresą (`https://formspree.io/f/xxxxxxxx`)
4. GitHub'e atidaryk `assets/js/main.js`, spausk pieštuką
5. Pirmose eilutėse pakeisk `PAKEISTI` į savo adresą:

```js
formEndpoint: "https://formspree.io/f/xxxxxxxx"
```

6. **Commit changes**

Būtinai išsiųsk sau testinę užklausą — Formspree pirmą kartą paprašo patvirtinti.

---

## 6. Jei kas nors sulūžo

Nieko baisaus neatsitiko. Kiekvienas išsaugojimas įsimintas, grąžinti galima taip:

1. Eik į https://github.com/tomlebedev-cloud/feelharmonic/commits/main
2. Rask paskutinį savo pakeitimą (viršuje)
3. Spustelėk jį, tada viršuje dešinėje **⋯ → Revert**
4. **Commit changes**

Puslapis grįš į būseną prieš tą pakeitimą.

---

## Ko geriau neliesti

- Failo `assets/css/style.css` — ten dizainas. Spalvas keisti galima
  pačiame viršuje (`--teal`, `--gold`), bet visa kita geriau palikti.
- Eilučių, kurios prasideda `<script` arba `<link`.
- Failo `assets/js/main.js` — išskyrus tą vieną Formspree eilutę.

Jei reikia keisti dizainą arba pridėti naują skiltį — tam reikia žmogaus,
mokančio HTML. Techninis aprašymas jam paruoštas faile `HANDOVER.md`.

---

## Kas dar neužpildyta

Žr. [TODO.md](TODO.md) — ten surašyta, ko trūksta ir kokia eilės tvarka.
