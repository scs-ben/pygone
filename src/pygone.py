#!/usr/bin/env python3
import copy, math, os, sys, subprocess, time

openingBook = {'e2e4': 'e7e5', 'd2d4': 'd7d5', 'c2c4': 'c7c5', 'g1f3': 'c7c5'}
piecePoints = {'p': 100.0, 'r': 479.0, 'n': 280.0, 'b': 320.0, 'q': 929.0, 'k': 60000.0}
attackPoints = {'p': 5.0, 'r': 18.0, 'n': 10.0, 'b': 10.0, 'q': 20.0, 'k': 30.0}

pPSQT = [[0,0,0,0,0,0,0,0],
  [78,83,86,73,102,82,85,90],
  [7,29,21,44,40,31,44,7],
  [-17,16,-2,15,14,0,15,-13],
  [-26,3,10,9,6,1,0,-23],
  [-22,9,5,-11,-10,-2,3,-19],
  [-31,8,-7,-37,-36,-14,3,-31],
  [0,0,0,0,0,0,0,0]]
nPSQT = [[-66,-53,-75,-75,-10,-55,-58,-70],
  [-3,-6,100,-36,4,62,-4,-14],
  [10,67,1,74,73,27,62,-2],
  [24,24,45,37,33,41,25,17],
  [-1,5,31,21,22,35,2,0],
  [-18,10,13,22,18,15,11,-14],
  [-23,-15,2,0,2,0,-23,-20],
  [-74,-23,-26,-24,-19,-35,-22,-69]]
bPSQT = [[-59,-78,-82,-76,-23,-107,-37,-50],
  [-11,20,35,-42,-39,31,2,-22],
  [-9,39,-32,41,52,-10,28,-14],
  [25,17,20,34,26,25,15,10],
  [13,10,17,23,17,16,0,7],
  [14,25,24,15,8,25,20,15],
  [19,20,11,6,7,6,20,16],
  [-7,2,-15,-12,-14,-15,-10,-10]]
rPSQT = [[35,29,33,4,37,33,56,50],
  [55,29,56,67,55,62,34,60],
  [19,35,28,33,45,27,25,15],
  [0,5,16,13,18,-4,-9,-6],
  [-28,-35,-16,-21,-13,-29,-46,-30],
  [-42,-28,-42,-25,-25,-35,-26,-46],
  [-53,-38,-31,-26,-29,-43,-44,-53],
  [-30,-24,-18,5,-2,-18,-31,-32]]
qPSQT = [[6,1,-8,-104,69,24,88,26],
  [14,32,60,-10,20,76,57,24],
  [-2,43,32,60,72,63,43,2],
  [1,-16,22,17,25,20,-13,-6],
  [-14,-15,-2,-5,-1,-10,-20,-22],
  [-30,-6,-13,-11,-16,-11,-16,-27],
  [-36,-18,0,-19,-15,-15,-21,-38],
  [-39,-30,-31,-13,-31,-36,-34,-42]]
kPSQT = [[ 4,54,47,-99,-99,60,83,-62],
  [-32,10,55,56,56,55,10,3],
  [-62,12,-57,44,-67,28,37,-31],
  [-55,50,11,-4,-19,13,0,-49],
  [-55,-43,-52,-28,-51,-47,-8,-50],
  [-47,-42,-43,-79,-64,-32,-29,-32],
  [-4,3,-14,-50,-57,-18,13,4],
  [22,30,-3,-14,6,-1,40,26]] 

allPSGT={'p': pPSQT,'n': nPSQT,'b':bPSQT,'r':rPSQT,'q':qPSQT,'k':kPSQT}

isupper = lambda c: 'A' <= c <= 'Z'
islower = lambda c: 'a' <= c <= 'z'

