from Domain.Dtos import *
from Domain.Entities import *
from Domain.MoveTokens import *
from Domain.Exceptions import *







class RockPaperScisorsService:
    
    
    def __init__(self):
        self.contests = dict()



    def CreateContest(self, contestRequest) -> ContestResponseDto:
        newContest: Contest = Contest(contestRequest)
        self.contests.update({newContest.contestId: newContest})
        return  ContestResponseDto(newContest, newContest.players[0])
    


    def JoinContest(self, contestId: uuid) -> ContestResponseDto:
        if not contestId in self.contests:
            raise ContestNotFoundException
        
        targetContest: Contest = self.contests[contestId]
        
        return targetContest.JoinContest()



    def GetContest(self, contestId: uuid, playerId: uuid) -> ContestResponseDto:
        if not contestId in self.contests:
            raise ContestNotFoundException
        
        targetContest: Contest = self.contests[contestId]

        return ContestResponseDto(targetContest, playerId)
    




    def GetContests(self) -> ContestListResponseDto:
        return ContestListResponseDto(self.contests)





    def PlaceMove(self, contestId: uuid, gameId: uuid, playerId: uuid, moveName: str) -> PlaceMoveResponseDto:
        if not contestId in self.contests:
            raise ContestNotFoundException
        
        targetContest: Contest = self.contests[contestId]

        playerMove: PlayerMove = PlayerMove(playerId, moveName)

        return targetContest.PlaceMove(gameId, playerMove)
