var input = document.querySelector('.custom-file-input');
var label = document.getElementById('file-label');

input.addEventListener('change', function() {
  if (input.files.length > 0) {
    label.textContent = input.files[0].name;
  } else {
    label.textContent = "";
  }
});
