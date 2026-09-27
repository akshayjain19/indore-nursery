(function () {
  var d = document;
  var b = d.querySelector(".burger");
  var dr = d.getElementById("nav-drawer") || d.querySelector(".drawer");
  if (b && dr) {
    b.addEventListener("click", function () {
      dr.classList.add("open");
      dr.setAttribute("aria-hidden", "false");
      b.setAttribute("aria-expanded", "true");
    });
    var x = dr.querySelector(".x");
    if (x) {
      x.addEventListener("click", function () {
        dr.classList.remove("open");
        dr.setAttribute("aria-hidden", "true");
        b.setAttribute("aria-expanded", "false");
      });
    }
  }
  var topBtn = d.getElementById("top");
  if (topBtn) {
    window.addEventListener(
      "scroll",
      function () {
        topBtn.style.display = window.scrollY > 600 ? "flex" : "none";
      },
      { passive: true }
    );
    topBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* Plant filter chips on /plants/ */
  var grid = d.getElementById("plant-grid");
  if (grid) {
    var chips = d.querySelectorAll("[data-plant-filter]");
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var tag = chip.getAttribute("data-plant-filter");
        chips.forEach(function (c) {
          c.classList.toggle("on", c === chip);
        });
        grid.querySelectorAll("[data-tags]").forEach(function (card) {
          var tags = (card.getAttribute("data-tags") || "").split(",");
          var show = tag === "all" || tags.indexOf(tag) >= 0;
          card.style.display = show ? "" : "none";
        });
      });
    });
  }

  /* Homepage plant carousel — arrow nav, hidden scrollbar */
  d.querySelectorAll(".carousel-shell[data-carousel]").forEach(function (shell) {
    var rail = shell.querySelector(".plant-rail, .pot-rail");
    if (!rail) return;
    var prev = shell.querySelector(".carousel-arrow.prev");
    var next = shell.querySelector(".carousel-arrow.next");
    if (!prev || !next) return;

    function scrollStep() {
      var card = rail.querySelector(".plant-card-v2, .pot-card-v2");
      if (!card) return Math.max(200, rail.clientWidth * 0.75);
      var gap = parseFloat(getComputedStyle(rail).gap) || 18;
      return card.getBoundingClientRect().width + gap;
    }

    function updateArrows() {
      var max = rail.scrollWidth - rail.clientWidth;
      var left = rail.scrollLeft;
      var eps = 3;
      prev.disabled = left <= eps;
      next.disabled = max <= eps || left >= max - eps;
    }

    prev.addEventListener("click", function () {
      rail.scrollBy({ left: -scrollStep(), behavior: "smooth" });
    });
    next.addEventListener("click", function () {
      rail.scrollBy({ left: scrollStep(), behavior: "smooth" });
    });
    rail.addEventListener("scroll", updateArrows, { passive: true });
    window.addEventListener("resize", updateArrows);
    if ("ResizeObserver" in window) {
      new ResizeObserver(updateArrows).observe(rail);
    }
    updateArrows();
  });
})();
