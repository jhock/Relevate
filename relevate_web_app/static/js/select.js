function handleSelectClick (event) {
  var input = event.target
  var menu = getMenu(input)

  input.focus()
  showMenu(menu, input)
}

function handleSelectKeyDown (event) {
  var input = event.target
  var menu = getMenu(input)
  var items = getVisibleItems(menu)
  var currentIndex = getHighlightedIndex(menu)
  var editable = isEditable(input)

  var up = event.keyCode === 38
  var down = event.keyCode === 40
  var space = event.keyCode === 32 && !editable
  var enter = event.keyCode === 13
  var esc = event.keyCode === 27
  var tab = event.keyCode === 9

  if (up || down || space || enter || esc) {
    event.preventDefault()

    if ((up || down || space) && !isMenuExpanded(input)) {
      showMenu(menu, input)
      return
    }

    if (up || down) {
      var step
      if (up || down) {
        if (down) {
          step = 1
        } else {
          step = -1
        }

        var newIndex = currentIndex + step

        if (newIndex < 0) {
          addHighlight(items[items.length - 1])
        } else if (newIndex > (items.length - 1)) {
          addHighlight(items[0])
        } else {
          addHighlight(items[newIndex])
        }
      }
    }

    if ((space || enter) && isMenuExpanded(input)) {
      selectItem(items[currentIndex], input)
    }

    if (esc) {
      hideMenu(menu, input)
      input.focus()
    }
  }

  if (tab) {
    hideMenu(menu, input)
  }
}

function handleSelectKeyUp (event) {
  var enter = event.keyCode === 13
  var esc = event.keyCode === 27
  var up = event.keyCode === 38
  var down = event.keyCode === 40
  var tab = event.keyCode === 9
  var shift = event.keyCode === 16
  var space = event.keyCode === 32
  
  if (enter || esc || up || down || tab || shift || space) {
    return
  }

  var input = event.target
  var menu = getMenu(input)

  filterOptions(menu, input)
}

function filterOptions (menu, input) {
  var items = getItems(menu)
  var query = input.value
  var itemsChanged = false

  query = query.trim().toLowerCase().replace(/\s/g, '')
  for (var i = 0; i < items.length; i++) {
    var item = items[i]
    var itemText = item.textContent.trim().toLowerCase().replace(/\s/g, '')
    if (itemText.indexOf(query) === -1) {
      itemsChanged = hideItem(item) || itemsChanged
    } else if (itemText === query) {
      input.value = item.textContent.trim()
    } else {
      itemsChanged = showItem(item) || itemsChanged
    }
  }

  if (itemsChanged) {
    if (!isMenuExpanded(input)) {
      showMenu(menu, input)
    }
    clearHighlightedOption(menu)

    var visibleItems = getVisibleItems(menu)
    if (visibleItems.length === 0) {
      showPlaceholder(menu)
    } else {
      hidePlaceholder(menu)
      highlightSelectInitialOption(menu, input)
    }
  }
}

function handleSelectInputFocus (event) {
  document.body.addEventListener('mousedown', handleSelectDocumentClick, false)
}

function handleSelectInputBlur (event) {
  document.body.removeEventListener('mousedown', handleSelectDocumentClick, false)
}

function handleSelectDocumentClick (event) {
  var target = event.target

  // In theory, the only thing the active element
  // could be here is the input because we assign
  // the click listener to the document body on focus
  // and then remove it on blur
  var input = document.activeElement
  var menu = getMenu(input)
  var select = input.parentElement.parentElement

  if (!select.contains(target)) {
    hideMenu(menu, input)
  }
}

function handleSelectOptionClick (event) {
  var item = event.target
  var input = event.target.parentElement.parentElement.getElementsByTagName('input')[0]
  selectItem(item, input)
}

function handleSelectOptionMouseOver (event) {
  var item = event.target
  var menu = item.parentElement
  var items = getItems(menu)
  addHighlight(item)
}

