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
├── config.toml # This is the config file
├── content
│   ├── index.md # This is where the markdown goes
│   ├── otherpage.md 
│   ├── yetanothermarkdownpage.md
├── main.py
└── templates
    └── base.html # This is where the template for the sites goes
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
At the moment there's only one built-in parameter in the config file, called `error-template`.
This file allows you to have a separate template for error pages, located in the `templates/` directory.
```toml
# in config.toml
error_template = "error.html" # talking about templates/error.html
```

TODO: add moar documentation

License: MIT
