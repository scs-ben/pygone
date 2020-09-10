#!/usr/bin/env python3
import math,os,sys,subprocess,time
opBk={'e2e4':'e7e5','d2d4':'d7d5','c2c4':'c7c5','g1f3':'c7c5'}
pPts={'p':100.0,'r':479.0,'n':280.0,'b':320.0,'q':929.0,'k':60000.0}
aPts={'p':10.0,'r':50.0,'n':30.0,'b':30.0,'q':100.0,'k':500.0}
pVT=[[0,0,0,0,0,0,0,0],[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0,0,0,0,0,0,0,0]]
nVT=[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]]
bVT=[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]]
rVT=[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]]
qVT=[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]]
kVT=[[4,54,47,-99,-99,60,83,-62],[-32,10,55,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[17,30,-3,-14,6,-1,40,18]]
pPV={'p':pVT,'n':nVT,'b':bVT,'r':rVT,'q':qVT,'k':kVT}
class Board:
 bdSt=[]
 plMvCt=0
 wVMv=[]
 bVMv=[]
 wALoc=''
 bALoc=''
 whKLoc='e1'
 blKLoc='e8'
 moveList=[]
 lastMove=''
 pv=''
 nodes=0
 depth=0
 def __init__(self):
  self.setDfBdSt()
  self.plMvCt=0
 def setDfBdSt(self):
  self.bdSt=[['r','n','b','q','k','b','n','r'],['p','p','p','p','p','p','p','p'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['-','-','-','-','-','-','-','-'],['P','P','P','P','P','P','P','P'],['R','N','B','Q','K','B','N','R'],]
 def setBdSt(self,state):
  self.bdSt=state
 def stMvCt(self,moves):
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
 def shBd(self):
  for i in range(8): 
   for j in range(8):
    print(self.bdSt[i][j],end=" ")
   print()
 def gVMv(self):
  wVMv=[]
  bVMv=[]
  wAMv=[]
  bAMv=[]
  self.wALoc=''
  self.bALoc=''
  evlSt=self.bdSt.copy()
  for row in range(8): 
   for column in range(8):
    piece=evlSt[row][column]
    if(piece!="-"):
     wSC=self.n2L(column+1)+str(abs(row-8))
     bSC=self.n2L(column+1)+str(abs(row-8))
     if((piece=='k' or piece=='K')):
      if(piece=='K'):
       isWhite=True
       self.whKLoc=wSC
      else:
       isWhite=False
       self.blKLoc=bSC
      kMoves={1:{'column':(column+0),'row':(row+1)},2:{'column':(column+0),'row':(row-1)},3:{'column':(column+1),'row':(row+0)},4:{'column':(column-1),'row':(row+0)},5:{'column':(column+1),'row':(row+1)},6:{'column':(column+1),'row':(row-1)},7:{'column':(column-1),'row':(row+1)},8:{'column':(column-1),'row':(row-1)},}
      if isWhite:
       if wSC=='e1' and evlSt[7][5]=='-' and evlSt[7][6]=='-' and evlSt[7][7]=='R':
        wVMv.append(wSC+'g1')
       if wSC=='e1' and evlSt[7][1]=='-' and evlSt[7][2]=='-' and evlSt[7][3]=='-' and evlSt[7][0]=='R':
        wVMv.append(wSC+'c1')
      else:
       if bVMv=='e8' and evlSt[0][1]=='-' and evlSt[0][1]=='-' and evlSt[0][2]=='-' and evlSt[0][0]=='r':
        bstMv.append(bSC+'c8')
       if bVMv=='e8' and evlSt[0][5]=='-' and evlSt[0][6]=='-' and evlSt[0][7]=='r':
        bstMv.append(bSC+'g8')
      for key,nMove in kMoves.items():
       if(nMove['column']>=0 and nMove['column']<=7 and nMove['row']>=0 and nMove['row']<=7):
        evalPiece=evlSt[nMove['row']][nMove['column']]
        if(isWhite):
         canCapture=(evalPiece!='-' and evalPiece.islower())
        else:
         canCapture=(evalPiece!='-' and not evalPiece.islower())
        dest=self.n2L(nMove['column']+1)+str(abs(nMove['row']-8))
        if(evalPiece=='-' or canCapture):
         if(isWhite):
          wVMv.append(wSC+dest)
         else:
          bVMv.append(bSC+dest)
        if(canCapture):
         if(isWhite):
          wAMv.append(evalPiece)
          self.wALoc+=dest
         else:
          bAMv.append(evalPiece)
          self.bALoc+=dest
     if((piece=='p' or piece=='P')):
      if(piece=='P'):
       if(row>1 and evlSt[row-1][column]=='-'):
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-9)))
       if(row==6 and evlSt[row-1][column]=='-' and evlSt[row-2][column]=='-'):
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-10)))
       if(row==1 and evlSt[row-1][column]=='-'):
        wVMv.append(wSC+self.n2L(column+1)+str(abs(row-9))+'q')
       if(((column-1)>=0 and(row-1)>=0)or((column+1)<8 and(row-1)>=0)):
        prom=''
        if(row==1):
         prom='q'
        if((column-1)>=0 and evlSt[row-1][column-1]!='-' and evlSt[row-1][column-1].islower()):
         wVMv.append(wSC+self.n2L(column)+str(abs(row-9))+prom)
         self.wALoc+=self.n2L(column)+str(abs(row-9))
         wAMv.append(evlSt[row-1][column-1])
        if((column+1)<8 and evlSt[row-1][column+1]!='-' and evlSt[row-1][column+1].islower()):
         wVMv.append(wSC+self.n2L(column+2)+str(abs(row-9))+prom)
         self.wALoc+=self.n2L(column+2)+str(abs(row-9))
         wAMv.append(evlSt[row-1][column+1])
      else:
       if(row<6 and evlSt[row+1][column]=='-'):
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-7)))
       if(row==1 and evlSt[row+1][column]=='-' and evlSt[row+2][column]=='-'):
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-6)))
       if(row==6 and evlSt[row+1][column]=='-'):
        bVMv.append(bSC+self.n2L(column+1)+str(abs(row-7))+'q')
       if(((column-1)>=0 and(row+1)<8)or((column+1)<8 and(row+1)<8)):
        prom=''
        if(row==6):
         prom='q'
        if((column+1)<8 and evlSt[row+1][column+1]!='-' and not evlSt[row+1][column+1].islower()):
         bVMv.append(bSC+self.n2L(column+2)+str(abs(row-7))+prom)
         self.bALoc+=self.n2L(column+2)+str(abs(row-7))
         bAMv.append(evlSt[row+1][column+1])
        if((column-1)>=0 and evlSt[row+1][column-1]!='-' and not evlSt[row+1][column-1].islower()):
         bVMv.append(bSC+self.n2L(column)+str(abs(row-7))+prom)
         self.bALoc+=self.n2L(column)+str(abs(row-7))
         bAMv.append(evlSt[row+1][column-1])
     if((piece=='n' or piece=='N')):
      isWhite=(piece=='N')
      nMoves={1:{'column':(column+1),'row':(row-2)},2:{'column':(column-1),'row':(row-2)},3:{'column':(column+2),'row':(row-1)},4:{'column':(column-2),'row':(row-1)},5:{'column':(column+1),'row':(row+2)},6:{'column':(column-1),'row':(row+2)},7:{'column':(column+2),'row':(row+1)},8:{'column':(column-2),'row':(row+1)},}
      for key,nMove in nMoves.items():
       if(nMove['column']>=0 and nMove['column']<=7 and nMove['row']>=0 and nMove['row']<=7):
        evalPiece=evlSt[nMove['row']][nMove['column']]
        if(isWhite):
         canCapture=(evalPiece!='-' and evalPiece.islower())
        else:
         canCapture=(evalPiece!='-' and not evalPiece.islower())
        if(evalPiece=='-' or canCapture):
         dest=self.n2L(nMove['column']+1)+str(abs(nMove['row']-8))
         if(isWhite):
          wVMv.append(wSC+dest)
          if(canCapture):
           self.wALoc+=dest
           wAMv.append(evalPiece)
         else:
          bVMv.append(bSC+dest)
          if(canCapture):
           self.bALoc+=dest
           bAMv.append(evalPiece)
     if((piece=='r' or piece=='R'))or((piece=='q' or piece=='Q')):
      isWhite=(piece=='R' or piece=='Q')
      tempRow=row-1
      while(tempRow>=0):
       evalPiece=evlSt[tempRow][column]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        dest=self.n2L(column+1)+str(abs(tempRow-8))
        if isWhite:
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(column+1)+str(abs(tempRow-8))
        if isWhite:
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(tempCol+1)+str(abs(row-8))
        if isWhite:
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(tempCol+1)+str(abs(row-8))
        if isWhite:
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
         break
       else:
        break
       tempCol-=1
     if((piece=='b' or piece=='B'))or((piece=='q' or piece=='Q')):
      isWhite=(piece=='B' or piece=='Q')
      tempRow=row-1
      tempCol=column-1
      while(tempRow>=0 and tempCol>=0):
       evalPiece=evlSt[tempRow][tempCol]
       if(isWhite):
        canCapture=(evalPiece!='-' and evalPiece.islower())
       else:
        canCapture=(evalPiece!='-' and not evalPiece.islower())
       if(evalPiece=='-' or canCapture):
        dest=self.n2L(tempCol+1)+str(abs(tempRow-8))
        if(isWhite):
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(tempCol+1)+str(abs(tempRow-8))
        if(isWhite):
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(tempCol+1)+str(abs(tempRow-8))
        if(isWhite):
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
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
        dest=self.n2L(tempCol+1)+str(abs(tempRow-8))
        if(isWhite):
         wVMv.append(wSC+dest)
         if(canCapture):
          self.wALoc+=dest
          wAMv.append(evalPiece)
        else:
         bVMv.append(bSC+dest)
         if(canCapture):
          self.bALoc+=dest
          bAMv.append(evalPiece)
        if(canCapture):
         break
       else:
        break
       tempRow+=1
       tempCol-=1
  self.wVMv=wVMv
  self.bVMv=bVMv
  self.wAMv=wAMv
  self.bAMv=bAMv
  return{'wVMv':wVMv,'bVMv':bVMv}
 def rmMv(self,isWhite):
  if(isWhite):
   moves=self.wVMv.copy()
  else:
   moves=self.bVMv.copy()
  masterMoves=moves.copy()
  for move in moves:
   lglBd=Board()
   lglBd.setBdSt([x[:]for x in self.bdSt.copy()])
   lglBd.stMvCt(self.plMvCt)
   lglBd.mkMv(move)
   lglBd.gVMv()
   if(isWhite):
    kLoc=lglBd.whKLoc
    availMvs=lglBd.bALoc
   else:
    kLoc=lglBd.blKLoc
    availMvs=lglBd.wALoc
   if(kLoc in availMvs):
    try:
     masterMoves.remove(move)
    except:
     continue
  return masterMoves
 def bdEval(self):
  bEval=0
  for row in range(8):
   for column in range(8):
    piece=self.bdSt[row][column]
    isWhite=not piece.islower()
    if(piece!='-'):
     if isWhite:
      bEval+=pPts[piece.lower()]
      bEval+=pPV[piece.lower()][row][column]
      if(self.blKLoc in self.wALoc):
       bEval+=(pPts[piece.lower()]/10)
     else:
      bEval-=pPts[piece]
      bEval-=(-1*pPV[piece][abs(row-7)][abs(column-7)])
      if(self.whKLoc in self.bALoc):
       bEval-=(pPts[piece.lower()]/10)
  for piece in self.wAMv:
   bEval+=aPts[piece.lower()]
  for piece in self.bAMv:
   bEval-=aPts[piece.lower()]
  return bEval
 def mmRt(self,depth,bd,isMax,maxTime):
  lglMvs=bd.rmMv(bd.plMvCt%2==0)
  if(bd.plMvCt==0):
   possMvs=['e2e4','d2d4','c2c4','g1f3']
   return[0,possMvs[0],'',1]
  elif bd.plMvCt==1:
   try:
    move=opBk[bd.moveList[0]]
    return[0,move,'',1]
   except:
    possMvs=lglMvs
  else:
   possMvs=lglMvs
  if(len(possMvs)==1):
   return[bd.bdEval(),possMvs[0],'',1]
  bstMv=-9999999
  bstMvFin=possMvs[0]
  originalState=[x[:]for x in bd.bdSt]
  calcDepth=1
  for move in possMvs:
   bd.nodes+=1
   bd.mkMv(move)
   startTime=time.perf_counter()+maxTime
   value=max(bstMv,self.mm(depth-1,-19999999,19999999,bd,not isMax,startTime,move)) 
   bd.setBdSt([x[:]for x in originalState])
   bd.plMvCt-=1
   if(value>bstMv):
    bstMv=value
    bstMvFin=move
  gBd.lastMove=bstMvFin
  return[bstMv,bstMvFin,'',calcDepth]
 def mm(self,depth,alpha,beta,bd,isMax,endTime,lastMove):
  bd.gVMv()
  possMvs=bd.rmMv(bd.plMvCt%2==0)
  startTime=time.perf_counter()
  if depth==0 or startTime>=endTime:
   offset=0
   if(lastMove==gBd.lastMove):
    if(bd.plMvCt%2==0):
     offset=-30.0
    else:
     offset=30.0
   return bd.bdEval()+offset
  originalState=[x[:]for x in bd.bdSt]
  if(isMax):
   bstMv=-9999999
   for move in possMvs:
    bd.nodes+=1
    bd.mkMv(move)
    bstMv=max(bstMv,self.mm(depth-1,alpha,beta,bd,not isMax,endTime,move))
    bd.setBdSt([x[:]for x in originalState])
    bd.plMvCt-=1
    alpha=max(alpha,bstMv)
    if(beta<=alpha):
     return bstMv
   return bstMv
  else:
   bstMv=9999999
   for move in possMvs:
    bd.nodes+=1
    bd.mkMv(move)
    bstMv=min(bstMv,self.mm(depth-1,alpha,beta,bd,not isMax,endTime,move))
    bd.setBdSt([x[:]for x in originalState])
    bd.plMvCt-=1
    beta=min(beta,bstMv)
    if(beta<=alpha):
     return bstMv
   return bstMv
