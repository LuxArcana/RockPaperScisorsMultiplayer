from os import system
from Service.RockPaperScisorsApiConsumer import *





class RockpaperScisorsConsoleUI:
    def __init__(self, apiBaseUrl: str, apiKey: str, maxRoundsToWin: int):
        self.apiConsumer: RockPaperScisorsApiConsumer = RockPaperScisorsApiConsumer(apiBaseUrl, apiKey)
        self.maxRoundsToWin = maxRoundsToWin

        self.createContestGuid: uuid = uuid.uuid4()
        self.refreshListGuid: uuid = uuid.uuid4()
        self.exitGameGuid: uuid = uuid.uuid4()

        self.waitForOponentJoinTimeoutSeconds = 20 #place holder for user input
        self.waitForOponentMoveTimeoutSeconds = 60 #place holder for user input + 10 seconds


    def Menu_Main(self, menuItems: dict) -> uuid:
        actionGuid: uuid = None

        system('cls')
        errorHeader: str = ''

        while actionGuid is None:
            system('cls')
            print(errorHeader)
            print( '/========================================================================================================\\')
            print(f'|{"MAIN MENU":^104}|')
            print( '|========================================================================================================|')
            print( '|{0:^5}| {1:31}|{2:^32}|{3:^9}| {4:21}|'.format('', 'Name', 'Type', 'Oponent','Status'))
            print( '|-----+--------------------------------+--------------------------------+---------+----------------------|')

            for menuItem in menuItems:
                menuText: str = menuItems[menuItem][0]
                if menuItem == 'C':
                    print( '|-----+--------------------------------------------------------------------------------------------------|')
                print(menuText)
            
            print('\\========================================================================================================/')

            menuSelection: str = input('\nChoose An Option: ').upper()

            if menuSelection in menuItems:
                actionGuid = menuItems[menuSelection][1]
            else:
                menuHeader = '\n### INVALID SELECTION, TRY AGAIN ###'
                
        return actionGuid



    def Menu_GameType(self) -> str:
        gameTypeName: str = None
        errorHeader: str = ''

        while gameTypeName is None:
            print(errorHeader)
            print( ' -------------------------------------')
            print(f'|{"Game Types":^37}|')
            print( '|-------------------------------------|')
            print( '| 1 |  Rock Paper Scisors             |')
            print( '| 2 |  Rock Paper Scisors Lizard Spok |')
            print( ' -------------------------------------')
        
            gameTypeMenuSelection = input("Choose A Game Type: ")

            if gameTypeMenuSelection == '1':
                gameTypeName ='ROCK_PAPER_SCISORS'
            
            if gameTypeMenuSelection == '2':
                gameTypeName = 'ROCK_PAPER_SCISORS_LIZARD_SPOK'

            if gameTypeName == '':
                errorHeader = errorHeader = '\n\n### INVALID OPONENT, TRY AGAIN ###'
        
        return gameTypeName



    def Menu_OponentType(self) -> str:
        oponentTypeName: str = None
        errorHeader: str = ''

        while oponentTypeName is None:
            print(errorHeader)
            print( ' ------------------------------')
            print(f'|{"Oponent Types":^30}|')
            print( '|------------------------------|')
            print( '| 1 |  Human                   |')
            print( '| 2 |  Computer                |')
            print( ' ------------------------------')
            oponentTypeMenuSelection = input("Choose An Oponent Type: ")

            if oponentTypeMenuSelection == '1':
                oponentTypeName ='PVP'
            
            if oponentTypeMenuSelection == '2':
                oponentTypeName = 'PVE'

            if oponentTypeName == '':
                errorHeader = errorHeader = '\n\n### INVALID OPONENT, TRY AGAIN ###'
        
        return oponentTypeName



    def Menu_RoundsToWin(self) -> int:
        roundsToWin: int = None
        while roundsToWin is None:
            rawRoundsToWin: str = input(f'How Many Victories Are Required To Win Your Contest (Max: {self.maxRoundsToWin})? ')
            try:
                roundsToWin = int(rawRoundsToWin)
            except:
                roundsToWin = None
        
        return roundsToWin



    def Menu_ContestName(self) -> str:
        contestName: str = input('Enter A Name For Your Contest: ')
        
        if len(contestName) == 0:
            contestName = 'NO CONTEST NAME'
        
        return contestName[:30]



    def Menu_GetMove(self, gameType: str) -> str:
        abrvMoves: str = 'R,P,S'
        errorHeader: str = ''
        moveName: str = None

        while moveName is None:
            print(errorHeader)
            print( ' ------------------------------')
            print(f'|{"Avaialbe Moves":^30}|')
            print( '|------------------------------|')
            print( '| R |  Rock                    |')
            print( '| P |  Paper                   |')
            print( '| S |  Scisors                 |')
            
            if gameType == 'ROCK_PAPER_SCISORS_LIZARD_SPOK':
                abrvMoves = 'R,P,S,L,K'
                print( '| L |  Lizard                  |')
                print( '| K |  Spok                    |')

            print( ' ------------------------------')

            rawInput = input(f'Enter A Move ({abrvMoves}): ')
            move = MoveTokenBuilder.FromName(rawInput)
            if move is not None and move.Name != 'INVALID':
                moveName = move.Name
            else:
                errorHeader = '\n\n### INVALID MOVE, TRY AGAIN ###'

        return moveName




    def GetMenuDisplayTextFromContestDict(self, contest: dict, menuIndex: int) -> str:
        return f'|{menuIndex:^5}| {contest["contestName"]:31}|{contest["gameType"]:^32}|{contest["oponentType"]:^9}| {contest["contestState"]:21}|'


    def BuildMainMenuItems(self, contestList: dict) -> dict:
        menuItems: dict = dict()
        menuIndex: int = 1

        for contestDict in contestList:
            menuText: str = self.GetMenuDisplayTextFromContestDict(contestDict, menuIndex)
            menuItems.update({str(menuIndex): (menuText, contestDict["contestId"])})
            menuIndex += 1

        menuText = f'|{"C":^5}| {"Create New Contest":31}  {"":31} {"":^9}  {"":21}|'
        menuItems.update({"C":(menuText, self.createContestGuid)})

        menuText = f'|{"R":^5}| {"Refresh Contests":31}  {"":31} {"":^9}  {"":21}|'
        menuItems.update({"R":(menuText, self.refreshListGuid)})

        menuText = f'|{"X":^5}| {"Exit Game":31}  {"":31} {"":^9}  {"":21}|'
        menuItems.update({"X":(menuText, self.exitGameGuid)})

        return menuItems




    def PlayContest(self, contestDtoDict: dict):
        self.DisplayContest(contestDtoDict)

        while contestDtoDict["contestState"] == 'WAIT_FOR_PLAYER_JOIN':
            print('Waiting For Player To Join')
            self.apiConsumer.WaitForContestStateChangeFrom(contestDtoDict, 'WAIT_FOR_PLAYER_JOIN', self.waitForOponentJoinTimeoutSeconds)
            if contestDtoDict["contestState"] == 'WAIT_FOR_PLAYER_JOIN':
                keepWaitingForOponent: str = input("No Oponent Has Joined This Game Yet.  Would You Like To Keep Waiting (y/n)? ")
                if keepWaitingForOponent.upper() != 'Y':
                    self.apiConsumer.CancelContest(contestDtoDict["contestId"], contestDtoDict["playerId"])
                    return

        
        while contestDtoDict["contestState"] == 'PLAYING':
            (gameDtoDict, contestDtoDict) = self.apiConsumer.PostMove(contestDtoDict, self.Menu_GetMove(contestDtoDict["gameType"]))
            self.DisplayContest(contestDtoDict)

            gameState: str = gameDtoDict["gameState"]
            gameId: str = gameDtoDict["gameId"]
            if gameState != "COMPLETE":
                print("\nWaiting For Oponent To Move...")
                (gameDtoDict, contestDtoDict) = self.apiConsumer.WaitForGameState(contestDtoDict, gameId, gameState, 'COMPLETE', self.waitForOponentMoveTimeoutSeconds)
                if gameDtoDict["gameState"] != "COMPLETE":
                    print("GAME IS BROKEN") #THIS SHOULD NOT HAPPEN AFTER MOVE COUNTDOWNS ARE IMPLIMENTED
                    return
                
        self.DisplayContest(contestDtoDict)
        input('Press Enter To Return To The Main Menu\n')




    def DisplayContest(self, contestDtoDict: dict):
        contestName: str = str(contestDtoDict["contestName"]) 
        gameType: str = str(contestDtoDict["gameType"])
        oponentType: str = str(contestDtoDict["oponentType"])
        roundsToWin: str = str(contestDtoDict["roundsToWin"])
        winner: str = str(contestDtoDict["winningPlayer"])

        system('cls')
        print( '/=================================================\\')
        print( '|  Contest Name:   {0:30} |'.format(contestName))
        print( '|  Game Type:      {0:30} |'.format(gameType))
        print( '|  Oponent Type:   {0:30} |'.format(oponentType))
        print( '|  Rounds To Win:  {0:30} |'.format(roundsToWin))
        print( '|                  {0:30} |'.format(""))
        print( '|  Winner:         {0:30} |'.format(winner))
        print( '|                  {0:30} |'.format(""))
        print( '|-----------\\      {0:30} |'.format(""))
        print( '|   Games   |      {0:30} |'.format(""))
        print( '|-------------------------------------------------|')
        print( '|{0:^11}|{1:^12}|{2:^12}|{3:^11}|'.format('State', 'Your Move', 'Their Move', 'Winner'))
        print( '|-------------------------------------------------|')
        
        for game in contestDtoDict["games"]:
            state: str = str(game["gameState"])
            if 'WAIT' in state:
                state = 'WAITING'
            yourMove: str = str(game["yourMove"])
            theirMove: str = str(game["opponentMove"])
            gameWinner: str = str(game["winner"])
            print(f'|{state:^11}|{yourMove:^12}|{theirMove:^12}|{gameWinner:^11}|')

        print('\\=================================================/\n')



    def Play(self):

        keepPlaying: bool = True

        while keepPlaying:
            contestDtoDict: dict = None

            contestList = self.apiConsumer.GetContestList()
            actionGuid: uuid = self.Menu_Main(self.BuildMainMenuItems(contestList))
            if actionGuid == self.createContestGuid:
                contestDtoDict = self.apiConsumer.CreateContest(self.Menu_ContestName(), self.Menu_RoundsToWin() , self.Menu_GameType(), self.Menu_OponentType())
            elif actionGuid == self.exitGameGuid:
                keepPlaying = False
            elif actionGuid == self.refreshListGuid or actionGuid is None:
                pass #do nothing and redraw menu
            else: #look for a contest
                for contestDto in contestList:
                    if contestDto["contestId"] == actionGuid:
                        contestDtoDict = contestDto
                        break
            
            if contestDtoDict is not None:
                self.PlayContest(contestDtoDict)

        print('\n================================\n--Goodbye, Thanks For Playing\n================================\n\n')

