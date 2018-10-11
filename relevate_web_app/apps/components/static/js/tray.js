var trigger = null

function handleTrayTriggerClick (event) {
  trigger = event.target
  var tray = trigger.parentElement.querySelector('.rv-tray')
  if (!tray.classList.contains('rv-tray--open')) {
    tray.classList.add('rv-tray--open')
    var closeButton = tray.querySelector('button[data-tray-close-button]')
    closeButton.focus()
  }
}

function handleTrayCloseButtonClick (event) {
  var closeButton = event.target
  var tray = closeButton.parentElement.parentElement
  tray.classList.remove('rv-tray--open')
  trigger.focus()
}