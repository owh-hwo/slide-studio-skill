/* slide-studio helper: writes "<label> n / N" into every slide's .foot .pg span.
   runtime.js only updates one global counter; per-slide footers also print and export.
   Label comes from <body data-page-label="หน้า"> (empty = just "n / N"). */
(function () {
  var label = document.body.getAttribute('data-page-label');
  if (label === null) label = 'หน้า';
  document.querySelectorAll('.slide').forEach(function (s, i, all) {
    s.querySelectorAll('.foot .pg').forEach(function (e) {
      e.textContent = (label ? label + ' ' : '') + (i + 1) + ' / ' + all.length;
    });
  });
})();
