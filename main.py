import markdown as mkdown
import jinja2
import tomli
from os import chdir, getcwd, mkdir, remove, listdir
from sys import path, argv
from shutil import copytree, rmtree

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

try:
    if argv[1] == "build":
        build = True
    else:
        build = False
except:
    build = False

# Load toml settings
with open("config.toml", mode="rb") as config:
    fsp = tomli.load(config)

# load jinja env
jinja_env = jinja2.Environment()

# load markdown env
md = mkdown.Markdown(extensions=["meta"])


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

"""
*fsp build*
This is the part of the program that build the static pages
"""

if build:
    build_path = getcwd()+"/build"
    if "build" in listdir(getcwd()):
        rmtree(getcwd()+"/build")
        mkdir(build_path)
    else:
        mkdir(build_path)
    
    # Add robots.txt to the root build directory
    try:
        robots = """"""
        with open("static/robots.txt") as file:
            for l in file:
                robots += l
        with open(build_path+"/robots.txt", "w") as file:
            file.write(robots)
        print("robots.txt: yes")
    except:
        with open(build_path+"/robots.txt", "w") as file:
            file.write("")
        print("robots.txt: auto-generated (blank)")

    # Add all of the static files to the root build directory
    try:
        copytree("static/", build_path+"/static", symlinks=True)
    except Exception as e:
        pass

    # Remove the unneeded robots.txt file from the static directory, now it's in the root directory.
    try:
        remove(build+path+"/static/robots.txt")
    except:
        pass

    # Make the link_to script
    def link_to(url):
        if url[0] == "/" and len(url) != 1:
            return "./"+url[1:]+".html"
        elif url[0] == "/" and len(url) == 1:
            return "./index.html"
        else:
            return "./"+url[1:]+'.html'

    # Make static script.
    def static(file):
        return "static/"+file

    # Now, actually get all the pages and yeet them into the root directory.
    # Do or throw an error, there is no try.
    files = listdir("content")
    i = 0
    for f in files:
        i += 1 
        with open("content/"+f) as file:
            md_text = """"""
            for l in file:
                md_text += l
            if scripts_usage:
                md_text = jinja_env.from_string(md_text).render(fsp=fsp, scripts=scripts, static=static, link_to=link_to)
                md_text = jinja_env.from_string(md_text).render(fsp=fsp, scripts=scripts, static=static, link_to=link_to)
                # [note]: run it twice because in testing sometimes static() and link_to() don't load if they're referenced in scripts.
            else:
                md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, link_to=link_to)
        with open("templates/base.html") as file:
            base = """"""
            for l in file:
                base += l
        with open(build_path+"/"+f[:-2]+"html", "w") as file:
            html_body = md.convert(md_text)
            if scripts_usage:
                full_html = jinja_env.from_string(base).render(fsp=fsp, scripts=scripts, static=static, md=md, md_metadata=md.Meta, body=html_body, link_to=link_to)
            else:
                full_html = jinja_env.from_string(base).render(fsp=fsp, static=static, md=md, md_metadata=md.Meta, body=html_body, link_to=link_to)
            file.write(full_html)
    print("pages:      "+str(i))

    # Now, error page with .htaccess file in the root directory
    if error_template:
        with open(build_path+"/.htaccess", "w") as file:
            file.write(
                "ErrorDocument 404 /404.html\n"
                "ErrorDocument 403 /403.html\n"
                "ErrorDocument 500 /500.html\n"
            )
        error = """"""
        with open("templates/"+fsp["error_template"]) as file:
            for l in file:
                error += l
        with open(build_path+"/404.html", "w") as file:
            file.write(jinja_env.from_string(error).render(fsp=fsp, static=static, md=md, md_metadata=md.Meta, body="Error: 404 Page not found", link_to=link_to))
        with open(build_path+"/403.html", "w") as file:
            file.write(jinja_env.from_string(error).render(fsp=fsp, static=static, md=md, md_metadata=md.Meta, body="Error: 403 Forbidden", link_to=link_to))
        with open(build_path+"/500.html", "w") as file:
            file.write(jinja_env.from_string(error).render(fsp=fsp, static=static, md=md, md_metadata=md.Meta, body="Error: 500 Internal Server Error", link_to=link_to))

    # And, we're done!
    print("\ndone! enjoy your new app located in "+build_path+" :)")
    exit()

# Do the flask stuff
from flask import Flask, url_for

app = Flask(__name__, root_path=getcwd())

# allow user to have static files in their markdown
def static(file):
    return url_for("static", filename=file)

# allow user to use proper fsp links that work w/ static as well
def link_to(url):
    if url[0] == "/":
        return url
    else:
        return "/"+url

# using dynamic routes to go through all html in templates/ and make routes out of them

# Make index route
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
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts, link_to=link_to)
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts, link_to=link_to)
        # [note]: run it twice because in testing sometimes static() and link_to() don't load if they're referenced in scripts.
    else:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, link_to=link_to)
    html_body = md.convert(md_text)

    if scripts_usage:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts, link_to=link_to)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts, link_to=link_to)
            else:
                return f"ERROR: {e}"
    else:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, link_to=link_to)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, link_to=link_to)
            else:
                return f"ERROR: {e}"


# Make dynamic route for all pages
@app.route("/<webpage>")
def pages(webpage):
    if webpage == "robots.txt":
        try:
            with open(getcwd()+"/static/robots.txt") as file:
                robots = """"""
                for l in file:
                    robots += l
                return robots
        except:
            pass
    if webpage == "sitemap.xml":
        try:
            with open(getcwd()+"/static/sitemap.xml") as file:
                sitemap = """"""
                for l in file:
                    sitemap += l
                return sitemap
        except:
            pass

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
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts, link_to=link_to)
            else:
                return f"ERROR: {e}"
    else:
        try:
            with open(f"content/{webpage}.md") as f:
                for l in f:
                    md_text += l
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, link_to=link_to)
            else:
                return f"ERROR: {e}"

    if scripts_usage:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts, link_to=link_to)
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, scripts=scripts, link_to=link_to)
        # [note]: run it twice because in testing sometimes static() and link_to() don't load if they're referenced in scripts.
    else:
        md_text = jinja_env.from_string(md_text).render(fsp=fsp, static=static, link_to=link_to) 
    html_body = md.convert(md_text)

    if scripts_usage:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts, link_to=link_to)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, scripts=scripts, link_to=link_to)
            else:
                return f"ERROR: {e}"
    else:
        try:
            return jinja_env.from_string(base).render(body=html_body, md_metadata=md.Meta, md=md, fsp=fsp, link_to=link_to)
        except Exception as e:
            if error_template:
                return jinja_env.from_string(err).render(body=e, md_metadata=md.Meta, md=md, fsp=fsp, link_to=link_to)
            else:
                return f"ERROR: {e}"


if __name__ == "__main__":
    app.run()
