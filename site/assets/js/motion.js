(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var els = document.querySelectorAll("[data-motion]");
  if (!("IntersectionObserver" in window)) {
    els.forEach(function (el) {
      el.classList.add("in");
    });
    return;
  }
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );
  els.forEach(function (el, i) {
    if (el.classList.contains("pillar") || el.classList.contains("blog-card-home")) {
      el.classList.add("stagger-" + ((i % 3) + 1));
    }
    io.observe(el);
  });
  document.querySelectorAll(".reveal").forEach(function (el) {
    io.observe(el);
  });
})();
