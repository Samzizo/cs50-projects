# TESTER ❓
#### Video Demo: [Final project cs50 presentation](https://www.youtube.com/watch?v=Fn8pOD8PRUY)!
#### Description:
This website was designed for the final project of the CS50 course in 2022.

### Note: 
**This site can be developed and is only a prototype as a collection of some of what I learned in this wonderful course.**

#### Project Idea
The main purpose is to create a web application that allows users learning about some common programming languages such as:
- JavaScript.
- Java.
- C.
- Python.

### Content:
#### Tester:
On the home page you find a full explanation of what the entire site contains and how to use it, also explained in the video attached to the link.
#### List:
Here you can view the list of existing questions with the answers attached underneath so that you can study the information before the exam.
It also contains a filter through which you can view only the questions according to the chosen language or all of them if **ALL** are selected.

#### Add:
On the Add page, you find a form for adding the question, its answer, and the language in question. After that, you can find what you added on the previous page of the list.

#### Play:
Here what you have learned will be tested from the list page. The questions will be random and unordered.
If your answer is correct from the first time, a point will be added to your total. If it is wrong, the question will be repeated until the correct answer is provided, and a mark will not be calculated for it.
When the list of questions is completed, you will be transferred to the Score page with your final result announced
If you want your name to be mentioned in it, log in.

#### Sign Up:
You will find three fields to fill in:
1-  The username, and here the user must not have previously registered with the same name.
2- password, which must be filled in and must match the third field.
After completing filling in all the information, you can then log in From the Login page.

#### Login:
In This page insert your username that you sign up with and the correct password.

#### Logout:
When logging out, all data related to the current session will be deleted from the server.

### Tools used for development
The site was developed using:
- HTML for structure
- CSS for site decoration
As for backend, I used:
- Ginja to connect it to frontend
- Python
- Flask

And for Data. I used:
- sqlite3
You will find the database attached to a file named **project.db**
I used these queries to Create questions and users tables:
```
CREATE TABLE IF NOT EXISTS questions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        language TEXT NOT NULL);
```

```
CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            language TEXT,
            score INT,
            DateTime datetime default current_timestamp);
```

You can insert questions manually using sql like this:
```
INSERT INTO questions (question, answer, language) VALUES
    ("How we print message in java language?", "println()", "java");
```

## Start the app:

To run the app using terminal run this command line:

1. First, go to your project file
```
cd project
```
2. Activate the venv, if you dont have venv please follow the steps [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
```
source venv/bin/activate
```

3. Install packages used :
```
pip3 install -r requirements.txt
```
4. Run the main.py script with flask:
```
flask run app
```
### Enjoy learning 😊

# All right reserved for &copy; SAMIHA AMROUNE.
