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

error_template = True
try:
    fsp["error_template"]
except:
    error_template = False

# Do the flask stuff
from flask import Flask, url_for

app = Flask(__name__)

# using dynamic routes to go through all html in templates/ and make routes out of them

print(f"templates/{fsp['error_template']}")

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
    if error_template:
        err = """"""
        with open(f"templates/{fsp['error_template']}") as f:
            for l in f:
                err += l

    html_body = md.convert(md_text)

    try:
        return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, url_for=url_for)
    except Exception as e:
        if error_template:
            return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, url_for=url_for)
        else:
            return f"ERROR: {e}"

# Make dynamic route for all pages
md = mkdown.Markdown(extensions=["meta"])
@app.route("/<webpage>")
def pages(webpage):
    base = """"""
    with open("templates/base.html") as f:
        for l in f:
            base += l
    if error_template:
        err=""""""
        with open(f"templates/{fsp['error_template']}") as f:
            for l in f:
                err += l
    md_text = """"""
    try:
        with open(f"content/{webpage}.md") as f:
            for l in f:
                md_text += l
    except Exception as e:
        if error_template:
            return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, url_for=url_for)
        else:
            return f"ERROR: {e}"

    html_body = md.convert(md_text)
 
    try:
        return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, url_for=url_for)
    except Exception as e:
        if error_template:
            return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, url_for=url_for)
        else:
            return f"ERROR: {e}"

if __name__ == "__main__":
    app.run()
