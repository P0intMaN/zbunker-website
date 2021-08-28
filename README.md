<img src="zbunker/static/img/zglitch-inverted.gif" width="100%">

[![Python Version](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/)
[![Pull Requests](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/P0intMaN/zbunker-website/issues)
[![GitHub issues](https://img.shields.io/github/issues/P0intMaN/zbunker-website?color=red)](https://github.com/P0intMaN/zbunker-website/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/P0intMaN/zbunker-website)](https://github.com/P0intMaN/zbunker-website/issues?q=is%3Aissue+is%3Aclosed)
[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UC1QZPervOHLiC4xpVnzbDFg?style=social)](https://www.youtube.com/channel/UC1QZPervOHLiC4xpVnzbDFg)



ZBunker is a community run by a bunch of university students with an aim to spread awareness about **open source** and the power of **programmming**.

The main mode of education is through our [YouTube channel](https://www.youtube.com/channel/UC1QZPervOHLiC4xpVnzbDFg), where we will walk you through some of the popular programming languages and how you can develop a skill set in the tech domain.

We believe in ***free and quality education for all***.

## About The Project 🚀:

*`zbunker-website`* project is focussed on creating an independent website dedicated to **ZBunker**. This website will feature all the courses, seminars, webinars and other learning resources that will be of great use for learners.

*`zbunker-website`* uses **Flask** as the backend. Check out the [Tech Stack](#tech-stack-) section to know about various tech stacks preferred and currently used for creating this website.

## ToDo List 📝

- [x] Create a landing page
- [x] Create interactve, functional homepage
- [x] Create About section
- [x] Add login/register functionality
- [x] Use SQLAlchemy(flask-sqlalchemy :: SQLite DB) to store user creds
- [x] Add anti-CSRF tokens
- [ ] Add video contents
- [ ] Add resources
- [ ] Create filter based gallery for courses
- [ ] Add footer
- [ ] Migrate to PostgreSQL
- [ ] Add forgot password functionality
- [ ] Add Google reCaptcha
- [ ] Add Donatoins Gateway (Instamojo or Stripe)
- [ ] Deploy rate limit check on login/register (Security)
- [ ] Make Website Responsive
- [ ] Deploy the website on a public server (Final)

## Getting Started / Viewing Project 🛰️

- ### Installing Python

    This Project breathes and lives on **Python**. You need to have Python in your system to view this project. Head over to the [official website](https://www.python.org) and download the latest version. You can also watch this video about [installing Python](https://youtu.be/MGhDEeIkarg)

    If you want to learn **Python**, you can refer to this [basic Python course](https://www.youtube.com/playlist?list=PLbsliZj8JocLu8b_13sVPZUciUBaLpMVw)

- ### Installing Dependencies

    The **packages and modules** you need to run *`zbunker-website`* is listed in the `requirements.txt` file. You can **install them** via this command:

    ```bash
    pip install -r requirements.txt
    ```

- ### Running the Project

    Open up your **terminal (cmd in windows)** and navigate inside the Project directory: `zbunker-website/`. Then simply run this command:

    ```bash
    python run.py
    ```

    This would spit out some verbose (simply ignore them). You **only need to look for something similar to** `Running on http://127.0.0.1:xxxx` where xxx is port no. Copy this code and paste it on your **web browser**.

     Voila! ZBunker website is **up and running**!

## Tech Stack 💻

1. [HTML](https://www.w3schools.com/html/) - A markup language for creating a webpage.
2. [CSS](https://www.w3schools.com/css/) - Styler for HTML webpages
3. [JavaScript](https://www.javascript.com/) - The programming language of web
4. [Flask](https://flask.palletsprojects.com/) - Flask is a microframework for Python based on Werkzeug and Jinja 2
5. [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - An extension for Flask that adds support for SQLAlchemy ORM to your application.
6. [Jinja2 Templates](https://jinja.palletsprojects.com/) - Templating language used with Flask for frontend purposes.
