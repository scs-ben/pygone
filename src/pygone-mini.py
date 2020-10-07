#!/usr/bin/env pypy3
import math,sys,time
import gc
from itertools import chain
from collections import namedtuple
A={'pe':100,'p':90,'r':500,'n':320,'b':330,'q':900,'k':2e4,'ke':2e4}
B={'p':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[0,0,0,20,20,0,0,0],[5,-5,-10,0,0,-10,-5,5],[5,10,10,-20,-20,10,10,5],[0,0,0,0,0,0,0,0]],'pe':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],'n':[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,0,0,0,0,-20,-40],[-30,0,10,15,15,10,0,-30],[-30,5,15,20,20,15,5,-30],[-30,0,15,20,20,15,0,-30],[-30,5,10,15,15,10,5,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]],'b':[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[-10,5,5,10,10,5,5,-10],[-10,0,10,10,10,10,0,-10],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]],'r':[[0,0,0,0,0,0,0,0],[5,10,10,10,10,10,10,5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[0,0,0,5,5,0,0,0]],'q':[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]],'k':[[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-20,-30,-30,-40,-40,-30,-30,-20],[-10,-20,-20,-20,-20,-20,-20,-10],[20,20,-10,-10,-10,-10,20,20],[20,30,10,0,0,10,30,20]],'ke':[[-50,-40,-30,-20,-20,-30,-40,-50],[-30,-20,-10,0,0,-10,-20,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-30,0,0,0,0,-30,-30],[-50,-30,-30,-30,-30,-30,-30,-50]]}
for C,_ in B.items():
 for D in range(8):
  for E in range(8):
   B[C][D][E]+=A[C]
F=['P','R','N','B','Q','K']
G=['p','r','n','b','q','k']
H=1
K=2
L=3
I=A['k']-10*A['q']
J=A['k']+10*A['q']
M={'k':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1),(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'q':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1),(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'r':[(0,1,1),(0,-1,1),(1,0,1),(-1,0,1)],'b':[(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)],'n':[(1,-2,1),(-1,-2,1),(2,-1,1),(-2,-1,1),(1,2,1),(-1,2,1),(2,1,1),(-2,1,1)],'p':[(0,1,0),(1,1,1),(-1,1,1)]}
def N(O):
 return chr(O+96)
def Q(P):
 print(P,flush=1)
def R(S,T,U,V,W,X):
 Q("info depth "+S+" score cp "+T+" time "+U+" nodes "+V+" nps "+W+" pv "+X)
def Y(A1):
 return(abs((ord(A1[0:1])-96)-1),abs(int(A1[1:2])-8),abs((ord(A1[2:3])-96)-1),abs(int(A1[3:4])-8))
def A2(A3):
 return any(A3.A4(m)>=I for m in A3.A5())
