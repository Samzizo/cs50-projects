"""Tester App"""
# import os
import random
# from models import *
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# allow zip for using with jinja
app.jinja_env.filters['zip'] = zip


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Home page
@app.route("/")
def tester():
    """home page"""
    return render_template("tester.html")

# List of questions
@app.route("/list", methods=["GET", "POST"])
def listed():
    """Show all question to review with thier answers"""
    if request.method == "POST" and "language" in request.form:
        language = request.form.get("language")
        if request.form['language'] == language:
            if language == 'All':
                data = db.execute("SELECT * FROM questions")
                question = []
                answer = []
                index = []
                for x in data:
                    question.append(x["question"])
                    answer.append(x["answer"])
                    index.append(x["id"])
                return render_template("list.html", data=zip(question,answer,index))

            lang = db.execute("SELECT * FROM questions WHERE language = ?", language)
            question = []
            answer = []
            index = []
            for i in lang:
                question.append(i["question"])
                answer.append(i["answer"])
                index.append(i["id"])
            return render_template("list.html", data=zip(question,answer,index))

    if request.method == "POST" and "deleted" in request.form:
        index = request.form.get("deleted")
        db.execute("DELETE FROM questions WHERE id=?", index)
        flash("question deleted")
        # rearange ids after deleting a question
        db.execute("UPDATE questions SET id = id - 1 WHERE id > ?", index)
        return redirect("/")


    data = db.execute("SELECT * FROM questions")
    question = []
    answer = []
    index = []
    for info in data:
        question.append(info["question"])
        answer.append(info["answer"])
        index.append(info["id"])
    return render_template("list.html", data=zip(question,answer,index))



# ADD question
@app.route("/add", methods=["GET", "POST"])
def add():
    """Add question"""
    question = request.form.get('question')
    answer = request.form.get('answer')
    language = request.form.get('language')
    if request.method == "POST":
        if request.form['submit_button']:
            if not question or not answer:
                flash("must provide question and answer")
                return render_template("add.html")

            db.execute(
                """ INSERT INTO questions (question, answer, language) VALUES (?, ?, ?)""",
                question, answer, language
            )
            flash('Question added')
            data = db.execute("SELECT * FROM questions")
            questions = []
            answers = []
            index = []
            for info in data:
                questions.append(info["question"])
                answers.append(info["answer"])
                index.append(info["id"])
            return render_template("list.html", data=zip(questions,answers,index))

    return render_template("add.html")

# reset score to 0 When play again
@app.before_request
def reset_counter():
    global score
    if "back"  in request.form:
        score = 0


# Store question IDs and language choosen throughout session
question_ids = []
language_choosen = []
# Store score
score = 0
# calculate if there is wrong answers
wrong = []

