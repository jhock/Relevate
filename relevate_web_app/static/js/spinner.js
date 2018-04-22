function renderSpinner (id, loadingMessage) {
  var container = document.getElementById(id)
  container.classList.add('rv-spinner_container')
  container.innerHTML = 
    '<svg class="rv-spinner" width="65px" height="65px" viewBox="0 0 66 66" xmlns="http://www.w3.org/2000/svg">' +
    '<circle class="rv-spinner_path" fill="none" stroke-width="6" stroke-linecap="round" cx="33" cy="33" r="30"></circle>' +
    '</svg>' + 
    '<div class="rv-spinner_loading-message">' + loadingMessage + '</div>'
}