class Board:

  boardState = []
  playedMoveCount = 0
  whiteValidMoves = []
  blackValidMoves = []
  whiteAttackLocations = ''
  blackAttackLocations = ''
  whiteKingLocation = 'e1'
  blackKingLocation = 'e8'
  moveList = []
  lastMove = ''
  nodes = 0
  depth = 0
  whiteCanCastleShort = True
  whiteCanCastleLong = True
  blackCanCastleShort = True
  blackCanCastleLong = True

  def __init__(self):
    self.setDefaultBoardState()
    self.playedMoveCount = 0

  def setDefaultBoardState(self):
    self.boardState = [['r','n','b','q','k','b','n','r'],
            ['p']*8,
            ['-']*8,
            ['-']*8,
            ['-']*8,
            ['-']*8,
            ['P']*8,
            ['R','N','B','Q','K','B','N','R'],]
  def setBoardState(self, state):
    self.boardState = state

  def makeMove(self, uciCoordinate):
    fromLetterNumber = self.letterToNumber(uciCoordinate[0:1])
    fromNumber = abs(int(uciCoordinate[1:2]) - 8)
    toLetterNumber = self.letterToNumber(uciCoordinate[2:3])
    toNumber = abs(int(uciCoordinate[3:4]) - 8)
    fromPiece = self.boardState[fromNumber][fromLetterNumber]
    toPiece = self.boardState[toNumber][toLetterNumber]
    promote = ""
    if (len(uciCoordinate) > 4):
      promote = uciCoordinate[4:5]
    if ((fromPiece == 'P' or fromPiece == 'p') and toPiece == '-' and uciCoordinate[0:1] != uciCoordinate[2:3]):
      self.boardState[fromNumber][fromLetterNumber] = '-'
      self.boardState[toNumber][toLetterNumber] = fromPiece
      self.boardState[fromNumber][toLetterNumber] = '-'
    elif ((fromPiece == 'K' or fromPiece == 'k') and (uciCoordinate == 'e1g1' or uciCoordinate == 'e1c1' or uciCoordinate == 'e8g8' or uciCoordinate == 'e8c8')):
      self.boardState[fromNumber][fromLetterNumber] = '-'
      if (uciCoordinate[2] == 'g'):
        self.boardState[toNumber][toLetterNumber + 1] = '-'

        if (self.playedMoveCount % 2 == 0):
          self.boardState[fromNumber][fromLetterNumber + 1] = 'R'
        else:
          self.boardState[fromNumber][fromLetterNumber + 1] = 'r'
      else:
        self.boardState[fromNumber][toLetterNumber - 2] = '-'
        if (self.playedMoveCount % 2 == 0):
          self.boardState[fromNumber][fromLetterNumber - 1] = 'R'
        else:
          self.boardState[fromNumber][fromLetterNumber - 1] = 'r'

      if (self.playedMoveCount % 2 == 0):
        self.boardState[fromNumber][toLetterNumber] = 'K'
      else:
        self.boardState[fromNumber][toLetterNumber] = 'k'
    else:
      self.boardState[fromNumber][fromLetterNumber] = '-'
      if (promote != ""):
        if (self.playedMoveCount % 2 == 0):
          self.boardState[toNumber][toLetterNumber] = promote.upper()
        else:
          self.boardState[toNumber][toLetterNumber] = promote
      else:
        self.boardState[toNumber][toLetterNumber] = fromPiece

    if (uciCoordinate[0:2] == 'e1'):
      self.whiteCanCastleShort = False
      self.whiteCanCastleLong = False
    if (uciCoordinate[0:2] == 'a1'):
      self.whiteCanCastleLong = False
    if (uciCoordinate[0:2] == 'h1'):
      self.whiteCanCastleShort = False
    if (uciCoordinate[0:2] == 'e8'):
      self.blackCanCastleShort = False
      self.blackCanCastleLong = False
    if (uciCoordinate[0:2] == 'a8'):
      self.blackCanCastleLong = False
    if (uciCoordinate[0:2] == 'h8'):
      self.blackCanCastleShort = False

    self.moveList.append(uciCoordinate)
    self.playedMoveCount += 1

  def letterToNumber(self, letter):
    return abs((ord(letter) - 96) - 1)

  def numberToLetter(self, number):
    return chr(number + 96)

  def showBoard(self):
    for i in range(8) :  
      for j in range(8) : 
        print(self.boardState[i][j], end=" ") 
      print()

  def getValidMoves(self):
    whiteValidMoves = []
    blackValidMoves = []
    whiteAttackPieces = []
    blackAttackPieces = []
    self.whiteAttackLocations = ''
    self.blackAttackLocations = ''
    evalState = self.boardState.copy()
    for row in range(8):  
      for column in range(8): 
        piece = evalState[row][column]
        if (piece == "-"):
          continue
        else:
          whiteStartCoordinate = self.numberToLetter(column + 1) + str(abs(row - 8))
          blackStartCoordinate = self.numberToLetter(column + 1) + str(abs(row - 8))
          if ((piece == 'k' or piece == 'K')):
            if (piece == 'K'):
              isWhite = True
              self.whiteKingLocation = whiteStartCoordinate
            else:
              isWhite = False
              self.blackKingLocation = blackStartCoordinate
            kMoves = {
              1: {'column': (column + 0), 'row': (row + 1)},
              2: {'column': (column + 0), 'row': (row - 1)},
              3: {'column': (column + 1), 'row': (row + 0)},
              4: {'column': (column - 1), 'row': (row + 0)},
              5: {'column': (column + 1), 'row': (row + 1)},
              6: {'column': (column + 1), 'row': (row - 1)},
              7: {'column': (column - 1), 'row': (row + 1)},
              8: {'column': (column - 1), 'row': (row - 1)},
            }
            if isWhite:
              if self.whiteCanCastleShort and whiteStartCoordinate == 'e1' and evalState[7][5] == '-' and evalState[7][6] == '-' and evalState[7][7] == 'R':
                whiteValidMoves.append(whiteStartCoordinate + 'g1')
              if self.whiteCanCastleLong and whiteStartCoordinate == 'e1' and evalState[7][1] == '-' and evalState[7][2] == '-' and evalState[7][3] == '-' and evalState[7][0] == 'R':
                whiteValidMoves.append(whiteStartCoordinate + 'c1')
            else:
              if self.blackCanCastleShort and blackValidMoves == 'e8' and evalState[0][1] == '-' and evalState[0][1] == '-' and evalState[0][2] == '-' and evalState[0][0] == 'r':
                bestMove.append(blackStartCoordinate + 'c8')
              if self.blackCanCastleLong and blackValidMoves == 'e8' and evalState[0][5] == '-' and evalState[0][6] == '-' and evalState[0][7] == 'r':
                bestMove.append(blackStartCoordinate + 'g8')
            for key, nMove in kMoves.items():
              if (nMove['column'] >= 0 and nMove['column'] <= 7 and nMove['row'] >= 0 and nMove['row'] <= 7):
                evalPiece = evalState[nMove['row']][nMove['column']]
                if (isWhite):
                  canCapture = (evalPiece != '-' and evalPiece.islower())
                else:
                  canCapture = (evalPiece != '-' and evalPiece.isupper())

                dest = self.numberToLetter(nMove['column'] + 1) + str(abs(nMove['row'] - 8))

                if (evalPiece == '-' or canCapture):
                  if (isWhite):
                    whiteValidMoves.append(whiteStartCoordinate + dest)
                  else:
                    blackValidMoves.append(blackStartCoordinate + dest)
                if (canCapture):
                  if (isWhite):
                    whiteAttackPieces.append([evalPiece, piece])
                    self.whiteAttackLocations += dest
                  else:
                    blackAttackPieces.append([evalPiece, piece])
                    self.blackAttackLocations += dest
          if ((piece == 'p' or piece == 'P')):
            if (piece == 'P'):
              if (row > 1 and evalState[row - 1][column] == '-'):
                whiteValidMoves.append(whiteStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 9)))
              if (row == 6 and evalState[row - 1][column] == '-' and evalState[row - 2][column] == '-'):
                whiteValidMoves.append(whiteStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 10)))
              if (row == 1 and evalState[row - 1][column] == '-'):
                whiteValidMoves.append(whiteStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 9)) + 'q')
              if (((column - 1) >= 0 and (row - 1) >= 0) or ((column + 1) < 8 and (row - 1) >= 0)):
                prom = ''
                if (row == 1):
                  prom = 'q'
                if ((column - 1) >= 0 and evalState[row - 1][column - 1] != '-' and evalState[row - 1][column - 1].islower()):
                  whiteValidMoves.append(whiteStartCoordinate + self.numberToLetter(column) + str(abs(row - 9)) + prom)
                  self.whiteAttackLocations += self.numberToLetter(column) + str(abs(row - 9))
                  whiteAttackPieces.append([evalState[row - 1][column - 1], piece])
                if ((column + 1) < 8 and evalState[row - 1][column + 1] != '-' and evalState[row - 1][column + 1].islower()):
                  whiteValidMoves.append(whiteStartCoordinate + self.numberToLetter(column + 2) + str(abs(row - 9)) + prom)
                  self.whiteAttackLocations += self.numberToLetter(column + 2) + str(abs(row - 9))
                  whiteAttackPieces.append([evalState[row - 1][column + 1], piece])
            else:
              if (row < 6 and evalState[row + 1][column] == '-'):
                blackValidMoves.append(blackStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 7)))
              if (row == 1 and evalState[row + 1][column] == '-' and evalState[row + 2][column] == '-'):
                blackValidMoves.append(blackStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 6)))
              if (row == 6 and evalState[row + 1][column] == '-'):
                blackValidMoves.append(blackStartCoordinate + self.numberToLetter(column + 1) + str(abs(row - 7)) + 'q')
              if (((column - 1) >= 0 and (row + 1) < 8) or ((column + 1) < 8 and (row + 1) < 8)):
                prom = ''
                if (row == 6):
                  prom = 'q'

                if ((column + 1) < 8 and evalState[row + 1][column + 1] != '-' and evalState[row + 1][column + 1].isupper()):
                  blackValidMoves.append(blackStartCoordinate + self.numberToLetter(column + 2) + str(abs(row - 7)) + prom)
                  self.blackAttackLocations += self.numberToLetter(column + 2) + str(abs(row - 7))
                  blackAttackPieces.append([evalState[row + 1][column + 1], piece])
                if ((column - 1) >= 0 and evalState[row + 1][column - 1] != '-' and evalState[row + 1][column - 1].isupper()):
                  blackValidMoves.append(blackStartCoordinate + self.numberToLetter(column) + str(abs(row - 7)) + prom)
                  self.blackAttackLocations += self.numberToLetter(column) + str(abs(row - 7))
                  blackAttackPieces.append([evalState[row + 1][column - 1], piece])
          if ((piece == 'n' or piece == 'N')):
            isWhite = (piece == 'N')
            nMoves = {
              1: {'column': (column + 1), 'row': (row - 2)},
              2: {'column': (column - 1), 'row': (row - 2)},
              3: {'column': (column + 2), 'row': (row - 1)},
              4: {'column': (column - 2), 'row': (row - 1)},
              5: {'column': (column + 1), 'row': (row + 2)},
              6: {'column': (column - 1), 'row': (row + 2)},
              7: {'column': (column + 2), 'row': (row + 1)},
              8: {'column': (column - 2), 'row': (row + 1)},
            }
            for key, nMove in nMoves.items():
              if (nMove['column'] >= 0 and nMove['column'] <= 7 and nMove['row'] >= 0 and nMove['row'] <= 7):
                evalPiece = evalState[nMove['row']][nMove['column']]
                if (isWhite):
                  canCapture = (evalPiece != '-' and evalPiece.islower())
                else:
                  canCapture = (evalPiece != '-' and evalPiece.isupper())
                if (evalPiece == '-' or canCapture):
                  dest = self.numberToLetter(nMove['column'] + 1) + str(abs(nMove['row'] - 8))
                  if (isWhite):
                    whiteValidMoves.append(whiteStartCoordinate + dest)
                    if (canCapture):
                      self.whiteAttackLocations += dest
                      whiteAttackPieces.append([evalPiece, piece])
                  else:
                    blackValidMoves.append(blackStartCoordinate + dest)
                    if (canCapture):
                      self.blackAttackLocations += dest
                      blackAttackPieces.append([evalPiece, piece])
          if ((piece == 'r' or piece == 'R')) or ((piece == 'q' or piece == 'Q')):
            isWhite = (piece == 'R' or piece == 'Q')

            horizontalMoves = {
              1: {'column': column, 'row': (row - 1), 'colIncrement': 0, 'rowIncrement': -1},
              2: {'column': column, 'row': (row + 1), 'colIncrement': 0, 'rowIncrement': 1},
              3: {'column': (column - 1), 'row': row, 'colIncrement': -1, 'rowIncrement': 0},
              4: {'column': (column + 1), 'row': row, 'colIncrement': 1, 'rowIncrement': 0}
            }

            for _, hMove in horizontalMoves.items():
              tempRow = hMove['row']
              tempCol = hMove['column']
              while (tempRow >= 0 and tempRow < 8 and tempCol >= 0 and tempCol < 8):
                evalPiece = evalState[tempRow][tempCol]
                canCapture = (isWhite and evalPiece != '-' and evalPiece.islower()) or (not isWhite and evalPiece != '-' and evalPiece.isupper())

                if (evalPiece == '-' or canCapture):
                  dest = self.numberToLetter(tempCol + 1) + str(abs(tempRow - 8))
                  if isWhite:
                    whiteValidMoves.append(whiteStartCoordinate + dest)
                    if (canCapture):
                      self.whiteAttackLocations += dest
                      whiteAttackPieces.append([evalPiece, piece])
                  else:
                    blackValidMoves.append(blackStartCoordinate + dest)
                    if (canCapture):
                      self.blackAttackLocations += dest
                      blackAttackPieces.append([evalPiece, piece])
                  if (canCapture):
                    break
                else:
                  break
                tempRow += hMove['rowIncrement']
                tempCol += hMove['colIncrement']

          if ((piece == 'b' or piece == 'B')) or ((piece == 'q' or piece == 'Q')):
            isWhite = (piece == 'B' or piece == 'Q')

            diagMoves = {
              1: {'column': (column - 1), 'row': (row - 1), 'colIncrement': -1, 'rowIncrement': -1},
              2: {'column': (column + 1), 'row': (row + 1), 'colIncrement': 1, 'rowIncrement': 1},
              3: {'column': (column - 1), 'row': (row + 1), 'colIncrement': -1, 'rowIncrement': 1},
              4: {'column': (column + 1), 'row': (row - 1), 'colIncrement': 1, 'rowIncrement': -1}
            }

            for _, dMove in diagMoves.items():
              tempRow = dMove['row']
              tempCol = dMove['column']
              while (tempRow >= 0 and tempRow < 8 and tempCol >= 0 and tempCol < 8):
                evalPiece = evalState[tempRow][tempCol]
                canCapture = (isWhite and evalPiece != '-' and evalPiece.islower()) or (not isWhite and evalPiece != '-' and evalPiece.isupper())

                if (evalPiece == '-' or canCapture):
                  dest = self.numberToLetter(tempCol + 1) + str(abs(tempRow - 8))
                  if (isWhite):
                    whiteValidMoves.append(whiteStartCoordinate + dest)
                    if (canCapture):
                      self.whiteAttackLocations += dest
                      whiteAttackPieces.append([evalPiece, piece])
                  else:
                    blackValidMoves.append(blackStartCoordinate + dest)
                    if (canCapture):
                      self.blackAttackLocations += dest
                      blackAttackPieces.append([evalPiece, piece])
                  if (canCapture):
                    break
                else:
                  break
                tempRow += dMove['rowIncrement']
                tempCol += dMove['colIncrement']

    sep = ''
    if (self.playedMoveCount % 2 == 0):
      moveCopy = whiteValidMoves.copy()
      kLoc = self.whiteKingLocation

      moveString = sep.join(blackValidMoves)
      pastMoves = sep.join(self.moveList)

      for move in moveCopy:
        overrideRemove = ((move == 'e1g1' and ('e1' in moveString or 'f1' in moveString or 'g1' in moveString)) or (move == 'e1c1' and ('e1' in moveString or 'd1' in moveString or 'c1' in moveString)))

        if overrideRemove:
          try:
            whiteValidMoves.remove(move)
          except:
            continue
    else:
      moveCopy = blackValidMoves.copy()
      kLoc = self.blackKingLocation

      moveString = sep.join(whiteValidMoves)
      pastMoves = sep.join(self.moveList)

      for move in moveCopy:
        overrideRemove = ((move == 'e8g8' and ('e8' in moveString or 'f8' in moveString or 'g8' in moveString)) or (move == 'e8c8' and ('e8' in moveString or 'd8' in moveString or 'c8' in moveString)))

        if overrideRemove:
          try:
            blackValidMoves.remove(move)
          except:
            continue

    self.whiteValidMoves = whiteValidMoves
    self.blackValidMoves = blackValidMoves
    self.whiteAttackPieces = whiteAttackPieces
    self.blackAttackPieces = blackAttackPieces
    return {'whiteValidMoves': whiteValidMoves, 'blackValidMoves': blackValidMoves}

  def moves(self):
    if (self.playedMoveCount % 2 == 0):
      return self.whiteValidMoves
    else:
      return self.blackValidMoves

  def getSideMoves(self, isWhite):
    if isWhite:
      return self.whiteValidMoves.copy()
    else:
      return self.blackValidMoves.copy()

  def boardEvaluation(self):
    bEval = 0
    for row in range(8):
      for column in range(8):
        piece = self.boardState[row][column]
        isWhite = piece.isupper()
        if (piece != '-'):
          if isWhite:
            bEval += piecePoints[piece.lower()] 
            bEval += (allPSGT[piece.lower()][row][column] / 10)
          else:
            bEval -= piecePoints[piece]
            bEval -= (allPSGT[piece][abs(row-7)][abs(column-7)] / 10)

    # for (attacked, attacker) in self.whiteAttackPieces:
    #   bEval += attackPoints[attacked.lower()] / 10
    # for (attacked, attacker) in self.blackAttackPieces:
    #   bEval -= attackPoints[attacked.lower()] / 10


    return bEval

  def minimaxRoot(self, depth, localBoard, maxTime):
    lglMvs = localBoard.getSideMoves(localBoard.playedMoveCount % 2 == 0)
    if (localBoard.playedMoveCount == 0):
      possMvs = ['e2e4', 'd2d4', 'c2c4', 'g1f3']
      localBoard.depth = 1
      return [0, possMvs[0]]
    elif localBoard.playedMoveCount == 1:
      try:
        localBoard.depth = 1
        move = openingBook[localBoard.moveList[0]]
        return [0, move]
      except:
        possMvs = lglMvs
    else:
      possMvs = lglMvs
    if(len(possMvs) == 1):
      localBoard.depth = 1
      return [localBoard.boardEvaluation(), possMvs[0]]

    isMaxingWhite = (localBoard.playedMoveCount % 2 == 0)
    global_score = -50000 if isMaxingWhite else 50000
    chosen_move = None

    originalState = [x[:] for x in localBoard.boardState]

    localBoard.depth = depth

    maxTime = maxTime / len(possMvs)
    # if maxTime < 2:
    #   maxTime = 20

    for move in possMvs:
      localBoard.nodes += 1
      localBoard.makeMove(move)

      startTime = time.perf_counter() + maxTime

      local_score = self.minimax(depth - 1, -50000, 50000, localBoard, startTime, move)

      if isMaxingWhite and local_score > global_score:
        global_score = local_score
        chosen_move = move
      elif not isMaxingWhite and local_score < global_score:
        global_score = local_score
        chosen_move = move

      localBoard.setBoardState([x[:] for x in originalState])
      localBoard.playedMoveCount -= 1

    gameBoard.lastMove = chosen_move
    return [global_score, chosen_move]

  def minimax(self, depth, alpha, beta, localBoard, endTime, lastMove):
    isMaxingWhite = (localBoard.playedMoveCount % 2 == 0)
    localBoard.getValidMoves()
    possMvs = localBoard.getSideMoves(isMaxingWhite)
    startTime = time.perf_counter()

    if depth == 0 or startTime >= endTime or len(possMvs) == 0:
      offset = 0
      if (lastMove == gameBoard.lastMove):
        if (isMaxingWhite):
          offset = -30.0
        else:
          offset = 30.0
      return localBoard.boardEvaluation() + offset 

    initialScore = localBoard.boardEvaluation()

    if (isMaxingWhite and initialScore < -50000) or (not isMaxingWhite and initialScore > 50000):
      return localBoard.boardEvaluation()

    originalState = [x[:] for x in localBoard.boardState]
    best_score = -50000 if isMaxingWhite else 50000
    for move in possMvs:
      localBoard.nodes += 1
      localBoard.makeMove(move)

      local_score = self.minimax(depth - 1, alpha, beta, localBoard, endTime, move)

      if isMaxingWhite:
        best_score = max(best_score, local_score)
        alpha = max(alpha, best_score)
      else:
        best_score = min(best_score, local_score)
        beta = min(beta, best_score)

      localBoard.setBoardState([x[:] for x in originalState])
      localBoard.playedMoveCount -= 1

      if beta <= alpha:
        break

    return best_score