# # play quiz
@app.route("/play", methods=["GET", "POST"])
def play():
    """Play quizz"""
    """create global variables for easy access to all scopes"""

    #create variable to track questions asked and score
    global question_ids
    global language_choosen
    global score
    global wrong

    # Retrieve the username from the session
    username = session.get('username')

    #  Select all languages in questions table
    language = db.execute("""SELECT DISTINCT language FROM questions """)

    # create languages list and add all to it to create list of filter dynamically
    languages=["All"]

    # Set the title to hide it when necessary
    title = "Choose the language"

    # append all languages found in questions table
    for lang in language:
        if lang not in languages:
            languages.append(lang['language'])
    

    if request.method == "POST" and "language" in request.form:
        # variable to hold language
        language_choosen = request.form.get("language")
        
        if request.form['language'] == language_choosen:
            if language_choosen == "All":
                all_questions = db.execute("""SELECT question , id FROM questions ORDER BY RANDOM()""")
            else:
                all_questions = db.execute("""SELECT question , id FROM questions WHERE language = ? ORDER BY RANDOM()""", language_choosen)

            questions= []

            # Get a specific set of questions based on user selection
            for q in all_questions:
                question_ids.append(q['id'])
                questions.append(q['question'])
                # Create randomized order of questions
            question=random.choice(questions)

        return render_template("play.html", question=question, title="Quiz")


    if request.method == "POST" and "check" in request.form:
        answer = request.form.get('answer')
        print(answer)

        question = request.form.get('question')
        print(question)

        check = db.execute(""" SELECT answer FROM questions WHERE question=? """, question)
        question_id = db.execute(""" SELECT id from questions WHERE question=?""", question)

        print("question ids: ", question_ids)
        print("question id : ", question_id[0]['id'])

        ids = question_id[0]['id']
        print("type : ", type(ids))

        previous_question=[]
        for p in question_id:
            previous_question.append(p['id'])

        print("previous : ", previous_question)
        print("check : ", check)
        checked =[]

        for i in check:
            checked.append(i["answer"])
        print("answer ",answer)

        """
        Calcuate Score
        """
        # check the answer if correct
        if checked[0].upper() == answer.upper():
            # calculate score if it is correct from the first time
            if question_id[0]['id'] not in wrong:
                score = score + 1
            print("score is : ", score)
            for q in previous_question:
                if q in question_ids:
                    question_ids.remove(q)
            print(question_ids)
            if len(question_ids) !=0:
                flash("Correct")

        # Check if Not correct
        if checked[0].upper() != answer.upper():
            # calculate score
            if question_id[0]['id'] not in wrong:
                wrong.append(question_id[0]['id'])
            print("wrong " ,wrong)
            flash("InCorrect try again")
        

        #calculate score at the end of session
        if len(question_ids) == 0:
            if 'user_id' in session:
                user_id = session['user_id']
                username = db.execute( """ SELECT username FROM users WHERE id = ? """, user_id)
                print("username: ", username)
                print("user_id: ", user_id)
                # save result for user
                # get score from data base:
                high_score = db.execute("""SELECT score FROM users WHERE id=? """, user_id)

                # If the high score is None, treat it as a negative infinity for comparison purposes
                high_score_value = high_score[0]['score'] if high_score[0]['score'] is not None else float('-inf')

                if high_score_value < score:
                    result = db.execute("""UPDATE users SET score = ?, language = ? WHERE id = ?""", score, language_choosen, user_id)
                    print("result ",result)

                return render_template("score.html", score=score, username=username[0]['username'])

            if 'user_id' not in session:
                return render_template("score.html", score=score, username='Anonymous')

        """
        Post next question filtred by language choosen
        """
        if language_choosen == 'All':
            print("question ids 2: ", question_ids)
            #check if question_ids not emty
            if len(question_ids) !=0:
                next_questions = db.execute(""" SELECT * FROM questions WHERE id IN (?)""" , question_ids)

        else: 
            if len(question_ids) !=0:
                next_questions = db.execute(""" SELECT question FROM questions WHERE language==? AND id IN (?) """,
                                        language_choosen, question_ids)
        print(f"next_questions: {next_questions}")

        next_question = []
        for n in next_questions:
            next_question.append(n["question"])
        print("next question else : ", next_question)
        print(f"next_question: {next_question}")

        return render_template("play.html", question=next_question[0])
    return render_template("play.html", languages=languages, title=title)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("invalid username and/or password", 403)
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash(f"Welcom {username} :)")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign():
    """sign up"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirme = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Ensure username not in database
        if len(rows) != 0:
            flash(f"The username '{username}' already exists. Please choose another name Or Login.")
            return render_template("sign_up.html")


        if not username:
            flash("must provide username")


        if not password:
            flash("must provide password")
            return render_template("sign_up.html")

        if not confirme:
            flash("must provide password again")
            return render_template("sign_up.html")

        if password != confirme :
            flash("Passwords don't matche")
            return render_template("sign_up.html")

        hashes = generate_password_hash(password)

        # Insert username into database
        index = db.execute("INSERT INTO users (username, password) VALUES (?, ?);",
                        username, hashes)

        # Remember which user has logged in
        session["user_id"] = index

        flash("Registered!")

        return redirect("/")

    return render_template("sign_up.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash("You loged out")

    # Redirect user to login form
    return redirect("/")

# flask run -h localhost -p 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
