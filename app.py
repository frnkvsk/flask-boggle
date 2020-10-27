from flask import Flask, request, redirect, render_template, session, jsonify, url_for
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "123abc"

try:
    boggle_game
except:
    boggle_game = Boggle()

@app.route("/")
def home_page():
    return render_template("boggle.html")     
           
@app.route("/start", methods=["POST"])
def start_game():
    req = request.get_json()
    rows = req["rows"]
    cols = req["cols"]           
    boggle_game = Boggle()
    board = boggle_game.make_board(rows, cols)    
    session["boggle"] = board
    session["guesses"] = []
    session["correct_guesses"] = []
    res = {"board": board}
    return res

@app.route("/guess", methods=["POST"])
def guess():
    req = request.get_json()
    guess = req["guess"].upper()
    board = session["boggle"]
    guesses = session["guesses"]
    correct_guesses = session["correct_guesses"]
    check_guess = False
    if guess not in guesses:
        check_guess = boggle_game.check_valid_word(board, guess)
        if check_guess:
            correct_guesses.append(guess)
            session["correct_guesses"] = correct_guesses
            guesses.append(guess)
            session["guesses"] = guesses
        
    res = {"isFound": check_guess}
    return res     

if __name__ == "__main__":
    app.run()
    