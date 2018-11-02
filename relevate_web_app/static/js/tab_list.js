function handleTabClick (event) {
  var tab = event.target
  var tabList = tab.parentElement
  var tabs = tabList.querySelectorAll('.rv-tab')

  for (var i = 0; i < tabs.length; i++) {
    var currentTab = tabs[i]
    if (tab === currentTab) {
      changeToTab(tabList, tab)
    }
  }
}

function handleTabKeyDown(event) {
  var tab = event.target
  var tabList = tab.parentElement
  var tabs = tabList.querySelectorAll('.rv-tab')

  var activeIndex = 0
  for (var i = 0; i < tabs.length; i++) {
    var currentTab = tabs[i]
    if (tab === currentTab) {
      activeIndex = i
    }
  }

  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    activeIndex -= 1
  }

  if (event.key === 'ArrowRight') {
    event.preventDefault()
    activeIndex += 1
  }

  if (activeIndex < 0) {
    activeIndex = tabs.length - 1
  }

  if (activeIndex > tabs.length - 1) {
    activeIndex = 0
  }

  changeToTab(tabList, tabs[activeIndex])
}

function changeToTab(tabList, tab) {
  var activePanelClass = 'rv-tab-panel--active'

  if (tab.getAttribute('aria-selected') !== 'true') {
    // deselect the old tab
    var currentActiveTab = tabList.querySelector('[aria-selected="true"]')
    currentActiveTab.setAttribute('tabindex', '-1')
    currentActiveTab.setAttribute('aria-selected', 'false')

    // remove the class from the current active panel
    var currentActivePanel = findCorrespondingTabPanel(currentActiveTab, tabList)
    currentActivePanel.classList.remove(activePanelClass)
    currentActivePanel.setAttribute('aria-hidden', 'true')

    // make the new tab active/selected
    tab.setAttribute('tabindex', '0')
    tab.setAttribute('aria-selected', 'true')
    tab.focus()

    // add the active class to the new panel
    var panel = findCorrespondingTabPanel(tab, tabList)
    panel.classList.add(activePanelClass)
    panel.setAttribute('aria-hidden', 'false')
  }
}

function findCorrespondingTabPanel(tab, tabList) {
  return tabList.querySelector(
    '[aria-labelledby="' + tab.id + '"]'
  )
}