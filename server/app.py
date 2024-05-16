# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>", methods=["GET", "POST"])
def earthquake_by_id(id):
    try:
        earthquake = Earthquake.query.get_or_404(id)
        return earthquake.to_dict(), 200
    except Exception as e:
        return {"message": f"Earthquake {id} not found."}, 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    try:
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude)
        serialized_objects = [quake.as_dict() for quake in earthquakes]
        return {"count": len(serialized_objects), "quakes": serialized_objects}, 200
    except Exception as e:
        return str(e), 404


if __name__ == "__main__":
    app.run(port=5555, debug=True)