gameBoard = Board()

while True:
  try:
    l = input()
    if l=="quit":
      sys.exit()
    elif l=="uci":
      print("pygone 1.0 by rcostheta")
      print("uciok")
    elif l=="ucinewgame":
      gameBoard = Board()
      gameBoard.playedMoveCount = 0
    elif l=="eval":
      gameBoard.getValidMoves()
      gameBoard.getSideMoves(1)
      # gameBoard.getSideMoves(0)
      print(gameBoard.boardEvaluation())
      gameBoard.showBoard()
    elif l=="isready":
      print("readyok")
    elif l.startswith("position"):
      m=l.split()
      offsetMoves = gameBoard.playedMoveCount + 3
      for move in m[offsetMoves:]:
        gameBoard.makeMove(move)
        offsetMoves += 1
      gameBoard.playedMoveCount = (offsetMoves - 3)
    elif l.startswith("go"):
      goBoard = Board()
      goBoard.setBoardState([x[:] for x in gameBoard.boardState.copy()])
      goBoard.playedMoveCount = gameBoard.playedMoveCount
      goBoard.getValidMoves()
      
      whiteTime = 300
      blackTime = 300
      depth = 4

      args = l.split()
      for key, arg in enumerate(args):
        if (arg == 'wtime'):
          whiteTime = int(args[key + 1])
        if (arg == 'btime'):
          blackTime = int(args[key + 1])
        # if (arg == 'depth')
        #   depth = int(args[key + 1])

      timeMoveCalc = 40
      if (gameBoard.playedMoveCount > 38):
        timeMoveCalc = 2
      else:
        timeMoveCalc = 40 - gameBoard.playedMoveCount

      if (gameBoard.playedMoveCount % 2 == 0):
        moveTime = whiteTime / (timeMoveCalc * 1000)
      else:
        moveTime = blackTime / (timeMoveCalc * 1000)

      moveTime -= 3

      if moveTime < 5:
        moveTime = 5

      startTime = time.perf_counter()
      (score, move) = goBoard.minimaxRoot(depth, goBoard, moveTime)
      elapsedTime = math.ceil(time.perf_counter() - startTime)
      nps = math.ceil(goBoard.nodes / elapsedTime)
      # if (gameBoard.playedMoveCount % 2 != 0):
      #   score = score * -1
      print("info depth " + str(goBoard.depth) + " score cp " + str(math.ceil(score)) + " time " + str(elapsedTime) + " nodes " + str(goBoard.nodes) + " nps " + str(nps) + " pv " + move)
      print("bestmove " + move)
  except (KeyboardInterrupt, SystemExit):
    print('quit')
    sys.exit()
  except Exception as e:
    print(e)
    raise