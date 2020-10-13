#!/usr/bin/env pypy3
import math,sys,time
from collections import namedtuple
A={'pe':100,'p':90,'n':290,'b':300,'r':500,'q':900,'k':2e4,'ke':2e4}
B={'p':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[40,40,40,40,40,40,40,40],[5,5,10,25,25,10,5,5],[0,0,0,20,20,0,0,0],[5,-5,-10,0,0,-10,-5,5],[5,10,10,-20,-20,10,10,5],[0,0,0,0,0,0,0,0]],'pe':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[40,40,40,40,40,40,40,40],[30,30,30,30,30,30,30,30],[20,20,20,20,20,20,20,20],[10,10,10,10,10,10,10,10],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],'n':[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,0,0,0,0,-20,-40],[-30,5,10,15,15,10,5,-30],[-30,10,15,20,20,15,10,-30],[-30,5,15,25,25,15,5,-30],[-30,10,10,10,10,10,10,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]],'b':[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[-10,5,5,10,10,5,5,-10],[-10,0,10,10,10,10,0,-10],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]],'r':[[0,0,0,0,0,0,0,0],[5,10,10,10,10,10,10,5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,5,0,5,0,-5],[0,0,0,5,5,0,0,0]],'q':[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]],'k':[[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-20,-30,-30,-40,-40,-30,-30,-20],[-10,-20,-20,-20,-20,-20,-20,-10],[20,20,-10,-10,-10,-10,20,20],[20,10,30,0,0,10,30,20]],'ke':[[-50,-40,-30,-20,-20,-30,-40,-50],[-30,-20,-10,0,0,-10,-20,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-30,0,0,0,0,-30,-30],[-50,-30,-30,-30,-30,-30,-30,-50]]}
for C,_ in B.items():
 for D in range(8):
  for E in range(8):
   B[C][D][E]+=A[C]
