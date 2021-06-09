<h1 align="center">BG-scores</h1>

[View the live project here.](https://bg-scores.herokuapp.com/)

add description of the website

<img src="" alt="BG-scores gif"/>

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

  - #### Colour Scheme
    - XXX

  - #### Typography
    - XXX
     
  - #### Favicon
    -

  - #### Animations
    - logo-bounce-animation: When there is a hover on the logo, logo-bounce-animation is applied to let the user know that the logo is a clickable link. The logo-bounce-animation adds some fun to the website.

### Wireframes

- Wireframes for this project are available [here](wireframe/bg-score.png).

<br>
<br>

## Features
<hr>

### As a potential user, I want to be able to register for an account.

<br>


### As a current user, I want to be able to log in of my account.
- Once the page is loaded, the function `get_games()` checks if session cookie storage has a value. 
  - If there is sometthing stored in the session cookie, the homepage is loaded.
  - If the session cookie storage is empty, the login page is loaded. 
  
<br>

### As a user, I want to be able to log out of my account.

<br>

### As a user, I want to be able to record the games that I played, by:
#### 1. Adding a board game from a list of pre-added board games
#### 2. Seeing a list of all my board games
#### 3. Editing a name of a board game
#### 4. Deleting a board game

<br>

### As a user, I want to be able to manage the board games in my account, by:
#### 1. Adding a board game
#### 2. Seeing a list of all my board games
#### 3.  Editing a name of a board game
explain why there's no delete

<br>

### As a user, I want to be able to manage the players in my account, by:
#### 1. Adding a player
#### 2. Seeing a list of all the players
#### 3. Editing a player's name
<br>

### Accessibility
Ensure accessibility throughout the website by:
  - Adding 'alt' text on all images.
  - Font awesome icons are in an `<i>` tag. A span with a class "sr-only" is added which describes the icons. The "sr-only" class has a display:none in the stylesheet, which hides the text on screen, but allows for screenreader to be read.

<br/>

## Technologies Used
<hr>

The following technologies have been used in this project:
* [Python 3.8.2](https://www.python.org/download/releases/3.0/) 
    * Python is supposed to be the main hero of this project.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * web framework written in Python.
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
    * is used as templating language for Python and its depending framework Flask
* [MongoDB](https://www.mongodb.com/)
    * It is a document-oriented database program.
* [Heroku](https://heroku.com/)
    * It is a cloud platform to run this python project.
* [HTML](https://www.w3.org/TR/html52/) 
    * used to structure and presenting the content.
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
    * used for styling.
* [JQuery](https://jquery.com/)
    * this project used JavaScript in the form of JQuery to simplify DOM manipulation.
* [Materialize 1.0.0](https://materializecss.com/)
    * CSS framework used for structuring and presenting the content.
* [FontAwesome](https://fontawesome.com/)
    * used to create icons. <br/><br/>

## Database architecture
<hr>


## Testing
<hr>

- remove white outline on header


The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

[W3C Markup Validator](https://validator.w3.org/#validate_by_input)

  

- ensure that only the details loaded by the user is rendered:
  - session user added
  - put condition
  - test if that works

- isWinner is incorrect
  - root cause - scores being stored as string
  - convert to string by: 
    ``` python
    scores = request.form.getlist("score")
    scores_int = [int(score) for score in scores]
    ```
- edit game, URL has game_id. If this game_id is incorrect (random digits put by user), a 500 error is given and page doesn't handle it. 
  - Write a function that will handle 500 error
  - Render html template
  - Along with this, write a handler for 404 too
### Manual testing were also performed to ensure that the application works as intended. During this, the following errors were found and were rectified:

1. xxx
2. xxx
3. xxx

## Deployment
<hr>

<br>
<br>
<br>

## Credits
<hr>
- Hide Arrows From Input Number 
https://www.w3schools.com/howto/howto_css_hide_arrow_number.asp

### Code


### Content

- All content was written by the developer.

### Media


### Acknowledgements

- My mentor, Narender Singh, for continuous helpful feedback.


