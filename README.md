# FSP
or Flask-Static-Pages


This program is a really simple, small, and scuffed static site generator written in python, which allows you to write websites with markdown.

Dependencies:
- python
- python-markdown `pip install markdown`
- flask `pip install flask`
- tomli `pip install tomli`

This program uses jinja templating.

Also, here's the file structure for an fsp project:
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
├── main.py
├── static
│   ├── style.css
│   └── pikachu.png # You can obviously have subfolders for different file types if you'd like!
└── templates
    ├── base.html
    └── error.html
```

## Configuration

fsp sites are configured by the `config.toml` file.
config.toml can be used in the templates.

**Example config.toml file**:
```toml
# title of the website
site_title = "My website"

# error template html file in templates/
error_template = "error.html"
```
The parameters from `config.toml` are can be accessed through the `fsp` variable.

**Example config.toml usage in template**:
```html
<!DOCTYPE html>
<head>
    <title>fsp["site_title"]</title>
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
TODO: add moar documentation

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

License: MIT
