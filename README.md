# Flask Static Pages

This is a static page generator that allows you to write websites with markdown.
This program uses flask and pandoc.

Dependencies:
    - Flask
    - pandoc
`
pip install flask
pip install pypandoc_binary # This is only if you don't have pandoc installed!
`

File Structure:
`
├── build.sh
├── content
│   ├── This is where the markdown goes!
├── main.py
└── templates
    ├── This is where the generated HTML for the sitde goes.
`

Also, because this uses flask, you can use jinja templating inside of the markdown.

TODO:
    - Make this cross-compatible
    - Fix formatting issues with markdown lists and codeblocks

License:
MIT
