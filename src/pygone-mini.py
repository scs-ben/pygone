#!/usr/bin/env pypy3
import copy,math,sys,time
t=time.time
A={'p':100,'n':285,'b':305,'r':600,'q':1250,'k':2e4}
B={'p':[[0]*8,[50]*8,[20]*8,[10,10,15,25,25,15,10,10],[0,0,0,20,20,0,0,0],[5,-5,-5,5,5,-5,-5,5],[5,10,10,-20,-20,10,10,5],[0]*8],'n':[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,5,5,5,5,-20,-40],[-30,5,10,15,15,10,5,-30],[-30,5,15,25,25,15,5,-30],[-30,5,15,25,25,15,5,-30],[-30,10,10,10,10,10,10,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]],'b':[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[0,5,5,10,10,5,5,0],[0,0,10,10,10,10,0,0],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]],'r':[[0]*8,[5,10,10,10,10,10,10,5],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-5,0,0,5,0,5,0,-5],[0,0,0,5,5,0,0,0]],'q':[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,5,5,5,5,5,5,-10],[-10,5,5,5,5,5,5,-10],[-5,5,5,5,5,5,5,-5],[-5,5,5,5,5,5,5,-5],[-10,5,5,5,5,5,5,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]],'k':[[-50,-40,-30,-20,-20,-30,-40,-50],[-20,-20,-10,0,0,-10,-20,-20],[-20,-10,20,30,30,20,-10,-20],[-20,-10,30,40,40,30,-10,-20],[-20,-10,30,40,40,30,-10,-20],[-20,-10,20,30,30,20,-10,-20],[20,20,-40,-40,-40,-40,20,20],[0,10,30,0,0,10,30,0]]}
for C,_ in B.items():
 for D in range(8):
  for E in range(8):
   B[C][D][E]+=A[C]
H=1
K=2
L=3
I=A['k']-10*A['q']
J=A['k']+10*A['q']
N5=30
N0=40
M={'k':[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)],'q':[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)],'r':[(0,1),(0,-1),(1,0),(-1,0)],'b':[(1,1),(1,-1),(-1,1),(-1,-1)],'n':[(1,-2),(-1,-2),(2,-1),(-2,-1),(1,2),(-1,2),(2,1),(-2,1)],'p':[(0,1),(1,1),(-1,1)]}
def N(O):
 return chr(O+96)
def Q(P):
 print(P,flush=1)
def R(S,K7,U,V,W,X):
 Q(f"info depth {S} score cp {K7} time {U} nodes {V} nps {W} pv {X}")
def Y(A1):
 return((ord(A1[0:1])-97),abs(int(A1[1:2])-8),(ord(A1[2:3])-97),abs(int(A1[3:4])-8))
def v(J9):
 J8=''
 for ch in J9:
  J8+=ch
 return J8
def J0(K1,K2):
 K8=0
 for ch in K1:
  if ch==K2:
   K8+=1
 return K8
