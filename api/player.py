from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from model.players import Player

player_api = Blueprint('player_api', __name__, url_prefix='/api/players')
api = Api(player_api)

class PlayerAPI:
    class Action(Resource):
        def post(self):
            body = request.get_json()
            user = body.get('user')
            
            if user is None or len(user) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400

            po = Player(user=user, score=0)  # Set an initial score, change as needed
                    
            player = po.create()
            if player:
                return jsonify(player.read()), 201
            return {'message': f'Error creating player'}, 500

        def get(self):
            players = Player.query.all()
            json_ready = [player.read() for player in players]
            return jsonify(json_ready)

        def put(self):
            body = request.get_json()
            user = body.get('user')
            data = body.get('data')
            
            if user is None:
                return {'message': 'User is missing in the request data'}, 400
            
            player = Player.query.filter_by(user=user).first()
            if player:
                player.update(data)
                return f"{player.read()} Updated", 200
            return {'message': f'Player with user {user} not found'}, 404

        def delete(self):
            body = request.get_json()
            user = body.get('user')
            
            if user is None:
                return {'message': 'User is missing in the request data'}, 400
            
            player = Player.query.filter_by(user=user).first()
            if player:
                player.delete()
                return f"{player.read()} Has been deleted", 200
            return {'message': f'Player with user {user} not found'}, 404

    api.add_resource(Action, '/')
