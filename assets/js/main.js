/* FeelHarmonic — puslapio logika
   ------------------------------------------------------------------
   VIENINTELĖ VIETA, KURIĄ REIKIA REDAGUOTI: CONFIG blokas žemiau.
   ------------------------------------------------------------------ */

var CONFIG = {
  // El. pašto adresas, kuriuo su tavimi susisieks užsakovai.
  email: "labas@feelharmonic.lt",

  // Formspree adresas. Registruokis formspree.io, sukurk formą ir
  // įklijuok gautą nuorodą (atrodo taip: https://formspree.io/f/abcdwxyz).
  // Kol čia lieka "PAKEISTI", forma atidarys el. pašto programą su
  // paruoštu laišku — puslapis veikia, tik be automatinio siuntimo.
  formEndpoint: "PAKEISTI"
};

(function () {
  "use strict";

  /* --- metai poraštėje --- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- el. pašto adresas įrašomas iš CONFIG --- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-email]"), function (el) {
    el.textContent = CONFIG.email;
    if (el.tagName === "A") el.setAttribute("href", "mailto:" + CONFIG.email);
  });

  /* --- užklausos forma --- */
  var form = document.getElementById("uzklausa");
  if (form) {
    var msg = document.getElementById("form-msg");
    var btn = form.querySelector("button[type=submit]");

    function say(text, state) {
      if (!msg) return;
      msg.textContent = text;
      msg.setAttribute("data-state", state || "");
    }

    function mailtoFallback(data) {
      var body = [
        "Vardas: " + (data.get("vardas") || ""),
        "Įstaiga: " + (data.get("istaiga") || ""),
        "El. paštas: " + (data.get("pastas") || ""),
        "Telefonas: " + (data.get("telefonas") || ""),
        "Ko ieško: " + (data.get("tipas") || ""),
        "Data: " + (data.get("data") || ""),
        "",
        data.get("zinute") || ""
      ].join("\n");

      window.location.href =
        "mailto:" + CONFIG.email +
        "?subject=" + encodeURIComponent("Užklausa dėl " + (data.get("tipas") || "programos")) +
        "&body=" + encodeURIComponent(body);

      say("Atidaryta jūsų el. pašto programa. Jei nieko neįvyko, rašykite adresu " + CONFIG.email, "");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // paprastas apsaugos nuo robotų laukas
      if (form.querySelector("[name=_gotcha]") && form.querySelector("[name=_gotcha]").value) return;

      var data = new FormData(form);

      if (CONFIG.formEndpoint.indexOf("formspree.io") === -1) {
        mailtoFallback(data);
        return;
      }

      btn.disabled = true;
      say("Siunčiama…", "");

      fetch(CONFIG.formEndpoint, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" }
      })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          form.reset();
          say("Ačiū — užklausa gauta. Atsakysiu per dvi darbo dienas.", "ok");
        })
        .catch(function () {
          say("Nepavyko išsiųsti. Parašykite tiesiai adresu " + CONFIG.email, "err");
        })
        .then(function () {
          btn.disabled = false;
        });
    });
  }

  /* --- harmonikų banga hero'jaus apačioje --- */
  var cv = document.getElementById("wave");
  if (!cv || !cv.getContext) return;

  var ctx = cv.getContext("2d");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var stroke = "#1E5C50";

  function readColor() {
    var v = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim();
    if (v) stroke = v;
  }

  function size() {
    var r = cv.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.max(1, r.width * dpr);
    cv.height = Math.max(1, r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  var harmonics = [
    { n: 1, amp: 0.30, alpha: 0.34, speed: 0.00022 },
    { n: 2, amp: 0.16, alpha: 0.24, speed: 0.00031 },
    { n: 3, amp: 0.10, alpha: 0.18, speed: 0.00044 }
  ];

  function draw(t) {
    var r = cv.getBoundingClientRect();
    var w = r.width, h = r.height;
    ctx.clearRect(0, 0, w, h);
    for (var i = 0; i < harmonics.length; i++) {
      var hm = harmonics[i];
      ctx.beginPath();
      for (var x = 0; x <= w; x += 2) {
        var y = h * 0.62 + Math.sin((x / w) * Math.PI * 2 * hm.n + t * hm.speed) * h * hm.amp;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.globalAlpha = hm.alpha;
      ctx.strokeStyle = stroke;
      ctx.lineWidth = 1.25;
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  readColor();
  size();
  draw(0);

  window.addEventListener("resize", function () { size(); draw(performance.now()); });

  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  if (mq.addEventListener) mq.addEventListener("change", readColor);
  else if (mq.addListener) mq.addListener(readColor);

  new MutationObserver(readColor).observe(document.documentElement, {
    attributes: true, attributeFilter: ["data-theme"]
  });

  if (!reduced) {
    (function loop(ts) { draw(ts); requestAnimationFrame(loop); })(0);
  }
})();
