#!/usr/bin/env pypy3
import math,sys,time
t=time.time
A={'p':136,'n':782,'b':830,'r':1289,'q':2529,'k':32e4}
B={'p':[[0,0,0,0,0,0,0,0],[-10,6,-5,-11,-2,-14,12,-1],[-6,-8,5,11,-14,0,-12,-14],[6,-3,-10,1,12,6,-12,1],[-9,-18,8,22,33,25,-4,-16],[-11,-10,15,22,26,28,4,-24],[0,-5,10,13,21,17,6,-3],[0,0,0,0,0,0,0,0]],'n':[[-200,-80,-53,-32,-32,-53,-80,-200],[-67,-21,6,37,37,6,-21,-67],[-11,28,63,55,55,63,28,-11],[-29,13,42,52,52,42,13,-29],[-28,5,41,47,47,41,5,-28],[-64,-20,4,19,19,4,-20,-64],[-79,-39,-24,-9,-9,-24,-39,-79],[-169,-96,-80,-79,-79,-80,-96,-169]],'b':[[-48,-3,-12,-25,-25,-12,-3,-48],[-21,-19,10,-6,-6,10,-19,-21],[-17,4,-1,8,8,-1,4,-17],[-7,30,23,28,28,23,30,-7],[1,8,26,37,37,26,8,1],[-8,24,-3,15,15,-3,24,-8],[-18,7,14,3,3,14,7,-18],[-44,-4,-11,-28,-28,-11,-4,-44]],'r':[[-22,-24,-6,4,4,-6,-24,-22],[-8,6,10,12,12,10,6,-8],[-24,-4,4,10,10,4,-4,-24],[-24,-12,-1,6,6,-1,-12,-24],[-13,-5,-4,-6,-6,-4,-5,-13],[-21,-7,3,-1,-1,3,-7,-21],[-18,-10,-5,9,9,-5,-10,-18],[-24,-13,-7,2,2,-7,-13,-24]],'q':[[-2,-2,1,-2,-2,1,-2,-2],[-5,6,10,8,8,10,6,-5],[-4,10,6,8,8,6,10,-4],[0,14,12,5,5,12,14,0],[4,5,9,8,8,9,5,4],[-3,6,13,7,7,13,6,-3],[-3,5,8,12,12,8,5,-3],[3,-5,-5,4,4,-5,-5,3]],'k':[[64,87,49,0,0,49,87,64],[87,120,64,25,25,64,120,87],[122,159,85,36,36,85,159,122],[145,176,112,69,69,112,176,145],[169,191,136,108,108,136,191,169],[198,253,168,120,120,168,253,198],[277,305,241,183,183,241,305,277],[272,325,273,190,190,273,325,272]],}
for C,_ in B.items():
 for D in range(8):
  for E in range(8):
   B[C][D][E]+=A[C]
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
 B1=[[],[]]
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
  Z.K3="rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR1"
 def B8(Z,A1):
  i=Z.A8%2==0
  Z.M9+=1
  (B9,B0,C1,O)=Y(A1)
  C2=Z.A7[B0][B9]
  if Z.A7[O][C1]!='-':
   Z.M9=0
  Z.A7[O][C1]=C2
  Z.A7[B0][B9]='-'
  B71=0
  if C2.lower()=='p':
   Z.M9=0
   B71=abs(B0-O)==2
   B72=-1 if i else 1
   if B71:
    Z.B7=A1[0:1]+str(int(A1[3:4])+B72)
   elif A1[2:4]==Z.B7:
    Z.A7[O-B72][C1]='-'
   if len(A1)>4:
    Z.A7[O][C1]=A1[4:5].upper()if i else A1[4:5]
  elif C2.lower()=='k':
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
  u.A8=Z.A8
  for Z1 in range(8):
   u.A7[Z1]=Z.A7[Z1].copy()
  u.B1[0]=Z.B1[0].copy()
  u.B1[1]=Z.B1[1].copy()
  u.A9=Z.A9.copy()
  u.A0=Z.A0.copy()
  u.B2=Z.B2.copy()
  u.B3=Z.B3.copy()
  u.B4=Z.B4
  u.B5=Z.B5
  u.B7=Z.B7
  u.M9=Z.M9
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
  u.B1[0]=Z.B1[0].copy()
  u.B1[1]=Z.B1[1].copy()
  u.B2=Z.B2.copy()
  u.B3=Z.B3.copy()
  u.B4=''
  u.B5=''
  u.B7=''
  u.B6=-Z.B6
  u.A9=[None]
  return u
 def C7(Z):
  return 64-J0(Z.K3,'-')
 def C8(Z):
  return Z.K4<16
 def M3(Z,A1):
  return Z.A4(A1,1)
 def A4(Z,A1,M4=0,reverse_capture=0):
  if not A1:
   return 0
  i=Z.A8%2==0
  D1=0 if i else 7
  D11=-1 if i else 1
  D5='P' if i else 'p'
  (B9,B0,C1,O)=Y(A1)
  D2=0
  C2=Z.A7[B0][B9].lower()
  D4=Z.A7[O][C1].lower()
  D2+=B[C2][abs(O-D1)][C1]- B[C2][abs(B0-D1)][B9]
  if D4!='-':
   D2+=B[D4][abs(O-D1)][C1]
   if M4:
    D2+=min(2,(A[D4]/10)-(A[C2]/10))
  if C2=='k':
   if abs(B9-C1)==2:
    if M4:
     D2+=500
    if A1[2]=='g':
     D2+=B['r'][abs(O-D1)][C1-1]- B['r'][abs(O-D1)][C1+1]
    else:
     D2+=B['r'][abs(O-D1)][C1+1]- B['r'][abs(O-D1)][C1-2]
   elif M4 and not Z.C8():
    D2-=1000
  elif M4 and Z.A8<30 and C2=='q' and abs(O-D1)>3:
   D2-=300
  elif C2=='p':
   if M4 and Z.A8<30:
    D2+=B[C2][abs(O-D1)][C1]/10
   if A1[2:4]==Z.B7:
    D2+=B[C2][abs(O-D1)][C1]
   elif len(A1)>4:
    D7=A1[4:5]
    D2+=B[D7][abs(O-D1)][C1]- B['p'][abs(O-D1)][C1]
    C2=D7
  return D2
 def C6(Z):
  return v(Z.A7[0])+ v(Z.A7[1])+ v(Z.A7[2])+ v(Z.A7[3])+ v(Z.A7[4])+ v(Z.A7[5])+ v(Z.A7[6])+ v(Z.A7[7])+ str(Z.A8%2==0)
 def A5(Z,E4=0):
  i=Z.A8%2==0
  if E4:
   i=not i
  Z.B1[i]=[]
  B=[]
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
    if Z2=='K':
     if Z.B2[1]and E9=='e1' and v(E8[7][5:8])=='--R' and not any(Z7 in Z.B1[0]for Z7 in['e1','f1','g1']):
      B.append(E9+'g1')
     if Z.B2[0]and E9=='e1' and v(E8[7][0:4])=='R---' and not any(Z7 in Z.B1[0]for Z7 in['e1','d1','c1']):
      B.append(E9+'c1')
    elif Z2=='k':
     if Z.B3[1]and E9=='e8' and v(E8[0][5:8])=='--r' and not any(Z7 in Z.B1[1]for Z7 in['e8','f8','g8']):
      B.append(E9+'g8')
     if Z.B3[0]and E9=='e8' and v(E8[0][0:4])=='r---' and not any(Z7 in Z.B1[1]for Z7 in['e8','d8','c8']):
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
       Z.B1[i].append(F7)
      if F6!='-' or K0 in('k','n','p'):
       break
      F4+=F3[0]
      F5+=(F3[1]*D1)
  return B
 def E0(Z,i):
  king_position=Z.B4 if i else Z.B5
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
     F4=Z4+F3[0]
     F5=Z1+(F3[1]*D1)
     while F4 in range(8)and F5 in range(8):
      F6=E8[F5][F4]
      F7=N(F4+1)+str(abs(F5-8))
      if F3[2]and F7==king_position:
       return 1
      if F6!='-' or Z2 in('k','n','p'):
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
  L3=-J
  L4=J
  for S in range(1,100):
   all(l.A5(1))
   all(l.A5())
   if S>2:
    L3=D2-10
    L4=D2+10
   D2=Z.H9(l,S,L3,L4)
   if D2<=L3 or D2>=L4:
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
 def H9(Z,l,S,L3,L4,H95=1,H93=1):
  if t()>Z.G2:
   return l.B6
  Z.V+=1
  if l.B6<=-I:
   return-J
  i=l.A8%2==0
  L1=(L3!=L4-1)
  E01=l.E0(i)
  S=max(0,S)
  if not H95 and(l.A0.count(l.K3)>1 or l.M9>=100):
   return 0
  I1=Z.G3.get((l.K3),{'M1':2*J,'M2':K,'M0':0,'N1':None})
  if I1['M0']>=S:
   if I1['M2']==H or (I1['M2']==L and I1['M1']>=L4)or (I1['M2']==K and I1['M1']<=L3):
    return I1['M1']
  L2=L3
  L5=I1['M1']if I1['M1']<J else l.B6
  if not L1 and not E01 and S<=7 and L5-85*S>L4:
   return L5
  T=l.B6 if S==0 else-J-1
  D2=-J
  L8='RNBQ' if i else 'rnbq'
  if S>0 and not L1 and not E01 and L5>=L4 and S>=2 and L8 in l.K3 and l.A9[0]:
   D2=-Z.H9(l.C5(),S-3,-L4,-L4+1,0,0)
   if D2>=L4:
    return L4
  if S>0 and not L1 and not E01 and l.A9[0]and I1['N1']:
   D2=-Z.H9(l.C4(I1['N1']),S-1,-L4,-L3,0,1)
   if D2>=L4:
    return L4
  I92=0
  H7=None
  S+=E01
  for F2 in sorted(l.A5(),key=l.M3,reverse=1):
   I6=l.A4(F2)
   G7=l.C4(F2)
   if G7.E0(i):
    continue
   I92+=1
   M7=I6>220 
   if(S>0 and I92<3)or(S==0 and M7):
    D2=-Z.H9(G7,S-1,-L4,-L3,0,M7)
   elif S>0:
    M8=1
    if S>2 and not M7:
     M8=2
    D2=-Z.H9(G7,S-M8,-L3-1,-L3,0,M7)
    if M8>1 and D2>L3:
     D2=-Z.H9(G7,S-1,-L3-1,-L3,0,M7)
    if L3<D2<L4:
     D2=-Z.H9(G7,S-1,-L4,-L3,0,M7)
   if D2>T:
    H7=F2
    T=D2
    if D2>L3:
     L3=D2
     if L3>=L4:
      break
  if I92==0:
   return-J if E01 else 0
  if t()<Z.G2 and S>0:
   I1['M1']=T
   I1['N1']=H7
   if T<=L2:
    I1['M2']=K
   elif T>=L4:
    I1['M2']=L
   else:
    I1['M2']=H
   Z.G3[l.K3]=I1
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
    elif arg=='depth':
     H91.S=int(J3[key+1])
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
   ponder_u=I7.C4(F2)
   ponder_bucket=H91.G3.get(ponder_u.K3)
   ponder=""
   if ponder_bucket:
    ponder=f" ponder {ponder_bucket['N1']}"
   Q(f"bestmove {str(F2)}{ponder}")
   if len(H91.G3)>2e6:
    H91.G3.clear()
 except(KeyboardInterrupt,SystemExit):
  sys.exit()
 except Exception as exc:
  Q(exc)
  raise

