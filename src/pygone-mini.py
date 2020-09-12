#!/usr/bin/env python3
import copy,math,os,sys,subprocess,time
A={'e2e4':'e7e5','d2d4':'d7d5','c2c4':'c7c5','g1f3':'c7c5'}
B={'p':100.0,'r':479.0,'n':280.0,'b':320.0,'q':929.0,'k':60000.0}
C={'p':5.0,'r':18.0,'n':10.0,'b':10.0,'q':20.0,'k':30.0}
D=[[0,0,0,0,0,0,0,0],[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0,0,0,0,0,0,0,0]]
E=[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]]
F=[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]]
G=[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]]
H=[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]]
I=[[4,54,47,-99,-99,60,83,-62],[-32,10,55,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[17,55,-3,-14,6,-1,55,18]]
J={'p':D,'n':E,'b':F,'r':G,'q':H,'k':I}
isupper=lambda c:'A'<=c<='Z'
islower=lambda c:'a'<=c<='z'
class Z:
 K=[]
 L=0
 M=[]
 N=[]
 O=''
 P=''
 Q='e1'
 R='e8'
 S=[]
 T=''
 nodes=0
 whiteCanCastleShort=True
 whiteCanCastleLong=True
 blackCanCastleShort=True
 blackCanCastleLong=True
 def __init__(self):
  self.V()
  self.L=0
 def V(self):
  self.K=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R'],]
 def W(self,AH):
  self.K=AH
 def X(self,Y):
  D3=self.b(Y[0:1])
  D6=abs(int(Y[1:2])-8)
  D4=self.b(Y[2:3])
  D8=abs(int(Y[3:4])-8)
  D9=self.K[D6][D3]
  D0=self.K[D8][D4]
  a=""
  if(len(Y)>4):
   a=Y[4:5]
  if((D9=='P' or D9=='p')and D0=='-' and Y[0:1]!=Y[2:3]):
   self.K[D6][D3]='-'
   self.K[D8][D4]=D9
   self.K[D6][D4]='-'
  elif((D9=='K' or D9=='k')and(Y=='e1g1' or Y=='e1c1' or Y=='e8g8' or Y=='e8c8')):
   self.K[D6][D3]='-'
   if(Y[2]=='g'):
    self.K[D8][D4+1]='-'
    if(self.L%2==0):
     self.K[D6][D3+1]='R'
    else:
     self.K[D6][D3+1]='r'
   else:
    self.K[D6][D4-2]='-'
    if(self.L%2==0):
     self.K[D6][D3-1]='R'
    else:
     self.K[D6][D3-1]='r'
   if(self.L%2==0):
    self.K[D6][D4]='K'
   else:
    self.K[D6][D4]='k'
  else:
   self.K[D6][D3]='-'
   if(a!=""):
    if(self.L%2==0):
     self.K[D8][D4]=a.upper()
    else:
     self.K[D8][D4]=a
   else:
    self.K[D8][D4]=D9
  if(Y[0:2]=='e1'):
   self.whiteCanCastleShort=False
   self.whiteCanCastleLong=False
  if(Y[0:2]=='a1'):
   self.whiteCanCastleLong=False
  if(Y[0:2]=='h1'):
   self.whiteCanCastleShort=False
  if(Y[0:2]=='e8'):
   self.blackCanCastleShort=False
   self.blackCanCastleLong=False
  if(Y[0:2]=='a8'):
   self.blackCanCastleLong=False
  if(Y[0:2]=='h8'):
   self.blackCanCastleShort=False
  self.S.append(Y)
  self.L+=1
 def b(self,letter):
  return abs((ord(letter)-96)-1)
 def c(self,number):
  return chr(number+96)
 def d(self):
  for i in range(8): 
   for j in range(8):
    print(self.K[i][j],end=" ")
   print()
 def e(self):
  M=[]
  N=[]
  f=[]
  g=[]
  self.O=''
  self.P=''
  h=self.K.copy()
  for t in range(8): 
   for u in range(8):
    z=h[t][u]
    if(z=="-"):
     continue
    else:
     i=self.c(u+1)+str(abs(t-8))
     j=self.c(u+1)+str(abs(t-8))
     if((z=='k' or z=='K')):
      if(z=='K'):
       k=True
       self.Q=i
      else:
       k=False
       self.R=j
      l={1:{'u':(u+0),'t':(t+1)},2:{'u':(u+0),'t':(t-1)},3:{'u':(u+1),'t':(t+0)},4:{'u':(u-1),'t':(t+0)},5:{'u':(u+1),'t':(t+1)},6:{'u':(u+1),'t':(t-1)},7:{'u':(u-1),'t':(t+1)},8:{'u':(u-1),'t':(t-1)},}
      if k:
       if self.whiteCanCastleShort and i=='e1' and h[7][5]=='-' and h[7][6]=='-' and h[7][7]=='R':
        M.append(i+'g1')
       if self.whiteCanCastleLong and i=='e1' and h[7][1]=='-' and h[7][2]=='-' and h[7][3]=='-' and h[7][0]=='R':
        M.append(i+'c1')
      else:
       if self.blackCanCastleShort and N=='e8' and h[0][1]=='-' and h[0][1]=='-' and h[0][2]=='-' and h[0][0]=='r':
        n.append(j+'c8')
       if self.blackCanCastleLong and N=='e8' and h[0][5]=='-' and h[0][6]=='-' and h[0][7]=='r':
        n.append(j+'g8')
      for x,AJ in l.items():
       if(AJ['u']>=0 and AJ['u']<=7 and AJ['t']>=0 and AJ['t']<=7):
        v=h[AJ['t']][AJ['u']]
        if(k):
         o=(v!='-' and v.islower())
        else:
         o=(v!='-' and v.isupper())
        dest=self.c(AJ['u']+1)+str(abs(AJ['t']-8))
        if(v=='-' or o):
         if(k):
          M.append(i+dest)
         else:
          N.append(j+dest)
        if(o):
         if(k):
          f.append([v,z])
          self.O+=dest
         else:
          g.append([v,z])
          self.P+=dest
     if((z=='p' or z=='P')):
      if(z=='P'):
       if(t>1 and h[t-1][u]=='-'):
        M.append(i+self.c(u+1)+str(abs(t-9)))
       if(t==6 and h[t-1][u]=='-' and h[t-2][u]=='-'):
        M.append(i+self.c(u+1)+str(abs(t-10)))
       if(t==1 and h[t-1][u]=='-'):
        M.append(i+self.c(u+1)+str(abs(t-9))+'q')
       if(((u-1)>=0 and(t-1)>=0)or((u+1)<8 and(t-1)>=0)):
        prom=''
        if(t==1):
         prom='q'
        if((u-1)>=0 and h[t-1][u-1]!='-' and h[t-1][u-1].islower()):
         M.append(i+self.c(u)+str(abs(t-9))+prom)
         self.O+=self.c(u)+str(abs(t-9))
         f.append([h[t-1][u-1],z])
        if((u+1)<8 and h[t-1][u+1]!='-' and h[t-1][u+1].islower()):
         M.append(i+self.c(u+2)+str(abs(t-9))+prom)
         self.O+=self.c(u+2)+str(abs(t-9))
         f.append([h[t-1][u+1],z])
      else:
       if(t<6 and h[t+1][u]=='-'):
        N.append(j+self.c(u+1)+str(abs(t-7)))
       if(t==1 and h[t+1][u]=='-' and h[t+2][u]=='-'):
        N.append(j+self.c(u+1)+str(abs(t-6)))
       if(t==6 and h[t+1][u]=='-'):
        N.append(j+self.c(u+1)+str(abs(t-7))+'q')
       if(((u-1)>=0 and(t+1)<8)or((u+1)<8 and(t+1)<8)):
        prom=''
        if(t==6):
         prom='q'
        if((u+1)<8 and h[t+1][u+1]!='-' and h[t+1][u+1].isupper()):
         N.append(j+self.c(u+2)+str(abs(t-7))+prom)
         self.P+=self.c(u+2)+str(abs(t-7))
         g.append([h[t+1][u+1],z])
        if((u-1)>=0 and h[t+1][u-1]!='-' and h[t+1][u-1].isupper()):
         N.append(j+self.c(u)+str(abs(t-7))+prom)
         self.P+=self.c(u)+str(abs(t-7))
         g.append([h[t+1][u-1],z])
     if((z=='n' or z=='N')):
      k=(z=='N')
      AJs={1:{'u':(u+1),'t':(t-2)},2:{'u':(u-1),'t':(t-2)},3:{'u':(u+2),'t':(t-1)},4:{'u':(u-2),'t':(t-1)},5:{'u':(u+1),'t':(t+2)},6:{'u':(u-1),'t':(t+2)},7:{'u':(u+2),'t':(t+1)},8:{'u':(u-2),'t':(t+1)},}
      for x,AJ in AJs.items():
       if(AJ['u']>=0 and AJ['u']<=7 and AJ['t']>=0 and AJ['t']<=7):
        v=h[AJ['t']][AJ['u']]
        if(k):
         o=(v!='-' and v.islower())
        else:
         o=(v!='-' and v.isupper())
        if(v=='-' or o):
         dest=self.c(AJ['u']+1)+str(abs(AJ['t']-8))
         if(k):
          M.append(i+dest)
          if(o):
           self.O+=dest
           f.append([v,z])
         else:
          N.append(j+dest)
          if(o):
           self.P+=dest
           g.append([v,z])
     if((z=='r' or z=='R'))or((z=='q' or z=='Q')):
      k=(z=='R' or z=='Q')
      B0={1:{'u':u,'t':(t-1),'s':0,'r':-1},2:{'u':u,'t':(t+1),'s':0,'r':1},3:{'u':(u-1),'t':t,'s':-1,'r':0},4:{'u':(u+1),'t':t,'s':1,'r':0}}
      for _,B1 in B0.items():
       p=B1['t']
       q=B1['u']
       while(p>=0 and p<8 and q>=0 and q<8):
        v=h[p][q]
        o=(k and v!='-' and v.islower())or(not k and v!='-' and v.isupper())
        if(v=='-' or o):
         dest=self.c(q+1)+str(abs(p-8))
         if k:
          M.append(i+dest)
          if(o):
           self.O+=dest
           f.append([v,z])
         else:
          N.append(j+dest)
          if(o):
           self.P+=dest
           g.append([v,z])
         if(o):
          break
        else:
         break
        p+=B1['r']
        q+=B1['s']
     if((z=='b' or z=='B'))or((z=='q' or z=='Q')):
      k=(z=='B' or z=='Q')
      B2={1:{'u':(u-1),'t':(t-1),'s':-1,'r':-1},2:{'u':(u+1),'t':(t+1),'s':1,'r':1},3:{'u':(u-1),'t':(t+1),'s':-1,'r':1},4:{'u':(u+1),'t':(t-1),'s':1,'r':-1}}
      for _,B3 in B2.items():
       p=B3['t']
       q=B3['u']
       while(p>=0 and p<8 and q>=0 and q<8):
        v=h[p][q]
        o=(k and v!='-' and v.islower())or(not k and v!='-' and v.isupper())
        if(v=='-' or o):
         dest=self.c(q+1)+str(abs(p-8))
         if(k):
          M.append(i+dest)
          if(o):
           self.O+=dest
           f.append([v,z])
         else:
          N.append(j+dest)
          if(o):
           self.P+=dest
           g.append([v,z])
         if(o):
          break
        else:
         break
        p+=B3['r']
        q+=B3['s']
  sep=''
  if(self.L%2==0):
   moveCopy=M.copy()
   A2=self.Q
   B5=sep.join(N)
   B4=sep.join(self.S)
   for move in moveCopy:
    B6=((move=='e1g1' and('e1' in B5 or 'f1' in B5 or 'g1' in B5))or(move=='e1c1' and('e1' in B5 or 'd1' in B5 or 'c1' in B5)))
    if B6:
     try:
      M.remove(move)
     except:
      continue
  else:
   moveCopy=N.copy()
   A2=self.R
   B5=sep.join(M)
   B4=sep.join(self.S)
   for move in moveCopy:
    B6=((move=='e8g8' and('e8' in B5 or 'f8' in B5 or 'g8' in B5))or(move=='e8c8' and('e8' in B5 or 'd8' in B5 or 'c8' in B5)))
    if B6:
     try:
      N.remove(move)
     except:
      continue
  self.M=M
  self.N=N
  self.f=f
  self.g=g
  return{'M':M,'N':N}
 def AI(self):
  if(self.L%2==0):
   return self.M
  else:
   return self.N
 def getSideMoves(self,k):
  if k:
   return self.M.copy()
  else:
   return self.N.copy()
 def A4(self):
  A5=0
  for t in range(8):
   for u in range(8):
    z=self.K[t][u]
    k=z.isupper()
    if(z!='-'):
     if k:
      A5+=B[z.lower()]
      A5+=(J[z.lower()][t][u]/10)
     else:
      A5-=B[z]
      A5-=(J[z][abs(t-7)][abs(u-7)]/10)
  return A5
 def A6(self,depth,AK,isMaxingWhite,maxTime):
  A8=AK.getSideMoves(AK.L%2==0)
  if(AK.L==0):
   A9=['e2e4','d2d4','c2c4','g1f3']
   return[0,A9[0],'',1]
  elif AK.L==1:
   try:
    move=A[AK.S[0]]
    return[0,move,'',1]
   except:
    A9=A8
  else:
   A9=A8
  if(len(A9)==1):
   return[AK.A4(),A9[0],'',1]
  global_score=-50000 if isMaxingWhite else 50000
  chosen_move=None
  AA=[x[:]for x in AK.K]
  for move in A9:
   AK.nodes+=1
   AK.X(move)
   AB=time.perf_counter()+maxTime
   local_score=self.A7(depth-1,not isMaxingWhite,-50000,50000,AK,AB,move)
   if isMaxingWhite and local_score>global_score:
    global_score=local_score
    chosen_move=move
   elif not isMaxingWhite and local_score<global_score:
    global_score=local_score
    chosen_move=move
   AK.W([x[:]for x in AA])
   AK.L-=1
  gameZ.T=chosen_move
  return[global_score,chosen_move,'',1]
 def A7(self,depth,isMaxingWhite,AM,AN,AK,AG,T):
  AK.e()
  A9=AK.getSideMoves(isMaxingWhite)
  AB=time.perf_counter()
  if depth==0 or AB>=AG or len(A9)==0:
   AP=0
   if(T==gameZ.T):
    if(isMaxingWhite):
     AP=-30.0
    else:
     AP=30.0
   return AK.A4()+AP 
  initialScore=AK.A4()
  if(isMaxingWhite and initialScore<-50000)or(not isMaxingWhite and initialScore>50000):
   return AK.A4()
  AA=[x[:]for x in AK.K]
  best_score=-1e8 if isMaxingWhite else 1e8
  for move in A9:
   AK.nodes+=1
   AK.X(move)
   local_score=self.A7(depth-1,not isMaxingWhite,AM,AN,AK,AG,move)
   if isMaxingWhite:
    best_score=max(best_score,local_score)
    AM=max(AM,best_score)
   else:
    best_score=min(best_score,local_score)
    AN=min(AN,best_score)
   AK.W([x[:]for x in AA])
   AK.L-=1
   if AN<=AM:
    break
  return best_score
gameZ=Z()
while True:
 try:
  l=input()
  if l=="quit":
   sys.exit()
  elif l=="uci":
   print("pygone 1.0 by rcostheta")
   print("uciok")
  elif l=="ucinewgame":
   gameZ=Z()
   gameZ.L=0
  elif l=="eval":
   gameZ.e()
   gameZ.getSideMoves(1)
   print(gameZ.A4())
   gameZ.d()
  elif l=="isready":
   print("readyok")
  elif l.startswith("position"):
   m=l.split()
   APMoves=gameZ.L+3
   for move in m[APMoves:]:
    gameZ.X(move)
    APMoves+=1
   gameZ.L=(APMoves-3)
  elif l.startswith("go"):
   gameZ.d()
   goZ=Z()
   goZ.W([x[:]for x in gameZ.K.copy()])
   goZ.L=gameZ.L
   goZ.e()
   if(gameZ.L%2==0):
    moveTime=250/len(goZ.M)
   else:
    moveTime=250/len(goZ.N)
   AB=time.perf_counter()
   (score,move,pv,calcDepth)=goZ.A6(2,goZ,(gameZ.L%2==0),moveTime)
   elapsedTime=math.ceil(time.perf_counter()-AB)
   nps=math.ceil(goZ.nodes/elapsedTime)
   print("info depth "+str(calcDepth)+" score cp "+str(math.ceil(score))+" time "+str(elapsedTime)+" nodes "+str(goZ.nodes)+" nps "+str(nps)+" pv "+move)
   print("bestmove "+move)
 except(KeyboardInterrupt,SystemExit):
  print('quit')
  sys.exit()
 except Exception as e:
  print(e)
  raise

