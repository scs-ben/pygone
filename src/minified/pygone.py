#!/usr/bin/env python3
import math,os,sys,subprocess,time
class Board:
 bdSt=[]
 plMvCt=0
 wVMv=[]
 wCP=0.0
 bVMv=[]
 bCP=0.0
 whKLoc='e1'
 blKLoc='e8'
 moveList=[]
 pv=''
 nodes=0
 def __init__(self):
  self.setDfBdSt()
  self.plMvCt=0
 def setDfBdSt(self):
  self.bdSt=[['r','n','b','q','k','b','n','r'],['p','p','p','p','p','p','p','p'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['P','P','P','P','P','P','P','P'],['R','N','B','Q','K','B','N','R'],]
 def setBdSt(self,state):
  self.bdSt=state
 def setMvCt(self,moves):
  self.plMvCt=moves
 def mkMv(self,uCo):
  fromCrd=uCo[0:2];
  toCrd=uCo[2:4]
  fromLet=fromCrd[0]
  toLet=toCrd[0]
  fromLetNumber=self.l2N(fromLet)
  fromNumber=abs(int(fromCrd[1])-8)
  toLetNumber=self.l2N(toLet)
  toNumber=abs(int(toCrd[1])-8)
  fromPc=self.bdSt[fromNumber][fromLetNumber]
  toPc=self.bdSt[toNumber][toLetNumber]
  promote=''
  if(len(uCo)>4):
   promote=uCo[4:5]
  if(fromPc.lower()=='p' and toPc=='-' and fromLet!=toLet):
   self.bdSt[fromNumber][fromLetNumber]='-'
   self.bdSt[toNumber][toLetNumber]=fromPc
   self.bdSt[fromNumber][toLetNumber]='-'
  elif(self.bdSt[fromNumber][fromLetNumber].lower()=='k' and(uCo=='e1g1' or uCo=='e1c1' or uCo=='e8g8' or uCo=='e8c8')):
   self.bdSt[fromNumber][fromLetNumber]='-'
   if(uCo[2]=='g'):
    self.bdSt[toNumber][toLetNumber+1]='-'
    if(self.plMvCt%2==0):
     self.bdSt[fromNumber][fromLetNumber+1]='R'
    else:
     self.bdSt[fromNumber][fromLetNumber+1]='r'
   else:
    self.bdSt[fromNumber][toLetNumber-2]='-'
    if(self.plMvCt%2==0):
     self.bdSt[fromNumber][fromLetNumber-1]='R'
    else:
     self.bdSt[fromNumber][fromLetNumber-1]='r'
   if(self.plMvCt%2==0):
    self.bdSt[fromNumber][toLetNumber]='K'
   else:
    self.bdSt[fromNumber][toLetNumber]='k'
  else:
   fromState=self.bdSt[fromNumber][fromLetNumber]
   toState=self.bdSt[toNumber][toLetNumber]
   self.bdSt[fromNumber][fromLetNumber]='-'
   if(len(promote)>0):
    if(self.plMvCt%2==0):
     self.bdSt[toNumber][toLetNumber]=promote.upper()
    else:
     self.bdSt[toNumber][toLetNumber]=promote
   else:
    self.bdSt[toNumber][toLetNumber]=fromState
  self.moveList.append(uCo)
  self.plMvCt+=1
 def l2N(self,letter):
  return abs((ord(letter)-96)-1)
 def n2L(self,number):
  return chr(number+96)
 def showBoard(self):
  for i in[0,1,2,3,4,5,6,7]: 
   for j in[0,1,2,3,4,5,6,7]:
    print(self.bdSt[i][j],end=" ")
   print()
 def getValMvs(self):
  wVMv=[]
  bVMv=[]
  pPts={'p':100.0,'r':500.0,'n':300.0,'b':300.0,'q':1000.0,'k':5000.0,}
  aPts={'p':10.0,'r':50.0,'n':30.0,'b':30.0,'q':80.0,'k':100.0,}
  wCP=0.0
  bCP=0.0
  evlSt=self.bdSt.copy()
  for row in[0,1,2,3,4,5,6,7]: 
   for column in[0,1,2,3,4,5,6,7]:
    piece=evlSt[row][column]
    if(piece!="-"):
     wSC=self.n2L(column+1)+str(abs(row-8))
     bSC=self.n2L(column+1)+str(abs(row-8))
     if((piece=='k' or piece=='K')):
      if(piece=='K'):
       isWhite=True
       wCP+=(pPts['k'])
       self.whKLoc=wSC
      else:
       isWhite=False
       bCP+=(pPts['k'])
       self.blKLoc=bSC
      nMoves={1:{'column':(column+0),'row':(row+1)},2:{'column':(column+0),'row':(row-1)},3:{'column':(column+1),'row':(row+0)},4:{'column':(column-1),'row':(row+0)},5:{'column':(column+1),'row':(row+1)},6:{'column':(column+1),'row':(row-1)},7:{'column':(column-1),'row':(row+1)},8:{'column':(column-1),'row':(row-1)},}
      for key,nMove in nMoves.items():
       if(nMove['column']>=0 and nMove['column']<=7 and nMove['row']>=0 and nMove['row']<=7):
        evalPiece=evlSt[nMove['row']][nMove['column']]
        if(isWhite):
         canCapture=(evalPiece!='-' and evalPiece.islower())
        else:
         canCapture=(evalPiece!='-' and not evalPiece.islower())
        if(evalPiece=='-' or canCapture):
         if(isWhite):
          wVMv.append(wSC+self.n2L(nMove['column']+1)+str(abs(nMove['row']-8)))
          wCP-=8.0
         else:
          bVMv.append(bSC+self.n2L(nMove['column']+1)+str(abs(nMove['row']-8)))
          bCP-=8.0
         if(evalPiece!='-'):
          if(isWhite):
           wCP+=(aPts[evalPiece.lower()])
          else:
           bCP+=(aPts[evalPiece.lower()])
     if((piece=='p' or piece=='P')):
      if(piece=='P'):
       wCP+=(pPts['p'])
       if(row>1 and evlSt[row-1][column]=='-'):
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-9)))
       if(row==6 and evlSt[row-1][column]=='-' and evlSt[row-2][column]=='-'):
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-10)))
       if(row==1 and evlSt[row-1][column]=='-'):
        wCP+=(pPts['q'])
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-9))+'q')
       if(((column-1)>=0 and(row-1)>=0)or((column+1)<8 and(row-1)>=0)):
        prom=''
        if(row==1):
         prom='q'
        if((column-1)>=0 and evlSt[row-1][column-1]!='-' and evlSt[row-1][column-1].islower()):
         wVMv.append(wSC+self.n2L(column)+str(abs(row-9))+prom)
         wCP+=(aPts[evlSt[row-1][column-1].lower()])
        if((column+1)<8 and evlSt[row-1][column+1]!='-' and evlSt[row-1][column+1].islower()):
         wVMv.append(wSC+self.n2L(column+2)+str(abs(row-9))+prom)
         wCP+=(aPts[evlSt[row-1][column+1].lower()])
      else:
       bCP+=(pPts['p'])
       if(row<6 and evlSt[row+1][column]=='-'):
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-7)))
       if(row==1 and evlSt[row+1][column]=='-' and evlSt[row+2][column]=='-'):
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-6)))
       if(row==6 and evlSt[row+1][column]=='-'):
        bCP+=(pPts['q'])
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-7))+'q')
       if(((column-1)>=0 and(row+1)<8)or((column+1)<8 and(row+1)<8)):
        prom=''
        if(row==6):
         prom='q'
        if((column+1)<8 and evlSt[row+1][column+1]!='-' and not evlSt[row+1][column+1].islower()):
         bVMv.append(bSC+self.n2L(column+2)+str(abs(row-7))+prom)
         bCP+=(aPts[evlSt[row+1][column+1].lower()])
        if((column-1)>=0 and evlSt[row+1][column-1]!='-' and not evlSt[row+1][column-1].islower()):
         bVMv.append(bSC+self.n2L(column)+str(abs(row-7))+prom)
         bCP+=(aPts[evlSt[row+1][column-1].lower()])
     if((piece=='n' or piece=='N')):
      if(piece=='N'):
       isWhite=True
       wCP+=(pPts['n'])
      else:
       isWhite=False
       bCP+=(pPts['n'])
      nMoves={1:{'column':(column+1),'row':(row-2)},2:{'column':(column-1),'row':(row-2)},3:{'column':(column+2),'row':(row-1)},4:{'column':(column-2),'row':(row-1)},5:{'column':(column+1),'row':(row+2)},6:{'column':(column-1),'row':(row+2)},7:{'column':(column+2),'row':(row+1)},8:{'column':(column-2),'row':(row+1)},}
      for key,nMove in nMoves.items():
       if(nMove['column']>=0 and nMove['column']<=7 and nMove['row']>=0 and nMove['row']<=7):
        evalPiece=evlSt[nMove['row']][nMove['column']]
        if(isWhite):
         canCapture=(evalPiece!='-' and evalPiece.islower())
        else:
         canCapture=(evalPiece!='-' and not evalPiece.islower())
        if(evalPiece=='-' or canCapture):
         if(isWhite):
          wVMv.append(wSC+self.n2L(nMove['column']+1)+str(abs(nMove['row']-8)))
         else:
          bVMv.append(bSC+self.n2L(nMove['column']+1)+str(abs(nMove['row']-8))) 
         if(evalPiece!='-'):
          if(isWhite):
           wCP+=(aPts[evalPiece.lower()])
          else:
           bCP+=(aPts[evalPiece.lower()])
     if((piece=='r' or piece=='R'))or((piece=='q' or piece=='Q')):
      if(piece=='R'):
       isWhite=True
       wCP+=(pPts['r'])
      elif(piece=='r'):
       isWhite=False
       bCP+=(pPts['r'])
      elif(piece=='Q'):
       isWhite=True
       wCP+=(pPts['q'])
      elif(piece=='q'):
       isWhite=False
       bCP+=(pPts['q'])
      tempRow=row-1
      while(tempRow>=0):
       evalPiece=evlSt[tempRow][column]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if isWhite:
         wVMv.append(wSC+self.n2L(column+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(column+1)+str(abs(tempRow-8)))
        if(canCapture):
         if isWhite:
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow-=1
      tempRow=row+1
      while(tempRow<8):
       evalPiece=evlSt[tempRow][column]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if isWhite:
         wVMv.append(wSC+self.n2L(column+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(column+1)+str(abs(tempRow-8)))
        if(canCapture):
         if isWhite:
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow+=1
      tempCol=column+1
      while(tempCol<8):
       evalPiece=evlSt[row][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if isWhite:
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(row-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(row-8)))
        if(canCapture):
         if isWhite:
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempCol+=1
      tempCol=column-1
      while(tempCol>=0):
       evalPiece=evlSt[row][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if isWhite:
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(row-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(row-8)))
        if(canCapture):
         if isWhite:
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempCol-=1
     if((piece=='b' or piece=='B'))or((piece=='q' or piece=='Q')):
      if(piece=='B'):
       isWhite=True
       wCP+=(pPts['b'])
      elif(piece=='b'):
       isWhite=False
       bCP+=(pPts['b'])
      tempRow=row-1
      tempCol=column-1
      while(tempRow>=0 and tempCol>=0):
       evalPiece=evlSt[tempRow][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if(isWhite):
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        if(canCapture):
         if(isWhite):
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow-=1
       tempCol-=1
      tempRow=row+1
      tempCol=column+1
      while(tempRow<8 and tempCol<8):
       evalPiece=evlSt[tempRow][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if(isWhite):
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        if(canCapture):
         if(isWhite):
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow+=1
       tempCol+=1
      tempRow=row-1
      tempCol=column+1
      while(tempRow>=0 and tempCol<8):
       evalPiece=evlSt[tempRow][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if(isWhite):
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        if(canCapture):
         if(isWhite):
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow-=1
       tempCol+=1
      tempRow=row+1
      tempCol=column-1
      while(tempRow<8 and tempCol>=0):
       evalPiece=evlSt[tempRow][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        if(isWhite):
         wVMv.append(wSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        else:
         bVMv.append(bSC+self.n2L(tempCol+1)+str(abs(tempRow-8)))
        if(canCapture):
         if(isWhite):
          wCP+=(aPts[evalPiece.lower()])
         else:
          bCP+=(aPts[evalPiece.lower()])
         break
       else:
        break
       tempRow+=1
       tempCol-=1
  self.wVMv=wVMv
  self.wCP=wCP
  self.bVMv=bVMv
  self.bCP=bCP
  return{'wVMv':wVMv,'wCP':wCP,'bVMv':bVMv,'bCP':bCP}
 def remMv(self,isWhite):
  if(isWhite):
   moves=self.wVMv.copy()
  else:
   moves=self.bVMv.copy()
  masterMoves=moves.copy()
  for move in moves:
   lglBd=Board()
   lglBd.setBdSt([x[:]for x in self.bdSt.copy()])
   lglBd.setMvCt(self.plMvCt)
   lglBd.mkMv(move)
   lglBd.getValMvs()
   if(isWhite):
    kLoc=lglBd.whKLoc
    availMvs=lglBd.bVMv
   else:
    kLoc=lglBd.blKLoc
    availMvs=lglBd.wVMv
   for oppMove in availMvs:
    if(oppMove[2:4]==kLoc):
     try:
      masterMoves.remove(move)
      break
     except:
      continue
  return masterMoves
 def mmRt(self,depth,bd,isMax,maxTime):
  openingBook={'e2e4':'e7e5','d2d4':'d7d5','c2c4':'c7c5','g1f3':'c7c5'}
  legalMoves=bd.remMv(bd.plMvCt%2==0)
  if(bd.plMvCt==0):
   possibleMoves=['e2e4','d2d4','c2c4','g1f3']
   return[0,possibleMoves[0],'']
  elif bd.plMvCt==1:
   try:
    move=openingBook[bd.moveList[0]]
    return[0,move,'']
   except:
    possibleMoves=legalMoves
  else:
   possibleMoves=legalMoves
  bestMove=-9999
  bestMoveFinal=None
  originalState=[x[:]for x in bd.bdSt]
  for move in possibleMoves:
   bd.nodes+=1
   bd.mkMv(move)
   startTime=time.perf_counter()+maxTime
   print(time.perf_counter())
   print(startTime)
   value=max(bestMove,self.mm(depth-1,-10000,10000,bd,not isMax,startTime))
   bd.setBdSt([x[:]for x in originalState])
   bd.plMvCt-=1
   if(value>bestMove):
    bestMove=value
    bestMoveFinal=move
  return[bestMove,bestMoveFinal,'']
 def mm(self,depth,alpha,beta,bd,isMax,endTime):
  bd.getValMvs()
  possibleMoves=bd.remMv(bd.plMvCt%2==0)
  startTime=time.perf_counter()
  if depth==0 or startTime>=endTime:
   return(bd.wCP-bd.bCP)
  originalState=[x[:]for x in bd.bdSt]
  if(isMax):
   bestMove=-9999
   for move in possibleMoves:
    bd.nodes+=1
    bd.mkMv(move)
    bestMove=max(bestMove,self.mm(depth-1,alpha,beta,bd,not isMax,endTime))
    bd.setBdSt([x[:]for x in originalState])
    bd.plMvCt-=1
    alpha=max(alpha,bestMove)
    if(beta<=alpha):
     return bestMove
   return bestMove
  else:
   bestMove=9999
   for move in possibleMoves:
    bd.nodes+=1
    bd.mkMv(move)
    bestMove=min(bestMove,self.mm(depth-1,alpha,beta,bd,not isMax,endTime))
    bd.setBdSt([x[:]for x in originalState])
    bd.plMvCt-=1
    beta=min(beta,bestMove)
    if(beta<=alpha):
     return bestMove
   return bestMove
gBd=Board()
while True:
 try:
  l=input()
  if l=="quit":
   sys.exit()
  elif l=="print":
   gBd.showBoard()
  elif l=="uci":
   print("pygone 1.0 by rcostheta")
   print("uciok")
  elif l=="valid":
   gBd.getValMvs()
   print(gBd.wVMv)
   print(gBd.bVMv)
  elif l=="ucinewgame":
   gBd=Board()
   gBd.setMvCt(moves=0)
  elif l=="isready":
   print("readyok")
  elif l.startswith("position"):
   m=l.split()
   offsetMoves=gBd.plMvCt+3
   for move in m[offsetMoves:]:
    gBd.mkMv(move)
    offsetMoves+=1
   gBd.setMvCt(offsetMoves-3)
  elif l.startswith("go"):
   goBoard=Board()
   goBoard.setBdSt([x[:]for x in gBd.bdSt])
   goBoard.setMvCt(gBd.plMvCt)
   goBoard.getValMvs()
   if(gBd.plMvCt%2==0):
    moveTime=200/len(goBoard.wVMv)
   else:
    moveTime=200/len(goBoard.bVMv)
   startTime=time.perf_counter()
   (score,move,pv)=goBoard.mmRt(4,goBoard,True,moveTime)
   elapsedTime=math.ceil(time.perf_counter()-startTime)
   nps=math.ceil(goBoard.nodes/elapsedTime)
   if(gBd.plMvCt%2!=0):
    score*=-1
   print("info depth "+str(3)+" score cp "+str(score)+" time "+str(elapsedTime)+" nodes "+str(goBoard.nodes)+" nps "+str(nps)+" pv "+move)
   print("bestmove "+move)
 except(KeyboardInterrupt,SystemExit):
  print('quit')
  sys.exit()
 except Exception as e:
  print(e)
  raise
# Created by pyminifier (https://github.com/liftoff/pyminifier)
