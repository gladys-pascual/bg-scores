<h1 align="center">BG-scores</h1>

[View the live project here.](https://bg-scores.herokuapp.com/)

BG scores is a web application that allows user to record the boardgames that they played, including the date of the game, the players and their scores. The application allows for the user to manage the list of boardgames and players in their account.

<img src="./static/assets/bg-scores.gif" alt="BG-scores gif"/>

<br/>
<br/>
<br/>

## User Experience (UX)

<hr>

### User stories

- As a potential user, I want to be able to register for an account.
- As a current user, I want to be able to log in and out of my account.
- As a user, I want to be able to record (create) the games that I played. The game information would include:
  - Boardgame
  - Date of when the game was played
  - The players and their scores
- As a user, I want to see all the games I played in the homepage (read).
- As a user, I want to be able to edit the game I played (update).
- As a user, I want to be able to delete a game I played (delete.
- As a user, I want to be able to manage the board games in my account, by being able to:
  - Create a boardgame
  - See a list of all the boardgames I created
  - Edit the name of a boardgame I created
- As a user, I want to be able to manage the players in my account, by being able to:
  - Create a player
  - See a list of all the players I created
  - Edit the name of a player I created

### Design

- #### Typography and Colour Scheme

  - In this project, [Materialize V1.0.0](https://materializecss.com/) was used to create a responsive front-end. The default typography was used, while [colour palette](https://materializecss.com/color.html) teal, with different shades, were used for the colour scheme.

- #### Logo
  - [Canva](https://www.canva.com/) was used to create a logo for bg-scores.
- #### Favicon
  - BG-scores favicon was used to allow the user to distinguish the tab when multiple tabs are open in their browser, which allows for a better user experience.

- #### Animations
  - logo-bounce-animation: When there is a hover on the logo, logo-bounce-animation is applied to let the user know that the logo is a clickable link. The logo-bounce-animation adds some fun to the website.

### Wireframes

- Wireframes for this project are available [here](wireframe/bg-score.png).

<br>
<br>

## Database architecture
<hr>

This project has four collections:

1. games

   - List of games played by each user, containing information about the game such as the name of the boardgame played, when the game is played, and a list of players and their scores.

     ```
     _id: ObjectId
     boardgame: id of the boardgame played, in string format
     game_date: date of the game, in ISO format
     created_by: user, stored in the session cookie storage, string format
     players_scores: [
       {
       player: id of the player, in string format,
       score: integer,
       isWinner: boolean,
       },
       {
       player: id of the player, in string format,
       score: integer,
       isWinner: boolean,
       },
     ]
     ```

     <img src="./static/assets/db_games.png" alt="structure of the game collection"/>


2. boardgames
   
   ``` 
   _id: ObjectId, 
   boardgame: name of the boardgame as input by the user, in string,
   creaetd_by: user, stored in the session cookie storage, string format 
   ```

3. players
   ```
   _id: ObjectId, 
   player: name of the player as input by the user, in string, 
   creaetd_by: user, stored in the session cookie storage, string format 
   ```

4. users
   ```
   _id: ObjectId, 
   username: string, 
   passsword: string (hash) 
   ```

In this project, the boardgame and player name stored in the game collecttion is the corresponding id (in string format) from the ObjectId, rather than the name of the boardgame or player. This was implemented to ensure that if the player or boardgame name is edited, the correct name will be displayed to the user, as the id will always be the same. 

<br>
<br>

## Features

<hr>

### As a potential user, I want to be able to register for an account.

- Once the page is loaded, the function `get_games()` checks if session cookie storage has a value.
  - If there is sometthing stored in the session cookie, the homepage is loaded.
  - If the session cookie storage is empty, the login page is loaded.
- In the login page, a link that will re-direct the user to the register page is available below the login form.
- The register page asks for a username and a password.
- Once the user clicks submit, a check is performed to see if the username is already in the database. If it's already in the database, a flash message of "Username already exists, please try a new one." is shown. If the username is not in the database, we add it and a flash messae "Registration was succesful." is shown.

<br>

### As a current user, I want to be able to log in of my account.

- The login page asks for a username and password.
- Once submitted, we first perform a check of whether the username exists in the database. If it doesn't exist, a flash message of "Invalid username and/or password" is shown. If the username exists, a check of whether the corresponding password_hash present in the databse matches. If it doesn't match, the same flash message will be shown. We don't want the user to know if it's the username or password that is incorrect to prevent brute forcing into our forms. If the username and password matches, the user is redirected to get_games, which is the homepage and will display all the games previously played.

<br>

### As a user, I want to be able to log out of my account.

- In the header, the user is greated with Hi, `username`!. When hovered,the logout button will be available. Once the logout button is clicked, the data `user` stored in the session cookie will be removed and the user will be redirected to the login page.

<br>

### As a user, I want to be able to record the games that I played, by:

  i) Adding a board game from a list of pre-added board games <br>
  ii) Seeing a list of all my board games <br>
  iii) Editing a name of a board game <br>
  iv) Deleting a board game <br>

