# Djang-Oh-No

Djang-Oh-No is a small, intentionally vulnerable web app written using Python 3, SQLite and the Django framework.  Django has great build in features to protect against some of the most common security vulnerabilities found in web applications.  The caveat: you have to make sure to use those features in order to be protected.  This application contains code that opens up the door for SQL Injection, Cross Site Scripting (XSS), and Cross Site Request Forgery (CSRF).  Read on for more details on what went wrong, and what Django features to use to avoid some common pitfalls.

DISCLAIMER: Use the code in this repo as sample code at your own peril.  This application is not intended to be deployed anywhere and the code is not intended to be re-used due to blatant security risks.

## Prerequisites

You'll need Python 3 (program written using Python 3.6.5 but anything 3 and above should do the trick), the pip package installer, and virtualenv.  Technically you could get this up and running without a virtual environment, but when installing using pip it's best to keep packages in a sandbox.  Because, y'know, security.

## Getting Started

Clone this repository, and cd into it

Create and activate a virtual environment that uses Python 3:
```
$ virtualenv -p python3 env
$ source env/bin/activate
```

Pip install requirements
```
$pip install -r requirements.txt
```

Enter the djangohno directory and make database migrations
```
$ cd djangohno
$ python3 manage.py migrate
```

Start the server on localhost
```
$ python3 manage.py runserver
```

Using a browser of your choice, navigate to localhost:8000.  Create a few users, add some posts to the forum, and you should be ready to rock.

## Running the tests

Tests?  What tests?  No but seriously you should always test your code to make sure it does what you think it does.  Flaws in your logic can lead to unintended consequences that leave your users at risk.  Don't forget to test for those pesky edge cases.

## Introducing the security vulnerabilities:

### Problem 1: Wrote a pretty bad custom authentication system instead of using the Django authentication system

I didn't feel like learning how this new fangled framework does user authentication, so I wrote my own logic for user logins.  Too bad I forgot to hash my users' passwords and stored them in plain text.  Django's user auth system uses the PBKDF2 hashing algorithm by default when storing user's passwords, and allows you to adjust the "work factor" according to your preferences.  Hashing user passwords makes it more difficult for attackers to compromise user accounts in the case of a database leak.  Although, there's another problem with my custom user auth system that renders user passwords completely useless.

### Problem 2: SQL Injection

I got annoyed with the Django Object Relational Mapper & decided to write some raw SQL instead for my user login.  I probably should have read about SQL Injection before dropping untrusted user input into raw SQL without using parameterized queries.  My login will interpret certain characters provided in username and password fields as SQL.  For example, if I login using any username followed by the characters '-- (ending the username string and commenting out the rest of the SQL query), I can log in as any user without knowing the password.  SQL Injection can get really nasty - but if I had used Django's built in ORM, I would have been protected because the framework uses parameterized queries.   

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [SQLite](https://www.sqlite.org/index.html) - Relational database used
