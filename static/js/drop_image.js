
const dropArea = document.getElementById("drop-area");
let filesDone = 0
let filesToDo = 0
const progressBar = document.getElementById('progress-bar');

//  prevent default behaviors and stop the events from bubbling up any higher than necessary
["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
});
function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

// Add and remove class name 'highlight' to alter styling when hovered
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
});
['drop', 'dragleave'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
});
function highlight(e) {
    dropArea.classList.add('highlight')
}
function unhighlight(e) {
    dropArea.classList.remove('highlight')
}

// gets the data for the files that were dropped and turns it into a list called 'files'
dropArea.addEventListener('drop', handleDrop, false)
function handleDrop(e) {
    const dt = e.dataTransfer
    const files = dt.files
    handleFiles(files)
}

// convert 'files' to an array in order to iterate over it 
function handleFiles(files) {
    files = [...files]
    initializeProgress(files.length)
    files.forEach(uploadFile)
    files.forEach(previewFile)
}

// send files to this url once uploaded
function uploadFile(file) {
    let url = 'PUT YOUR URL HERE'
    let formData = new FormData()

    formData.append('file', file)

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(progressDone)
    .catch(() => { console.log('error'); })
}


function previewFile(file) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function() {
        let img = document.createElement('img')
        img.src = reader.result
        document.getElementById('gallery').appendChild(img)
    }
}

function initializeProgress(numfiles) {
    progressBar.value = 0
    filesDone = 0
    filesToDo = numfiles
}

function progressDone() {
    filesDone++
    progressBar.value = filesDone / filesToDo * 100
}

