import os
from flask import (Flask, flash, render_template, 
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# Function to transform from DB format of 
# players collection to ideal template
def mapPlayer(p):
    updated_player = {
        "_id": str(p["_id"]),
        "player": p["player"]
    }
    return updated_player


# Function to transform from DB format of 
# boardgames collection to ideal template
def mapBoardgame(bg):
    updated_boardgame = {
        "_id": str(bg["_id"]),
        "boardgame": bg["boardgame"]
    }
    return updated_boardgame


# Function to compare the ObjectId of the boardgames and players from
# the boardgames and player collection to the data in the games collection
def mapGame(game):
    players = list(mongo.db.players.find())
    boardgames = list(mongo.db.boardgames.find())

    for bg in boardgames:
        if str(bg["_id"]) == game["boardgame"]:
            game["game_name"] = bg["boardgame"]

    for p in players:
        for bg_player in game["players_scores"]:
            if str(p["_id"]) == bg_player["player"]:
                bg_player["player_name"] = p["player"]
    return game


# Function that creates the players_scores array
# that will be added to the database
def mapPlayersScores():
    scores = request.form.getlist("score")
    players = request.form.getlist("player")
    players_scores = []
    for i in range(len(scores)):
        players_scores.append({
            "player": players[i],
            "score": scores[i],
            "isWinner": max(scores) == scores[i]
        })
    return players_scores


@app.route("/")
@app.route("/get_games")
def get_games():
    if session:
        games = mongo.db.games.find()
        players = list(mongo.db.players.find())
        boardgames = list(mongo.db.boardgames.find())
        return render_template("games.html", 
            games=map(mapGame, games), players=map(mapPlayer, players), boardgames=map(mapBoardgame, boardgames))
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists, please try a new one.")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        flash("Registration was successful!")
        return render_template("login.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for("get_games"))
            else:
                # Invalid password match
                flash("Invalid username and/or password.")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect username and/or password.")
            return redirect(url_for("login"))
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game = {
            "boardgame": request.form.get("boardgame"),
            "game_date": request.form.get("game_date"),
            "created_by": session["user"],
        }
        game['players_scores'] = mapPlayersScores()
        mongo.db.games.insert_one(game)
        
        flash("Game added sucessfully!")
        return redirect(url_for("get_games"))
    
    players = list(mongo.db.players.find().sort("player", 1))
    boardgames = list(mongo.db.boardgames.find().sort("boardgame", 1))
    return render_template("add_game.html", players=map(mapPlayer, players), boardgames=map(mapBoardgame, boardgames))


@app.route("/get_boardgames")
def get_boardgames():
    boardgames = list(mongo.db.boardgames.find())
    return render_template("boardgames.html", boardgames=map(mapBoardgame, boardgames))


@app.route("/get_players")
def get_players():
    players = list(mongo.db.players.find())
    return render_template("players.html", players=map(mapPlayer, players))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
# make sure to put debug = False prior to submitting project