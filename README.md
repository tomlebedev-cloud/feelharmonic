# FeelHarmonic

Vieno puslapio svetainė: koncertinės programos, sezoninės šventės kultūros centrams,
edukaciniai užsiėmimai mokykloms ir renginiai po raktu.

Statinis puslapis — jokių duomenų bazių, jokio WordPress. Trys failai, kuriuos redaguoji:

| Failas | Kam |
|---|---|
| `index.html` | Visas tekstas ir turinys |
| `assets/js/main.js` | `CONFIG` blokas viršuje: el. paštas ir formos adresas |
| `assets/css/style.css` | Spalvos (`:root` blokas viršuje) |

---

## 1. Paleisti lokaliai

Užtenka du kartus spustelėti `index.html` — atsidarys naršyklėje ir viskas veiks.
Pakeitęs tekstą, faile paspausk `Ctrl+S`, naršyklėje `Ctrl+F5`.

Jei kada įsidiegsi Python arba Node, gali paleisti ir tikrą serverį:

```bash
python -m http.server 8000
```

---

## 2. Įkelti į GitHub

Repozitorija dar nesukurta GitHub'e. Prisijunk ir sukurk:

```bash
gh auth login
```

Tada iš šio aplanko:

```bash
gh repo create feelharmonic --public --source=. --remote=origin --push
```

Jei nenori naudoti `gh`, sukurk tuščią repozitoriją per github.com (pavadinimas `feelharmonic`,
**be** README) ir paleisk:

```bash
git remote add origin https://github.com/tomlebedev-cloud/feelharmonic.git
git push -u origin main
```

---

## 3. Įjungti GitHub Pages

GitHub → repozitorija `feelharmonic` → **Settings** → **Pages**:

- **Source:** `Deploy from a branch`
- **Branch:** `main`, aplankas `/ (root)`
- **Save**

Po 1–2 min. svetainė bus adresu:
`https://tomlebedev-cloud.github.io/feelharmonic/`

Pastaba: GitHub Pages nemokamai veikia tik **viešose** repozitorijose.

---

## 4. Prijungti formą (kad užklausos ateitų į paštą)

Kol kas mygtukas „Siųsti užklausą“ atidaro el. pašto programą su paruoštu laišku.
Kad užklausos ateitų automatiškai:

1. Registruokis [formspree.io](https://formspree.io) (nemokamai — 50 užklausų per mėnesį).
2. Sukurk naują formą, nurodyk savo el. paštą.
3. Nukopijuok gautą adresą (`https://formspree.io/f/xxxxxxxx`).
4. `assets/js/main.js`, `CONFIG` blokas:

```js
var CONFIG = {
  email: "daunyte.elena@gmail.com",
  formEndpoint: "https://formspree.io/f/xxxxxxxx"
};
```

5. `git commit` ir `git push` — po minutės veiks.

Pirmą užklausą Formspree paprašys patvirtinti el. paštu. Būtinai išsiųsk testinę.

---

## 5. Savas domenas — vėliau

Puslapis parašytas be jokių prisirišimų prie adreso: visos nuorodos reliatyvios,
todėl jis vienodai veikia atidarytas iš failo, GitHub Pages adresu ar bet kuriame
kitame hostinge. Nusipirkus domeną nieko perrašinėti nereikės — užteks jį prijungti
GitHub Pages nustatymuose ir pridėti `robots.txt` bei `sitemap.xml`.

---

## 6. Kaip atnaujinti turinį

```bash
git add -A
git commit -m "Atnaujintas turinys"
git push
```

GitHub Pages perkuria puslapį per ~1 min.

---

## Ką dar reikia užpildyti

Žr. [TODO.md](TODO.md). Puslapyje visos neužpildytos vietos pažymėtos
punktyriniu rėmeliu — jos matomos ir lankytojui, todėl prieš siunčiant
nuorodą užsakovams jas reikia pakeisti tikru turiniu.
