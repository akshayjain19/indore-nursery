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
})();
