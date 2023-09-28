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
        #system('cls')
        menuHeader: str = '\n\n-----------------------\nMain Menu\n-----------------------'

        while actionGuid is None:
            print(menuHeader)
            for menuItem in menuItems:
                menuText: str = menuItems[menuItem][0]
                print(f'{menuItem})\t{menuText}')
            
            menuSelection: str = input('\nChoose An Option: ').upper()

            if menuSelection in menuItems:
                actionGuid = menuItems[menuSelection][1]
            else:
                menuHeader = '\n\n-----------------------\nINVALID SELECTION\nMain Menu\n-----------------------'
                
        return actionGuid



    def Menu_GameType(self) -> str:

        gameTypeName: str = None

        while gameTypeName is None:
            print ('\n\n-----------------------')
            print ('++    Game Type      ++')
            print ('-----------------------')
            print('1)\tRock Paper Scisors')
            print('2)\tRock Paper Scisors Lizard Spok\n')
        
            gameTypeMenuSelection = input("Choose A Game Type: ")

            if gameTypeMenuSelection == '1':
                gameTypeName ='ROCK_PAPER_SCISORS'
            
            if gameTypeMenuSelection == '2':
                gameTypeName = 'ROCK_PAPER_SCISORS_LIZARD_SPOK'
        
        return gameTypeName



    def Menu_OponentType(self) -> str:
        oponentTypeName: str = None

        while oponentTypeName is None:
            print ('-----------------------')
            print ('++    Oponent Type   ++')
            print ('-----------------------')
            print('1)\tHuman')
            print('2)\tComputer\n')
        
            oponentTypeMenuSelection = input("Choose An Oponent Type: ")

            if oponentTypeMenuSelection == '1':
                oponentTypeName ='PVP'
            
            if oponentTypeMenuSelection == '2':
                oponentTypeName = 'PVE'
        
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
        
        return contestName



    def Menu_GetMove(self, gameType: str) -> str:
        abrvMoves: str = 'R,P,S'
        menuHeader: str = '\n\nMove Menu\n---------'
        moveName: str = None

        while moveName is None:
            #system('cls')
            print(menuHeader)
            print('R)\tRock')
            print('P)\tPaper')
            print('S)\tScisors')
            if gameType == 'ROCK_PAPER_SCISORS_LIZARD_SPOK':
                abrvMoves = 'R,P,S,L,K'
                print('L)\tLizard')
                print('K)\tspoK')

            rawInput = input(f'Enter A Move ({abrvMoves}): ')
            move = MoveTokenBuilder.FromName(rawInput)
            if move is not None and move.Name != 'INVALID':
                moveName = move.Name
            else:
                menuHeader = '\n\n-----------------\nINVALID SELECTION\nTry Again\nMove Menu\n-----------------'

        return moveName




    def GetMenuDisplayTextFromContestDict(self, contest: dict) -> str:
        return f'Name: {contest["contestName"]}\tType: {contest["gameType"]}\tOponent: {contest["oponentType"]}\tStatus: {contest["contestState"]}'



    def BuildMainMenuItems(self, contestList: dict) -> dict:
        menuItems: dict = dict()
        menuIndex: int = 1

        for contestDict in contestList:
            menuText: str = self.GetMenuDisplayTextFromContestDict(contestDict)
            menuItems.update({str(menuIndex): (menuText, contestDict["contestId"])})
            menuIndex += 1

        menuItems.update({"C":("Create New Contest", self.createContestGuid)})
        menuItems.update({"R":("Refresh Contests", self.refreshListGuid)})
        menuItems.update({"X":("Exit Game", self.exitGameGuid)})
        return menuItems




    def PlayContest(self, contestDtoDict: dict):
        
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
            print(f'{gameDtoDict}\n')

            gameState: str = gameDtoDict["gameState"]
            gameId: str = gameDtoDict["gameId"]
            if gameState != "COMPLETE":
                print("Waiting For Oponent")
                (gameDtoDict, contestDtoDict) = self.apiConsumer.WaitForGameState(contestDtoDict, gameId, gameState, 'COMPLETE', self.waitForOponentMoveTimeoutSeconds)
                if gameDtoDict["gameState"] != "COMPLETE":
                    print("GAME IS BROKEN") #THIS SHOULD NOT HAPPEN AFTER MOVE COUNTDOWNS ARE IMPLIMENTED
                    return
            
            print(f'\n{gameDtoDict}\n')
                
        print(contestDtoDict)
        input('Press Enter To Return To The Main Menu\n')




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