class A6:
 A7=[]
 K3=''
 A8=0
 A9=[]
 A0=[]
 B2=[1,1]
 B3=[1,1]
 B4='e1'
 B5='e8'
 B6=0
 K4=32
 B7=''
 M9=0
 def __init__(Z):
  Z.A7=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def B8(Z,A1):
  i=Z.A8%2==0
  Z.M9+=1
  (B9,B0,C1,O)=Y(A1)
  C2=Z.A7[B0][B9].lower()
  if Z.A7[O][C1]!='-':
   Z.M9=0
  Z.A7[O][C1]=Z.A7[B0][B9]
  Z.A7[B0][B9]='-'
  B71=0
  if C2=='p':
   Z.M9=0
   B71=abs(B0-O)==2
   B72=-1 if i else 1
   if B71:
    Z.B7=A1[0:1]+str(int(A1[3:4])+B72)
   elif A1[2:4]==Z.B7:
    Z.A7[O-B72][C1]='-'
   if len(A1)>4:
    Z.A7[O][C1]=A1[4:5].upper()if i else A1[4:5]
  elif C2=='k':
   if i:
    Z.B4=A1[2:4]
   else:
    Z.B5=A1[2:4]
   if A1 in('e1g1','e8g8'):
    Z.A7[O][C1+1]='-'
    Z.A7[B0][B9+1]='R' if i else 'r'
   elif A1 in('e1c1','e8c8'):
    Z.A7[O][C1-2]='-'
    Z.A7[B0][B9-1]='R' if i else 'r'
  if not B71:
   Z.B7=''
  Z.K3=Z.C6()
  Z.K4=Z.C7()
 def C4(Z,A1):
  u=A6()
  u=copy.deepcopy(Z)
  for Z1 in range(8):
   u.A7[Z1]=Z.A7[Z1].copy()
  u.A9=Z.A9.copy()
  u.A0=Z.A0.copy()
  u.B2=Z.B2.copy()
  u.B3=Z.B3.copy()
  u.B6=-(Z.B6+Z.A4(A1))
  if 'e1' in A1:
   u.B2=[0,0]
  elif 'a1' in A1:
   u.B2[0]=0
  elif 'h1' in A1:
   u.B2[1]=0
  if 'e8' in A1:
   u.B3=[0,0]
  elif 'a8' in A1:
   u.B3[0]=0
  elif 'h8' in A1:
   u.B3[1]=0
  u.B8(A1)
  u.A9.append(A1)
  u.A8+=1
  u.A0.append(u.K3)
  return u
 def C5(Z):
  u=A6()
  u.A8=Z.A8+1
  for Z1 in range(8):
   u.A7[Z1]=Z.A7[Z1].copy()
  u.B2=Z.B2.copy()
  u.B3=Z.B3.copy()
  u.B6=-Z.B6
  u.B4=u.B5=''
  u.A9=[None]
  return u
 def C7(Z):
  return 64-J0(Z.K3,'-')
 def C8(Z):
  return Z.K4<14 or(Z.K4<20 and 'q' not in Z.K3.lower())
 def M3(Z,A1):
  return Z.A4(A1,1)
 def A4(Z,A1,M4=0):
  if not A1:
   return 0
  i=Z.A8%2==0
  D1=0 if i else 7
  D11=-1 if i else 1
  D5='P' if i else 'p'
  C8=Z.C8()
  (B9,B0,C1,O)=Y(A1)
  D2=0
  C2=Z.A7[B0][B9].lower()
  D4=Z.A7[O][C1].lower()
  D2+=B[C2][abs(O-D1)][C1]- B[C2][abs(B0-D1)][B9]
  if D4!='-':
   D2+=B[D4][abs(O-D1)][C1]
   if M4:
    D2+=5+A[D4]/A[C2]
    if C8 and C2=='p':
     D2-=50
   if D4=='p':
    if Z.N6(O,C1,-D11,D4):
     D2+=N5
    if Z.N9(C1,D4)==2 or Z.N9(C1,D5)==1:
     D2-=N0
    if Z.N9(C1,D5)==0:
     D2+=N0
  if M4 and Z.A8<30 and C2!='k' and B0 in(0,7):
   D2+=100
  if C2=='k':
   if abs(B9-C1)==2:
    if M4:
     D2+=500
    if A1[2]=='g':
     D2+=B['r'][abs(O-D1)][C1-1]- B['r'][abs(O-D1)][C1+1]
    else:
     D2+=B['r'][abs(O-D1)][C1+1]- B['r'][abs(O-D1)][C1-2]
  elif M4 and Z.A8<26 and C2 in 'qrbn' and abs(B0-O)>3:
   D2-=500-abs(O-8)
  elif C2=='r':
   O3=Z.N9(B9,'-')
   O4=Z.N9(C1,'-')
   if O3<7 and O4==8:
    D2+=15
   elif O3==7 and O4<8:
    D2-=15
  elif C2=='p':
   if M4 and Z.A8<30:
    D2+=B[C2][abs(O-D1)][C1]/10
   if A1[2:4]==Z.B7:
    D2+=B[C2][abs(O-D1)][C1]
   elif len(A1)>4:
    D7=A1[4:5]
    D2+=B[D7][abs(O-D1)][C1]- B['p'][abs(O-D1)][C1]
    C2=D7
   if D4=='-':
    if Z.N6(O,C1,D11,D5):
     D2+=N5
    if Z.N6(O,C1,-D11,D5):
     D2+=N5
    if Z.N6(B0,B9,D11,D5):
     D2-=N5
    if Z.N6(B0,B9,-D11,D5):
     D2-=N5
   if(D4!='-' and D4!='p')or A1[2:4]==Z.B7:
    if Z.N6(B0,B9,D11,D5):
     D2-=N5
    if Z.N6(O,C1,-D11,D5):
     D2+=N5
    if Z.N9(B9,D5)==2:
     D2+=N0
    if Z.N9(C1,D5)==1:
     D2-=N0
   if not C8:
    if 'k' in ''.join(Z.A7[B0-D11][max(0,B9-1):min(7,B9+1)]).lower():
     D2-=30
   O1=Z.B4 if i else Z.B5
   if M4 and A1[2:4]==O1:
    D2+=300
  return D2
 def N6(Z,Z1,Z4,D11,D5):
  if(Z1-D11)in range(8):
   return(Z4<7 and Z.A7[Z1-D11][Z4+1]==D5)or (Z4>0 and Z.A7[Z1-D11][Z4-1]==D5)
  return 0
 def N9(Z,Z4,D5):
  K4=0
  for Z1 in range(8):
   K4+=Z.A7[Z1][Z4]==D5
  return K4
 def C6(Z):
  return v(Z.A7[0])+ v(Z.A7[1])+ v(Z.A7[2])+ v(Z.A7[3])+ v(Z.A7[4])+ v(Z.A7[5])+ v(Z.A7[6])+ v(Z.A7[7])+ str(Z.A8%2==0)
 def N7(Z):
  return Z.A5(0,1)
 def A5(Z,E4=0,N8=0):
  i=Z.A8%2==0
  if E4:
   i=not i
  D1=1
  E6=1
  E7=6
  E5='prnbqk-'
  if not i:
   E5='PRNBQK-'
   E6=6
   E7=1
  E8=Z.A7
  for Z1 in range(8):
   for Z4 in range(8):
    Z2=E8[Z1][Z4]
    if Z2=="-" or(i and Z2.islower())or(not i and Z2.isupper()):
     continue
    E9=N(Z4+1)+str(abs(Z1-8))
    K0=Z2.lower()
    if Z2=='P':
     D1=-1
    if Z2=='K' and not N8:
     if Z.B2[1]and E9=='e1' and v(E8[7][5:8])=='--R' and not any(Z.O2(i,Z7)for Z7 in['e1','f1','g1']):
      yield(E9+'g1')
     if Z.B2[0]and E9=='e1' and v(E8[7][0:4])=='R---' and not any(Z.O2(i,Z7)for Z7 in['e1','d1','c1']):
      yield(E9+'c1')
    elif Z2=='k' and not N8:
     if Z.B3[1]and E9=='e8' and v(E8[0][5:8])=='--r' and not any(Z.O2(i,Z7)for Z7 in['e8','f8','g8']):
      yield(E9+'g8')
     if Z.B3[0]and E9=='e8' and v(E8[0][0:4])=='r---' and not any(Z.O2(i,Z7)for Z7 in['e8','d8','c8']):
      yield(E9+'c8')
    elif K0=='p' and Z1==E7 and E8[Z1+D1][Z4]=='-' and E8[Z1+2*D1][Z4]=='-' and not N8:
     yield(E9+N(Z4+1)+str(abs(Z1-8+2*D1)))
    for F3 in M[K0]:
     F4=Z4+F3[0]
     F5=Z1+(F3[1]*D1)
     while F4 in range(8)and F5 in range(8):
      F6=E8[F5][F4]
      F7=N(F4+1)+str(abs(F5-8))
      if not N8 or(N8 and F6!='-'):
       if K0=='p':
        if(Z1==E6 and F3[0]==0 and F6=='-')or (Z1==E6 and F3[0]!=0 and F6!='-' and F6 in E5):
         for G8 in 'qrbn':
          yield(E9+F7+G8)
        else:
         if(F3[0]==0 and F6=='-')or (F3[0]!=0 and F6!='-' and F6 in E5)or F7==Z.B7:
          yield(E9+F7)
       elif F6 in E5:
        yield(E9+F7)
      if F6!='-' or K0 in 'knp':
       break
      F4+=F3[0]
      F5+=(F3[1]*D1)
 def E0(Z,i):
  O1=Z.B4 if i else Z.B5
  return Z.O2(i,O1)
 def O2(Z,i,I0):
  D1=1
  E8=Z.A7
  for Z1 in range(8):
   for Z4 in range(8):
    Z2=E8[Z1][Z4]
    if Z2=="-" or(i and Z2.isupper())or(not i and Z2.islower()):
     continue
    if Z2=='P':
     D1=-1
    Z2=Z2.lower()
    for F3 in M[Z2]:
     if Z2=='p' and not F3[0]:
      continue
     F4=Z4+F3[0]
     F5=Z1+(F3[1]*D1)
     while F4 in range(8)and F5 in range(8):
      F6=E8[F5][F4]
      F7=N(F4+1)+str(abs(F5-8))
      if F7==I0:
       return 1
      if F6!='-' or Z2 in 'knp':
       break
      F4+=F3[0]
      F5+=(F3[1]*D1)
  return 0
