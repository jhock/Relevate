function ddmenuHandleMenuTriggerClick (trigger) {
  var menu = trigger.parentElement.getElementsByClassName('rv-dropdown-menu')[0]
  var arrow = menu.parentElement.getElementsByTagName('svg')[0]

  menu.style.display = 'initial'
  menu.setAttribute('aria-hidden', 'false')
  trigger.setAttribute('aria-expanded', 'true')

  if (arrow) {
    arrow.style.transform = 'rotate(90deg)'
  }

  var items = menu.getElementsByClassName('rv-dropdown-menu_item')
  if (items[0]) {
    items[0].focus()
  }
}

function ddmenuHandleMenuItemKeyDown (event, item) {
  var menu = item.parentElement.parentElement
  var items = menu.getElementsByClassName('rv-dropdown-menu_item')
  var trigger = menu.parentElement.getElementsByClassName('rv-dropdown-menu_trigger')[0]
  var arrow = menu.parentElement.getElementsByTagName('svg')[0]

  if (event.key === 'Escape') {
    menu.style.display = 'none'
    menu.setAttribute('aria-hidden', 'true')
    trigger.setAttribute('aria-expanded', 'false')

    if (arrow) {
      arrow.style.transform = 'rotate(0deg)'
    }

    trigger.focus()
    return
  }

  var arrow = false
  var step

  if (event.key === 'ArrowDown') {
    arrow = true
    step = 1
  }

  if (event.key === 'ArrowUp') {
    arrow = true
    step = -1
  }

  if (arrow) {
    event.preventDefault()
    event.stopPropagation

    var index
    for (var i = 0; i < items.length; i++) {
      if (items[i] === item) {
        index = i
        break
      }
    }

    var newIndex = index + step

    if (newIndex < 0) {
      items[items.length - 1].focus()
    } else if (newIndex > (items.length - 1)) {
      items[0].focus()
    } else {
      items[newIndex].focus()
    }
  }
}

function ddmenuHandleMenuItemBlur (event, item) {
  var menu = item.parentElement.parentElement
  var items = menu.getElementsByClassName('rv-dropdown-menu_item')
  var trigger = menu.parentElement.getElementsByClassName('rv-dropdown-menu_trigger')[0]
  var arrow = menu.parentElement.getElementsByTagName('svg')[0]

  setTimeout(function () {
    for (var i = 0; i < items.length; i++) {
      var item = items[i]
      if (item === document.activeElement) {
        return
      }
    }

    menu.style.display = 'none'
    menu.setAttribute('aria-hidden', 'true')
    trigger.setAttribute('aria-expanded', 'false')

    if (arrow) {
      arrow.style.transform = 'rotate(0deg)'
    }

  }, 50)
}