(function () {
  var root = document.getElementById("pot-variant-root");
  if (!root) return;
  var data = null;
  try {
    data = JSON.parse(document.getElementById("pot-variant-data").textContent);
  } catch (e) {
    return;
  }
  var sizesEl = root.querySelector("[data-size-options]");
  var coloursEl = root.querySelector("[data-colour-options]");
  var priceEl = root.querySelector("[data-variant-price]");
  var regEl = root.querySelector("[data-variant-regular]");
  var waEl = root.querySelector("[data-variant-wa]");
  var model = data.model_name;
  var variants = data.variants.filter(function (v) {
    return v.active;
  });
  var sel = { size: null, colour: null };

  function money(n) {
    if (n == null) return "On Request";
    return "Rs " + Number(n).toLocaleString("en-IN");
  }

  function availableColours(size) {
    return variants
      .filter(function (v) {
        return !size || v.size === size;
      })
      .map(function (v) {
        return v.colour;
      })
      .filter(function (c, i, a) {
        return a.indexOf(c) === i;
      });
  }

  function availableSizes(colour) {
    return variants
      .filter(function (v) {
        return !colour || v.colour === colour;
      })
      .map(function (v) {
        return v.size;
      })
      .filter(function (s, i, a) {
        return a.indexOf(s) === i;
      });
  }

  function findVariant() {
    return variants.find(function (v) {
      return v.size === sel.size && v.colour === sel.colour;
    });
  }

  function renderChips(container, values, key, current) {
    container.innerHTML = "";
    values.forEach(function (val) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip" + (val === current ? " on" : "");
      btn.textContent = val;
      btn.addEventListener("click", function () {
        sel[key] = val;
        if (key === "size") {
          var cols = availableColours(val);
          if (cols.indexOf(sel.colour) < 0) sel.colour = cols[0] || null;
        } else {
          var sizes = availableSizes(val);
          if (sizes.indexOf(sel.size) < 0) sel.size = sizes[0] || null;
        }
        paint();
      });
      container.appendChild(btn);
    });
  }

  function waMessage() {
    var parts = ["Hi Indore Nursery, I'm interested in " + model];
    if (sel.size) parts.push("size " + sel.size);
    if (sel.colour && sel.colour !== "Standard") parts.push(sel.colour);
    return (
      "https://wa.me/" +
      data.wa_phone +
      "?text=" +
      encodeURIComponent(parts.join(", ") + ". Please share availability and details.")
    );
  }

  function paint() {
    renderChips(sizesEl, availableSizes(sel.colour), "size", sel.size);
    renderChips(coloursEl, availableColours(sel.size), "colour", sel.colour);
    var v = findVariant();
    if (v) {
      priceEl.textContent = money(v.price);
      if (regEl) {
        regEl.textContent =
          v.regular_price && v.regular_price > v.price ? money(v.regular_price) : "";
      }
    } else {
      priceEl.textContent = "Select size & colour";
      if (regEl) regEl.textContent = "";
    }
    if (waEl) {
      waEl.href = waMessage();
    }
  }

  sel.size = data.sizes[0] || null;
  sel.colour = data.colours[0] || null;
  paint();
})();
