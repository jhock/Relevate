var trayTrigger = null
var trayListener = null

function handleTrayDocumentClick (event) {
  var tray = document.querySelector('.rv-tray')

  if (!tray.contains(event.target)) {
    closeTray(tray)
  }
}

function closeTray (tray) {
  tray.classList.remove('rv-tray--open')
  tray.setAttribute('aria-hidden', 'true')
  trayTrigger.focus()

  var hideTray = function () {
    tray.classList.add('rv-tray--closed')
  }.bind(this)

  window.setTimeout(hideTray, 200)

  document.removeEventListener('click', handleTrayDocumentClick)
}

function handleTrayTriggerClick (event) {
  trayTrigger = event.target
  var tray = trayTrigger.parentElement.querySelector('.rv-tray')
  if (!tray.classList.contains('rv-tray--open')) {
    tray.classList.remove('rv-tray--closed')
    tray.setAttribute('aria-hidden', 'false')
    var closeButton = tray.querySelector('button[data-tray-close-button]')
    closeButton.focus()

    var showTray = function () {
      tray.classList.add('rv-tray--open')
    }.bind(this)

    window.setTimeout(showTray, 0)

    var appendDocumentListener = function () {
      trayListener = document.addEventListener('click', handleTrayDocumentClick)
    }.bind(this)

    window.setTimeout(appendDocumentListener, 0)
  }
}

function handleTrayCloseButtonClick (event) {
  var closeButton = event.target
  var tray = closeButton.parentElement.parentElement
  closeTray(tray)
}