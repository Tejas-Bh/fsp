<h1 align="center"><b>fsp</b></h1>
fsp stands for flask static pages.

It's a versatile, small, simple, slightly stubborn, and scuffed site generator written in python.

fsp can be used to write websites with markdown, without having to write **too much** html.
<hr />

**note: this is still in beta. lots of changes will be made. please help contribute to this!**

*another note: an official release isn't out yet. For development purposes, I've been just adding main.py to my env/libs/python/site-packages (in a virtual environment) folder in a folder called fsp, with \_\_init.py\_\_ and \_\_main.py\_\_ linking to the main.py file.*

Dependencies:
- python
- python-markdown `pip install markdown`
- flask `pip install flask`
- tomli `pip install tomli`

## Installation / Deployment
fsp doesn't officially have a package yet as I'm still working on this (pls contribute pls) and will be making lots of more changes, I think.

But, if you'd like to check it out, these are the steps that I'd take:

Note: This is assuming that you can make python virtual environments and have git.

First, I'd make a virtual environment, and activate it.

Linux:
```bash
python3 -m venv env
source ./env/bin/activate
```

Windows (powershell):
```powershell
python -m venv env
./env/Scripts/Activate.ps1
```


Then, I'd pull this project from github.

```bash
git init
git pull https://github.com/Tejas-Bh/fsp.git
```

Then, I'd install the things from earlier in this README or from requirements.txt.

Then, I'd do something weird. I'd go in the virtual environment directory (in my case it'd be `env`), and i'd go inside the lib folder, I'd find the site-packages directory.

Then, I'd make a new folder: `fsp`

Then, go inside of it, and make a symbolic link for an \_\_init\_\_.py \_\_main\_\_.py to main.py in the root directory (where you pulled this project).

Then, I'd continuously git pull every so often since before official release is out, there wil be a lot of changes.

example for linux:
```bash
pip install -r requirements.txt
cd env/lib/python*/site-packages/
mkdir fsp
cd fsp
ln -s ../../../../../main.py ./__init__.py
ln -s ../../../../../main.py ./__main__.py
```

That's it!

Now, all you have to do to use fsp, is to activate the virtual environment, and do python3 -m fsp in the root directory of your project! (for development server)

If you want to use it in a proper WSGI server like `gunicorn` or `waitress` for whatever reason (deployment, or just for fun), you can simply do:
```bash
gunicorn fsp:app
```
in the root directory :)

And, if you ever need to import the app (again, usually for deployment purposes), simply do `from fsp import app`.

## The Basics

here's the file structure for an fsp project:
```bash
.
├── config.toml
├── content
│   ├── index.md
│   ├── page1.md
│   ├── page2.md
│   ├── page3.md
│   ├── page4.md
│   └── page5.md
├── scripts.py
├── static
│   ├── style.css
│   ├── robots.txt
│   └── pikachu.png # You can obviously have subfolders for different file types if you'd like!
└── templates
    ├── base.html
    └── error.html
```

to run an fsp app, simply run the fsp program from the root directory of your app.

## Configuration

fsp sites are configured by the `config.toml` file.
config.toml can be used in the templates.

**Example config.toml file**:
```toml
# title of the website
site_title = "My website"

# error template html file in templates/
error_template = "error.html"

# am I using scripts? yes.
scripts_usage = true
```
The parameters from `config.toml` can be accessed through the `fsp` variable.

**Example config.toml usage in template**:
```html
<!DOCTYPE html>
<head>
    <title>{{ fsp["site_title"] }}</title>
</head>
```

### Built-in parameters
At the moment there's only one built-in parameter in the config file, called `error_template`.
This file allows you to have a separate template for error pages, located in the `templates/` directory.
```toml
# in config.toml
error_template = "error.html" # talking about templates/error.html
```

## Built-in Functions and tools
These are functions and variables which you can use in your markdown and html templates.


**fsp (dictionary)** - like I mentioned earlier, fsp is a dictionary which has all of the things in your config.toml file.

**static (function)** - this is **important to know!** This function allows you to access files in the static folder.
**example:**
```markdown
# Hello World!
This is an example markdown page.

Now, below is an image using static().
![pikachu]({{ static("pikachu.png") }})
```

**md_metadata (dictionary/only for templates)** - metadata for markdown files.

Example:
```markdown
---
title: Welcome to my website!
date: 10-10-10
---
```
and then in your template, these can be accessed by:
```html
{{ md_metadata["title"] }}
{{ md_metadata["date"] }}
```

**md (object/only for templates)** - the rest of the information by using the markdown library if you want to use it

**body (string/only for templates)** - **THE MOST IMPORTANT ONE!** this is the html which was converted from the markdown to use in templates.

**EXAMPLE USAGE:** this is an example barebones template.
```html
<!DOCTYPE html>
<head>
    <title>{{ fsp["site_title"] }}</title>
</head>
<body>
    {{ body }}
</body>
```
As you can see, you can access all of these by using double curly braces{{  }}.

## Custom Scripts
fsp has a feature for custom scripts that you can write which can be accessed in templates and markdown.
These scripts are written in python.

**Usage**

To use custom scripts, first go to config.toml, and add:
```toml
scripts_usage = true
```

Then, make a ***scripts.py*** file in the root directory.
The scripts.py file can be used anywhere in the md/html, via the `scripts` object.

Example:
```python
# scripts.py
def func():
    print("Hello from func()!")
```
and in markdown or html, you can call func() by doing:
```md
This is a message from func():
{{ scripts.func() }}
```

As you can see, any function or variable defined in scripts.py can be accessed.

## Robots and sitemaps
(note: i have literally no idea how these files work so i made these features based off of 5 minutes of googling, pls feel free to contribute!)

To use a robots.txt and sitemap.xml, simply include them in the `static` folder in the root directory (the same one where the rest of the static files are stored), and fsp will take care.

---

**PLEASE FEEL FREE TO REACH OUT AND CONTRIBUTE**

TODO: add moar documentation

License: MIT
