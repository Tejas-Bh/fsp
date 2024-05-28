import markdown as mkdown
import jinja2
import tomli
from os import chdir, getcwd
from sys import path

######################################
"""
FSP - a really simple (and scuffed) static site generator written in python
FSP uses a flask web server.
(Flask - Static - Pages)
This program also uses markdown, meaning that it's really easy to make sites.
"""
######################################

# Change the working directory to the user's directory
chdir(getcwd())

# Load toml settings
with open("config.toml", mode="rb") as config:
    fsp = tomli.load(config)

error_template = True
try:
    fsp["error_template"]
except:
    error_template = False

scripts_usage = True
try:
    fsp["scripts_usage"]
except:
    scripts_usage = False
if scripts_usage:
    if fsp["scripts_usage"]:
        try:
            path.insert(1, getcwd())
            import scripts
        except Exception as e:
            raise Exception(f"""
It looks like there's an error. Try:
If you have scripts_usage in config.toml set to true, make sure that scripts.py exists.
Else, if you don't mean to use outside scripts, don't use scripts_usage in config.toml.
Hope this helps!
-fsp
Meanwhile, here's the original error message:
{e}""") from None


# Do the flask stuff
from flask import Flask, url_for

app = Flask(__name__, root_path=getcwd())

# allow user to have static file in their markdown
def static(file):
    return url_for("static", filename=file)

# using dynamic routes to go through all html in templates/ and make routes out of them

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

    if scripts_usage:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts)
    else:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static)
    html_body = md.convert(md_text)

    if scripts_usage:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts)
            else:
                return f"ERROR: {e}"
    else:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp)
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
    if scripts_usage:
        try:
            with open(f"content/{webpage}.md") as f:
                for l in f:
                    md_text += l
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts)
            else:
                return f"ERROR: {e}"
    else:
        try:
            with open(f"content/{webpage}.md") as f:
                for l in f:
                    md_text += l
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp)
            else:
                return f"ERROR: {e}"

    if scripts_usage:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts)
    else:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static) 
    html_body = md.convert(md_text)

    if scripts_usage:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts)
            else:
                return f"ERROR: {e}"
    else:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp)
            else:
                return f"ERROR: {e}"


if __name__ == "__main__":
    app.run()