class A6:
 A7=[]
 A8=0
 A9=[]
 A0=[]
 B=[[],[]]
 B1=[[],[]]
 B2=[1,1]
 B3=[1,1]
 B4='e1'
 B5='e8'
 B6=0
 B7=''
 def __init__(Z):
  Z.A7=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def B8(Z,A1):
  (B9,B0,C1,O)=Y(A1)
  C2=Z.A7[B0][B9]
  C3=Z.A8%2==0
  Z.A7[O][C1]=C2
  Z.A7[B0][B9]='-'
  set_B7=0
  if C2 in('P','p'):
   set_B7=abs(B0-O)==2
   B7_D1=-1 if C3 else 1
   if set_B7:
    Z.B7=A1[0:1]+str(int(A1[3:4])+B7_D1)
   elif A1[2:4]==Z.B7:
    Z.A7[O-B7_D1][C1]='-'
   if len(A1)>4:
    Z.A7[O][C1]=A1[4:5].upper()if C3 else A1[4:5]
  if not set_B7:
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
 def C4(Z,A1):
  Z5=A6()
  Z5.A8=Z.A8
  Z5.A7=[x[:]for x in Z.A7]
  Z5.B=[x[:]for x in Z.B]
  Z5.B1=[x[:]for x in Z.B1]
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
  Z5.A0.append(Z5.C6())
  Z5.B6=-Z5.B6
  return Z5
 def C5(Z):
  Z5=A6()
  Z5.A8=Z.A8+1
  Z5.A7=[x[:]for x in Z.A7]
  Z5.B2=Z.B2.copy()
  Z5.B3=Z.B3.copy()
  Z5.B4=''
  Z5.B5=''
  Z5.B7=''
  Z5.B6=-Z.B6
  return Z5
 def C7(Z):
  return 64-Z.C6().count('-')
 def C8(Z):
  C9=Z.C7()
  C0=Z.C6().lower().count('p')
  return C9<=14 or C0<=8
 def A4(Z,A1):
  C3=Z.A8%2==0
  D1=0 if C3 else 7
  (B9,B0,C1,O)=Y(A1)
  D2=0
  C2=Z.A7[B0][B9]
  D3=C2.lower()
  if Z.C8():
   if C2.lower()=='k':
    D3='ke'
   if C2.lower()=='p':
    D2+=6
    D3='pe'
  D4=Z.A7[O][C1]
  D2+=B[D3][abs(O-D1)][C1]-B[D3][abs(B0-D1)][B9]
  if D4!='-':
   D2+=B[D4.lower()][abs(O-D1)][C1]
  if C2 in('K','k'):
   if abs(B0-O)==2:
    if A1[2]=='g':
     D2+=B['r'][abs(O-D1)][C1-1]-B['r'][abs(O-D1)][C1+1]
    else:
     D2+=B['r'][abs(O-D1)][C1+1]-B['r'][abs(O-D1)][C1-2]
  elif C2 in('P','p'):
   p_D1=-1 if C3 else 1
   D5='P' if C3 else 'p'
   D6=0
   if O>0 and O<7:
    if C1>0:
     D6+=Z.A7[O+p_D1][C1-1]==D5
    if C1<7:
     D6+=Z.A7[O+p_D1][C1+1]==D5
   if D6>0:
    D2+=10
   if A1[2:4]==Z.B7:
    D2+=B[D3][abs(O-D1)][C1]
   if len(A1)>4:
    D7=A1[4:5]
    D2+=B[D7][abs(O-D1)][C1]-B['p'][abs(O-D1)][C1]
  if Z.C8():
   D8=Z.B5 if C3 else Z.B4
   if D8 in Z.B[C3]:
    D2+=8
  return D2+Z.D9(C3)
 def D9(Z,C3):
  D0='P' if C3 else 'p'
  E1=0
  E2=0
  for Z4 in range(8):
   E3=0
   for Z1 in range(8):
    if Z.A7[Z1][Z4]==D0:
     E1+=1
     E3=1
   E2+=E3
  return(E2-E1)*5
 def C6(Z):
  return ''.join(list(chain.from_iterable(Z.A7)))+str(Z.A8%2==0)
 def A5(Z,E4=0):
  C3=Z.A8%2==0
  if E4:
   C3=not C3
  Z.B[C3]=[]
  Z.B1[C3]=[]
  E5=['p','r','n','b','q','k','-']
  if not C3:
   E5=['P','R','N','B','Q','K','-']
  E6=1
  E7=6
  D1=1
  if not C3:
   E6=6
   E7=1
  E8=Z.A7
  for Z1 in range(8):
   for Z4 in range(8):
    Z2=E8[Z1][Z4]
    if Z2=="-" or(C3 and Z2.islower())or(not C3 and Z2.isupper()):
     continue
    E9=N(Z4+1)+str(abs(Z1-8))
    if Z2=='P':
     D1=-1
    if Z2=='K':
     if Z.B2[1]and E9=='e1' and ''.join(E8[7][5:8])=='--R':
      Z.B[C3].append(E9+'g1')
      yield E9+'g1'
     if Z.B2[0]and E9=='e1' and ''.join(E8[7][0:4])=='R---':
      Z.B[C3].append(E9+'c1')
      yield E9+'c1'
    elif Z2=='k':
     if Z.B3[1]and E9=='e8' and ''.join(E8[0][5:8])=='--r':
      Z.B[C3].append(E9+'g8')
      yield E9+'g8'
     if Z.B3[0]and E9=='e8' and ''.join(E8[0][0:4])=='r---':
      Z.B[C3].append(E9+'c8')
      yield E9+'c8'
    elif Z2.lower()=='p' and Z1==E7 and E8[Z1+D1][Z4]=='-' and E8[Z1+2*D1][Z4]=='-':
     Z.B[C3].append(E9+N(Z4+1)+str(abs(Z1-8+2*D1)))
     yield E9+N(Z4+1)+str(abs(Z1-8+2*D1))
    for F3 in M[Z2.lower()]:
     F4=Z4+F3[0]
     F5=Z1+(F3[1]*D1)
     while F4 in range(8)and F5 in range(8):
      F6=E8[F5][F4]
      F7=N(F4+1)+str(abs(F5-8))
      if Z2.lower()=='p':
       if(Z1==E6 and F3[0]==0 and F6=='-')or (Z1==E6 and F3[0]!=0 and F6!='-' and F6 in E5):
        for G8 in('q','r','b','n'):
         Z.B[C3].append(E9+F7+G8)
         yield E9+F7+G8
       else:
        if(F3[0]==0 and F6=='-')or (F3[0]!=0 and F6!='-' and F6 in E5)or F7==Z.B7:
         Z.B[C3].append(E9+F7)
         yield E9+F7
      elif F6 in E5:
       Z.B[C3].append(E9+F7)
       yield E9+F7
      if F3[2]:
       Z.B1[C3].append(F7)
      if F6!='-' or Z2.lower()in('k','n','p'):
       break
      F4+=F3[0]
      F5+=(F3[1]*D1)
 def E0(Z,C3):
  if C3:
   return Z.B4 in Z.B1[0]
  return Z.B5 in Z.B1[1]
 def F1(Z,F2):
  if Z.B4=='e1' and F2=='e1g1':
   return not any(Z7 in Z.B1[0]for Z7 in['e1','f1','g1'])
  elif Z.B4=='e1' and F2=='e1c1':
   return not any(Z7 in Z.B1[0]for Z7 in['e1','d1','c1'])
  elif Z.B5=='e8' and F2=='e8g8':
   return not any(Z7 in Z.B1[1]for Z7 in['e8','f8','g8'])
  elif Z.B5=='e8' and F2=='e8c8':
   return not any(Z7 in Z.B1[1]for Z7 in['e8','d8','c8'])
  return 1
