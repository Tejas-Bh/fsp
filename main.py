import os
import markdown as mkdown
import jinja2
import tomli

######################################
"""
FSP - a really simple (and scuffed) static site generator written in python
FSP uses a flask web server.
(Flask - Static - Pages)
This program also uses markdown, meaning that it's really easy to make sites.
"""
######################################


# Load toml settings
with open("config.toml", mode="rb") as config:
    fsp = tomli.load(config)

# Do the flask stuff
from flask import Flask

app = Flask(__name__)

# using dynamic routes to go through all html in templates/ and make routes out of them

html = os.listdir("templates/")


# Make index route
md = mkdown.Markdown(extensions=["meta"])
jinja_env = jinja2.Environment()
@app.route("/")
def index():
    md_text = """"""
    with open("content/index.md") as f:
        for l in f:
            md_text += l

    base = """"""
    with open("templates/base.html") as f:
        for l in f:
            base += l
    err = """"""
    with open(f"templates/{error_template}"):
        for l in f:
            err += 1

    html_body = md.convert(md_text)

    try:
        return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp)
    except Exception as e:
        return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp)

# Make dynamic route for all pages
md = mkdown.Markdown(extensions=["meta"])
@app.route("/<webpage>")
def pages(webpage):
    md_text = """"""
    with open(f"content/{webpage}.md") as f:
        for l in f:
            md_text += l

    base = """"""
    with open("templates/base.html") as f:
        for l in f:
            base += l

    html_body = md.convert(md_text)
 
    try:
        return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp)
    except Exception as e:
        return f"There was an error: {e}"

if __name__ == "__main__":
    app.run()
