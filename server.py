import os
import markdown
import markdown.extensions.fenced_code

from flask import Flask
from flask_cors import CORS, cross_origin
from git import Repo

# TODO: Parse img tags to prepend https://raw.githubusercontent.com/sins621/Obsidian-Notes/main

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
git_url = "https://github.com/sins621/Obsidian-Notes"
to_path = "./github-files"
repo = None

if os.path.isdir(to_path):
    repo = Repo(to_path)
    origin = repo.remotes.origin
    origin.pull()
else:
    Repo.clone_from(git_url, to_path)
    repo = Repo(to_path)

md_file = None
with open(
    "./github-files/Programming/CPP/Controlling Program Flow/Looping.md",
    "r",
    encoding="utf8",
) as f:
    md_file = f.read()

html = markdown.markdown(md_file, extensions=["fenced_code"])


@app.route("/")
@cross_origin()
def hello_world():
    return html


if __name__ == "__main__":
    app.run(debug=True, port=3000)