F8=9e5
Entry=namedtuple('Entry','lower upper')
F9=0
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
  H3=Z.G4.get(A3.C6())
  if H3:
   if H3 in('e1c1','e1g1','e8c8','e8g8')and A3.E0(A3.A8%2==0):
    Z.G4[A3.C6()]=None
  for S in range(1,100):
   H4=-J
   H5=J
   while H4<H5-10:
    H6=(H4+H5+1)//2
    D2=Z.H9(A3,H6,S)
    if D2>=H6:
     H4=D2
    if D2<H6:
     H5=D2
   Z.H9(A3,H4,S)
   H7=Z.G4.get(A3.C6())
   if Z.G3.get((A3.C6(),S,1))is not None:
    J3=Z.G3.get((A3.C6(),S,1)).lower
   else:
    J3=D2
   H8=time.time()-H2
   W=math.ceil(Z.V/H8)
   R(str(S),str(math.ceil(J3)),str(math.ceil(H8)),str(Z.V),str(W),str(H7))
   yield S,H7,J3
 def H9(Z,A3,H6,S,H92=1,root=1):
  Z.V+=1
  if time.time()>Z.G2:
   return A3.B6
  S=max(0,S)
  if A3.B6<=-I:
   return-J
  if not root and A3.A0.count(A3.C6())>=2:
   return F9
  I1=Z.G3.get((A3.C6(),S,root),Entry(-J,J))
  if I1 is not None and I1.lower>=H6 and(not root or Z.G4.get(A3.C6())is not None):
   return I1.lower
  if I1 is not None and I1.upper<H6:
   return I1.upper
  C3=A3.A8%2==0
  def I9():
   I2=A3.C7()
   if S==0:
    yield None,A3.B6
   I5=Z.G4.get(A3.C6())
   if I5:
    I3=A3.A4(I5)
    I4=A3.C4(I5)
    if S>0 or I3>800 or I2!=I4.C7():
     yield I5,-Z.H9(I4,1-H6,S-1,root=0)
   for F2 in sorted(A3.A5(),key=A3.A4,reverse=H92):
    I6=A3.A4(F2)
    if not A3.F1(F2):
     continue
    G7=A3.C4(F2)
    J4=G7.C7()
    if A3.E0(C3):
     if A2(G7.C5()):
      continue
    if S>0 or I6>800 or I2!=J4:
     yield F2,-Z.H9(G7,1-H6,S-1,root=0)
  J5=-J
  for F2,D2 in I9():
   J5=max(J5,D2)
   if J5>=H6:
    if H92:
     Z.G4[A3.C6()]=F2
    break
  if J5<H6 and J5<0 and S>=0:
   if all(A2(A3.C4(m))for m in A3.A5()):
    E0=A2(A3.C5())
    J5=-J if E0 else F9
  if J5>=H6:
   Z.G3[A3.C6(),S,root]=Entry(J5,I1.upper)
  if J5<H6:
   Z.G3[A3.C6(),S,root]=Entry(I1.lower,J5)
  return J5
def main():
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
    gc.collect()
   elif Z3=="isready":
    Q("readyok")
   elif Z3.startswith("position"):
    I9=Z3.split()
    I7=A6()
    for I0 in I9[3:]:
     I7=I7.C4(I0)
    all(I7.A5())
    all(I7.A5(1))
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
    if I7.A8<13:
     J6+=10
    J6=max(J6,3)
    H91.G1=time.time()+J6
    H91.V=0
    F2=None
    start=time.time()
    for _depth,F2,score in H91.H1(I7):
     if I7.A8>13:
      if(H91.G1-time.time())<25:
       H91.S=5
     if _depth>=H91.S or time.time()>H91.G1:
      break
    Q("bestmove "+F2)
    if len(H91.G4)>F8:
     H91.G4.clear()
    if len(H91.G3)>F8:
     H91.G3.clear()
  except(KeyboardInterrupt,SystemExit):
   sys.exit()
  except Exception as exc:
   Q(exc)
   raise
main()

