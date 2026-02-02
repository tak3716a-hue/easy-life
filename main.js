
const generateBtn = document.getElementById("generate");
const numbersDiv = document.getElementById("numbers");
const darkModeToggle = document.getElementById("darkModeToggle");

generateBtn.addEventListener("click", () => {
    generateNumbers();
});

darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

function generateNumbers() {
    numbersDiv.innerHTML = "";
    const numbers = new Set();
    while (numbers.size < 6) {
        const randomNumber = Math.floor(Math.random() * 45) + 1;
        numbers.add(randomNumber);
    }

    for (const number of numbers) {
        const numberEl = document.createElement("div");
        numberEl.classList.add("number");
        numberEl.textContent = number;
        numbersDiv.appendChild(numberEl);
    }
}
