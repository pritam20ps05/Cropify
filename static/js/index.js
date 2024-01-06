// Using Jquery syntax
var verylow = "var(--very-low)";
var low = "var(--low)";
var medium = "var(--medium)";
var normal = "var(--normal)";
var alkaline = "var(--alkaline)";

var gcolormap = [verylow, normal, alkaline];
var params = ['N', 'P', 'K', 'pH', 'EC', 'OC', 'S', 'Zn', 'Fe', 'Cu', 'Mn', 'B'];

function setGaugeValue(value) {
  if (value < 0 || value > 1) {
    return;
  }

  var gaugefill = $(".gauge .gauge__fill");
  var gaugecover = $(".gauge .gauge__cover");
  var status = $("#status");

  gaugefill.css({transform: `rotate(${value / 2}turn)`});
  gaugecover.text(`${Math.round(value * 100)}%`);

  if (value >= 0 && value < 0.25) {
    gaugefill.css({"background-color": `${verylow}`});
    status.css({color: `${verylow}`});
    status.text("Very low");
  }
  else if (value >= 0.25 && value < 0.5) {
    gaugefill.css({"background-color": `${low}`});
    status.css({color: `${low}`});
    status.text("Low");
  }
  else if (value >= 0.5 && value < 0.75) {
    gaugefill.css({"background-color": `${medium}`});
    status.css({color: `${medium}`});
    status.text("Medium");
  }
  else if (value >= 0.75) {
    gaugefill.css({"background-color": `${normal}`});
    status.css({color: `${normal}`});
    status.text("Normal");
  }
}

$("#nutrient-form").on("submit", (e) => {
  e.preventDefault();
  var values = {};
  $.each($('#nutrient-form').serializeArray(), function(i, field) {
    values[field.name] = parseFloat(field.value);
  });
  console.log(values);

  $.ajax({
    method: "POST",
    url: "/api/fertility",
    data: JSON.stringify({
      input: values,
    }),
    contentType: "application/json",
    dataType: "json",
  }).done((msg) => {
    $("#page2").removeClass("d-none");
    setTimeout(() => {
      window.location = "#page2";
    }, 500);
    console.log(msg);
    setGaugeValue((msg['score']*5 + msg['score1'])/6);
    for (let i = 0; i < 12; i++) {
      let idev = msg['dev'][i];
      let iver = msg['verdict'][i];
      let icol = msg['colorarr'][i];
      
      let nutcard_dev = $(`#nut-${params[i]} .dev`);
      let nutcard_soln = $(`#nut-${params[i]} .soln`);
      let nutcard_verdict = $(`#nut-${params[i]} .verdict`);
      nutcard_soln.addClass("d-none");

      if (idev>=0) {
        nutcard_dev.html(`<div class="up"><i class="fa-solid fa-play"></i><span> ${Math.abs(Math.round(idev*100))}%</span></div>`);
        if (idev==0) {
          $(`#nut-${params[i]} .soln-n`).removeClass("d-none");
        }
        else {
          $(`#nut-${params[i]} .soln-u`).removeClass("d-none");
        }
      }
      else {
        nutcard_dev.html(`<div class="down"><i class="fa-solid fa-play"></i><span> ${Math.abs(Math.round(idev*100))}%</span></div>`);
        $(`#nut-${params[i]} .soln-d`).removeClass("d-none");
      }

      nutcard_verdict.children().text(iver);
      nutcard_verdict.children().css({color: gcolormap[icol-1]});
    }
  });
});

// setGaugeValue(0.9);
