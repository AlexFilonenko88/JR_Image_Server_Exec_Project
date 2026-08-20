const allImgBloks = document.querySelectorAll('.hero__img');
const randomIndex = Math.floor(Math.random() * allImgBloks.length);
const randomBlock = allImgBloks[randomIndex];
randomBlock.classList.add('is-visible');

document.body.style.setProperty('background-color', '#517864');



