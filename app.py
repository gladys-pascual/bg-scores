import os
from copy import copy
from datetime import datetime
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

### FUNCTIONS ###
# Function to transform the format of the player collection
# in the database to ideal format where the _id is converted to string
# and player converted from player id to actual player name
def mapPlayer(p):
    updated_player = {
        "_id": str(p["_id"]),
        "player": p["player"],
        "created_by": p["created_by"]
    }
    return updated_player


# Function to transform from format of the boardgame collection
# in the database to an ideal format where the _id is converted to string
# and boardgame converted from boardgame id to actual boardgame name
def mapBoardgame(bg):
    updated_boardgame = {
        "_id": str(bg["_id"]),
        "boardgame": bg["boardgame"],
        "created_by": bg["created_by"]
    }
    return updated_boardgame


# Function to compare the ObjectId of the boardgames and players from
# the boardgames and player collection to the data in the games collection
def mapGame(game):
    players = list(mongo.db.players.find())
    boardgames = list(mongo.db.boardgames.find())

    game["game_date"] = game["game_date"].strftime('%d %b %Y')

    for bg in boardgames:
        if str(bg["_id"]) == game["boardgame"]:
            game["game_name"] = bg["boardgame"]

    for p in players:
        for bg_player in game["players_scores"]:
            if str(p["_id"]) == bg_player["player"]:
                bg_player["player_name"] = p["player"]

    return game


# Function that adds selected (true/false) property to all players
# to use in pre-selecting select element
def mapSelectedPlayers(players, selected_player_ids):
    updated_players = []
    for i in range(len(players)):
        updated_player = mapPlayer(players[i])
        updated_player['selected'] = True if updated_player['_id'] in selected_player_ids else False
        updated_players.append(updated_player)

    return updated_players


# Function that maps players object list to player ids list
def mapToPlayerIds(players):
    return map(lambda p: p['player'], players)


# Function that loops through selected_players
# find selected_player in players then add name to it
def mapSelectedPlayersScores(players, selected_players):
    players_name_dict = {
        str(players[i]['_id']): players[i]['player'] for i in range(0, len(players))}
    updated_selected_players = []
    for i in range(len(selected_players)):
        updated_selected_player = copy(selected_players[i])
        updated_selected_player['name'] = players_name_dict[updated_selected_player['player']]
        updated_selected_players.append(updated_selected_player)
    return updated_selected_players


# Function that creates the players_scores array
# that will be added to the database
def mapPlayersScores(players, scores):
    players_scores = []
    for i in range(len(scores)):
        players_scores.append({
            "player": players[i],
            "score": scores[i],
            "isWinner": max(scores) == scores[i]
        })
    return players_scores


#############################################


@app.route("/")
@app.route("/get_games")
def get_games():
    if session:
        games = list(mongo.db.games.find().sort("game_date", -1))
        players = list(mongo.db.players.find())
        boardgames = list(mongo.db.boardgames.find())

        # Check if the user does not have a game yet
        user = session.get("user")
        user_games = list(mongo.db.games.find({"created_by": user}))
        if len(user_games) == 0:
            return render_template("no_games.html")

        return render_template("games.html",
                               games=map(mapGame, games), players=map(mapPlayer, players),
                               boardgames=map(mapBoardgame, boardgames))

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
    # Check if there is a user data saved in the cookie session storage
    # If not, redirect to login page
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        game = {
            "boardgame": request.form.get("boardgame"),
            "game_date": datetime.strptime(request.form.get('game_date'), '%d %b %Y'),
            "created_by": session["user"],
        }
        scores = request.form.getlist("score")
        scores_int = [int(score) for score in scores]
        players = request.form.getlist("player")
        game['players_scores'] = mapPlayersScores(players, scores_int)
        mongo.db.games.insert_one(game)

        flash("Game was sucessfully added!")
        return redirect(url_for("get_games"))
    players = list(mongo.db.players.find().sort("player", 1))
    boardgames = list(mongo.db.boardgames.find().sort("boardgame", 1))
    return render_template("add_game.html", players=map(mapPlayer, players), boardgames=map(mapBoardgame, boardgames))


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        edit_game = {
            "boardgame": request.form.get("edit_bg"),
            "game_date": datetime.strptime(request.form.get("edit_game_date"), '%d %b %Y'),
            "created_by": session["user"],
        }
        edit_players = request.form.getlist("edit_p")
        edit_scores = request.form.getlist("edit_score")
        edit_scores_int = [int(score) for score in edit_scores]
        edit_game['players_scores'] = mapPlayersScores(
            edit_players, edit_scores_int)
        mongo.db.games.update({"_id": ObjectId(game_id)}, edit_game)
        flash("Game was sucessfully edited!")
        return redirect(url_for("get_games"))

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    game_date = game["game_date"].strftime('%d %b %Y')
    edit_players_scores = game["players_scores"]
    players = list(mongo.db.players.find().sort("player", 1))
    boardgames = list(mongo.db.boardgames.find().sort("boardgame", 1))

    edit_game_creator = game["created_by"]
    if session.get("user").lower() != edit_game_creator.lower():
        return render_template("no_access.html")

    return render_template("edit_game.html", game=game, game_date=game_date, edit_players_scores=mapSelectedPlayersScores(players, edit_players_scores),
                           players=mapSelectedPlayers(players, list(mapToPlayerIds(edit_players_scores))), boardgames=map(mapBoardgame, boardgames))


