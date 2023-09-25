from Domain.Dtos import *
from Domain.Entities import *
from Domain.MoveTokens import *
from Service.RockPaperScisorsService import *

_service = RockPaperScisorsService()

contestRequest = CreateContestRequestDto('Bob', 3, 'rock_paper_scisors', 'pvp') #server call

player1Contest: ContestResponseDto = _service.CreateContest(contestRequest) #server call




#get the last contest in the list
contestId: uuid = None
contestList: ContestListResponseDto = _service.GetContests() #server call
for cId in contestList.contestList:
    contestId = cId



player2Contest: ContestResponseDto = _service.JoinContest(contestId) #CALL SERVER TO GET THIS



print(f'\nPlayer 1 Created Match\n{str(player1Contest)}')
print(f'\n\nPlayer 2 Joined Match\n{str(player2Contest)}')
player1Contest = _service.GetContest(contestId, player1Contest.playerId) #request to update state from server
print(f'\n\nPlayer 1 Refreshed Match\n{str(player1Contest)}')

print('===============================================================================')

placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'ROCK') #REQUEST SERVER TO PLACE MOVE
player2Contest = placeMoveResponse.contestResponse


placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'PAPER')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')

player2Contest = _service.GetContest(player2Contest.contestId, player2Contest.playerId)
placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'ROCK') #REQUEST SERVER TO PLACE MOVE
player2Contest = placeMoveResponse.contestResponse

placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'PAPER')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')


player2Contest = _service.GetContest(player2Contest.contestId, player2Contest.playerId)
placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'ROCK') #REQUEST SERVER TO PLACE MOVE
player2Contest = placeMoveResponse.contestResponse
print(f'\n\nPlayer 2 Game State:\n{str(placeMoveResponse.contestResponse)}')

placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'ROCK')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')


player2Contest = _service.GetContest(player2Contest.contestId, player2Contest.playerId)
placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'ROCK') #REQUEST SERVER TO PLACE MOVE
player2Contest = placeMoveResponse.contestResponse


placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'SCISORS')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')

player2Contest = _service.GetContest(player2Contest.contestId, player2Contest.playerId)
placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'SCISORS') #REQUEST SERVER TO PLACE MOVE
player2Contest = placeMoveResponse.contestResponse


placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'PAPER')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')


player2Contest = _service.GetContest(player2Contest.contestId, player2Contest.playerId)
placeMoveResponse = _service.PlaceMove(player2Contest.contestId, player2Contest.currentGameId, player2Contest.playerId, 'SCISORS')
player2Contest = placeMoveResponse.contestResponse

placeMoveResponse = _service.PlaceMove(player1Contest.contestId, player1Contest.currentGameId, player1Contest.playerId, 'PAPER')
player1Contest = placeMoveResponse.contestResponse

print(f'\n\nPlayer 1 Game State:\n{str(placeMoveResponse.contestResponse)}')

