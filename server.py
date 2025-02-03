import base64

import markdown
import markdown.extensions.fenced_code
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/get_tree")
@cross_origin()
def get_tree():
    github_tree_api_url = f"https://api.github.com/repos/{request.args.get("github_user")}/{request.args.get("github_repo")}/git/trees/main?recursive=1"
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
@cross_origin()
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
