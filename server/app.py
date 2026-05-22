# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


def earthquake_to_dict(earthquake):
    return {
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year,
    }


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if not earthquake:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(body, 404)

    return make_response(earthquake_to_dict(earthquake), 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    body = {
        "count": len(quakes),
        "quakes": [earthquake_to_dict(quake) for quake in quakes],
    }

    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