function getMenu (input) {
  return input.parentElement.parentElement.getElementsByClassName('rv-select_dropdown')[0]
}

function getInput (menu) {
  return menu.parentElement.getElementsByTagName('input')[0]
}

function getItems (menu) {
  return menu.getElementsByClassName('rv-select_option')
}

function getVisibleItems (menu) {
  var items = getItems(menu)
  var visibleItems = []
  for (var i = 0; i < items.length; i++) {
    var item = items[i]
    if (!item.classList.contains('rv-select_option--hidden')) {
      visibleItems.push(item)
    }
  }
  return visibleItems
}

function getDisplayingItems(menu) {
  return menu.getElementsByClassName()
}

function getHighlightedIndex (menu) {
  var items = getVisibleItems(menu)
  for (var i = 0; i < items.length; i++) {
    if (isHighlighted(items[i])) {
      return i
    }
  }
  return 0
}

function getPlaceholder (menu) {
  return menu.querySelector('[class="rv-select_option--placeholder"]')
}

function isMenuExpanded (input) {
  return input.getAttribute('aria-expanded') === 'true'
}

function isHighlighted (item) {
  return item.classList.contains('rv-select_option--highlighted')
}

function isEditable (input) {
  return input.getAttribute('readonly') === null
}

function hideMenu (menu, input) {
  var items = getItems(menu)
  clearHighlightedOption(menu)
  for (var i = 0; i < items.length; i++) {
    showItem(items[i])
  }
  menu.style.display = 'none'
  input.setAttribute('aria-expanded', 'false')
}

function showMenu (menu, input) {
  menu.style.display = 'block'
  input.setAttribute('aria-expanded', 'true')
  highlightSelectInitialOption(menu, input)
}

function hideItem (item) {
  if (!item.classList.contains('rv-select_option--hidden')) {
    item.classList.add('rv-select_option--hidden')
    return true
  }
  return false
}

function showItem (item) {
  if (item.classList.contains('rv-select_option--hidden')) {
    item.classList.remove('rv-select_option--hidden')
    return true
  }
  return false
}

function hidePlaceholder (menu) {
  var placeholder = getPlaceholder(menu)
  placeholder.style.display = 'none'
}

function showPlaceholder (menu) {
  var placeholder = getPlaceholder(menu)
  placeholder.style.display = 'block'
}

function clearHighlightedOption (menu) {
  var items = getItems(menu)
  for (var i = 0; i < items.length; i++) {
    removeHighlight(items[i])
  }
}

function highlightSelectInitialOption (menu, input) {
  var items = getVisibleItems(menu)
  var highlighted = false
  if (items.length > 0) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].textContent.trim() === input.value) {
        addHighlight(items[i])
        return
      }
    }

    addHighlight(items[0])
  }
}

function addHighlight (item) {
  var menu = item.parentElement
  clearHighlightedOption(menu)
  item.classList.add('rv-select_option--highlighted')
  
  var currentIndex = getHighlightedIndex(menu)
  var maxOptions = 6
  var optionHeight = 32

  var scrollTop = menu.scrollTop
  var scrollOffsetItems = scrollTop / optionHeight

  if (scrollOffsetItems + maxOptions < (currentIndex + 1)) {
    var offset = optionHeight * ((currentIndex + 1) - maxOptions)
    menu.scrollTop = offset
  }

  if (scrollOffsetItems > currentIndex) {
    var offset = optionHeight * currentIndex
    menu.scrollTop = offset
  }
}

function removeHighlight (item) {
  item.classList.remove('rv-select_option--highlighted')
}

function selectItem (item, input) {
  var menu = getMenu(input)
  var items = item.parentElement.children
  for (var i = 0; i < items.length; i++) {
    if (input.value !== items[i].textContent.trim()) {
      items[i].setAttribute('aria-selected', 'false')
    }
  }
  var value = item.textContent.trim()
  input.setAttribute('value', value)
  input.value = value
  item.setAttribute('aria-selected', 'true')
  hideMenu(menu, input)
  input.focus()
}