class F0:
 V=0
 S=0
 G1=0
 G2=0
 G3={}
 def G9(Z):
  Z.V=0
  Z.S=0
  Z.G1=0
  Z.G2=0
  Z.G3.clear()
 def H1(Z,l):
  H2=t()
  a=-J
  b=J
  D2=-J
  for S in range(1,100):
   if S>2:
    a=D2-20
    b=D2+20
   D2=Z.H9(l,S,a,b)
   if D2<=a or D2>=b:
    D2=Z.H9(l,S,-J,J)
   if t()<Z.G2:
    H7=Z.G3.get(l.K3)
    if H7:
     H7=H7['N1']
   else:
    break
   H8=t()-H2
   W=math.ceil(Z.V/H8)
   R(str(S),str(math.ceil(D2)),str(math.ceil(H8)),str(Z.V),str(W),str(H7))
   yield S,H7,D2
 def H9(Z,l,S,a,b,H95=1,H93=1):
  if t()>Z.G2:
   return l.B6
  Z.V+=1
  if l.B6<=-I:
   return-J
  i=l.A8%2==0
  L1=(a!=b-1)
  E01=l.E0(i)
  S=max(0,S)
  if S==0:
   return Z.H93(l,a,b)
  if not H95 and(l.A0.count(l.K3)>1 or l.M9>=100):
   return 0
  e=Z.G3.get((l.K3),{'M1':2*J,'M2':K,'M0':0,'N1':None})
  if e['M0']>=S>2 and abs(e['M1'])<J:
   if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
    return e['M1']
  L2=a
  L5=e['M1']if e['M1']<J else l.B6
  if S<=7 and not L1 and not E01 and L5-(75*S)>=b:
   return L5
  T=-J-1
  D2=-J
  L8='RNBQ' if i else 'rnbq'
  if not L1 and not E01 and L5>=b and S>=4 and L8 in l.K3 and l.A9[0]and e['M2']!=K and e['M1']<b:
   D2=-Z.H9(l.C5(),min(1,S-4),-b,-b+1,0,0)
   if D2>=b:
    return b
  if S>1 and not L1 and not E01 and l.A9[0]and e['N1']:
   D2=-Z.H9(l.C4(e['N1']),S-1,-b,-a,0,1)
   if D2>=b:
    return b
  I92=0
  H7=None
  S+=E01 and not H95
  for F2 in sorted(l.A5(),key=l.M3,reverse=1):
   I6=l.A4(F2)
   G7=l.C4(F2)
   if G7.E0(i):
    continue
   I92+=1
   M7=I6>160
   if I92==1:
    D2=-Z.H9(G7,S-1,-b,-a,0,M7)
   else:
    M8=1
    if S>2 and not M7:
     M8=min(3,S)
    D2=-Z.H9(G7,S-M8,-a-1,-a,0,M7)
    if M8>1 and D2>a:
     D2=-Z.H9(G7,S-1,-a-1,-a,0,M7)
    if a<D2<b:
     D2=-Z.H9(G7,S-1,-b,-a,0,M7)
   if D2>T:
    H7=F2
    T=D2
    if D2>a:
     a=D2
     if a>=b:
      break
  if I92==0:
   return-J if E01 else 0
  if t()<Z.G2 and S>=e['M0']:
   e['M1']=T
   e['N1']=H7
   if T<=L2:
    e['M2']=K
   elif T>=b:
    e['M2']=L
   else:
    e['M2']=H
   Z.G3[l.K3]=e
  return T
 def H93(Z,l,a,b):
  Z.V+=1
  if l.A0.count(l.K3)>1 or l.M9>=100:
   return 0
  e=Z.G3.get((l.K3),{'M1':2*J,'M2':K,'M0':0,'N1':None})
  if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
   return e['M1']
  L0=l.B6
  T=L0
  i=l.A8%2==0
  a=max(a,T)
  if a>=b:
   return b
  for F2 in sorted(l.N7(),key=l.M3,reverse=1):
   D2=-Z.H93(l.C4(F2),-b,-a)
   if D2>T:
    T=D2
    if D2>a:
     a=D2
   if a>b:
    return b
  return T
