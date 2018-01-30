function handleTextInputFocus (event) {
  var input = event.target
  var label = input.parentElement.getElementsByTagName('label')[0]
  label.classList.add('rv-text-input_focus')
  console.log('got focus')
}

function handleTextInputBlur (event) {
  var input = event.target
  var label = input.parentElement.getElementsByTagName('label')[0]
  label.classList.remove('rv-text-input_focus')
  console.log('lost focus')
}