import json

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

domain_api = "https://api.github.com/"
current_user = "user"
repositories = "user/repos"
organizations = "user/orgs"

issues = "search/issues"


class GithubProfile():
    headers = {}

    def __init__(self, access_token):
        self.headers["Authorization"] = f"token {access_token}"

    def query_api(self, url, params=None):
        if params is None:
            r = requests.get(url, headers=self.headers)
        else:
            r = requests.get(url, headers=self.headers, params=params)
        return r.json()

    def user(self):
        self.username = self.query_api(domain_api + current_user)["login"]

    def user_repos(self):
        self.repos = {"public": [], "private": []}
        for repo in self.query_api(domain_api + repositories):
            repo_info = {}
            repo_info["name"] = repo["name"]
            repo_info["full_name"] = repo["full_name"]
            repo_info["owner"] = repo["owner"]["login"]
            repo_info["owner_type"] = repo["owner"]["type"]
            self.repos["public" if not repo["private"] else "private"].append(
                repo_info)

    def user_orgs(self):
        self.orgs = []
        for org in self.query_api(domain_api + organizations):
            self.orgs.append({
                "username": org["login"],
                "name": self.query_api(org["url"])["name"]
            })

    def user_prs(self):
        data = self.query_api(domain_api + issues,
                              params={"q": f'author:{self.username} type:pr'
                                      })["items"]
        prs = {}
        for pr in data:
            if pr["repository_url"] not in prs:
                pr_data = self.query_api(pr["repository_url"])
                prs.update({
                    pr["repository_url"]: {
                        "repo": pr_data["full_name"],
                        "author_association": pr["author_association"],
                        "pr_list": []
                    }
                })
            prs[pr["repository_url"]]["pr_list"].append({"number": pr["number"], "title": pr["title"]})
        self.prs = list(prs.values())


    def user_info(self):
        self.user()
        self.user_repos()
        self.user_orgs()
        self.user_prs()
        return jsonify({
            "username": self.username,
            "repositories": self.repos,
            "organizations": self.orgs,
            "pull_requests": self.prs
        })


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        token = request.form["token"]
    else:
        token = request.args["token"]
    gh_profile = GithubProfile(token)
    return gh_profile.user_info()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)