@app.route("/delete_game_confirmation/<game_id>")
def delete_game_confirmation(game_id):
    if not session.get("user"):
        return redirect(url_for("login"))

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    delete_game_creator = game["created_by"]
    if session.get("user").lower() != delete_game_creator.lower():
        return render_template("no_access.html")
    return render_template("delete_game_confirmation.html", game=game)


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    if not session.get("user"):
        return redirect(url_for("login"))

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    delete_game_creator = game["created_by"]
    if session.get("user").lower() != delete_game_creator.lower():
        return render_template("no_access.html")

    mongo.db.games.remove({"_id": ObjectId(game_id)})
    flash("Game successfully deleted.")
    return redirect(url_for("get_games"))


@app.route("/get_boardgames")
def get_boardgames():
    if not session.get("user"):
        return redirect(url_for("login"))

    boardgames = list(mongo.db.boardgames.find().sort("boardgame", 1))

    # Check if the user does not have a boardgame yet
    user = session.get("user")
    user_boardgames = list(mongo.db.boardgames.find({"created_by": user}))
    if len(user_boardgames) == 0:
        return render_template("no_boardgames.html")

    return render_template("boardgames.html", boardgames=map(mapBoardgame, boardgames))


@app.route("/add_boardgame", methods=["GET", "POST"])
def add_boardgame():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        boardgame = {
            "boardgame": request.form.get("add_boardgame"),
            "created_by": session["user"],
        }
        mongo.db.boardgames.insert_one(boardgame)
        flash("Boardgame was sucessfully added.")
        return redirect(url_for("get_boardgames"))
    return render_template("add_boardgame.html")


@app.route("/edit_boardgame/<boardgame_id>", methods=["GET", "POST"])
def edit_boardgame(boardgame_id):
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        submit_bg = {
            "boardgame": request.form.get("edit_boardgame"),
            "created_by": session["user"],
        }
        mongo.db.boardgames.update({"_id": ObjectId(boardgame_id)}, submit_bg)
        flash("Boardgame was sucessfully edited!")
        return redirect(url_for("get_boardgames"))

    boardgame = mongo.db.boardgames.find_one({"_id": ObjectId(boardgame_id)})
    edit_bg_creator = boardgame["created_by"]
    if session.get("user").lower() != edit_bg_creator.lower():
        return render_template("no_access.html")

    return render_template("edit_boardgame.html", boardgame=boardgame)


@app.route("/get_players")
def get_players():
    if not session.get("user"):
        return redirect(url_for("login"))

    players = list(mongo.db.players.find().sort("player", 1))

    # Check if the user does not have a player yet
    user = session.get("user")
    user_players = list(mongo.db.players.find({"created_by": user}))
    if len(user_players) == 0:
        return render_template("no_players.html")

    return render_template("players.html", players=map(mapPlayer, players))


@app.route("/add_player", methods=["GET", "POST"])
def add_player():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        player = {
            "player": request.form.get("add_player"),
            "created_by": session["user"],
        }
        mongo.db.players.insert_one(player)
        flash("Player was added sucessfully!")
        return redirect(url_for("get_players"))
    return render_template("add_player.html")


@app.route("/edit_player/<player_id>", methods=["GET", "POST"])
def edit_player(player_id):
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        submit_bg = {
            "player": request.form.get("edit_player"),
            "created_by": session["user"],
        }
        mongo.db.players.update({"_id": ObjectId(player_id)}, submit_bg)
        flash("Player was sucessfully edited!")
        return redirect(url_for("get_players"))

    player = mongo.db.players.find_one({"_id": ObjectId(player_id)})
    edit_player_creator = player["created_by"]
    if session.get("user").lower() != edit_player_creator.lower():
        return render_template("no_access.html")

    return render_template("edit_player.html", player=player)


# Handling error 404 and displaying relevant webpage
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# 500 Error Page
@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
# make sure to put debug = False prior to submitting project
