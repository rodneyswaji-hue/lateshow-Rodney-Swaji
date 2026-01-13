# app.py
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        # The prompt output for /episodes does NOT show appearances, so we exclude them here
        results = [e.to_dict(rules=('-appearances',)) for e in episodes]
        return make_response(jsonify(results), 200)

class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id=id).first()
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        # The prompt requires nested appearances, and inside appearances, the guest info.
        # Our model serialize_rules handle most of this, but we need to ensure deep serialization matches.
        return make_response(jsonify(episode.to_dict()), 200)

    def delete(self, id):
        episode = Episode.query.filter_by(id=id).first()
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        db.session.delete(episode)
        db.session.commit()
        return make_response(jsonify({}), 204) # 204 means No Content (success)

class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        # Prompt output for guests is simple, no appearances needed
        results = [g.to_dict(rules=('-appearances',)) for g in guests]
        return make_response(jsonify(results), 200)

class Appearances(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            new_appearance = Appearance(
                rating=data['rating'],
                episode_id=data['episode_id'],
                guest_id=data['guest_id']
            )
            db.session.add(new_appearance)
            db.session.commit()
            
            # The prompt wants the response to include the full nested episode and guest objects.
            # Appearance.to_dict() should handle this based on our serialize_rules in models.py
            return make_response(jsonify(new_appearance.to_dict()), 201)
            
        except ValueError as e:
            # This catches our validation error from models.py
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        except Exception as e:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)

api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)