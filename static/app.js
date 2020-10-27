const BASE_URL = "http://127.0.0.1:5000";
const btnMain = document.querySelector(".btnMain");
const btnStart = document.querySelector(".btnStart");
const mainDisplay = document.querySelector("#mainDisplay");
const optionDisplay = document.querySelector("#optionDisplay");
let currTime = 60;
let currScore = 0;

/**
 * Event Listeners
 */
btnMain.addEventListener("click", async () => {
    btnMainClickHandler();
});
btnStart.addEventListener("click", async () => {
    btnOptionClickHandler();
});

/**
 * btnMainClickHandler: Handles button that enters word to be tested during the play of the game.
 * Makes an axios POST to app.py
 */
async function btnMainClickHandler() {
    const input = document.querySelector(".form-control");
    const word = input.value.toUpperCase();
    input.value = "";
    input.focus();
    let res;
    try {
        res = await axios.post(`${BASE_URL}/guess`, {"guess":word});
    }catch(e) {
        console.error(e);
    }
    if(res.data.isFound) {
        const jumboTron = document.querySelector(".correct-guesses");
        jumboTron.innerText += " "+ word;
        updateScore(word.length);
    }
}

/**
 * btnOptionClickHandler: Handles button that enters user entered   size of game board
 * Makes an axios POST to app.py
 */
async function btnOptionClickHandler() {
    let row = document.querySelector(".rowsCount").value;
    let col = document.querySelector(".colsCount").value;
    rows = Math.max(5, row);
    cols = Math.max(5, col);
    row.value = "";
    col.value = "";
    let res;
    try {
        res = await axios.post(`${BASE_URL}/start`, {
            "rows": rows,
            "cols": cols
        });
    }catch(e) {
        console.error(e);
    }
    createTable(res.data.board);
    optionDisplay.className = "hidden";
    mainDisplay.className = "boggle";
    timer();
}

/**
 * createTable: Write a HTML table to boggle.html as the display game board
 */
const createTable = board => {
    const tbody = document.querySelector(".tbody");
    tbody.innerHTML = "";
    for(let row of board) {
        const tr = document.createElement("TR");
        for(let e of row) {
            const td = document.createElement("TD");
            td.innerText = e;
            tr.append(td);
        }
        tbody.append(tr);
    }
}

/**
 * updateScore: Updates the score on the game display
 */
function updateScore(newScore) {
    currScore = newScore ? currScore + newScore : 0;
    let div = document.querySelector("#score");
    let p = document.createElement("p");
    p.innerText = currScore;
    div.replaceChild(p, div.childNodes[3]);
}

/**
 * timer: Timer for each game
 * Stops game after 1 minute
 */
function timer() {
    let time = 60;
    let t = setInterval(() => {
        if(--time > -1) {
            updateTime();
        } else {
            clearInterval(t);
            gameOver();
        }        
    }, 1000);
}

/**
 * updateTime: Decrements the game time displayed on the game board
 */
function updateTime() {
    currTime--;
    let div = document.querySelector("#time");
    let p = document.createElement("p");
    p.innerText = currTime;
    div.replaceChild(p, div.childNodes[3]);
}

/**
 * gameOver: Stops the game and displays the option.html with score and 
 * option to start a new game
 */
function gameOver() {    
    const gameOverScore = document.querySelector("#gameOverScore");
    const row = document.querySelector(".rowsCount").value;
    const col = document.querySelector(".colsCount").value;
    const jumboTron = document.querySelector(".correct-guesses");
    row.innerText = "";
    col.innerText = "";
    jumboTron.innerText = "";
    gameOverScore.className = "gameOverScore";
    gameOverScore.innerText = `Your Score: ${currScore}`;
    optionDisplay.className = "boggle";
    mainDisplay.className = "hidden";
    currScore = 0;
    currTime = "60";
    rows = 0;
    cols = 0; 
    updateScore(0);  
}