- In the homepage, a button labelled as "Add a Game" is available to allow the user to add their game details. Once the button is clicked, the user is navigated to `/add_game` page where a form is available.
- In this form, a the user can:
  - Select a previously added boardgame from the dropdown
  - Pick the date of the game
  - Select players using the dropdown checklist
  - Once the players are selected, an input field will be available beside the player's name wher the user can add their score
  - All these information are required. The user will not be able to submit the form if an information is missing. The line below the input will turn red to let the user know that the information is missing. 
  - Once submitted, the information in the form is inserted and stored in the games collection of the database, in a format discussed in the database architecture section above. Python functions were written to transform the data from what is given by the form inputs to the desired format.
  - Finally, the user is redirected to `/get_games` where the user can see all the games recorded.
  - In the games card, an edit and delete buttons are available.
  - If the edit button is clicked, a similar to add_game form is used for editing the game, with the inputs pre-filled with the information previously filled.
  - The add_game and edit_game forms have a "back to games" button on the top left corner to allow the user to go back in case the change their minds and does not want to add or edit the game. This allows for a better user experience.
  - If the delete button is clicked, the user is asked if they are sure that they want to delete the game. The user can either pick "yes, delete the game", which will delete the game, or "no, don't delete the game", which will bring the user back to the game page without deleting the game.

<br>

### As a user, I want to be able to manage the boardgames in my account, by:

i) Adding a board game <br>
ii) Seeing a list of all my board games <br>
iii) Editing a name of a board game <br>
explain why there's no delete <br>

### As a user, I want to be able to manage the players in my account, by:

i) Adding a player <br>
ii) Seeing a list of all the players <br>
iii) Editing a player's name <br>

<br>

- Adding a new boardgame and player has the same functionality as adding a game. Once submitted, a list of the previously added boardgames or players will be available in the `/get_boardgames` or `/get_players` page, and these boardgames and players will be available in the add / edit games form.
- It has been decided that in this application, the user cannot delete the boardgame or player, and only able to delete it. This is to avoid having an error on the game collection if a boardgame or player is missing in the collection. 
- Instead, the user can edit the boardgame or player. The boardgame and player name stored in the game collecttion is the corresponding id (in string format) from the ObjectId, rather than the name of the boardgame or player. This was implemented to ensure that if the player or boardgame name is edited, the correct name will be displayed to the user, as the id will always be the same. 

### Accessibility

Ensure accessibility throughout the website by:

- Adding 'alt' text on all images.
- Font awesome icons are in an `<i>` tag. A span with a class "sr-only" is added which describes the icons. The "sr-only" class has a display:none in the stylesheet, which hides the text on screen, but allows for screenreader to be read.

<br/>

## Technologies Used

<hr>

The following technologies have been used in this project:

