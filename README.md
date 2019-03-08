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

Using a browser of your choice, navigate to localhost:8000/forum.  Create a few users, add some posts to the Stack Over-Oh-No forum, and you should be ready to rock.

## Running the tests

Tests?  What tests?  No, but seriously you should always test your code to make sure it does what you think it does.  Flaws in your logic can lead to unintended consequences that leave your users at risk.  Don't forget to test for those pesky edge cases.

## Introducing the security vulnerabilities:

### Problem 1: Poorly written custom user auth system

I didn't feel like learning how this new fangled framework does [user authentication](https://docs.djangoproject.com/en/2.1/topics/auth/), so I wrote my own logic for user logins.  Too bad I forgot to hash my users' passwords and stored them in plain text.  [Django's user auth system](https://docs.djangoproject.com/en/2.1/topics/auth/passwords/) uses the [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) hashing algorithm by default when storing user's passwords, and allows you to adjust the "work factor" according to your preferences.  Hashing user passwords makes it more difficult for attackers to compromise user accounts in the case of a database leak.  Although, there's another problem with my custom user auth system that renders user passwords completely useless.

### Problem 2: SQL Injection

I got annoyed with the Django Object Relational Mapper & decided to write some [raw SQL](https://docs.djangoproject.com/en/2.1/topics/db/sql/) instead for my user login.  I probably should have read about [SQL Injection](https://www.owasp.org/index.php/SQL_Injection) before dropping untrusted user input into raw SQL without using parameterized queries.  My login will interpret certain characters provided in username and password fields as SQL.  For example, if I login using any username followed by the characters '-- (ending the username string and commenting out the rest of the SQL query), I can log in as any user without knowing the password.  SQL Injection can get really nasty - but if I had used Django's built in ORM, I would have been protected because the framework uses parameterized queries to retrieve information from databases.  OK, so now that I can log in as any user, I can post anything I want on this forum app, including a payload that would help me exploit the next vulnerability.

### Problem 3: Cross-Site Scripting (XSS)

I really wanted to keep my users safe, and I've seen this pattern used in Django templates before: ```{{ data | safe }}```.  I figured this must be a safety and security feature so I made sure to use the "safe" flag on forum posts.  As it turns out, [Django's safe flag](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/#safe) in templates turns off [XSS](https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29) protections that keep the application from interpreting untrusted input as Javascript.  Now people can insert arbitrary Javascript code that will execute in the context of the browser of any user that visits my application's home page.  This could allow an attacker to add a keylogger to the page to steal passwords, add a script that sends all users' cookies to the attacker, or post to the forum on behalf of the user.  Speaking of misconfigurations that could allow an attacker to perform actions on behalf of another user.

### Problem 4: Cross-Site Request Forgery

I started playing around with writing a React front end to my app, but I kept getting errors about a "csrf token".  Anyway, I found a Stack Overflow post that showed how to turn off that pesky csrf middleware.  I also really wanted people to be able to post to the forum from other websites while logged in to Stack Over-Oh-No if they want to, so I set the "SESSION_COOKIE_SAMESITE" setting to False.  Welp, turns out this was a bad idea.  I opened myself right up to [Cross-Site Request Forgery](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29), and now any site can send POST requests to my web app.  A user who is logged in to my app could navigate to a different site containing a hidden POST request to send a new post to Stack Over-Oh-No on behalf of the logged in user without them realizing anything happened.  Django's CSRF middleware and default setting for [same site session cookies](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SESSION_COOKIE_SAMESITE) usually will protect applications from Cross Site Request Forgery.  But if you decide to turn off those protections for convenience, you could put your users at risk.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [SQLite](https://www.sqlite.org/index.html) - Relational database used
