import base64

import markdown
import markdown.extensions.fenced_code
import requests


def get_tree(github_user, github_repo):
    github_tree_api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/git/trees/main?recursive=1"
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
    return filtered_data


def get_file(github_user, github_repo, file_url, path):
    if file_url:
        response = requests.get(url=file_url)
        response.raise_for_status()
        data = response.json()
        content = data["content"]
        dir = path.rpartition("/")[0]
        decoded_string = base64.b64decode(content).decode("utf-8")
        decoded_string = decoded_string.replace(
            "![](",
            f"![](https://raw.githubusercontent.com/{github_user}/{github_repo}/refs/heads/main/{dir}/",
        )
        html = markdown.markdown(decoded_string, extensions=["fenced_code"])
        return html