gBd=Board()
while True:
 try:
  l=input()
  if l=="quit":
   sys.exit()
  elif l=="print":
   gBd.shBd()
  elif l=="uci":
   print("pygone 1.0 by rcostheta")
   print("uciok")
  elif l=="valid":
   gBd.gVMv()
   print(gBd.rmMv(1))
   print(gBd.rmMv(0))
  elif l=="ucinewgame":
   gBd=Board()
   gBd.stMvCt(moves=0)
  elif l=="isready":
   print("readyok")
  elif l.startswith("position"):
   m=l.split()
   offsetMoves=gBd.plMvCt+3
   for move in m[offsetMoves:]:
    gBd.mkMv(move)
    offsetMoves+=1
   gBd.stMvCt(offsetMoves-3)
  elif l.startswith("go"):
   goBoard=Board()
   goBoard.setBdSt([x[:]for x in gBd.bdSt])
   goBoard.stMvCt(gBd.plMvCt)
   goBoard.gVMv()
   if(gBd.plMvCt%2==0):
    moveTime=10/len(goBoard.wVMv)
   else:
    moveTime=10/len(goBoard.bVMv)
   startTime=time.perf_counter()
   (score,move,pv,calcDepth)=goBoard.mmRt(4,goBoard,(gBd.plMvCt%2==0),moveTime)
   elapsedTime=math.ceil(time.perf_counter()-startTime)
   nps=math.ceil(goBoard.nodes/elapsedTime)
   if(gBd.plMvCt%2==0):
    score=score*-1
   print("info depth "+str(calcDepth)+" score cp "+str(math.ceil(score))+" time "+str(elapsedTime)+" nodes "+str(goBoard.nodes)+" nps "+str(nps)+" pv "+move)
   print("bestmove "+move)
   goBoard.shBd()
 except(KeyboardInterrupt,SystemExit):
  print('quit')
  sys.exit()
 except Exception as e:
  print(e)
  raise
# Created by pyminifier (https://github.com/liftoff/pyminifier)
