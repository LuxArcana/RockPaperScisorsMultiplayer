from flask import Flask, request, make_response
from Domain.Dtos import *
from Domain.Entities import *
from Domain.Exceptions import *
from Domain.MoveTokens import *
from Service.RockPaperScisorsService import *


app = Flask(__name__)


#main service to handel game logic
_service = RockPaperScisorsService()






#test route to check health of api
@app.route('/api/v1/test', methods=['GET'])
def test():
    response = make_response(f'{{"message":"OK"}}', 200)
    response.headers.add('Content-Type', 'application/json')
    return response
    



#list all contests
@app.route('/api/v1/contests', methods=['GET'])
def GetContests():
    contestListResponseDto: ContestListResponseDto = _service.GetContests()
    response = make_response(contestListResponseDto.to_json(), 200)
    response.headers.add('Content-Type', 'application/json')
    return response




#get a specific contest
@app.route('/api/v1/contest/<rawContestId>', methods=['GET'])
def GetContest(rawContestId: str):
    try:

        if rawContestId == 'null':
            raise ContestNotFoundException
    
        contestId: uuid = uuid.UUID(rawContestId)
        response = make_response(_service.GetContest(contestId, None).to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ContestNotFoundException:
        response = make_response(f'{{"error":"ContestNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ValueError:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided contestId |{rawContestId}| into a GUID"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response





#get a specific contest from a players point of view
@app.route('/api/v1/contest/<rawContestId>/player/<rawPlayerId>', methods=['GET'])
def GetContestAsPlayer(rawContestId: str, rawPlayerId: str):
    try:

        if rawContestId == 'null':
            raise ContestNotFoundException
        
        if rawPlayerId == 'null':
            raise PlayerNotFoundException

        contestId: uuid = uuid.UUID(rawContestId)
        playerId: uuid = uuid.UUID(rawPlayerId)
    
        response = make_response(_service.GetContest(contestId, playerId).to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ContestNotFoundException:
        response = make_response(f'{{"error":"ContestNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except PlayerNotFoundException:
        response = make_response(f'{{"error":"PlayerNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ValueError:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided contestId |{rawContestId}| or playerId |{rawPlayerId}| into a GUID"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response




#create a new contest
@app.route('/api/v1/contest', methods=['POST'])
def PostNewContest():
    contestRequest = None

    try:

        data = request.get_json()
        contestRequest = CreateContestRequestDto(data['contestName'], data['roundsToWin'], data['gameType'], data['oponentType'])

    except:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided Request JSON"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response
    

    try:

        response = make_response(_service.CreateContest(contestRequest).to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except InvalidGameTypeException:
        response = make_response(f'{{"error":"InvalidGameTypeException"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except InvalidOponentTypeException:
        response = make_response(f'{{"error":"InvalidOponentTypeException"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response




#join a contest
@app.route('/api/v1/contest/<rawContestId>/join', methods=['POST'])
def JoinContest(rawContestId: str):
    try:

        if rawContestId == 'null':
            raise ContestNotFoundException
        
        contestId: uuid = uuid.UUID(rawContestId)
        response = make_response(_service.JoinContest(contestId).to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ContestNotFoundException:
        response = make_response(f'{{"error":"ContestNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ValueError:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided contestId |{rawContestId}| into a GUID"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response




#cancel a contest
@app.route('/api/v1/contest/<rawContestId>/player/<rawPlayerId>/cancel', methods=['PATCH'])
def CancelContest(rawContestId: str, rawPlayerId: str):
    try:
        if rawContestId == 'null':
            raise ContestNotFoundException
        
        if rawPlayerId == 'null':
            raise PlayerNotFoundException
        
        contestId: uuid = uuid.UUID(rawContestId)
        playerId: uuid = uuid.UUID(rawPlayerId)

        response = make_response(_service.CancelContest(contestId, playerId).to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response


    except ContestNotFoundException:
        response = make_response(f'{{"error":"ContestNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response

    except PlayerNotFoundException:
        response = make_response(f'{{"error":"PlayerNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response

    except CancelContestNotAllowed:
        response = make_response(f'{{"error":"CancelContestNotAllowed"}}', 403)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ValueError:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided contestId |{rawContestId}| or playerId |{rawPlayerId}| into a GUID"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except Exception as e:
        response = make_response(f'{{"error":"Exception","message":"{e.args[0]}"}}', 500)
        response.headers.add('Content-Type', 'application/json')
        return response


#post a move to a game
@app.route('/api/v1/contest/<rawContestId>/game/<rawGameId>/player/<rawPlayerId>/<moveName>', methods=['POST'])
def PostMoveToGame(rawContestId: str, rawGameId: str, rawPlayerId: str, moveName: str):
    try:

        if rawContestId == 'null':
            raise ContestNotFoundException
        
        if rawGameId == 'null':
            raise GameNotFoundException
        
        if rawPlayerId == 'null':
            raise PlayerNotFoundException

        contestId: uuid = uuid.UUID(rawContestId)
        gameId: uuid = uuid.UUID(rawGameId)
        playerId: uuid = uuid.UUID(rawPlayerId)

        placeMoveResponseDto: PlaceMoveResponseDto =_service.PlaceMove(contestId, gameId, playerId, moveName)

        response = make_response(placeMoveResponseDto.to_json(), 200)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ContestNotFoundException:
        response = make_response(f'{{"error":"ContestNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except GameNotFoundException:
        response = make_response(f'{{"error":"GameNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except PlayerNotFoundException:
        response = make_response(f'{{"error":"PlayerNotFoundException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except InvalidMoveException:
        response = make_response(f'{{"error":"InvalidMoveException"}}', 404)
        response.headers.add('Content-Type', 'application/json')
        return response
    
    except ValueError:
        response = make_response(f'{{"error":"ValueError","message":"Could Not Parse Provided contestId |{rawContestId}| or playerId |{rawPlayerId}| or gameId |{rawGameId}| into a GUID"}}', 400)
        response.headers.add('Content-Type', 'application/json')
        return response













#start the web service manually if this was launched directly instead of from WSGI
if __name__ == '__main__':
    print('Starting From Main Not Flask')
    app.run()