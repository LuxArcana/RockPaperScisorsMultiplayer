import uuid
import random

from Domain.Dtos import *
from Domain.MoveTokens import *
from Domain.Exceptions import *





##################################
class Contest:
  def __init__ (self, createMatchRequest):
    self.contestName: str = createMatchRequest.contestName
    self.roundsToWin: int = createMatchRequest.roundsToWin
    
    gameType: str = createMatchRequest.gameType.upper()
    if gameType != 'ROCK_PAPER_SCISORS' and gameType != 'ROCK_PAPER_SCISORS_LIZARD_SPOK':
      raise InvalidGameTypeException
    self.gameType: str = gameType

    oponentType: str = createMatchRequest.oponentType.upper()
    if oponentType != 'PVP' and oponentType != 'PVE':
      raise InvalidOponentTypeException
    self.oponentType: str = oponentType

    self.contestId: uuid = uuid.uuid4()
    self.contestState: str = 'WAIT_FOR_PLAYER_JOIN'
    self.players = [uuid.uuid4()]
    self.games = dict()
    self.currentGameId: uuid = None
    self.winningPlayerId: uuid = None

    if self.oponentType == 'PVE':
      self.players.append(uuid.uuid4())
      game = Game(self.players, self.gameType, self.oponentType)
      self.games.update({game.gameId: game})
      self.currentGameId = game.gameId
      self.contestState = 'PLAYING'


  
  def Join (self) -> ContestResponseDto:
    if len(self.players) >= 2:
      raise ContestFullException

    playerId = uuid.uuid4()
    self.players.append(playerId)
    self.contestState = 'PLAYING'
    game = Game(self.players, self.gameType, self.oponentType)
    self.games.update({game.gameId: game})
    self.currentGameId = game.gameId
    return ContestResponseDto(self, playerId)



  def Cancel(self, playerId: uuid) -> ContestResponseDto:

    if self.contestState != 'WAIT_FOR_PLAYER_JOIN':
      raise CancelContestNotAllowed

    if not playerId in self.players:
      raise PlayerNotFoundException

    self.contestState = 'CANCELED'
    return ContestResponseDto(self, playerId)



  def PlaceMove (self, gameId: uuid, playerMove) -> PlaceMoveResponseDto:
    if not gameId in self.games:
      raise GameNotFoundException
    
    gameResponse = self.games[gameId].PlaceMove(playerMove)
    
    if gameResponse.gameState == 'COMPLETE': #if the game is finished add a game or end the match
      
      #calculate wins
      score = dict()
      for scoreGameId in self.games:
        scoreGame = self.games[scoreGameId]
        if scoreGame.gameState == 'COMPLETE':
          if scoreGame.winningPlayerId is not None:
            if scoreGame.winningPlayerId in score:
              playerScore = score[scoreGame.winningPlayerId] + 1
              score.update({scoreGame.winningPlayerId: playerScore})
            else:
              score.update({scoreGame.winningPlayerId: 1})
          
          
      
      for pId in score:
        if score[pId] >= self.roundsToWin:
          self.contestState = 'COMPLETE'
          self.winningPlayerId = pId
          self.currentGameId = None
          return PlaceMoveResponseDto(gameResponse, ContestResponseDto(self, playerMove.playerId))
      
      #if not enough wins make a new game
      game = Game(self.players, self.gameType, self.oponentType)
      self.games.update({game.gameId: game})
      self.currentGameId = game.gameId
      return PlaceMoveResponseDto(gameResponse, ContestResponseDto(self, playerMove.playerId))
      
    return PlaceMoveResponseDto(gameResponse, ContestResponseDto(self, playerMove.playerId))


    
