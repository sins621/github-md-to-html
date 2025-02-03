import base64
import json

import markdown
import markdown.extensions.fenced_code
import requests
from flask import Flask, jsonify, request
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

github_file_api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/contents/{dir_path}/{file_path}"
github_tree_api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/git/trees/main?recursive=1"
# https://api.github.com/repos/sins621/Obsidian-Notes/git/trees/main?recursive=1
response = requests.get(url=github_tree_api_url)
data = response.json()
content = data["tree"]
filter_string = ".md"
filtered_data = []

for dict in content:
    if filter_string in dict["path"]:
        filtered_data.append(dict)
# print(json.dumps(filtered_data, indent=2))

for dict in filtered_data:
    print(dict["path"].rpartition("/")[0])


@app.route("/get_tree/")
@cross_origin()
def get_tree():
    github_tree_api_url = f"https://api.github.com/repos/{request.args.get("github_user")}/{request.args.get("github_repo")}/git/trees/main?recursive=1"
    # https://api.github.com/repos/sins621/Obsidian-Notes/git/trees/main?recursive=1
    response = requests.get(url=github_tree_api_url)
    data = response.json()
    content = data["tree"]
    filter_string = ".md"
    filtered_data = []

    for dict in content:
        if filter_string in dict["path"]:
            filtered_data.append(
                {
                    "path": dict["path"],
                    "url": dict["url"],
                }
            )
    return jsonify(filtered_data)


@app.route("/get_file")
def get_file():
    args = request.args
    response = requests.get(url=args.get("url"))
    data = response.json()
    content = data["content"]
    dir = args.get("path").rpartition("/")[0]
    decoded_string = base64.b64decode(content).decode("utf-8")
    decoded_string = decoded_string.replace(
        "![](",
        f"![](https://raw.githubusercontent.com/{args.get("github_user")}/{args.get("github_repo")}/refs/heads/main/{dir}/",
    )
    html = markdown.markdown(decoded_string, extensions=["fenced_code"])
    return html


if __name__ == "__main__":
    app.run(debug=True, port=3000)


# content = data["content"]
# decoded_string = base64.b64decode(content).decode("utf-8")

# decoded_string = decoded_string.replace(
#     "![](",
#     f"![](https://raw.githubusercontent.com/{github_user}/{github_repo}/refs/heads/main/{dir_path}/",
# )

# html = markdown.markdown(decoded_string, extensions=["fenced_code"])


# @app.route("/")
# @cross_origin()
# def hello_world():
#     return html


# if __name__ == "__main__":
#     app.run(debug=True, port=3000)
