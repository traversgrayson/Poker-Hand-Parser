#import some libraries we will need
import csv
import glob

#These are the global variables we use to
#keep track of game data. Not the most 
#elegant approach, but suitable for this 
#purpose
writer = 0
myState = 0
numPlayers = 0
potSize = 0
seatVec = [0,0,0,0,0,0]
stackVec = [0,0,0,0,0,0]
betVec3 = [0,0,0,0,0,0]
raiseVec3 = [[],[],[],[],[],[]]
callVec3 = [[],[],[],[],[],[]]
betVec4 = [0,0,0,0,0,0]
raiseVec4 = [[],[],[],[],[],[]]
callVec4 = [[],[],[],[],[],[]]
betVec5 = [0,0,0,0,0,0]
raiseVec5 = [[],[],[],[],[],[]]
callVec5 = [[],[],[],[],[],[]]
betVec6 = [0,0,0,0,0,0]
raiseVec6 = [[],[],[],[],[],[]]
callVec6 = [[],[],[],[],[],[]]
winVec = [0,0,0,0,0,0]

#setRaises(stringy,raisey,dingle,4)

# setState
# INPUTS: a string for every line
# The current gamestate
def setState(myStr):
    global myState
    if "Stage" in myStr:
        myState = 1
        return
    # Check to see if we have proper number of players
    if ("sit out" in myStr) or ("sitout" in myStr) or ("No small blind" in myStr):
        myState = 0
    if "Posts small blind" in myStr:
        if numPlayers != 6:
            myState = 0
            return
        else:
            myState = 2 
            return
    # If we have 6 players proceed parsing normally
    # o/w gameState doesn't change
    if myState != 0:        
        if "*** POCKET CARDS ***" in myStr:
            myState = 3
            return
        if "*** FLOP ***" in myStr:
            myState = 4
            return
        if "*** TURN ***" in myStr:
            myState = 5
            return
        if "*** RIVER ***" in myStr:
            myState = 6
            return
        if "*** SHOW DOWN **" in myStr:
            myState = 7
            return
        if "*** SUMMARY ***" in myStr:
            myState = 8
            return
        else:
            return
    else:
        return
    
# setSeats
# INPUTS: a string in the gamestate 1
#         a vector linking player names to seats
#         and an index for current seat number
# OUTPUTS: an updated vector linking player names
#         to seats
def setSeats(myStr):
    global seatVec
    global numPlayers
    if "chips" in myStr:
        if not(numPlayers >= 6):
            #Get player name from myString
            namesky = myStr.split(" ")[3]
            seatVec[numPlayers] = namesky
            numPlayers = numPlayers + 1
            return
        else: 
            numPlayers = numPlayers + 1
            return
    else:
        return
       
# setChipCount
# INPUTS: a string in the gamestate 1
#         a vector linking chip counts to seats
#         and an index for current seat number
# OUTPUTS: an updated vector linking player names
#         to seats
def setChipCount(myStr):
    global stackVec
    if "chips" in myStr:
        if not(numPlayers >= 7):
            chipskystr = myStr.split("$")[1].split(" ")[0]
            chipsky = float(chipskystr)
            stackVec[numPlayers-1] = chipsky
            return
        else: 
            return
    else: 
        return
    
# setPotSize
# INPUTS: a string in the gamestate 2-5
#         a float of current pot size
# OUTPUTS: an updated pot size        
def setPotSize(myStr):
    global potSize
    if ("$" in myStr) and not("returned" in myStr) and not("Collects" in myStr):
        moneys = float(myStr.split("$")[1].split(" ")[0])
        potSize = potSize + moneys
        return

