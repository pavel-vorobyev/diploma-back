import os
import datetime
import jwt

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from auth import parse_token
from db import guard as guard_pkg, visit as visit_pkg, visitor as visitor_pkg
from recognition import recognize


def handle_http_error(e):
    return jsonify(error=e.description), e.code


# SECRET = os.environ["SECRET"]
SECRET = "qwe"
app = Flask(__name__)
app.register_error_handler(HTTPException, handle_http_error)


@app.route("/subsystem/guard/login", methods=["POST"])
def guard_login():
    body = request.json
    login = body["login"]
    password = body["password"]

    guard = guard_pkg.login(login, password)

    if guard:
        token = jwt.encode({"guard": guard.to_dict()}, SECRET)
        return jsonify(token=token, guard=guard.to_dict())
    else:
        return jsonify(error="Wrong data"), 401


@app.route("/subsystem/guard/visits")
def guard_get_visits():
    if "Authorization" not in request.headers:
        return jsonify(message="No token"), 401

    session = parse_token(request.headers["Authorization"], SECRET)

    if not session:
        return jsonify(message="Token invalid"), 401

    visits = visit_pkg.get_visits(session["guard"]["id"])
    visits = [visit.to_dict() for visit in visits]

    return jsonify(visits)


@app.route("/subsystem/visitor/verify", methods=["POST"])
def lock_verify():
    if "Authorization" not in request.headers:
        return jsonify(message="No token"), 401

    session = parse_token(request.headers["Authorization"], SECRET)

    if not session:
        return jsonify(message="Token invalid"), 401

    if 'file' not in request.files:
        return jsonify(message="No file attached"), 400

    photo = request.files['file']
    photo_filename, photo_ext = os.path.splitext(photo.filename)

    if photo_filename == "":
        return jsonify(message="No file attached"), 400

    if photo_ext not in [".jpg", ".jpeg", ".JPG", ".JPEG"]:
        return jsonify(message="Unsupported file extension. Use: `.jpg`, `.jpeg`"), 400

    photo_path = os.path.join("static/", "{}{}".format(photo_filename, photo_ext))
    photo.save(photo_path)

    vehicle_license = recognize(photo_path).replace("\n", "")
    vehicle_license = vehicle_license[:6]
    print(vehicle_license)

    visitor = visitor_pkg.get_visitor_by_vehicle_license(vehicle_license)

    if visitor:
        visit = visit_pkg.add_visit(session["guard"]["id"], visitor.id, datetime.datetime.now().isoformat(), True,
                                    photo_path)
    else:
        visit = visit_pkg.add_visit(session["guard"]["id"], None, datetime.datetime.now().isoformat(), False,
                                    photo_path)

    visit.visitor = visitor
    return jsonify(visit.to_dict())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9173)
