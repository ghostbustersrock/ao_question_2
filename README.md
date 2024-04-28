# Question 2 - Library
##### By Luca Santarelli

## Set-up
**PLEASE NOTE** - I have worked on this project using a **MacBook Pro**.

Once you have cloned the repository (or downloaded the project as a folder):

1. Drag and drop the `ao_question_2` folder into your preferred IDE (I used VSCode).

2. In the command line's root directory (`ao_question_2`), activate the virtual environment (`venv-alliedoffset`) using
`source venv-alliedoffset/bin/activate`.
a. This shouldn't be needed, however, in case you want to be double sure, run the
`pip3 install -r requirements.txt` command to install all necessary libraries for the app to work.

3. In the command line root directory simply execute `flask run`.

All of the app data will be saved in the `library.db` SQLite database. If you wish to view the contents of this SQLite database, I would recommend downloading [DB Browser for SQLite](https://sqlitebrowser.org/ "DB Browser for SQLite") and simply open the `library.db` file within that app.

#### Debugging
If while you are running the app you encounter any database issues (there should not be any FYI), for example, missing tables, issues with the migrations, etc., I would recommend doing a full database and migrations erasure and start with a completely new setup and ready to go database. Please follow the below steps:

1. Remove the `library.db` file and `migrations` folder from the project.
2. In the command line root directory (`ao_question_2`) run the below commands, INDIVIDUALLY:
```python
flask db init
```
```python
flask db migrate -m "<a short description i.e. migration creation>"
```
```python
flask db upgrade
```

This should solve your issue :)

## Testing the endpoints
To test the functinoality of every endpoint, I have saved in the project's root directory a JSON file called `AlliedOffsets - Q2.postman_collection.json`. Please download [Postman](https://www.postman.com/downloads/?utm_source=postman-home "Postman") or use its web portal and import the JSON file into it. This way you will have an already setup `AlliedOffsets - Q2` collection with all requests already set-up and ready to be used to test all of the six API requests implemented in the app. 

**NOTE**: 
1. Please remember to run the Flask app first, before sending any of the Postman requests, otherwise these will not work, as the app is not running.
2. If when you run your Flask app, your localhost port number is different (i.e. not 5000), make sure to change the port number in every of the Postman API requests, as I have always used 5000, as the port number.