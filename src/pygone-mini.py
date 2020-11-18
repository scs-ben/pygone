#!/usr/bin/env pypy3
import math,sys,time
t=time.time
A={'p':85,'n':290,'b':320,'r':620,'q':1250,'k':25000}
B={'p':(0,0,0,0,0,0,0,0,20,20,20,20,20,20,20,20,8,8,8,8,8,8,8,8,4,4,6,10,10,6,4,4,0,0,0,8,8,0,0,0,2,-2,-2,3,3,-2,-2,2,2,4,4,-8,-8,4,4,2,0,0,0,0,0,0,0,0),'n':(-20,-16,-12,-12,-12,-12,-16,-20,-16,-8,2,2,2,2,-8,-16,-8,2,4,6,6,4,2,-8,0,2,6,10,10,6,2,0,0,2,6,10,10,6,2,0,-8,4,4,4,4,4,4,-8,-16,-8,0,2,2,0,-8,-16,-20,-16,-12,-12,-12,-12,-16,-20),'b':(-8,-4,-4,-4,-4,-4,-4,-8,-4,0,0,0,0,0,0,-4,-4,0,2,4,4,2,0,-4,0,2,2,4,4,2,2,0,0,0,4,4,4,4,0,0,-4,4,4,4,4,4,4,-4,-4,2,0,0,0,0,2,-4,-8,-4,-4,-4,-4,-4,-4,-8),'r':(0,0,0,0,0,0,0,0,2,4,4,4,4,4,4,2,-4,0,2,2,2,2,0,-4,-2,0,2,2,2,2,0,-2,0,0,2,2,2,2,0,-2,-4,2,2,2,2,2,0,-4,-2,0,0,2,0,2,0,-2,0,0,0,2,2,0,0,0),'q':(-8,-4,-4,-2,-2,-4,-4,-8,-4,6,6,6,6,6,6,-4,-4,4,4,4,4,4,4,-4,-2,2,2,2,2,2,2,-2,-2,2,2,2,2,2,2,-2,-4,2,2,2,2,2,2,-4,-4,0,2,0,0,0,0,-4,-8,-4,-4,-2,-2,-4,-4,-8),'k':(-20,-16,-12,-8,-8,-12,-16,-20,-8,-8,-4,0,0,-4,-8,-8,-8,-4,8,12,12,8,-4,-8,-8,-4,12,16,16,12,-4,-8,-8,-4,12,16,16,12,-4,-8,-8,-4,8,12,12,8,-4,-8,8,8,-16,-16,-16,-16,8,8,0,4,8,0,0,4,8,0)}
for C,set_u in B.items():
 pZ1=lambda Z1:(0,)+tuple(Z2+A[C]for Z2 in Z1)+(0,)
 B[C]=sum((pZ1(set_u[Z4*8:Z4*8+8])for Z4 in range(8)),())
 B[C]=(0,)*20+B[C]+(0,)*20
H=1
K=2
L=3
J=A['k']
N5=7
N0=20
P5=10
M={'k':[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)],'q':[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)],'r':[(0,10),(0,-10),(1,0),(-1,0)],'b':[(1,10),(1,-10),(-1,10),(-1,-10)],'n':[(1,-20),(-1,-20),(2,-10),(-2,-10),(1,20),(-1,20),(2,10),(-2,10)],'p':[(0,-10),(1,-10),(-1,-10)]}
def N(O):
 return chr(O+96)
def Q(P):
 print(P,flush=1)
def R(S,K7,U,V,W,X):
 Q(f"info depth {S} score cp {K7} time {U} nodes {V} nps {W} pv {X}")
def Y(A1):
 return(O7(A1[0:2]),O7(A1[2:4]))
