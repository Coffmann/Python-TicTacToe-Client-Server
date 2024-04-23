from threading import Thread
import socket as so
from time import sleep

symbol_X = [
    " XX   XX ",
    "  XX XX  ",
    "   XXX   ",
    "  XX XX  ",
    " XX   XX "
]

symbol_O = [
    "  OOOOO  ",
    " OO   OO ",
    " OO   OO ",
    " OO   OO ",
    "  OOOOO  "
]

symbol_None = [
    "         ",
    "         ",
    "    x    ",
    "         ",
    "         "
]

symbol_border = [
    "┌─────────┬─────────┬─────────┐",
    "│",
    "├─────────┼─────────┼─────────┤",
    "└─────────┴─────────┴─────────┘"
]

#DEBUG
printConsole = False

class Board:
    def __init__(self,  GameID) -> None:
        for _ in allBoards:
            if _.GameID == GameID:
                return
        self.GameID = GameID
        self.BoardData = [None] * 9 #BoardData is a list of 9 elements None = Leer, 0 = O , 1 = X
        self.Player2_Data:so.socket = None 
        self.Game_Thread = None
        allBoards.append(self)
        #PlayerX_Data.send handles both Printing and Input so to make a diffrence between them is a Prefix needed
        #Prefix for print its "P_" and for an input its "I_", "C_" will clear the Console and "X_" will end the Game for the client
        pass

    def getBoardStr(self) -> str:
        '''
        This function returns a string of the current board, formatted to be used in the console.
        '''
        if printConsole:
            print(symbol_border[0])
        #Top Border
        fullstr = symbol_border[0] + "\n"
        #Row 1
        for _ in range(0, 5): # Check what should go into each Field and then gets all 5 Lines of the Symbol to print it.
            row1 = symbol_X[_] if self.BoardData[0] == 1 else (symbol_O[_] if self.BoardData[0] == 0 else symbol_None[_].replace("x","1"))
            row2 = symbol_X[_] if self.BoardData[1] == 1 else (symbol_O[_] if self.BoardData[1] == 0 else symbol_None[_].replace("x","2"))
            row3 = symbol_X[_] if self.BoardData[2] == 1 else (symbol_O[_] if self.BoardData[2] == 0 else symbol_None[_].replace("x","3"))
            if printConsole: # Debug print
                print(symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1])
            fullstr += symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1] + "\n"
        #Middle Line
        fullstr += symbol_border[2] + "\n"
        #Row 2
        if printConsole:
            print(symbol_border[2])
        for _ in range(0, 5):
            row1 = symbol_X[_] if self.BoardData[3] == 1 else (symbol_O[_] if self.BoardData[3] == 0 else symbol_None[_].replace("x","4"))
            row2 = symbol_X[_] if self.BoardData[4] == 1 else (symbol_O[_] if self.BoardData[4] == 0 else symbol_None[_].replace("x","5"))
            row3 = symbol_X[_] if self.BoardData[5] == 1 else (symbol_O[_] if self.BoardData[5] == 0 else symbol_None[_].replace("x","6"))
            if printConsole:
                print(symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1])
            fullstr += symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1] + "\n"
        #Middle Line
        fullstr += symbol_border[2] + "\n"
        #Row 3
        if printConsole:
            print(symbol_border[2])
        for _ in range(0, 5):
            row1 = symbol_X[_] if self.BoardData[6] == 1 else (symbol_O[_] if self.BoardData[6] == 0 else symbol_None[_].replace("x","7"))
            row2 = symbol_X[_] if self.BoardData[7] == 1 else (symbol_O[_] if self.BoardData[7] == 0 else symbol_None[_].replace("x","8"))
            row3 = symbol_X[_] if self.BoardData[8] == 1 else (symbol_O[_] if self.BoardData[8] == 0 else symbol_None[_].replace("x","9"))
            if printConsole:
                print(symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1])
            fullstr += symbol_border[1] + row1 + symbol_border[1] + row2 + symbol_border[1] + row3 + symbol_border[1] + "\n"
        #Bottom Border
        fullstr += symbol_border[3] + "\n"
        if printConsole:
            print(symbol_border[3])

        return fullstr
    def User1Pick(self):
        '''
         This function handles the User's (Host) turn. It takes the input from the user and checks if the position is already taken.
         If the position is already taken, it will ask the user to enter another position.
        '''
        self.Player2_Data.send(str("P_User 1's turn").encode())
        handleSocketResponse(str("P_User 1's turn"))

        position = int(input(str("Enter position (1-9):")))-1
        while self.BoardData[position] is not None:
            handleSocketResponse(str("P_Position already taken. Choose another position."))
            position = int(input(str("Enter position (1-9):")))-1
        self.BoardData[position] = 1

    def User2Pick(self):
        '''
         This function handles the User's (Client) turn. It takes the input from the user and checks if the position is already taken.
         If the position is already taken, it will ask the user to enter another position.
        '''
        handleSocketResponse(str("P_User 2's turn"))
        self.Player2_Data.send(str("P_User 2's turn").encode())

        self.Player2_Data.send(str("I_Enter position (1-9):").encode())
        position = int(self.Player2_Data.recv(1024).decode())-1
        while self.BoardData[position] is not None:
            self.Player2_Data.send(str("P_Position already taken. Choose another position.").encode())
            self.Player2_Data.send(str("I_Enter position (1-9):").encode())
            position = int(self.Player2_Data.recv(1024).decode())-1
        self.BoardData[position] = 0

    def tic_tac_toe_winner(self):
        # check horizontal lines
        for i in range(0, 9, 3):
            if self.BoardData[i] == self.BoardData[i + 1] == self.BoardData[i + 2] and self.BoardData[i] is not None:
                #
                return self.BoardData[i]

        # check vertical lines
        for i in range(3):
            if self.BoardData[i] == self.BoardData[i + 3] == self.BoardData[i + 6] and self.BoardData[i] is not None:
                return self.BoardData[i]

        # check cross lines \ /
        if self.BoardData[0] == self.BoardData[4] == self.BoardData[8] and self.BoardData[0] is not None:
            return self.BoardData[0]
        if self.BoardData[2] == self.BoardData[4] == self.BoardData[6] and self.BoardData[2] is not None:
            return self.BoardData[2]

        # No Winner Found (Draw or Game not finished)
        return None
    
    def __UpdateBoardForPlayers(self):
        '''
        This function will update the Board for both Players.
        It will send the Board to both Players.
        (It will clear the Terminals first)
        '''
        board_text = self.getBoardStr()
        handleSocketResponse(str("C_"))
        sleep(0.1)
        handleSocketResponse(str("P_"+board_text))
        self.Player2_Data.send(str("C_").encode())
        sleep(0.1)
        self.Player2_Data.send(str("P_"+board_text).encode())
    
    def __GameLoop(self) -> None:
        ''' 
        This function gets called in a new Thread to Manage the Game itself.
        It will loop until a winner is found or the board is full.
        '''
        # Clear Terminal
        handleSocketResponse(str("C_"))
        self.Player2_Data.send(str("C_").encode())
        sleep(0.1)
        #Check for Free Spaces inside the Game Grid
        empty = 0
        for _ in self.BoardData:
            if _ is None:
                empty=empty+1
        while self.tic_tac_toe_winner() is None and empty != 0: #Wenn Winner is None and the Board still got free Spaces
            # Update Board for Players
            self.__UpdateBoardForPlayers()
            sleep(0.1)
            #Player 1 Turn
            self.User1Pick()
            #Check for Free Spaces inside the Game Grid
            empty = 0
            for _ in self.BoardData:
                if _ is None:
                    empty=empty+1
            if self.tic_tac_toe_winner() is not None or empty ==0: # If Winner is found or no free Spaces left
                break
            # Update Board for Players
            self.__UpdateBoardForPlayers()
            sleep(0.1)
            #Player 2 Turn
            self.User2Pick()
            #Check for Free Spaces inside the Game Grid
            empty = 0
            for _ in self.BoardData:
                if _ is None:
                    empty=empty+1
            #Recieve Text 
        sleep(0.1)
        # Update Board for Players
        self.__UpdateBoardForPlayers()
        #Gets the Winner
        winner = self.tic_tac_toe_winner()
        if winner is None:
            winner = "It's a draw!"
        elif str(winner) == "1":
            winner = "Player1 (host) won!"
        else:  
            winner = "Player2 (client) won!"
        #Sends the Winner to both Players
        handleSocketResponse(str("P_"+winner))
        self.Player2_Data.send(str("P_"+winner).encode())
        sleep(0.1)
        #Sends "GameEnd" command to Client.
        self.Player2_Data.send(str("X_").encode())

    def startGame(self) -> None:
        ''' Starts the Game '''
        if(self.Player2_Data is not None):
            self.Game_Thread = Thread(target=self.__GameLoop)
            self.Game_Thread.start()

    def joinGame(self,Player_data:so.socket):
        ''' Adds a Player to the Game '''
        if self.Player2_Data is None:
            self.Player2_Data = Player_data
            self.Player2_Data.send(str("P_You are User 2").encode())
        else:
            raise Exception("JoIn FaIlEd BuT HoW Tf DiD yOu GeT hErE")
        return
    
