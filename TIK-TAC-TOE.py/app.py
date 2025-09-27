from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)

board = [[" " for _ in range(3)] for _ in range(3)]
players = ["X", "O"]
turn = 0
mode = None  # "friend" or "computer"


def check_winner(player_symbol):
    for i in range(3):
        if all(board[i][j] == player_symbol for j in range(3)):
            return True
        if all(board[j][i] == player_symbol for j in range(3)):
            return True
    if all(board[i][i] == player_symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == player_symbol for i in range(3)):
        return True
    return False


def is_full():
    return all(cell != " " for row in board for cell in row)


def available_moves():
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]


def computer_move():
    moves = available_moves()
    # Try winning move
    for r, c in moves:
        board[r][c] = "O"
        if check_winner("O"):
            return
        board[r][c] = " "
    # Try blocking player
    for r, c in moves:  
        board[r][c] = "X"
        if check_winner("X"):
            board[r][c] = "O"
            return
        board[r][c] = " "
    # Else random
    if moves:
        r, c = random.choice(moves)
        board[r][c] = "O"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tic-tac-toe")
def tic_tac_toe_mode():
    return render_template("mode.html")


@app.route("/start/<string:selected_mode>")
def start(selected_mode):
    global board, turn, mode
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    mode = selected_mode
    return redirect(url_for("index"))


@app.route("/game")
def index():
    winner = None
    draw = False

    if check_winner("X"):
        winner = "X"
    elif check_winner("O"):
        winner = "O"
    elif is_full():
        draw = True

    return render_template(
        "index.html", board=board, winner=winner, draw=draw, turn=players[turn % 2], mode=mode
    )


@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    global turn
    if board[row][col] == " " and not check_winner("X") and not check_winner("O"):
        if mode == "friend":  # Two players
            board[row][col] = players[turn % 2]
            turn += 1
        elif mode == "computer":  # Player vs AI
            board[row][col] = "X"
            if not check_winner("X") and not is_full():
                computer_move()
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    global board, turn
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)