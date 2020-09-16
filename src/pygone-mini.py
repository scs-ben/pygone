#!/usr/bin/env pypy3
import math,sys
from time import perf_counter
A1={'p':100,'r':500,'n':300,'b':300,'q':1e3,'k':6e4}
A3=[[0]*8,[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0]*8]
A4=[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]]
A5=[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]]
A6=[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]]
A7=[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]]
A8=[[4,54,47,-99,-99,60,83,-62],[-32,10,55,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[22,30,-3,-14,6,-1,40,26]]
A9={'p':A3,'n':A4,'b':A5,'r':A6,'q':A7,'k':A8}
K5=['P','R','N','B','Q','K']
K6=['p','r','n','b','q','k']
pc=perf_counter()
isupper=lambda c:'A'<=c<='Z'
islower=lambda c:'a'<=c<='z'
def B1(letter):
 return abs((ord(letter)-96)-1)
def B2(number):
 return chr(number+96)
class H9:
 B3=[]
 B4=0
 B5=[]
 B6=[]
 B7=''
 B8=''
 B9='e1'
 B0='e8'
 C11=[]
 C1=[]
 def __init__(self):
  self.K3()
 def K3(self):
  self.B31()
  self.B4=0
  self.B5=[]
  self.B6=[]
  self.D9=[]
  self.D0=[]
  self.B7=''
  self.B8=''
  self.B9='e1'
  self.B0='e8'
  self.C11=[]
  self.C1=[]
 def B31(self):
  self.B3=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def B32(self,state):
  self.B3=state
 def D1(self,C2,C3=False,C4=False,C91='',C01=''):
  C5=B1(C2[0:1])
  C6=abs(int(C2[1:2])-8)
  C7=B1(C2[2:3])
  C8=abs(int(C2[3:4])-8)
  C9=self.B3[C6][C5]
  C0=self.B3[C8][C7]
  E7=self.B4%2==0
  if len(C91)>0:
   C9=C91
  if len(C01)>0:
   C0=C01
  if C3:
   C9='-'
   C0='P' if E7 else 'p'
  if C4:
   D2=1
   if C2[0:1]=='c':
    D2=-2
    self.B3[C8][C7-1]='-'
   else:
    self.B3[C8][C7+2]='-'
   self.B3[C6][C5+D2]='R' if E7 else 'r'
   self.B3[C8][C7]='K' if E7 else 'k'
   self.B3[C8][C7+D2]='-'
   return[C9,C0]
  D3=""
  if len(C2)>4:
   D3=C2[4:5]
  if(C9 in('P','p')and C0=='-' and C2[0:1]!=C2[2:3]and len(C91)==0 and len(C01)==0):
   self.B3[C6][C5]='-'
   self.B3[C8][C7]=C9
   self.B3[C6][C7]='-'
  elif(C9 in('K','k')and C2 in('e1g1','e1c1','e8g8','e8c8')):
   self.B3[C6][C5]='-'
   if C2[2]=='g':
    self.B3[C8][C7+1]='-'
    if E7:
     self.B3[C6][C5+1]='R'
    else:
     self.B3[C6][C5+1]='r'
   else:
    self.B3[C8][C7-2]='-'
    if E7:
     self.B3[C6][C5-1]='R'
    else:
     self.B3[C6][C5-1]='r'
   if E7:
    self.B3[C8][C7]='K'
   else:
    self.B3[C8][C7]='k'
  else:
   if len(C01)==0:
    self.B3[C6][C5]='-'
   else:
    self.B3[C6][C5]=C01
   if D3!="":
    if E7:
     self.B3[C8][C7]=D3.upper()
    else:
     self.B3[C8][C7]=D3
   else:
    if len(C91)==0:
     self.B3[C8][C7]=C9
    else:
     self.B3[C8][C7]=C91
  return[C9,C0]
 def D4(self,C2):
  (C9,C0)=self.D1(C2)
  self.C1.append(C2)
  self.C11.append([C2,C9,C0])
  self.B4+=1
 def D6(self):
  self.C1.pop()
  F81=self.C11.pop()
  C2=F81[0]
  C9=F81[1]
  C0=F81[2]
  C4=(C2 in('e1g1','e1c1')and C9=='K' and C0=='R')or(C2 in('e8g8','e8c8')and C9=='k' and C0=='r')
  self.D1(C2[2:4]+C2[0:2],len(C2)>4,C4,C9,C0)
  self.B4-=1
 def D7(self):
  for i in range(8):
   for j in range(8):
    print(self.B3[i][j],end=" ")
   print()
 def J9(self):
  result=[]
  for _list in self.B3:
   result+=_list
  return hash(''.join(result))
 def D8(self):
  E7=self.B4%2==0
  if(E7):
   self.B5=[]
   self.D9=[]
   self.B7=''
  else:
   self.B6=[]
   self.D0=[]
   self.B8=''
  E1=self.B3.copy()
  for E2 in range(8):
   for E3 in range(8):
    Z1=E1[E2][E3]
    if Z1=="-" or(E7 and Z1 in K6)or(not E7 and Z1 in K5):
     continue
    K7=B2(E3+1)+str(abs(E2-8))
    if Z1.lower()=='k':
     E8={1:{'E3':(E3+0),'E2':(E2+1)},2:{'E3':(E3+0),'E2':(E2-1)},3:{'E3':(E3+1),'E2':(E2+0)},4:{'E3':(E3-1),'E2':(E2+0)},5:{'E3':(E3+1),'E2':(E2+1)},6:{'E3':(E3+1),'E2':(E2-1)},7:{'E3':(E3-1),'E2':(E2+1)},8:{'E3':(E3-1),'E2':(E2-1)},}
     if E7:
      self.B9=K7
      if K7=='e1' and E1[7][5]=='-' and E1[7][6]=='-' and E1[7][7]=='R':
       self.B5.append(K7+'g1')
      if K7=='e1' and E1[7][1]=='-' and E1[7][2]=='-' and E1[7][3]=='-' and E1[7][0]=='R':
       self.B5.append(K7+'c1')
     else:
      self.B0=K7
      if K7=='e8' and E1[0][1]=='-' and E1[0][1]=='-' and E1[0][2]=='-' and E1[0][0]=='r':
       self.B6.append(K7+'c8')
      if K7=='e8' and E1[0][5]=='-' and E1[0][6]=='-' and E1[0][7]=='r':
       self.B6.append(K7+'g8')
     for _,k_move in E8.items():
      if(k_move['E3']>=0 and k_move['E3']<=7 and k_move['E2']>=0 and k_move['E2']<=7):
       E9=E1[k_move['E2']][k_move['E3']]
       if E7:
        E0=(E9!='-' and E9.islower())
       else:
        E0=(E9!='-' and E9.isupper())
       F1=B2(k_move['E3']+1)+str(abs(k_move['E2']-8))
       if E9=='-' or E0:
        if E7:
         self.B5.append(K7+F1)
        else:
         self.B6.append(K7+F1)
       if E0:
        if E7:
         self.D9.append([E9,Z1])
         self.B7+=F1
        else:
         self.D0.append([E9,Z1])
         self.B8+=F1
    if Z1.lower()=='p':
     if E7:
      if E2>1 and E1[E2-1][E3]=='-':
       self.B5.append(K7+B2(E3+1)+str(abs(E2-9)))
      if E2==6 and E1[E2-1][E3]=='-' and E1[E2-2][E3]=='-':
       self.B5.append(K7+B2(E3+1)+str(abs(E2-10)))
      if E2==1 and E1[E2-1][E3]=='-':
       self.B5.append(K7+B2(E3+1)+str(abs(E2-9))+'q')
      if((E3-1)>=0 and(E2-1)>=0)or((E3+1)<8 and(E2-1)>=0):
       prom=''
       if E2==1:
        prom='q'
       if(E3-1)>=0 and E1[E2-1][E3-1]!='-' and E1[E2-1][E3-1].islower():
        self.B5.append(K7+B2(E3)+str(abs(E2-9))+prom)
        self.B7+=B2(E3)+str(abs(E2-9))
        self.D9.append([E1[E2-1][E3-1],Z1])
       if(E3+1)<8 and E1[E2-1][E3+1]!='-' and E1[E2-1][E3+1].islower():
        self.B5.append(K7+B2(E3+2)+str(abs(E2-9))+prom)
        self.B7+=B2(E3+2)+str(abs(E2-9))
        self.D9.append([E1[E2-1][E3+1],Z1])
     else:
      if E2<6 and E1[E2+1][E3]=='-':
       self.B6.append(K7+B2(E3+1)+str(abs(E2-7)))
      if E2==1 and E1[E2+1][E3]=='-' and E1[E2+2][E3]=='-':
       self.B6.append(K7+B2(E3+1)+str(abs(E2-6)))
      if E2==6 and E1[E2+1][E3]=='-':
       self.B6.append(K7+B2(E3+1)+str(abs(E2-7))+'q')
      if((E3-1)>=0 and(E2+1)<8)or((E3+1)<8 and(E2+1)<8):
       prom=''
       if E2==6:
        prom='q'
       if(E3+1)<8 and E1[E2+1][E3+1]!='-' and E1[E2+1][E3+1].isupper():
        self.B6.append(K7+B2(E3+2)+str(abs(E2-7))+prom)
        self.B8+=B2(E3+2)+str(abs(E2-7))
        self.D0.append([E1[E2+1][E3+1],Z1])
       if(E3-1)>=0 and E1[E2+1][E3-1]!='-' and E1[E2+1][E3-1].isupper():
        self.B6.append(K7+B2(E3)+str(abs(E2-7))+prom)
        self.B8+=B2(E3)+str(abs(E2-7))
        self.D0.append([E1[E2+1][E3-1],Z1])
    if Z1.lower()=='n':
     F3={1:{'E3':(E3+1),'E2':(E2-2)},2:{'E3':(E3-1),'E2':(E2-2)},3:{'E3':(E3+2),'E2':(E2-1)},4:{'E3':(E3-2),'E2':(E2-1)},5:{'E3':(E3+1),'E2':(E2+2)},6:{'E3':(E3-1),'E2':(E2+2)},7:{'E3':(E3+2),'E2':(E2+1)},8:{'E3':(E3-2),'E2':(E2+1)}}
     for _,F4 in F3.items():
      if F4['E3']>=0 and F4['E3']<=7 and F4['E2']>=0 and F4['E2']<=7:
       E9=E1[F4['E2']][F4['E3']]
       if E7:
        E0=(E9!='-' and E9.islower())
       else:
        E0=(E9!='-' and E9.isupper())
       if E9=='-' or E0:
        F1=B2(F4['E3']+1)+str(abs(F4['E2']-8))
        if E7:
         self.B5.append(K7+F1)
         if E0:
          self.B7+=F1
          self.D9.append([E9,Z1])
        else:
         self.B6.append(K7+F1)
         if E0:
          self.B8+=F1
          self.D0.append([E9,Z1])
    if Z1.lower()in('b','r','q'):
     F7={1:{'E3':E3,'E2':(E2-1),'E24':0,'E23':-1},2:{'E3':E3,'E2':(E2+1),'E24':0,'E23':1},3:{'E3':(E3-1),'E2':E2,'E24':-1,'E23':0},4:{'E3':(E3+1),'E2':E2,'E24':1,'E23':0},5:{'E3':(E3-1),'E2':(E2-1),'E24':-1,'E23':-1},6:{'E3':(E3+1),'E2':(E2+1),'E24':1,'E23':1},7:{'E3':(E3-1),'E2':(E2+1),'E24':-1,'E23':1},8:{'E3':(E3+1),'E2':(E2-1),'E24':1,'E23':-1},}
     for key,F8 in F7.items():
      if(key<=4 and Z1.lower()=='b')or(key>=5 and Z1.lower()=='r'):
       continue
      E21=F8['E2']
      E22=F8['E3']
      while E21 in range(8)and E22 in range(8):
       E9=E1[E21][E22]
       E0=(E7 and E9 in K6)or(not E7 and E9 in K5)
       if E9=='-' or E0:
        F1=B2(E22+1)+str(abs(E21-8))
        if E7:
         self.B5.append(K7+F1)
         if E0:
          self.B7+=F1
          self.D9.append([E9,Z1])
        else:
         self.B6.append(K7+F1)
         if E0:
          self.B8+=F1
          self.D0.append([E9,Z1])
        if E0:
         break
       else:
        break
       E21+=F8['E23']
       E22+=F8['E24']
  F0=''.join(self.C1)
  if E7:
   F9=self.B5.copy()
   F0+=''.join(self.B6.copy())
   for K7 in F9:
    G1=((K7=='e1g1' and('e1' in F0 or 'f1' in F0 or 'g1' in F0))or(K7=='e1c1' and('e1' in F0 or 'd1' in F0 or 'c1' in F0)))
    if G1:
     try:
      self.B5.remove(K7)
     except Exception:
      continue
  else:
   F9=self.B6.copy()
   F0+=''.join(self.B5.copy())
   for K7 in F9:
    G1=((K7=='e8g8' and('e8' in F0 or 'f8' in F0 or 'g8' in F0))or(K7=='e8c8' and('e8' in F0 or 'd8' in F0 or 'c8' in F0)))
    if G1:
     try:
      self.B6.remove(K7)
     except Exception:
      continue
 def I9(self,E7):
  if E7:
   for(K8,K9)in self.D0:
    if K8=='K':
     return True
   return False
  else:
   for(K8,K9)in self.D9:
    if K8=='k':
     return True
   return False
 def G2(self,E7):
  if E7:
   return self.B5
  return self.B6
 def G3(self):
  K0=0
  for Z2 in range(64):
   E2=math.floor(Z2/8)
   E3=Z2%8
   Z1=self.B3[E2][E3]
   E7=Z1.isupper()
   if Z1!='-':
    if E7:
     K0+=A1[Z1.lower()]
     K0+=(A9[Z1.lower()][E2][E3]/8)
    else:
     K0-=A1[Z1]
     K0-=(A9[Z1][abs(E2-7)][abs(E3-7)]/8)
  return K0
class G4:
 nodes=0
 depth=0
 G6=0
 def G71(self,G9,depth,I7):
  I8=perf_counter()
  self.G6=perf_counter()+I7
  self.depth=0
  while depth>0:
   self.depth+=1
   depth-=1
   (J3,J4)=self.G7(G9,self.depth)
   I6=math.ceil(perf_counter()-I8)
   nps=math.ceil(self.nodes/I6)
   print("info depth "+str(self.depth)+" score cp "+str(math.ceil(J3))+" time "+str(I6)+" nodes "+str(self.nodes)+" nps "+str(nps)+" pv "+str(J4),flush=True)
   if perf_counter()>=self.G6 or depth<1:
    break
  return[J3,J4]
 def G7(self,G9,depth):
  E7=G9.B4%2==0
  G0=-1e8
  F41=None
  H3=-1e8
  H4=1e8
  G9.D8()
  H1=G9.G2(E7)
  depth=max(depth,1)
  for K7 in H1:
   self.nodes+=1
   G9.D4(K7)
   G9.D8()
   if not G9.I9(E7):
    H2=-self.J5(G9,-H4,-H3,depth-1,not E7)
    if H2>=G0:
     G0=H2
     F41=K7
   G9.D6()
   if self.nodes%1e5==0:
    print("info calculating",flush=True)
  return[G0,F41]
 def J5(self,G9,H3,H4,depth,E7):
  G9.D8()
  H1=G9.G2(E7)
  if len(H1)==0 or(depth<=0):
   if E7:
    return G9.G3()
   else:
    return-1*G9.G3()
  b_G7_pv=True
  H2=-1e8
  for K7 in H1:
   G9.D4(K7)
   G9.D8()
   if not G9.I9(E7):
    self.nodes+=1
    if b_G7_pv:
     H2=-self.J5(G9,-H4,-H3,depth-1,not E7)
    else:
     H2=-self.J5(G9,-H3-1,-H3,depth-1,not E7)
     if H2>H3 and H2<H4:
      H2=-self.J5(G9,-H4,-H3,depth-1,not E7)
   G9.D6()
   if H2>=H4:
    return H4
   if H2>H3:
    H3=H2
    b_G7_pv=False
  return H3
H8=H9()
def main():
 while True:
  try:
   line=input()
   if line=="quit":
    sys.exit()
   elif line=="uci":
    print("pygone 1.0 by rcostheta",flush=True)
    print("uciok",flush=True)
   elif line=="ucinewgame":
    H8.K3()
   elif line=="eval":
    H8.D8()
    print(H8.G3())
    H8.D7()
   elif line=="isready":
    print("readyok",flush=True)
   elif line.startswith("position"):
    moves=line.split()
    H0=H8.B4+3
    for F42 in moves[H0:]:
     H8.D4(F42)
     H0+=1
    H8.B4=(H0-3)
   elif line.startswith("go"):
    I2=1e8
    I3=1e8
    I4=8
    I5=line.split()
    for key,arg in enumerate(I5):
     if arg=='wtime':
      I2=int(I5[key+1])
     if arg=='btime':
      I3=int(I5[key+1])
     if arg=='depth':
      I4=int(I5[key+1])
    K4=max(40-H8.B4,2)
    I7=1e8
    E7=H8.B4%2==0
    if E7:
     I7=I2/(K4*1e3)
    else:
     I7=I3/(K4*1e3)
    if I7<10:
     I4=5
    if I7<4:
     I7=2
     I4=3
    G7er=G4()
    I8=perf_counter()
    (score,K7)=G7er.G71(H8,I4,I7)
    print("bestmove "+K7,flush=True)
  except(KeyboardInterrupt,SystemExit):
   print('quit')
   sys.exit()
  except Exception as exc:
   print(exc)
   raise
main()