# Functions
    
def get_ip():
    # Get LocalIP Adress from PC to host it in LAN
    s = so.socket(so.AF_INET, so.SOCK_DGRAM)
    s.settimeout(0)
    try:
        #Even when there is no Device at this IP it will still work
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0] # Get Local IP
    except Exception:
        IP = '127.0.0.1' #If a Error Occurs it will be localhost
    finally:
        s.close() # Close Socket
    return IP

allBoards : list[Board] = []


#--------------------
#ClientSide Code to Play
#--------------------
import os

#Clientside Handler nearly 1:1 copy from client.py
def handleSocketResponse(text):
    if "C_" in text:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    if "P_" in text:
        print(text[2:].replace("P_",""))
    if "I_" in text:
        text = text[2:].replace("I_","")
        return input(text)
    if "X_" in text:
        return # Useless on ServerSide


server_socket = so.socket(so.AF_INET, so.SOCK_STREAM) # Create Socket for Server
server_socket.bind((get_ip(), 45545)) # Bind Socket to IP and Port
server_socket.listen() # Wait for a Connection
client_socket, address = server_socket.accept() # Accept the Connection and save in Vars
MyGame= Board("IAmAGame") # Create the Game
MyGame.joinGame(client_socket) # Add the connected Player to the Game
MyGame.startGame() # Starts the Game.

