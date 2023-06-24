import dataclasses
import json

from flask import Flask, request, Response
from flask_cors import CORS

from website.database import LocalThoughtDb
from website.models import Thought

app = Flask(__name__)
CORS(app)


db = LocalThoughtDb()

def wrap_response(response: dict) -> Response:
    return Response(json.dumps(response), mimetype="application/json")

@app.route("/")
def index():
    return "yep you found me"

@app.route("/ping")
def ping():
    return wrap_response({"entity": "it's a me mario!"})


@app.route("/thought/getAll", methods=['GET'])
def get_all_thoughts():
    result: list[Thought] = db.get_all(sort_function=lambda t: t.createDate, reverse=True)
    result: list[dict] = list(map(lambda r: dataclasses.asdict(r), result))
    response = {"allThoughts": result}
    return wrap_response(response)


@app.route("/thought/create", methods=['POST'])
def create_thought():
    data = request.get_json(force=True)
    if not data or not data.get("thoughtData", None):
        return "Nothing found in thoughtData", 400
    else:
        thought_id = db.create(thought_data=data["thoughtData"])
        response = {
            "tid": thought_id
        }
        return wrap_response(response)


@app.route("/thought/delete/<thought_id>", methods=['DELETE'])
def delete_thought(thought_id):
    if not thought_id:
        return "Empty thought_id", 400

    response = {"success": db.delete(thought_id)}
    return wrap_response(response)




if __name__ == '__main__':
    app.run(debug=True, port=8080)