- [Python 3.8.2](https://www.python.org/download/releases/3.0/)
  - Python was used to implement a back-end, by creating the CRUD functionality.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  - Web framework written in Python to allow build web applications.
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
  - A templating engine language for Python and dependent on the Flask framework.
- [MongoDB](https://www.mongodb.com/)
  - A document-oriented database program, where the data is stored.
- [Heroku](https://heroku.com/)
  - Used to deploy the project.
- [HTML](https://www.w3.org/TR/html52/)
  - Used to structure and presenting the web content.
- [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
  - Used for styling the web content.
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
  - Used to make the website interactive.
- [JQuery](https://jquery.com/)
  - JavaScript library used to ensure interactivity, especially on Materialize components to work as intended.
- [Materialize 1.0.0](https://materializecss.com/)
  - CSS framework used for this project for structuring and presenting the content.
- [FontAwesome](https://fontawesome.com/)
  - Font Awesome was used throughout the website to add icons for better aesthetic and UX purposes. <br/><br/>

## Testing

<hr>



The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

- [W3C Markup Validator](https://validator.w3.org/#validate_by_uri) <br>

The warning below appeared:
```
Warning: Section lacks heading. Consider using h2-h6 elements to add identifying headings to all sections.

From line 48, column 5; to line 48, column 13

der>↩↩    <section>↩     
```
To solve, `<h2>` heading were added on `<section>` tags, with a class name of `sr-only` so it does not appear on the page and not change the current UI, but avoid the warning. 

- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_uri) <br>
1. The following errror appeared: 
```
URI : http://bg-scores.herokuapp.com/static/css/style.css
160	a:-webkit-any-link:focus-visible	none is not a outline-offset value : none
```
  This was fixed by changing changing the `outline-offset` from none to 0.

<br>
<br>

2. An error in relation to the imported materialize css exist:
```
URI : https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css
13	.table-of-contents a	Value Error : letter-spacing only 0 can be a unit. You must put a unit after your number : 0.4
```
Since it came from the framework materialize css and not my css, I couldn't rectify the error. The application was checked again to see if this error affects the functionality of the app, and it was concluded that it did not. In additon, there are a number of warnings in relation to the materialize css.

<br>

### During the development, the following issues were encountered:

- Remove white outline on header

- Ensure that only the details added by the specific user is rendered, by
  - adding a "created_by" key in each collection, which adds the session user
  - a check is performed to see if the item "created_by" key matches what is stored in the collection. If it does, then the collection (game, boardgame or player) is shown in the page.
  - this was manually tested to ensure that the functionality works.

- isWinner information is incorrect, not giving the correct boolean result 
  - After investigation, the root cause was determined to be that the scores were being stored as a string
  - To convert to the score from string to integer, the following code is used:
    ```python
    scores = request.form.getlist("score")
    scores_int = [int(score) for score in scores]
    ```
### Manual testing were also performed to ensure that the application works as intended. During this, the following errors were found and were rectified:

1. If the user has a url of edit or delete game, edit boardgame, or edit player (for example, edit game: http://0.0.0.0:5000/edit_game/60bfd8c0e67d2a5f4ac05115), even if the user is logged out, theu can access the edit or delete game, edit boardgame, or edit player. This is a risk because:

   - Unauthorized user, a user that does not have an account, can manipulate the items.
   - As a precaution, edit or delete game, edit boardgame, or edit player are only displayed if a user is logged in by checking the session cookie storage. Otherwise, the user will be navigated to the login page. This code was added for this purpose:

   ```python
   # Check if there is a user data saved in the cookie session storage
   # If not, redirect to login page
   if not session.get("user"):
       return redirect(url_for("login"))
   ```

    <br>

2. Another potential issue was a user can access another users' data if they have a link that contains the id of the item. To avoid this:

   - In the edit game, delete game, edit boardgame, or edit player, an additional if statement was added to check if the user stored in the session cookie storage is the same user that created the item. If not, the `no_access.html` is rendered.
  <img src="./static/assets/no_access.png" alt="no access"/>

   Checks / tests on each below were performed by getting the data from one user, saving the link, logging out, logging in to a different user, then copy pasting the link saved from the previous user, to check if the `no_access.html` would work. 
   
   <br>
   Local version: <br>
   - edit game: working <br>
   - delete game: working <br>
   - edit boardgame: working <br>
   - edit player: working 
   - <br>
     <br>
    Deployed: <br>
   - edit game: working <br>
   - delete game: working <br>
   - edit boardgame: working <br>
   - edit player: working <br>
<br>


3. Create an error handler for 500 and 404. This article, [Flask Error Handling](https://www.askpython.com/python-modules/flask/flask-error-handling), was followed.

<br>

4. Mostv `<i>` tags used for font awesome icons did not have a span with a class "sr-only" is added which describes the icons, where the "sr-only" class has a display:none in the stylesheet, which hides the text on screen, but allows for screenreader to be read. This was rectified.
   
<br>

5. For a new user, there will initially be no game, boardgame or player present. The page was empty, which does not give a great user experience. Therefore, a card component was created to indicate that there is no game, boardgame or player for better user experience.
     <img src="./static/assets/no_game.png" alt="no game"/>
     <img src="./static/assets/no_boardgame.png" alt="no boardgame"/>
     <img src="./static/assets/no_player.png" alt="no player"/>

6. While step 4 was being tested, it was noticed that despite adding a boardgame and player, the `/get_boardgames` and `/get_players` page was not rendering the recently added players. It was found that an error in python code exists, where for games collection was being searched instead of the boardgames and players collection. This was rectified and tested, and was able to display the recently added boardgame and player.

7. Error on the console about missing favicon. Favicon was added based on the information from this [link](https://flask.palletsprojects.com/en/2.0.x/patterns/favicon/).

   
## Deployment

<hr>

### Heroku
1. Create a heroku account. Create a new app and select your region.
2. Prepare the local workspace for Heroku. Create a `requirements.txt` file by:
   ```
   pip3 freeze --local > requirements.txt
   ```
3. Create a Procfile
   ```
   echo web: python app.py > Procfile
   ```
4. Setup the configuration variables in heroku, by: <br>
   IP            = 0.0.0.0 <br>
   PORT          = 5000 <br>
   MONGO_URI     = mongo_db_uri <br>
   SECRET_KEY    = your_secret_key <br>
   MONGO_DBNAME  = your_database_name <br>

5. Connect the GitHub repository to the project and allow for automatic deployment. 
<br>
<br>

### Forking the GitHub Repository

By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps:

1. At the top of the Repository, above the "Settings" Button on the menu, locate the "Fork" Button.
2. You should now have a copy of the original repository in your GitHub account.
   
<br>
<br>

### Making a Local Clone

1. Under the repository name, click "Clone or download".
2. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
3. Open Git Bash.
4. Change the current working directory to the location where you want the cloned directory to be made.
5. Type `git clone`, and then paste the URL you copied in Step 2.

```
git clone https://github.com/USERNAME/REPOSITORY
```

## Credits

<hr>

### Code
- [Hide Arrows From Input Number](https://www.w3schools.com/howto/howto_css_hide_arrow_number.asp)
- [Adding Favicon](https://flask.palletsprojects.com/en/2.0.x/patterns/favicon/)
- [Flask Error Handling](https://www.askpython.com/python-modules/flask/flask-error-handling)

### Content

- All content was written by the developer.

### Acknowledgements

- My mentor, Narender Singh, for continuous helpful feedback.
