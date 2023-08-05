
try {
  new Function("import('/hacsfiles/frontend/main-6af9b8d9.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-6af9b8d9.js';
  document.body.appendChild(el);
}
  