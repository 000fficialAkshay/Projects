const images = [
  "1.jpg",
  "2.jpg",
  "3.jpg",
  "4.jpg",
  "5.jpg",
  "6.jpg",
  "7.jpg",
  "8.jpg",
  "9.jpg",
  "10.jpg"
];

let lastIndex = -1;

function setRandomImage() {
  let randomIndex;

  do {
    randomIndex = Math.floor(Math.random() * images.length);
  } while (randomIndex === lastIndex);

  lastIndex = randomIndex;

  const imgElement = document.getElementById("bgImage");
  imgElement.style.opacity = 0; // hide before change

  const newImage = new Image();
  newImage.src = images[randomIndex];

  newImage.onload = () => {
    imgElement.src = newImage.src;
    imgElement.style.opacity = 1; // fade in
  };
}

// This changes new tab images 
setRandomImage();
