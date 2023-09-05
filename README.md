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
├── main.py
└── templates
    └── base.html # This is where the template for the sites goes
```

TODO: add documentation

License: MIT
