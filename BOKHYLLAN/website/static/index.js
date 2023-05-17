
function updateLabel(input) {
    var label = document.getElementById('file-label');
    if (input.files.length > 0) {
    label.textContent = input.files[0].name;
    } else {
    label.textContent = "";
    }
}