###############################################################################
class Game:
  def __init__(self, players, gameType, oponentType):
    self.gameId: uuid = uuid.uuid4()
    self.gameState: str = 'WAIT_FOR_BOTH_PLAYER_MOVE'
    self.gameType: str = gameType
    self.oponentType: str = oponentType
    self.players = players
    self.moves = dict()
    self.winningPlayerId: uuid = None

    if self.oponentType == "PVE":
      self.gameState = 'WAIT_FOR_ONE_PLAYER_MOVE'
  
  
  def GetOtherPlayerId(self, playerId) -> uuid:
    for pId in self.players:
      if pId != playerId:
        return pId
      
    return None
  
  
  def PlaceMove(self, playerMove) -> GameResponseDto:
    thisPlayerId: uuid = playerMove.playerId
    
    if thisPlayerId in self.moves:
      return self.BuildResponseDto(thisPlayerId, 'YOU')
    
    if not thisPlayerId in self.players:
      raise PlayerNotFoundException
    
    move = MoveToken.FromName(playerMove.move)

    if move is None:
      raise InvalidMoveException
    
    if len(self.moves) == 0 and self.oponentType == 'PVE':
      
      posibleMoves: int = 3

      if self.gameType == 'ROCK_PAPER_SCISORS_LIZARD_SPOK':
        posibleMoves = 5

      computerMoveNumber: int = random.randint(0,posibleMoves -1)
      moveList = ['R', 'P', 'S', 'L', 'K']
      computerMoveName: str = moveList[computerMoveNumber]
      #match(computerMoveNumber):
      #  case 1:
      #    computerMoveName = 'R'
      #  case 2:
      #    computerMoveName = 'P'
      #  case 3:
      #    computerMoveName = 'S'
      #  case 4:
      #    computerMoveName = 'L'
      #  case 5:
      #    computerMoveName = 'K'
      #  case _:
      #    computerMoveName = 'INVALID'
      

      computerMove: MoveToken = MoveToken.FromName(computerMoveName)
      computerPlayerId: uuid = self.GetOtherPlayerId(thisPlayerId)
      self.moves.update({computerPlayerId: computerMove})
      
      
    
    if len(self.moves) == 0:
      self.moves.update({thisPlayerId: move})
      self.gameState = 'WAIT_FOR_ONE_PLAYER_MOVE'
      return self.BuildResponseDto(thisPlayerId, 'YOU')

    #try to add second move
    if len(self.moves) == 1:
      self.moves.update({thisPlayerId: move})
    
    
    #figure out and record the winner
    if len(self.moves) == 2:
      otherPlayerId = self.GetOtherPlayerId(thisPlayerId)
      otherPlayerMove = self.moves[otherPlayerId]
      
      if move > otherPlayerMove:
        self.winningPlayerId = thisPlayerId
      elif move < otherPlayerMove:
        self.winningPlayerId = otherPlayerId
      else:
        self.winningPlayerId = None
      
      self.gameState = 'COMPLETE'

      #if move.equality(otherPlayerMove) > 0:
      #  self.winningPlayerId = thisPlayerId
      #  self.gameState = 'COMPLETE'
      #elif move.equality(otherPlayerMove) < 0:
      #  self.winningPlayerId = otherPlayerId
      #  self.gameState = 'COMPLETE'
      #else:
      #  self.winningPlayerId = None
      #  self.gameState = 'COMPLETE'

      #result = move.equality(otherPlayerMove)
      #match result:
      #  case -1:
      #    self.winningPlayerId = otherPlayerId
      #    self.gameState = 'COMPLETE'
      #  case 0:
      #    self.winningPlayerId = None
      #    self.gameState = 'COMPLETE'
      #  case 1:
      #    self.winningPlayerId = thisPlayerId
      #    self.gameState = 'COMPLETE'
      #  case _:
      #    self.winningPlayerId = None
      #    self.gameState = 'ERROR'
        
      return self.BuildResponseDto(thisPlayerId, 'YOU')
    
    return GameResponseDto(self.gameId, 'INVALID', None, None, None)
    
    
  def BuildResponseDto(self, playerId, playerLabel: str) -> GameResponseDto:
    
    opponentMove = None
    yourMove = None
    winner = None
    
    if playerId in self.moves:
      yourMove = self.moves[playerId].Name
    
    
    
    if self.winningPlayerId is not None:
      if self.winningPlayerId == playerId:
        winner = playerLabel
      else:
        winner = 'OPPONENT'
    
      #bounds check the players array
    opponentId = None
    if self.players[0] == playerId:
      opponentId = self.players[1]
    else:
      opponentId = self.players[0]
    
    if opponentId in self.moves:
      if yourMove is not None:
        opponentMove = self.moves[opponentId].Name
        
    
    return GameResponseDto(self.gameId, self.gameState, yourMove, opponentMove, winner)

  
#########################################
class PlayerMove:
  def __init__(self, playerId, move):
    self.playerId: uuid = playerId
    self.move: str = move
  