H=1
K=2
L=3
I=19e3
J=29e3
M={'k':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1),(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'q':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1),(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'r':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1)],'b':[(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'n':[(1,-2,1),(-1,-2,1),(2,-1,1),(-2,-1,1),(1,2,1),(-1,2,1),(2,1,1),(-2,1,1)],'p':[(0,1,0),(1,1,1),(-1,1,1)]}
def N(O):
 return chr(O+96)
def Q(P):
 print(P,flush=1)
def R(S,T,U,V,W,X):
 Q("info depth "+S+" score cp "+T+" time "+U+" nodes "+V+" nps "+W+" pv "+X)
def Y(A1):
 return((ord(A1[0:1])-97),abs(int(A1[1:2])-8),(ord(A1[2:3])-97),abs(int(A1[3:4])-8))
def J7(J9):
 J8=''
 for c in J9:
  J8+=c
 return J8
def J0(K1,K2):
 K8=0
 for c in K1:
  if c==K2:
   K8+=1
 return K8
class A6:
 A7=[]
 K3=''
 A8=0
 A9=[]
 A0=[]
 B1=[[],[]]
 B2=[1,1]
 B3=[1,1]
 B4='e1'
 B5='e8'
 B6=0
 K4=32
 B7=''
 def __init__(Z):
  Z.A7=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
  Z.K3="rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR1"
 def B8(Z,A1):
  C3=Z.A8%2==0
  (B9,B0,C1,O)=Y(A1)
  C2=Z.A7[B0][B9]
  Z.A7[O][C1]=C2
  Z.A7[B0][B9]='-'
  B71=0
  if C2 in('P','p'):
   B71=abs(B0-O)==2
   B72=-1 if C3 else 1
   if B71:
    Z.B7=A1[0:1]+str(int(A1[3:4])+B72)
   elif A1[2:4]==Z.B7:
    Z.A7[O-B72][C1]='-'
   if len(A1)>4:
    Z.A7[O][C1]=A1[4:5].upper()if C3 else A1[4:5]
  if not B71:
   Z.B7=''
  if C2 in('K','k'):
   if C2=='K':
    Z.B4=A1[2:4]
   else:
    Z.B5=A1[2:4]
   if A1 in('e1g1','e8g8'):
    Z.A7[O][C1+1]='-'
    Z.A7[B0][B9+1]='R' if C2=='K' else 'r'
   elif A1 in('e1c1','e8c8'):
    Z.A7[O][C1-2]='-'
    Z.A7[B0][B9-1]='R' if C2=='K' else 'r'
  Z.K3=Z.C6()
  Z.K4=Z.C7()
 def C4(Z,A1):
  Z5=A6()
  Z5.A8=Z.A8
  Z5.A7[0]=Z.A7[0].copy()
  Z5.A7[1]=Z.A7[1].copy()
  Z5.A7[2]=Z.A7[2].copy()
  Z5.A7[3]=Z.A7[3].copy()
  Z5.A7[4]=Z.A7[4].copy()
  Z5.A7[5]=Z.A7[5].copy()
  Z5.A7[6]=Z.A7[6].copy()
  Z5.A7[7]=Z.A7[7].copy()
  Z5.B1[0]=Z.B1[0].copy()
  Z5.B1[1]=Z.B1[1].copy()
  Z5.A9=Z.A9.copy()
  Z5.A0=Z.A0.copy()
  Z5.B2=Z.B2.copy()
  Z5.B3=Z.B3.copy()
  Z5.B4=Z.B4
  Z5.B5=Z.B5
  Z5.B7=Z.B7
  Z5.B6=Z.B6+Z.A4(A1)
  if 'e1' in A1:
   Z5.B2=[0,0]
  elif 'a1' in A1:
   Z5.B2[0]=0
  elif 'h1' in A1:
   Z5.B2[1]=0
  if 'e8' in A1:
   Z5.B3=[0,0]
  elif 'a8' in A1:
   Z5.B3[0]=0
  elif 'h8' in A1:
   Z5.B3[1]=0
  Z5.B8(A1)
  Z5.A9.append(A1)
  Z5.A8+=1
  Z5.A0.append(Z5.K3)
  Z5.B6=-Z5.B6
  return Z5
 def C5(Z):
  Z5=A6()
  Z5.A8=Z.A8+1
  Z5.A7[0]=Z.A7[0].copy()
  Z5.A7[1]=Z.A7[1].copy()
  Z5.A7[2]=Z.A7[2].copy()
  Z5.A7[3]=Z.A7[3].copy()
  Z5.A7[4]=Z.A7[4].copy()
  Z5.A7[5]=Z.A7[5].copy()
  Z5.A7[6]=Z.A7[6].copy()
  Z5.A7[7]=Z.A7[7].copy()
  Z5.B1[0]=Z.B1[0].copy()
  Z5.B1[1]=Z.B1[1].copy()
  Z5.B2=Z.B2.copy()
  Z5.B3=Z.B3.copy()
  Z5.B4=''
  Z5.B5=''
  Z5.B7=''
  Z5.B6=-Z.B6
  return Z5
 def C7(Z):
  return 64-J0(Z.K3,'-')
 def C8(Z):
  return Z.K4<=14 or Z.K4<=20 and 'q' not in Z.K3.lower()
 def M3(Z,A1):
  return Z.A4(A1,1)
 def A4(Z,A1,M4=0):
  if len(A1)==0:
   return 0
  A8=Z.A8
  C3=1
  D1=0
  if A8%2!=0:
   C3=0
   D1=7
  D11=-1 if C3 else 1
  Z1=7 if C3 else 0
  (B9,B0,C1,O)=Y(A1)
  D2=0
  C2=Z.A7[B0][B9].lower()
  D3=C2
  if Z.C8():
   if D3=='k':
    D3='ke'
   if D3=='p':
    D2+=20
    D3='pe'
  D4=Z.A7[O][C1].lower()
  D2+=B[D3][abs(O-D1)][C1]- B[D3][abs(B0-D1)][B9]
  if D4!='-':
   D2+=B[D4][abs(O-D1)][C1]
   if M4:
    D2+=100
  if C2=='k':
   if abs(B9-C1)==2:
    if M4:
     D2+=200
    if A1[2]=='g':
     D2+=B['r'][abs(O-D1)][C1-1]- B['r'][abs(O-D1)][C1+1]
    else:
     D2+=B['r'][abs(O-D1)][C1+1]- B['r'][abs(O-D1)][C1-2]
   elif C2 in('K','k')and A8>15 and not Z.C8():
    if M4:
     D2-=200
   if O+D11 in range(8):
    if Z.A7[O+D11][C1].lower()=='p':
     D2+=10
    if C1-1>0 and Z.A7[O+D11][C1-1].lower()=='p':
     D2+=10
    if C1+1<8 and Z.A7[O+D11][C1+1].lower()=='p':
     D2+=10
  elif M4 and C2=='b' and A8<20 and abs(O-B0)>4:
   D2-=300
  elif M4 and C2=='q' and A8<20 and abs(O-B0)>2:
   D2-=500
  elif C2=='p':
   if A1[2:4]==Z.B7:
    D2+=B[D3][abs(O-D1)][C1]
   if len(A1)>4:
    D7=A1[4:5]
    D2+=B[D7][abs(O-D1)][C1]- B['p'][abs(O-D1)][C1]
    C2=D7
  if M4 and C2!='k':
   D2+=(B0==Z1)*15
   D8=Z.B5 if C3 else Z.B4
   for F3 in M[C2]:
    F4=C1+F3[0]
    F5=O+(F3[1]*D11)
    F7=''
    while F4 in range(8)and F5 in range(8):
     F6=Z.A7[F5][F4]
     F7=N(F4+1)+str(abs(F5-8))
     if F7==D8 or F6!='-' or C2 in 'np':
      Z.B1[C3].append(F7)
      break
     F4+=F3[0]
     F5+=(F3[1]*D11)
    if F7==D8:
     D2+=200
     break
  return D2
 def C6(Z):
  return J7(Z.A7[0])+ J7(Z.A7[1])+ J7(Z.A7[2])+ J7(Z.A7[3])+ J7(Z.A7[4])+ J7(Z.A7[5])+ J7(Z.A7[6])+ J7(Z.A7[7])+ str(Z.A8%2==0)
 def A5(Z,E4=0):
  C3=Z.A8%2==0
  if E4:
   C3=not C3
  Z.B1[C3]=[]
  B=[]
  D1=1
  E6=1
  E7=6
  E5='prnbqk-'
  if not C3:
   E5='PRNBQK-'
   E6=6
   E7=1
  E8=Z.A7
  for Z1 in range(8):
   for Z4 in range(8):
    Z2=E8[Z1][Z4]
    if Z2=="-" or(C3 and Z2.islower())or(not C3 and Z2.isupper()):
     continue
    E9=N(Z4+1)+str(abs(Z1-8))
    K0=Z2.lower()
    if Z2=='P':
     D1=-1
    if Z2=='K':
     if Z.B2[1]and E9=='e1' and J7(E8[7][5:8])=='--R' and not any(Z7 in Z.B1[0]for Z7 in['e1','f1','g1']):
      B.append(E9+'g1')
     if Z.B2[0]and E9=='e1' and J7(E8[7][0:4])=='R---' and not any(Z7 in Z.B1[0]for Z7 in['e1','d1','c1']):
      B.append(E9+'c1')
    elif Z2=='k':
     if Z.B3[1]and E9=='e8' and J7(E8[0][5:8])=='--r' and not any(Z7 in Z.B1[1]for Z7 in['e8','f8','g8']):
      B.append(E9+'g8')
     if Z.B3[0]and E9=='e8' and J7(E8[0][0:4])=='r---' and not any(Z7 in Z.B1[1]for Z7 in['e8','d8','c8']):
      B.append(E9+'c8')
    elif K0=='p' and Z1==E7 and E8[Z1+D1][Z4]=='-' and E8[Z1+2*D1][Z4]=='-':
     B.append(E9+N(Z4+1)+str(abs(Z1-8+2*D1)))
    for F3 in M[K0]:
     F4=Z4+F3[0]
     F5=Z1+(F3[1]*D1)
     while F4 in range(8)and F5 in range(8):
      F6=E8[F5][F4]
      F7=N(F4+1)+str(abs(F5-8))
      if K0=='p':
       if(Z1==E6 and F3[0]==0 and F6=='-')or (Z1==E6 and F3[0]!=0 and F6!='-' and F6 in E5):
        for G8 in('q','r','b','n'):
         B.append(E9+F7+G8)
       else:
        if(F3[0]==0 and F6=='-')or (F3[0]!=0 and F6!='-' and F6 in E5)or F7==Z.B7:
         B.append(E9+F7)
      elif F6 in E5:
       B.append(E9+F7)
      if F3[2]:
       Z.B1[C3].append(F7)
      if F6!='-' or K0 in 'knp':
       break
      F4+=F3[0]
      F5+=(F3[1]*D1)
  return B
 def E0(Z,C3):
  if C3:
   return Z.B4 in Z.B1[0]
  return Z.B5 in Z.B1[1]
Z8=namedtuple('Z8','M1 M2 depth')
class F0:
 V=0
 S=0
 G1=0
 G2=0
 G3={}
 G4={}
 def G9(Z):
  Z.V=0
  Z.S=0
  Z.G1=0
  Z.G2=0
  Z.G3.clear()
  Z.G4.clear()
 def H1(Z,A3):
  H2=time.time()
  H3=Z.G4.get(A3.K3)
  if H3:
   if H3 in('e1c1','e1g1','e8c8','e8g8')and A3.E0(A3.A8%2==0):
    Z.G4[A3.K3]=None
  L3=-J
  L4=J
  for S in range(1,100):
   A3.A5(1)
   A3.A5()
   D2=Z.H9(A3,S,L3,L4)
   H7=Z.G4.get(A3.K3)
   H8=time.time()-H2
   W=math.ceil(Z.V/H8)
   R(str(S),str(math.ceil(D2)),str(math.ceil(H8)),str(Z.V),str(W),str(H7))
   yield S,H7,D2
 def H9(Z,A3,S,L3,L4,H95=1,M8=0):
  if time.time()>Z.G2:
   return A3.B6
  Z.V+=1
  if A3.B6<=-I:
   return-J
  C3=A3.A8%2==0
  L1=(L3!=L4-1)
  E01=A3.E0(C3)
  S=max(E01,S)
  if L1 and S==0:
   return A3.B6
  if not H95 and A3.A0.count(A3.K3)>=2:
   return 0
  I1=Z.G3.get((A3.K3,H95),Z8(2*J,K,S))
  if not L1 and not E01 and I1.depth>=S and(I1.M2==H or(I1.M2==L and I1.M1>=L4)or(I1.M2==K and I1.M1<=L3)):
   return I1.M1
  L2=L3
  L5=I1.M1 if I1.M1<J else A3.B6
  if not L1 and not E01 and S<=8 and L5-85*S>L4:
   return L5
  T=A3.B6 if S==0 else-J-1
  L8='RNBQ' if C3 else 'rnbq'
  if not L1 and not E01 and L5>=L4 and S>=2 and not L8 in A3.K3:
   T=-Z.H9(A3.C5(),-L4,-L4+1,S-3,0,1)
   if T>=L4:
    return L4
  if not L1 and not E01 and S>0:
   I5=Z.G4.get(A3.K3)
   if I5 and A3.A4(I5)>220:
    T=max(T,-Z.H9(A3.C4(I5),S-1,-L4,-L3,0,1))
    if T>=L4:
     return L4
  I92=0
  H94=1
  M7=0
  D2=-J
  for F2 in sorted(A3.A5(),key=A3.M3,reverse=1):
   I6=A3.A4(F2)
   G7=A3.C4(F2)
   G7.A5(1)
   G7.A5()
   if G7.E0(C3):
    continue
   I92+=1
   H93=I6>200 or A3.K4!=G7.K4 or G7.E0(not C3)
   if not M8 and S>=3 and not H93:
    M7=1
    S-=1
   if S>0 and not H94 or M7:
    D2=-Z.H9(G7,S-1,-L3-1,-L3,0,M8)
    if M7:
     S+=1
     M7=0
   if H94 or L3<D2<L4:
    if S>0 or H93:
     D2=-Z.H9(G7,S-1,-L4,-L3,0,M8)
    H94=0
   if D2>T:
    Z.G4[A3.K3]=F2
    T=D2
   L3=max(L3,D2)
   if L3>=L4:
    break
  if I92==0:
   return-J if E01 else 0
  if T<=L2:
   Z.G3[A3.K3,H95]=Z8(T,K,S)
  elif T>=L4:
   Z.G3[A3.K3,H95]=Z8(T,L,S)
  else:
   Z.G3[A3.K3,H95]=Z8(T,H,S)
  return T
def main():
 I7=A6()
 H91=F0()
 I91=0
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
    I91=0
   elif Z3=="isready":
    Q("readyok")
   elif Z3.startswith("position"):
    I9=Z3.split()
    I7=A6()
    for I0 in I9[3:]:
     I7=I7.C4(I0)
    if I91==0:
     I91=I7.A8
   elif Z3.startswith("go"):
    J1=1e8
    J2=1e8
    H91.S=30
    J3=Z3.split()
    for key,arg in enumerate(J3):
     if arg=='wtime':
      J1=int(J3[key+1])
     elif arg=='btime':
      J2=int(J3[key+1])
     elif arg=='depth':
      H91.S=int(J3[key+1])
    J6=1e8
    C3=I7.A8%2==0
    J6=(J2/20000)
    H91.G2=time.time()+(J2/1000)-3
    if C3:
     J6=(J1/20000)
     H91.G2=time.time()+(J1/1000)-3
    if I7.A8-I91<10:
     J6+=10
    J6=max(J6,3)
    H91.G1=time.time()+J6
    H91.V=0
    F2=None
    start=time.time()
    for S,F2,T in H91.H1(I7):
     if(H91.G1-time.time())<2:
      H91.S=3
     if S>=H91.S or time.time()>H91.G1 or abs(T)>=J:
      break
    Q("bestmove "+str(F2))
    if len(H91.G4)>9e5:
     H91.G4.clear()
    if len(H91.G3)>9e5:
     H91.G3.clear()
  except(KeyboardInterrupt,SystemExit):
   sys.exit()
  except Exception as exc:
   Q(exc)
   raise
main()

