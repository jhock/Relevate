var trigger = null

function handleTrayTriggerClick (event) {
  trigger = event.target
  var tray = trigger.parentElement.querySelector('.rv-tray')
  if (!tray.classList.contains('rv-tray--open')) {
    tray.classList.remove('rv-tray--closed')
    tray.setAttribute('aria-hidden', 'false')
    var closeButton = tray.querySelector('button[data-tray-close-button]')
    closeButton.focus()

    var showTray = function () {
      tray.classList.add('rv-tray--open')
    }.bind(this)

    window.setTimeout(showTray, 0)
  }
}

function handleTrayCloseButtonClick (event) {
  var closeButton = event.target
  var tray = closeButton.parentElement.parentElement
  tray.classList.remove('rv-tray--open')
  tray.setAttribute('aria-hidden', 'true')
  trigger.focus()

  var hideTray = function () {
    tray.classList.add('rv-tray--closed')
  }.bind(this)

  window.setTimeout(hideTray, 200)
}