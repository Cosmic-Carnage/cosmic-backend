from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from model.players import Player

# create a blueprint for player-related api routes
player_api = Blueprint('player_api', __name__, url_prefix='/api/players')
api = Api(player_api)

class PlayerAPI:
    class Action(Resource):
        # handle post requests to create a new player
        def post(self):
            body = request.get_json()
            user = body.get('user')

            if user is None or len(user) < 2:
                return {'message': f'name is missing, or is less than 2 characters'}, 400

            # create a new player object with an initial score
            po = Player(user=user, score=0)

            # call the create method to persist the player in the database
            player = po.create()
            if player:
                return jsonify(player.read()), 201

            # return an error message if player creation fails
            return {'message': f'error creating player'}, 500

        # handle get requests to retrieve all players
        def get(self):
            players = Player.query.all()
            # prepare player data for json serialization
            json_ready = [player.read() for player in players]
            return jsonify(json_ready)

        # handle put requests to update a player's data
        def put(self):
            body = request.get_json()
            user = body.get('user')
            data = body.get('data')

            if user is None:
                return {'message': 'user is missing in the request data'}, 400

            # query the player by 'user' from the database
            player = Player.query.filter_by(user=user).first()
            if player:
                # update the player's data using the 'data' field
                player.update(data)
                return f"{player.read()} updated", 200

            # return a not found error if the player doesn't exist
            return {'message': f'player with user {user} not found'}, 404

        # handle delete requests to delete a player
        def delete(self):
            body = request.get_json()
            user = body.get('user')

            if user is None:
                return {'message': 'user is missing in the request data'}, 400

            # query the player by 'user' from the database
            player = Player.query.filter_by(user=user).first()
            if player:
                # delete the player record from the database
                player.delete()
                return f"{player.read()} has been deleted", 200

            # return a not found error if the player doesn't exist
            return {'message': f'player with user {user} not found'}, 404

    class _Create(Resource):
        def post(self):
            body = request.get_json()

            # validate make
            user = body.get('user')
            if user is None or len(user) < 1:
                return {'message': f'Username is missing, or is less than 1 character'}, 210
            score = body.get('score')
            if score is None:
                return {'message': f'Score is missing, or is less than 1 number'}, 210

            player = Player(user=user, score=score)

            # creates the info in the database
            info = player.create()
            # success returns json of user
            if info:
                return jsonify(info.read())
            # failure returns error
            return {'message': f'ERROR'}, 210

    # add the action resource to the api with the specified url endpoint
    api.add_resource(Action, '/')
    api.add_resource(_Create, '/create')