I7=A6()
H91=F0()
while 1:
 try:
  Z3=input()
  if Z3=="quit":
   sys.exit()
  elif Z3=="uci":
   Q("pygone 1.3\nuciok")
  elif Z3=="ucinewgame":
   I7=A6()
   H91.G9()
  elif Z3=="isready":
   Q("readyok")
  elif Z3.startswith("position"):
   I9=Z3.split()
   I7=A6()
   for I0 in I9[3:]:
    I7=I7.C4(I0)
  elif Z3.startswith("go"):
   H91.S=30
   J6=1e8
   i=I7.A8%2==0
   J3=Z3.split()
   for key,arg in enumerate(J3):
    if arg=='wtime' and i or arg=='btime' and not i:
     J6=int(J3[key+1])/1e3
   UU=12 if I7.A8<30 else 4
   H91.G2=t()+(J6)-1
   J6=max(3,J6/UU)
   H91.G1=t()+J6
   H91.V=0
   F2=None
   start=t()
   for S,F2,T in H91.H1(I7):
    if(H91.G1-t())<1:
     H91.S=3
    if S>=H91.S or t()>H91.G1:
     break
   Q(f"bestmove {str(F2)}")
 except(KeyboardInterrupt,SystemExit):
  sys.exit()
 except Exception as exc:
  Q(exc)
  raise