def O8(O0):
 return N(O0%10)+str(abs(O0//10-10))
def O7(Z7):
 return 10*(abs(int(Z7[1])-8)+2)+(ord(Z7[0])-97)+1
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
 S=1
 def __init__(Z):
  Z.A7=('.....................rnbqkbnr..pppppppp..--------..--------..--------..--------..PPPPPPPP..RNBQKBNR.....................')
 def O9(Z,O0,Z2):
  Z.A7=Z.A7[:O0]+Z2+Z.A7[O0+1:]
 def B8(Z,A1):
  i=Z.A8%2==0
  Z.M9+=1
  (B0,O)=Y(A1)
  C2=Z.A7[B0].lower()
  if Z.A7[O]!='-':
   Z.M9=0
  Z.O9(O,Z.A7[B0])
  Z.O9(B0,'-')
  B71=0
  if C2=='p':
   Z.M9=0
   B71=abs(B0-O)==20
   B72=-1 if i else 1
   if B71:
    Z.B7=A1[0:1]+str(int(A1[3:4])+B72)
   elif A1[2:4]==Z.B7:
    Z.O9(O-10*B72,'-')
   if len(A1)>4:
    Z.O9(O,A1[4:5].upper()if i else A1[4:5])
  elif C2=='k':
   if i:
    Z.B4=A1[2:4]
   else:
    Z.B5=A1[2:4]
   if A1 in('e1g1','e8g8'):
    Z.O9(O+1,'-')
    Z.O9(B0+1,'R' if i else 'r')
   elif A1 in('e1c1','e8c8'):
    Z.O9(O-2,'-')
    Z.O9(B0-1,'R' if i else 'r')
  if not B71:
   Z.B7=''
  Z.K3=Z.C6()
  Z.K4=Z.C7()
 def C4(Z,A1):
  u=Z.P1()
  u.B6=Z.B6+Z.A4(A1)
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
  u.B6=-u.B6
  u.A0.append(u.K3)
  return u
 def C5(Z):
  u=Z.P1()
  u.A8+=1
  u.B6=-Z.B6
  u.A9=[None]
  return u
 def P1(Z):
  u=A6()
  u.A8=Z.A8
  u.B4=Z.B4
  u.B5=Z.B5
  u.K3=Z.K3
  u.K4=Z.K4
  u.B7=Z.B7
  u.M9=Z.M9
  u.A7=Z.A7
  u.A9=Z.A9.copy()
  u.A0=Z.A0.copy()
  u.B2=Z.B2.copy()
  u.B3=Z.B3.copy()
  return u
 def C7(Z):
  return 64-J0(Z.K3,'-')
 def C8(Z):
  return Z.K4<14 
 def M3(Z,A1):
  return Z.A4(A1,1)
 def A4(Z,A1,M4=0):
  i=Z.A8%2==0
  D1=0 if i else 119
  D11=-10 if i else 10
  D5='P' if i else 'p'
  C8=Z.C8()
  (B0,O)=Y(A1)
  d=0
  C2=Z.A7[B0].lower()
  D4=Z.A7[O].lower()
  d+=B[C2][abs(O-D1)]- B[C2][abs(B0-D1)]
  if D4!='-':
   d+=B[D4][abs(O-D1)]
   if M4:
    d+=B[D4][abs(O-D1)]/B[C2][abs(O-D1)]
   if D4=='p':
    d-=Z.E11(A1,Z.A7[O],-D11)
  if C2=='p':
   if A1[2:4]==Z.B7:
    d+=B[C2][abs(O-D1)]
   elif len(A1)>4:
    D7=A1[4:5]
    d+=B[D7][abs(O-D1)]- B['p'][abs(O-D1)]
   d+=Z.E11(A1,D5,D11)
  elif C2=='k':
   if abs(B0-O)==2:
    if A1[2]=='g':
     d+=B['r'][abs(O-D1)-1]- B['r'][abs(O-D1)+1]
    else:
     d+=B['r'][abs(O-D1)+1]- B['r'][abs(O-D1)-2]
    d+=P5
    if M4:
     d+=50
  if not C8:
   d+=Z.P6(A1,i,D11)
  if M4 and Z.A8<24:
   if O in range(40,80):
    d-=40
   elif not B0 in range(30,90):
    d+=40
  if M4:
   G7=Z.C4(A1)
   if G7.E0(not i):
    d+=100+B[C2][abs(O-D1)]
  return d
 def E11(Z,A1,D5,D11):
  D61=Z.N61(D5,D11)
  E12=Z.P7(D5)
  P9=Z.P1()
  P9.B8(A1)
  D6=P9.N61(D5,D11)
  stacked_E1=P9.P7(D5)
  return(D6-D61)*N5+ (E12-stacked_E1)*N0
 def N61(Z,D5,D11):
  D6=0
  for O0,Z2 in enumerate(Z.A7):
   if Z2==D5:
    D6+=Z.N6(O0,D11,D5)
  return D6
 def N6(Z,O0,D11,D5):
  return D5 in(Z.A7[O0-D11+1],Z.A7[O0-D11-1])
 def P7(Z,D5):
  stacked_E1=0
  for O0,Z2 in enumerate(Z.A7):
   if Z2==D5:
    stacked_E1+=Z.N9(O0,D5)>1
  return stacked_E1/2
 def N9(Z,O0,D5):
  K4=0
  Z4=O0%10
  for Z1 in range(1,9):
   K4+=Z.A7[(Z1*10+Z4)]==D5
  return K4
 def P6(Z,A1,i,D11):
  O1=O7(Z.B4 if i else Z.B5)
  L8='PNB' if i else 'pnb'
  D61=0
  P8=Z.A7[(O1+D11-1):(O1+D11+2)]
  for Z2 in L8:
   D61+=P8.count(Z2)
  P9=Z.P1()
  P9.B8(A1)
  D6=0
  P8=P9.A7[(O1+D11-1):(O1+D11+2)]
  for Z2 in L8:
   D6+=P8.count(Z2)
  return(D6-D61)*P5 
 def C6(Z):
  return Z.A7+ str(Z.A8%2)
 def N7(Z):
  return Z.A5(1)
 def A5(Z,N8=0):
  i=Z.A8%2==0
  D1=1
  E7=81 if i else 31
  E6=31 if i else 81
  E5='prnbqk-' if i else 'PRNBQK-'
  for O0,Z2 in enumerate(Z.A7):
   if Z2 in "-." or i==Z2.islower():
    continue
   E9=O8(O0)
   K0=Z2.lower()
   if Z2=='p':
    D1=-1
   if not N8:
    if Z2=='K':
     if Z.B2[1]and Z.A7[96:99]=='--R' and not any(Z.O2(i,Z7)for Z7 in['e1','f1','g1']):
      yield E9+'g1'
     if Z.B2[0]and Z.A7[91:95]=='R---' and not any(Z.O2(i,Z7)for Z7 in['e1','d1','c1']):
      yield E9+'c1'
    elif Z2=='k':
     if Z.B3[1]and Z.A7[26:29]=='--r' and not any(Z.O2(i,Z7)for Z7 in['e8','f8','g8']):
      yield E9+'g8'
     if Z.B3[0]and Z.A7[21:25]=='r---' and not any(Z.O2(i,Z7)for Z7 in['e8','d8','c8']):
      yield E9+'c8'
    elif K0=='p' and E7<=O0<E7+8 and Z.A7[O0+-10*D1]=='-' and Z.A7[O0+-20*D1]=='-':
     yield E9+O8(O0+-20*D1)
   for F3 in M[K0]:
    P3=O0+F3[0]+(F3[1]*D1)
    while 20<P3<99:
     F6=Z.A7[P3]
     if not N8 or(N8 and F6 not in '-.'):
      F7=O8(P3)
      if K0=='p':
       if(O0 in range(E6,E6+8)and F3[0]==0 and F6=='-')or (O0 in range(E6,E6+8)and F3[0]!=0 and F6!='-' and F6 in E5):
        for G8 in 'qrbn':
         yield E9+F7+G8
       else:
        if(F3[0]==0 and F6=='-')or (F3[0]!=0 and F6!='-' and F6 in E5)or F7==Z.B7:
         yield E9+F7
      elif F6 in E5:
       yield E9+F7
     if F6!='-' or K0 in 'knp':
      break
     P3=P3+F3[0]+(F3[1]*D1)
 def E0(Z,i):
  O1=Z.B4 if i else Z.B5
  return Z.O2(i,O1)
 def O2(Z,i,Z7):
  D1=1
  E5='PRNBQK-' if i else 'prnbqk-'
  O2=O7(Z7)
  for O0,Z2 in enumerate(Z.A7):
   if Z2 in "-." or i==Z2.isupper():
    continue
   if Z2=='p':
    D1=-1
   Z2=Z2.lower()
   for F3 in M[Z2]:
    if Z2=='p' and not F3[0]:
     continue
    P3=O0+F3[0]+(D1*F3[1])
    while 20<P3<99:
     F6=Z.A7[P3]
     if F6 in E5 and P3==O2:
      return 1
     if F6!='-' or Z2 in 'knp':
      break
     P3=P3+F3[0]+D1*F3[1]
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
  for S in range(1,100):
   d=Z.H9(l,S,-J,J)
   if t()<Z.G2:
    H7=Z.G3.get(l.K3)
    if H7:
     H7=H7['N1']
   else:
    break
   H8=t()-H2
   W=math.ceil(Z.V/H8)if H8>0 else 1
   R(str(S),str(math.ceil(d)),str(math.ceil(H8)),str(Z.V),str(W),str(H7))
   yield S,H7,d
 def H9(Z,l,S,a,b):
  if t()>Z.G2:
   return-J
  Z.V+=1
  is_L1=(a!=b-1)
  E01=l.E0(l.A8%2==0)
  S+=E01
  if S==0:
   return Z.H93(l,a,b)
  if l.A0.count(l.K3)>1 or l.M9>=100:
   return 0
  P4=J-S
  if P4<b:
   b=P4
   if a>=P4:
    return P4
  P4=-J+S
  if P4>a:
   a=P4
   if b<=P4:
    return P4
  L2=a
  e=Z.G3.get((l.K3),{'M1':2*J,'M2':K,'M0':-1,'N1':None})
  if e['M0']>=S and not is_L1:
   if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
    return e['M1']
  if not is_L1 and not E01 and S<=7 and l.B6-(85*S)>=b:
   return l.B6
  if not is_L1 and not E01 and S<=3 and l.B6+325*S<=a:
   return l.B6
  T=-J-1
  d=-J
  i=l.A8%2==0
  L8='RNBQ' if i else 'rnbq'
  if not is_L1 and not E01 and L8 in l.K3:
   d=-Z.H9(l.C5(),S-4,-b,-b+1)
   if d>=b:
    return b
  if not is_L1 and not E01 and abs(e['M1'])<J and e['N1']:
   d=-Z.H9(l.C4(e['N1']),S-2,-b,-a)
   if d>=b:
    return b
  I92=0
  H7=None
  for F2 in sorted(l.A5(),key=l.M3,reverse=1):
   G7=l.C4(F2)
   if G7.E0(i):
    continue
   I6=G7.B6-l.B6
   I92+=1
   r_depth=1
   if abs(I6)<100 and S>2 and I92>1:
    r_depth+=not is_L1
    r_depth+=E01
    r_depth=min(S-1,r_depth)
   if r_depth!=1:
    d=-Z.H9(G7,S-r_depth,-a-1,-a)
   if(r_depth!=1 and d>a)or(r_depth==1 and not(is_L1 and I92==1)):
    d=-Z.H9(G7,S-1,-a-1,-a)
   if is_L1 and(I92==1 or d>a):
    d=-Z.H9(G7,S-1,-b,-a)
   if not H7:
    H7=F2
   if d>T:
    H7=F2
    T=d
    if d>=b:
     break
    if d>a:
     a=d
  if I92==0:
   return-J if E01 else 0
  if t()<Z.G2:
   e['M1']=T
   e['N1']=H7
   e['M0']=S
   if T<=L2:
    e['M2']=K
   elif T>=b:
    e['M2']=L
   else:
    e['M2']=H
   Z.G3[l.K3]=e
  return T
 def H93(Z,l,a,b):
  if t()>Z.G2:
   return-J
  Z.V+=1
  if l.A0.count(l.K3)>1 or l.M9>=100:
   return 0
  e=Z.G3.get(l.K3)
  if e:
   if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
    return e['M1']
  d=l.B6
  if d>=b:
   return b
  a=max(a,d)
  for F2 in sorted(l.N7(),key=l.M3,reverse=1):
   G7=l.C4(F2)
   if G7.E0(l.A8%2==0):
    continue
   d=-Z.H93(G7,-b,-a)
   if d>=b:
    return b
   if d>a:
    a=d
  return a
P2=F0()
def main():
 I7=A6()
 while 1:
  try:
   Z3=input()
   if Z3=="quit":
    sys.exit()
   elif Z3=="uci":
    Q("pygone 1.4\nuciok")
   elif Z3=="ucinewgame":
    I7=A6()
    P2.G9()
   elif Z3=="isready":
    Q("readyok")
   elif Z3.startswith("position"):
    I9=Z3.split()
    I7=A6()
    for I0 in I9[3:]:
     I7=I7.C4(I0)
   elif Z3.startswith("go"):
    P2.S=30
    J6=1e8
    i=I7.A8%2==0
    J3=Z3.split()
    for key,arg in enumerate(J3):
     if arg=='wtime' and i or arg=='btime' and not i:
      J6=int(J3[key+1])/1e3
     elif arg=='depth':
      P2.S=int(J3[key+1])
    UU=20 
    P2.G2=t()+max(0.5,J6-1)
    J6=max(3,J6/UU)
    P2.G1=t()+J6
    P2.V=0
    F2=None
    start=t()
    for S,F2,T in P2.H1(I7):
     if(P2.G1-t())<1:
      P2.S=3
     if S>=P2.S or t()>P2.G1 or abs(T)>=J:
      break
    Q(f"bestmove {str(F2)}")
  except(KeyboardInterrupt,SystemExit):
   sys.exit()
  except Exception as exc:
   Q(exc)
   raise
main()

