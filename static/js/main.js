//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  console.log("submit");

  if (!imagePreview.src || !imagePreview.src.startsWith("data")) {
    window.alert("Select an image before feeding Picky!");
    return;
  }

  loader.classList.remove("hidden");
  imagePreview.classList.add("loading");

  // call the predict function of the backend
  predictImage(imagePreview.src);
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(loader);
  hide(predResult);
  show(uploadCaption);

  imagePreview.classList.remove("loading");
}

function previewFile(file) {
  // show the preview of the image
  console.log(file.name);

  let reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    imagePreview.classList.remove("loading");

    displayImage(reader.result, "image-preview")
    //displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image) {
  fetch("/gui_predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image),
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong with Picky.");
    });
}

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  hide(loader);

  let food_probs = [];
  let pred_class = "";
  let max_prob = 0;

  Object.keys(data).forEach(function (key) {
    food_probs.push({
      "food": key,
      "value": parseFloat(data[key]),
    });

    if (parseFloat(data[key]) > max_prob) {
      max_prob = parseFloat(data[key]);
      pred_class = key;
    }
  });

  predResult.innerHTML = pred_class;
  console.log(food_probs);
  updateChart(food_probs);
  show(predResult);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}