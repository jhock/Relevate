function handleFileInputChange (event) {
  var input = event.target
  var icon = input.parentElement.querySelector('[data-file-icon]')
  var filename = input.parentElement.querySelector('[data-filename]')
  var files = input.files

  if (files.length > 0) {
    var file = files[0]
    filename.textContent = file.name
    icon.classList.remove('hidden')
    filename.classList.remove('rv-file-input_instructions')
    filename.classList.add('rv-file-input_file-name')
  } else {
    icon.classList.add('hidden')
    filename.textContent = 'No file chosen'
    filename.classList.remove('rv-file-input_file-name')
    filename.classList.add('rv-file-input_instructions')
  }
}

function handleFileInputDragEnter (event) {
  event.preventDefault()
  var input = event.target
  var dragging = input.parentElement.querySelector('[data-dragging]')
  dragging.classList.remove('hidden')
}

function handleFileInputDragLeave (event) {
  var input = event.target
  var dragging = input.parentElement.querySelector('[data-dragging]')
  dragging.classList.add('hidden')
}

function handleFileInputDrop (event) {
  var input = event.target
  var dragging = input.parentElement.querySelector('[data-dragging]')
  dragging.classList.add('hidden')
  input.files = event.dataTransfer.files
}