import base64

import markdown
import markdown.extensions.fenced_code
import requests
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
git_url = "https://github.com/sins621/Obsidian-Notes"
to_path = "./github-files"

github_user = "sins621"
github_repo = "Obsidian-Notes"
dir_path = "Programming/CPP/Controlling Program Flow"
file_path = "Looping.md"

github_api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/contents/{dir_path}/{file_path}"
response = requests.get(url=github_api_url)
data = response.json()
content = data["content"]
decoded_string = base64.b64decode(content).decode("utf-8")

decoded_string = decoded_string.replace(
    "![](",
    f"![](https://raw.githubusercontent.com/{github_user}/{github_repo}/refs/heads/main/{dir_path}/",
)

html = markdown.markdown(decoded_string, extensions=["fenced_code"])


@app.route("/")
@cross_origin()
def hello_world():
    return html


if __name__ == "__main__":
    app.run(debug=True, port=3000)
