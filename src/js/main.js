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
  //     allImages.push(src);
  //   });
  document.getElementById("image-desc").innerText = "Images found: " + arr.length;
}

let testImages = [
  "../input/anna.jpg",
  "../input/anna.png",
  "../input/ant.jpg",
  "../input/ant.png",
  "../input/arceus.jpg",
  "../input/arceus.png",
  "../input/ariel.jpg",
  "../input/ariel.png",
  "../input/arlo.jpg",
  "../input/arlo.png",
  "../input/ash.jpg",
  "../input/ash.png",
  "../input/baby.jpg",
  "../input/baby.png",
  "../input/baby_groot.jpg",
  "../input/baby_groot.png",
];
// eel.get_images()(setImages);

setImages(testImages);

function changeParam(param, value) {}
function refreshImages() {
  document.getElementById("image-desc").innerText = "Images found: " + arr.length;
}
function startConversion() {
  document.getElementById("inputs-box").style.height = "85vmin";
  document.getElementById("loading-bar");
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
