from flask import Blueprint, request
import uuid
from app.services.DBservices import DBservices
db = DBservices()

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# Webhook defined for recording the push and merge events.
# Event name in Github webhook Dashboard: "Just the push event."
@webhook.route('/track_push_n_merge', methods=["POST"])
def track_push_n_merge():
    try:
        if request.headers['Content-Type'] == 'application/json':
            if request.json.get("head_commit")["committer"]["username"] == "web-flow":
                action = "MERGE"
                to_branch = request.json.get("ref").split("/")[-1]
                from_branch = request.json.get("head_commit")["message"].split("/")[1].split("\n")[0]
            else:
                action = "PUSH"
                from_branch = request.json.get("ref").split("/")[-1]
                to_branch = None
            dataObj = {
                "_id": uuid.uuid4(),
                "request_id": request.json.get("head_commit")["id"],
                "author": request.json.get("head_commit")["author"]["name"],
                "action": action,
                "from_branch" : from_branch,
                "to_branch" : to_branch,
                "timestamp" : request.json.get("head_commit")["timestamp"]
            }
            if db.saveToHistory(dataObj):
                return {"error" : False, "message" : "Data is sucessfully inserted into the system", "data" : dataObj}, 200
            else:
                return {"error" : True, "message" : "Something went wrong !!"}, 403
        else:
            return {"error" : True, "message" : "API is expecting content type as JSON !!"}, 403
    except Exception as e:
        return {"error" : True, "message" : str(e)}, 400


# Webhook defined for recording the pull request events.
# Event name in Github webhook Dashboard: "Pull requests"
@webhook.route('/pull_request', methods=["POST"])
def pull_request():
    try:
        if request.headers['Content-Type'] == 'application/json':
            rid = request.json.get("pull_request")["id"]
            if db.isExist(rid) == False:
                dataObj = {
                    "_id": uuid.uuid4(),
                    "request_id": rid,
                    "author": request.json.get("sender")["login"],
                    "action": "PULL_REQUEST",
                    "from_branch" : request.json.get("pull_request")["head"]["ref"],
                    "to_branch" : request.json.get("pull_request")["base"]["ref"],
                    "timestamp" : request.json.get("pull_request")["created_at"]
                }
                if db.saveToHistory(dataObj):
                    return {"error" : False, "message" : "Data is sucessfully inserted into the system", "data" : dataObj}, 200
                else:
                    return {"error" : True, "message" : "Something went wrong !!"}, 403
            else:
                return {"error" : True, "message" : "Already exists!!"}, 403
        else:
            return {"error" : True, "message" : "API is expecting content type as JSON !!"}, 403
    except Exception as e:
        return {"error" : True, "message" : str(e)}, 400
