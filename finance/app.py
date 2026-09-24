import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    users = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
    cash = users[0]['cash']
    print(cash)

    # Get user currently stocks
    user_stock = db.execute("""SELECT user_id, symbol, SUM(shares) as totalShares
                              FROM transactions
                              WHERE user_id = ?
                              GROUP BY user_id, symbol
                              HAVING totalShares > 0;""", session["user_id"])

    # Create holding dictionary
    hold = []
    # Create variable to track total cash
    totalCash = 0

    # eterate through user stock
    for row in user_stock:
        stock= lookup(row['symbol'])
        total = stock["price"] * row["totalShares"]
        hold.append({
            "symbol" : stock["symbol"],
            "name": stock["name"],
            "shares": row["totalShares"],
            "price": usd(stock["price"]),
            "total": usd(total)
        })
        # Calculate total cash
        totalCash += total

    return render_template("index.html", hold=hold, cash=usd(cash), totalCash=usd(totalCash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure symbol was entred
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # Ensure shares was entred
        if not request.form.get("shares"):
            return apology("must provide share", 400)

         # Ensure user enter valid number
        if not request.form.get("shares").isdigit():
            return apology("Provide integer numbers only", 400)

        # Check if symbol in stock
        symbol = request.form.get("symbol").upper()
        stock =lookup(symbol)

        # Check if stock is empty
        if stock is None:
            return apology("Invalid Symbol", 400)

        # Get the cash of the user
        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        cash = rows[0]["cash"]

        # Get shares
        shares = request.form.get("shares")

        # calculate remaining cash
        remaining_cash = cash - int(shares) *stock["price"]

        # Regect negative numbers
        if remaining_cash < 0:
            return apology("CAN'T AFFORD")

        # Update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", remaining_cash, session["user_id"])

        # Insert into transaction
        db.execute("""
            INSERT INTO transactions(user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?);
        """,
        session["user_id"], stock["symbol"], shares, stock["price"])

        # Alert user
        flash("Bought!")

        # redirect to home page
        return redirect("/")

    else:
        # Otherwise render buy.html
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("""
        SELECT * FROM transactions
        WHERE user_id = ?;""",
         session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensure Symbol is exists
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("INVALID SYMBOL")
        stocked = {
            "name": symbol["name"],
            "symbol": symbol["symbol"],
            "price": usd(symbol["price"])
        }
        return render_template("quoted.html", stocked=stocked)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirme = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password:
            return apology("must provide password")

        if not confirme:
            return apology("must provide password again")

        if password != confirme :
            return apology("Passwords don't matche")

         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Ensure username not in database
        if len(rows) != 0:
            return apology(f"The username '{username}' already exists. Please choose another name.")

        hash = generate_password_hash(password)

        # Insert username into database
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                        username, hash)

        # Remember which user has logged in
        session["user_id"] = id

        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    validShares = db.execute("""SELECT symbol, sum(shares) as totalShares
                                  FROM transactions
                                  WHERE user_id = ?
                                  GROUP BY user_id, symbol
                                  HAVING totalShares > 0;""", session["user_id"])
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        # Ensure symbol was entred
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was entred
        if not shares:
            return apology("must provide share", 400)

         # Ensure user enter valid number
        if not shares.isdigit():
            return apology("Provide integer numbers only", 400)

        for row in validShares :
            if row["symbol"] == symbol:
                if int(shares) > row["totalShares"]:
                    return apology("Too much Shares", 400)


        # Check if symbol in stock
        stock =lookup(symbol)

        # Get the cash of the user
        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        cash = rows[0]["cash"]

        # Get shares
        shares = request.form.get("shares")

        # calculate new cash
        new_cash = cash + int(shares) * stock["price"]


        # Update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", new_cash, session["user_id"])

        # Insert into transaction
        db.execute("""
            INSERT INTO transactions(user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?);
        """,
        session["user_id"], stock["symbol"], - int(shares), stock["price"])

        # Alert user
        flash("Sold")

        # redirect to home page
        return redirect("/")

    else:
        symbols = []
        for row in validShares:
            symbols.append(row["symbol"])
        # Otherwise render buy.html
        return render_template("sell.html", symbols=symbols)

# Allow users to add additional cash to their account
@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        # Get the user entred
        add = request.form.get("cash")
        # Execute original cash
        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        cash = rows[0]["cash"]

        #Calculate new cash
        new_cash= int(add)+ cash

        # Update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", new_cash, session["user_id"])

        # Alert user
        flash("Cash Added")

        # redirect to home page
        return redirect("/")

    else:
        return render_template("add_cash.html")