# setWinner
# INPUTS: a string in the gamestate 7
# OUTPUTS: a vector of 0’s and 1’s
# 	  representing the winner(s) 
#         of the round
def setWinner(myStr):
    global winVec       
    if ("Collects" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        betVec3[indy] = 1
        return
    else:
        return
    
# setBets3
# INPUTS: a string in gamestate 3
#         a vector of bet info
#         a vector of seat info
# OUTPUTS: and updated vector representing
#        bets in the Pocket Cards
def setBets3(myStr):
    global betVec3       
    if ("Bets" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        betVec3[indy] = float(moneys/potSize)
        return
    else:
        return
    
# setRaises3
# INPUTS: a string in gamestate 3
#         a vector of raise info
#         a vector of seat info
# OUTPUTS: and updated vector representing
#        raises in the Pocket Cards
def setRaises3(myStr):
    global raiseVec3
    if ("Raise" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        raiseVec3[indy].append(moneys/potSize)
        return
    else:
        return
    
# setCalls3
# INPUTS: a string in gamestate 3
#         a vector of call info
#         a vector of seat info
# OUTPUTS: and updated vector representing
#        calls in the Pocket Cards
def setCalls3(myStr):
    global callVec3
    if ("Call" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        callVec3[indy].append(moneys/potSize)
        return
    else:
        return
    
# same as setBets3 but for Flop
def setBets4(myStr):
    global betVec4       
    if ("Bets" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        betVec4[indy] = moneys/potSize
        return
    else:
        return
    
# same as setRaises3 but for Flop
def setRaises4(myStr):
    global raiseVec4
    if ("Raise" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        raiseVec4[indy].append(moneys/potSize)
        return
    else:
        return
    
# same as setCalls3 but for Flop
def setCalls4(myStr):
    global callVec4
    if ("Call" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        callVec4[indy].append(moneys/potSize)
        return
    else:
        return
    
    
# same as setBets3 but for Turn
def setBets5(myStr):
    global betVec5       
    if ("Bets" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        betVec5[indy] = moneys/potSize
        return
    else:
        return

# same as setRaises3 but for Turn
def setRaises5(myStr):
    global raiseVec5
    if ("Raise" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        raiseVec5[indy].append(moneys/potSize)
        return
    else:
        return
    
# same as setRaises3 but for Turn
def setCalls5(myStr):
    global callVec5
    if ("Call" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        callVec5[indy].append(moneys/potSize)
        return
    else:
        return
    
# same as setBets3 but for River
def setBets6(myStr):
    global betVec6       
    if ("Bets" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        betVec6[indy] = moneys/potSize
        return
    else:
        return
    
# same as setRaises3 but for River
    global raiseVec6
    if ("Raise" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        raiseVec6[indy].append(moneys/potSize)
        return
    else:
        return
    
# same as setCalls3 but for River
def setCalls6(myStr):
    global callVec6
    if ("Call" in myStr):
        name = myStr.split(" ")[0]
        indy = seatVec.index(name)
        moneys = float(myStr.split("$")[1].split(" ")[0])
        callVec6[indy].append(moneys/potSize)
        return
    else:
        return
# avgVec
# INPUTS: a vector to be averaged
# OUTPUTS: a float of the average
def avgVec(vecky):
    for i in range(0, len(vecky)):
        if len(vecky[i])==0:
            vecky[i] = 0
        else:    
            vecky[i] = sum(vecky[i])/len(vecky[i])
    return(vecky)    
#initGame
#INPUTS: none
#OUTPUTS: resets all global vars  
def initGame():
     global myState
     global numPlayers
     global potSize
     global seatVec
     global stackVec
     global betVec3
     global raiseVec3
     global callVec3
     global betVec4
     global raiseVec4
     global callVec4
     global betVec5
     global raiseVec5
     global callVec5
     global betVec6
     global raiseVec6
     global callVec6
     global winVec
     myState = 0
     numPlayers = 0
     potSize = 0
     seatVec = [0,0,0,0,0,0]
     stackVec = [0,0,0,0,0,0]
     betVec3 = [0,0,0,0,0,0]
     raiseVec3 = [[],[],[],[],[],[]]
     callVec3 = [[],[],[],[],[],[]]
     betVec4 = [0,0,0,0,0,0]
     raiseVec4 = [[],[],[],[],[],[]]
     callVec4 = [[],[],[],[],[],[]]
     betVec5 = [0,0,0,0,0,0]
     raiseVec5 = [[],[],[],[],[],[]]
     callVec5 = [[],[],[],[],[],[]]
     betVec6 = [0,0,0,0,0,0]
     raiseVec6 = [[],[],[],[],[],[]]
     callVec6 = [[],[],[],[],[],[]]
     winVec = [0,0,0,0,0,0]

#makeGameArray
#INPUTS: all global arrays
#OUTPUTS: collapses into a 1 dimensional
#       array containing all of the info
#      to be saved
def makeGameArray():
    gameArray = []
    gameArray.extend(seatVec)
    gameArray.extend(stackVec)
    gameArray.extend(winVec)
    gameArray.extend(avgVec(raiseVec3))
    gameArray.extend(avgVec(callVec3))
    gameArray.extend(betVec4)
    gameArray.extend(avgVec(raiseVec4))
    gameArray.extend(avgVec(callVec4))
    gameArray.extend(betVec5)
    gameArray.extend(avgVec(raiseVec5))
    gameArray.extend(avgVec(callVec5))
    gameArray.extend(betVec6)
    gameArray.extend(avgVec(raiseVec6))
    gameArray.extend(avgVec(callVec6))

    gameArray.extend(betVec3)
    return gameArray

header = ['Dealer (0)','SB (1)','BB (2)', 'UTG (3)', 'UTG+1 (4)', 'CUT-OFF (5)', 'Stack (0)', 'Stack(1)', 'Stack(2)', 'Stack(3)','Stack(4)', 'Stack(5)', 
'PC Bet (0)', 'PC Bet (1)', 'PC Bet (2)', 'PC Bet (3)', 'PC Bet (4)', 'PC Bet (5)',
'PC Raise (0)', 'PC Raise (1)', 'PC Raise (2)', 'PC Raise (3)', 'PC Raise (4)', 'PC Raise (5)',
'PC Call (0)', 'PC Call (1)', 'PC Call (2)', 'PC Call (3)', 'PC Call (4)', 'PC Call (5)',
'Flop Bet (0)', 'Flop Bet (1)', 'Flop Bet (2)', 'Flop Bet (3)', 'Flop Bet (4)', 'Flop Bet (5)',
'Flop Raise (0)', 'Flop Raise (1)', 'Flop Raise (2)', 'Flop Raise (3)', 'Flop Raise (4)', 'Flop Raise (5)',
'Flop Call (0)', 'Flop Call (1)', 'Flop Call (2)', 'Flop Call (3)', 'Flop Call (4)', 'Flop Call (5)',
'Turn Bet (0)', 'Turn Bet (1)', 'Turn Bet (2)', 'Turn Bet (3)', 'Turn Bet (4)', 'Turn Bet (5)',
'Turn Raise (0)', 'Turn Raise (1)', 'Turn Raise (2)', 'Turn Raise (3)', 'Turn Raise (4)', 'Turn Raise (5)',
'Turn Call (0)', 'Turn Call (1)', 'Turn Call (2)', 'Turn Call (3)', 'Turn Call (4)', 'Turn Call (5)',
'River Bet (0)', 'River Bet (1)', 'River Bet (2)', 'River Bet (3)', 'River Bet (4)', 'River Bet (5)',
'River Raise (0)', 'River Raise (1)', 'River Raise (2)', 'River Raise (3)', 'River Raise (4)', 'River Raise (5)',
'River Call (0)', 'River Call (1)', 'River Call (2)', 'River Call (3)', 'River Call (4)', 'River Call (5)', 
'Winner? (0)', 'Winner? (1)', 'Winner? (2)', 'Winner? (3)', 'Winner? (4)', 'Winner? (5)']

#parseHandFile
#INPUTS: A text file
#OUTPUTS: A set of csv rows with all of the 
#         data from that file
def parseHandFile(filename):
    global writer
    file = open(filename)
    for line in file:
        myStr = line.strip()
       # print(myStr)
        if ("Stage" in myStr):
            if myState != 0:
               gmAry = makeGameArray()
               writer.writerow(gmAry) 
        ### Write to CSV ###
            initGame()
        setState(myStr) 
       # print(myStr + ":   " + str(myState))   
        if myState == 1: 
            setSeats(myStr)
            setChipCount(myStr)
        if myState == 2:
            setPotSize(myStr)
        if myState == 3:
            setBets3(myStr)
            setRaises3(myStr)
            setCalls3(myStr)
            setPotSize(myStr)
        if myState == 4:
            setBets4(myStr)
            setRaises4(myStr)
            setCalls4(myStr)
            setPotSize(myStr)
        if myState == 5:
            setBets5(myStr)
            setRaises5(myStr)
            setCalls5(myStr)
            setPotSize(myStr)
        if myState == 6:
            setBets6(myStr)
            setRaises6(myStr)
            setCalls6(myStr)
            setPotSize(myStr)
        if myState == 7:
            setWinner(myStr)

  
#main
#INPUTS: a folder filled with poker text files
#OUTPUTS: a csv of parsed data            
def main():
    global writer
    f = open('test.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(header)
    listy = glob.glob('./*.txt')
    for file in listy:
        try:
            print(file)
            parseHandFile(file)
        except:
            continue
    f.close()
            
            
main()          