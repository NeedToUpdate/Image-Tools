const imageContainer = document.getElementById("image-container");

let allImages = [];
function setImages(arr) {
  //   console.log(arr);
  //   imageContainer.childNodes.forEach((node) => {
  //     node.remove();
  //   });
  //   arr.forEach((src) => {
  //     const template = document.getElementById("imageTemplate");
  //     let newImage = template.content.cloneNode(true).childNodes[1];
  //     newImage.childNodes[1].src = src;
  //     imageContainer.appendChild(newImage);
  //
  //   });
  allImages = arr;
  document.getElementById("image-desc").innerText = "Images found: " + arr.length;
}

// setImages(testImages);

eel.get_images()(setImages);
function changeParam(param, value) {
  eel.set_param(param, value);
}
function refreshImages() {
  eel.get_images()(setImages);
}
let RUNNING = false;
let CANCEL = false;
let TOTAL = 0;
function startConversion() {
  if (allImages.length === 0) return;
  if (RUNNING) {
    CANCEL = true;
    document.getElementById("convert-btn").classList.add("disabled");
    return;
  }
  RUNNING = true;
  document.getElementById("convert-btn").classList.add("cancel");
  document.getElementById("convert-btn").innerText = "Cancel";
  document.getElementById("inputs-box").style.height = "85vmin";
  document.getElementById("loading-bar").style.opacity = "";
  document.getElementById("loading-bar").value = "0";
  console.log(allImages);
  requestAnimationFrame(() => {
    convertImage(0);
  });
}

function reset() {
  CANCEL = false;
  RUNNING = false;
  document.getElementById("convert-btn").innerText = "Convert";
  document.getElementById("inputs-box").style.height = "75vmin";
  document.getElementById("loading-bar").style.opacity = 0;
  document.getElementById("loading-bar").value = "0";
  document.getElementById("convert-btn").classList.remove("disabled");
  TOTAL = 0;
}

function convertImage(int) {
  let parts = 100 / allImages.length || 0;
  if (CANCEL) {
    reset();
    return;
  } else {
    eel.convert(allImages[int])(() => {
      TOTAL += parts;
      document.getElementById("loading-bar").value = TOTAL + "";
      if (int == allImages.length - 1) {
        reset();
      } else {
        convertImage(int + 1);
      }
    });
  }
}

document.getElementById("max_res").value = "2100";
document.getElementById("max_res_text").innerText = "None";
document.getElementById("max_res").addEventListener("input", (ev) => {
  document.getElementById("max_res_text").innerText = ev.target.value === "2100" ? "None" : ev.target.value + "px";
  changeParam("max_res", ev.target.value === "2100" ? "None" : ev.target.value);
});
document.getElementById("compression").value = 100;
document.getElementById("compression_text").innerText = "100% (None)";
document.getElementById("compression").addEventListener("input", (ev) => {
  let text = ev.target.value + "%";
  let value = parseInt(ev.target.value);
  if (value < 15) {
    text += " (Tiny)";
  } else if (value < 25) {
    text += " (Small)";
  } else if (value < 50) {
    text += " (Medium)";
  } else if (value < 85) {
    text += " (Regular)";
  } else if (value < 100) {
    text += " (Quality)";
  } else {
    text += " (None)";
  }
  document.getElementById("compression_text").innerText = text;
  changeParam("compression", ev.target.value);
});
document.getElementById("strip_exif").addEventListener("input", (ev) => {
  changeParam("strip_exif", ev.target.checked);
});
document.getElementById("filetype").value = "png";
document.getElementById("filetype").addEventListener("change", (ev) => {
  changeParam("filetype", ev.target.value);
});
document.getElementById("remove_bg").addEventListener("input", (ev) => {
  changeParam("remove_bg", ev.target.checked);
});
document.getElementById("convert-btn").addEventListener("click", startConversion);
document.getElementById("refresh-btn").addEventListener("click", refreshImages);

document.getElementById("inputs-box").style.height = "75vmin";
document.getElementById("loading-bar").style.opacity = 0;
