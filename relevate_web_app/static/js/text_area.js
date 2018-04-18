function handleTextAreaFocus (event) {
  var input = event.target
  var label = input.parentElement.getElementsByTagName('label')[0]
  label.classList.add('rv-text-area_focus')
}

function handleTextAreaBlur (event) {
  var input = event.target
  var label = input.parentElement.getElementsByTagName('label')[0]
  label.classList.remove('rv-text-area_focus')
}