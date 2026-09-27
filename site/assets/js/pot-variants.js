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
  var sizeField = root.querySelector("[data-size-field]");
  var colourField = root.querySelector("[data-colour-field]");
  var priceEl = root.querySelector("[data-variant-price]");
  var regEl = root.querySelector("[data-variant-regular]");
  var waEl = root.querySelector("[data-variant-wa]");
  var model = data.model_name;
  var variants = data.variants.filter(function (v) {
    return v.active;
  });
  var sel = { size: null, colour: null };

  function isPlaceholder(v) {
    return !v || String(v).trim().toLowerCase() === "standard";
  }

  function displayValues(values) {
    return values.filter(function (v) {
      return !isPlaceholder(v);
    });
  }

  function money(n) {
    if (n == null) return "On Request";
    return "₹" + Number(n).toLocaleString("en-IN");
  }

  function internalColours(size) {
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

  function internalSizes(colour) {
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
    if (!container) return;
    container.innerHTML = "";
    values.forEach(function (val) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip" + (val === current ? " on" : "");
      btn.textContent = val;
      btn.addEventListener("click", function () {
        sel[key] = val;
        if (key === "size") {
          var cols = internalColours(val);
          if (cols.indexOf(sel.colour) < 0) sel.colour = cols[0] || null;
        } else {
          var sizes = internalSizes(val);
          if (sizes.indexOf(sel.size) < 0) sel.size = sizes[0] || null;
        }
        paint();
      });
      container.appendChild(btn);
    });
  }

  function waMessage() {
    var parts = ["Hi Indore Nursery, I'm interested in " + model];
    if (sel.size && !isPlaceholder(sel.size)) parts.push("size " + sel.size);
    if (sel.colour && !isPlaceholder(sel.colour)) parts.push(sel.colour);
    return (
      "https://wa.me/" +
      data.wa_phone +
      "?text=" +
      encodeURIComponent(parts.join(", ") + ". Please share availability and details.")
    );
  }

  function paint() {
    var sizeChoices = displayValues(data.sizes || internalSizes(sel.colour));
    var colourChoices = displayValues(
      (data.colours && data.colours.length ? data.colours : internalColours(sel.size))
    );

    if (sizeField) {
      sizeField.style.display =
        data.show_sizes && sizeChoices.length ? "" : "none";
    }
    if (colourField) {
      colourField.style.display =
        data.show_colours && colourChoices.length ? "" : "none";
    }

    renderChips(sizesEl, sizeChoices, "size", sel.size);
    renderChips(coloursEl, colourChoices, "colour", sel.colour);

    var v = findVariant();
    if (v) {
      priceEl.textContent = money(v.price);
      if (regEl) {
        regEl.textContent =
          v.regular_price && v.regular_price > v.price ? money(v.regular_price) : "";
      }
    } else if (variants.length === 1) {
      priceEl.textContent = money(variants[0].price);
      if (regEl) {
        regEl.textContent =
          variants[0].regular_price && variants[0].regular_price > variants[0].price
            ? money(variants[0].regular_price)
            : "";
      }
    } else {
      priceEl.textContent = sizeChoices.length || colourChoices.length ? "Select options" : money(data.from_price);
      if (regEl) regEl.textContent = "";
    }
    if (waEl) waEl.href = waMessage();
  }

  sel.size = (data.sizes && data.sizes[0]) || (variants[0] && variants[0].size) || null;
  sel.colour = (data.colours && data.colours[0]) || (variants[0] && variants[0].colour) || null;
  paint();
})();
