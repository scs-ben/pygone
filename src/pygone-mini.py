#!/usr/bin/env pypy3
import copy,math,random,sys,time
t=time.time
A={'p':100,'n':290,'b':300,'r':620,'q':1250,'k':2e4}
B={'p':(0,0,0,0,0,0,0,0,20,20,20,20,20,20,20,20,8,8,8,8,8,8,8,8,4,4,6,10,10,6,4,4,0,0,0,8,8,0,0,0,2,-2,-2,2,2,-2,-2,2,2,4,4,-8,-8,4,4,2,0,0,0,0,0,0,0,0),'n':(-20,-16,-12,-12,-12,-12,-16,-20,-16,-8,2,2,2,2,-8,-16,-12,2,4,6,6,4,2,-12,-12,2,6,10,10,6,2,-12,-12,2,6,10,10,6,2,-12,-12,4,4,4,4,4,4,-12,-16,-8,0,2,2,0,-8,-16,-20,-16,-12,-12,-12,-12,-16,-20),'b':(-8,-4,-4,-4,-4,-4,-4,-8,-4,0,0,0,0,0,0,-4,-4,0,2,4,4,2,0,-4,0,2,2,4,4,2,2,0,0,0,4,4,4,4,0,0,-4,4,4,4,4,4,4,-4,-4,2,0,0,0,0,2,-4,-8,-4,-4,-4,-4,-4,-4,-8),'r':(0,0,0,0,0,0,0,0,2,4,4,4,4,4,4,2,-4,0,2,2,2,2,0,-4,-2,0,2,2,2,2,0,-2,0,0,2,2,2,2,0,-2,-4,2,2,2,2,2,0,-4,-2,0,0,2,0,2,0,-2,0,0,0,2,2,0,0,0),'q':(-8,-4,-4,-2,-2,-4,-4,-8,-4,2,2,2,2,2,2,-4,-4,2,2,2,2,2,2,-4,-2,2,2,2,2,2,2,-2,-2,2,2,2,2,2,2,-2,-4,2,2,2,2,2,2,-4,-4,0,2,0,0,0,0,-4,-8,-4,-4,-2,-2,-4,-4,-8),'k':(-20,-16,-12,-8,-8,-12,-16,-20,-8,-8,-4,0,0,-4,-8,-8,-8,-4,8,12,12,8,-4,-8,-8,-4,12,16,16,12,-4,-8,-8,-4,12,16,16,12,-4,-8,-8,-4,8,12,12,8,-4,-8,8,8,-16,-16,-16,-16,8,8,0,4,12,0,0,4,12,0)}
for C,u in B.items():
 pZ1=lambda Z1:(0,)+tuple(Z2+A[C]for Z2 in Z1)+(0,)
 B[C]=sum((pZ1(u[Z4*8:Z4*8+8])for Z4 in range(8)),())
 B[C]=(0,)*20+B[C]+(0,)*20
H=1
K=2
L=3
I=A['k']-10*A['q']
J=A['k']+10*A['q']
N5=8
N0=12
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
  Z.A7=('..........' '..........' '.rnbqkbnr.' '.pppppppp.' '.--------.' '.--------.' '.--------.' '.--------.' '.PPPPPPPP.' '.RNBQKBNR.' '..........' '..........')
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
  u=Z.u_copy()
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
  u=Z.u_copy()
  u.A8+=1
  u.B6=-Z.B6
  u.A9=[None]
  return u
 def u_copy(Z):
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
 def A4(Z,A1,M4=0,S=1):
  if not A1:
   return 0
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
    d+=(A[D4]-A[C2])
   if D4=='b' and Z.A7.count(Z.A7[O])==2:
    d+=N0
   elif D4=='p':
    if Z.N6(O,-D11,D4):
     d+=N5
    if Z.N9(O,D4)==2 or Z.N9(O,D5)==1:
     d-=N0
    if Z.N9(O,D5)==0:
     d+=N0
  if C2=='k':
   if abs(B0-O)==2:
    if A1[2]=='g':
     d+=B['r'][abs(O-D1)-1]- B['r'][abs(O-D1)+1]
    else:
     d+=B['r'][abs(O-D1)+1]- B['r'][abs(O-D1)-2]
  elif C2=='r':
   O3=Z.N9(B0,'-')
   O4=Z.N9(O,'-')
   if O3<7 and O4==8:
    d+=N5
   elif O3==7 and O4<8:
    d-=N5
  elif C2=='p':
   if A1[2:4]==Z.B7:
    d+=B[C2][abs(O-D1)]
   elif len(A1)>4:
    D7=A1[4:5]
    d+=B[D7][abs(O-D1)]- B['p'][abs(O-D1)]
   if D4=='-':
    if Z.N6(O,D11,D5):
     d+=N5
    if Z.N6(O,-D11,D5):
     d+=N5
    if Z.N6(B0,D11,D5):
     d-=N5
    if Z.N6(B0,-D11,D5):
     d-=N5
   if(D4!='-' and D4!='p')or A1[2:4]==Z.B7:
    if Z.N6(B0,D11,D5):
     d-=N5
    if Z.N6(O,-D11,D5):
     d+=N5
    if Z.N9(B0,D5)==2:
     d+=N0
    if Z.N9(O,D5)==1:
     d-=N0
   if not C8:
    if 'k' in Z.A7[(B0-D11-1):(B0-D11+2)].lower():
     d-=2*N0
  if M4:
   d+=random.randint(1,min(1,Z.S))
  return d
 def N6(Z,O0,D11,D5):
  return Z.A7[O0-D11+1]==D5 or Z.A7[O0-D11-1]==D5
 def N9(Z,O0,D5):
  K4=0
  Z4=O0%10
  for Z1 in range(1,9):
   K4+=Z.A7[(Z1*10+Z4)]==D5
  return K4
 def C6(Z):
  return Z.A7+ str(Z.A8%2==0)
 def N7(Z):
  return Z.A5(1)
 def A5(Z,N8=0):
  i=Z.A8%2==0
  D1=1
  E7=81
  E6=31
  E5='prnbqk-'
  if not i:
   E5='PRNBQK-'
   E7=31
   E6=81
  for O0,Z2 in enumerate(Z.A7):
   if Z2 in "-." or(i and Z2.islower())or(not i and Z2.isupper()):
    continue
   E9=O8(O0)
   K0=Z2.lower()
   if Z2=='p':
    D1=-1
   if Z2=='K' and not N8:
    if Z.B2[1]and Z.A7[96:99]=='--R' and not any(Z.O2(i,Z7)for Z7 in['e1','f1','g1']):
     yield E9+'g1'
    if Z.B2[0]and Z.A7[91:95]=='R---' and not any(Z.O2(i,Z7)for Z7 in['e1','d1','c1']):
     yield E9+'c1'
   elif Z2=='k' and not N8:
    if Z.B3[1]and Z.A7[26:29]=='--r' and not any(Z.O2(i,Z7)for Z7 in['e8','f8','g8']):
     yield E9+'g8'
    if Z.B3[0]and Z.A7[21:25]=='r---' and not any(Z.O2(i,Z7)for Z7 in['e8','d8','c8']):
     yield E9+'c8'
   elif K0=='p' and O0 in range(E7,E7+8)and Z.A7[O0+-10*D1]=='-' and Z.A7[O0+-20*D1]=='-' and not N8:
    yield E9+O8(O0+-20*D1)
   for F3 in M[K0]:
    to_position=O0+F3[0]+(F3[1]*D1)
    while 20<to_position<99:
     F6=Z.A7[to_position]
     F7=O8(to_position)
     if not N8 or(N8 and F6 not in '-.'):
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
     to_position=to_position+F3[0]+(F3[1]*D1)
 def E0(Z,i):
  O1=Z.B4 if i else Z.B5
  return Z.O2(i,O1)
 def O2(Z,i,Z7):
  D1=1
  E5='PRNBQK-'
  if not i:
   E5='prnbqk-'
  O2=O7(Z7)
  for O0,Z2 in enumerate(Z.A7):
   if Z2 in "-." or(i and Z2.isupper())or(not i and Z2.islower()):
    continue
   E9=O8(O0)
   if Z2=='p':
    D1=-1
   Z2=Z2.lower()
   for F3 in M[Z2]:
    if Z2=='p' and not F3[0]:
     continue
    to_position=O0+F3[0]+D1*F3[1]
    while 20<to_position<99:
     F6=Z.A7[to_position]
     if F6 in E5 and to_position==O2:
      return 1
     if F6!='-' or Z2 in 'knp':
      break
     to_position=to_position+F3[0]+D1*F3[1]
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
   pv=''
   counter=1
   pv_u=l.C4(H7)
   while counter<min(6,S):
    counter+=1
    pv_entry=Z.G3.get(pv_u.K3)
    if not pv_entry:
     break
    pv_u=pv_u.C4(pv_entry['N1'])
    pv+=' '+pv_entry['N1']
   R(str(S),str(math.ceil(d)),str(math.ceil(H8)),str(Z.V),str(W),str(H7+pv))
   yield S,H7,d
 def H9(Z,l,S,a,b):
  if t()>Z.G2:
   return l.B6
  Z.V+=1
  if l.B6<=-I:
   return-J
  i=l.A8%2==0
  L1=(a!=b-1)
  E01=l.E0(i)
  S=max(0,S)
  if S==0 and not E01:
   return Z.H93(l,a,b)
  if l.A0.count(l.K3)>=2 or l.M9>=100:
   return 0
  S+=E01
  L2=a
  e=Z.G3.get((l.K3),{'M1':2*J,'M2':K,'M0':-1,'N1':None})
  if e['M0']>=S and not E01:
   if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
    return e['M1']
  L5=e['M1']if e['M1']<J else l.B6
  if not L1 and not E01 and S<=7 and L5-(100*S)>=b:
   return L5
  T=-J-1
  d=-J
  L8='RNBQ' if i else 'rnbq'
  if not L1 and not E01 and L5>=b and S>=4 and L8 in l.K3 and l.A9[0]and e['M2']!=K and e['M1']<b:
   d=-Z.H9(l.C5(),min(1,S-4),-b,-b+1)
   if d>=b and abs(d)<J:
    return b
  if not L1 and not E01 and l.A9[0]and e['N1']:
   d=-Z.H9(l.C4(e['N1']),S-1,-b,-a)
   if d>=b and abs(d)<J:
    return b
  I92=0
  H7=None
  l.S=S
  for F2 in sorted(l.A5(),key=l.M3,reverse=1):
   G7=l.C4(F2)
   I6=G7.B6-l.B6
   if G7.E0(i):
    continue
   I92+=1
   if I92==1:
    d=-Z.H9(G7,S-1,-b,-a)
   else:
    M8=1
    M7=I6>800 or l.K4!=G7.K4
    if S>2 and not M7:
     M8=min(3,S)
    d=-Z.H9(G7,S-M8,-a-1,-a)
    if M8>1 and d>a:
     d=-Z.H9(G7,S-1,-a-1,-a)
    if a<d<b:
     d=-Z.H9(G7,S-1,-b,-a)
   if d>T:
    H7=F2
    T=d
    a=max(a,d)
    if a>=b:
     break
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
  Z.V+=1
  if l.B6<=-I:
   return-J
  if l.A0.count(l.K3)>=2 or l.M9>=100:
   return 0
  e=Z.G3.get(l.K3)
  if e:
   if e['M2']==H or (e['M2']==L and e['M1']>=b)or (e['M2']==K and e['M1']<=a):
    return e['M1']
  i=l.A8%2==0
  E01=l.E0(i)
  d=l.B6 if not E01 else-J
  if d>=b:
   return b
  T=d
  a=max(a,d)
  for F2 in sorted(l.N7(),key=l.M3,reverse=1):
   G7=l.C4(F2)
   I6=G7.B6-l.B6
   M7=I6>800 or l.K4!=G7.K4
   if G7.E0(i)or not M7:
    continue
   d=-Z.H93(G7,-b,-a)
   if d>T:
    T=d
    if d>a:
     a=d
   if a>=b:
    return T
  return T
I7=A6()
H91=F0()
while 1:
 try:
  Z3=input()
  if Z3=="quit":
   sys.exit()
  elif Z3=="uci":
   Q("pygone 1.4\nuciok")
  elif Z3=="ucinewgame":
   I7=A6()
   H91.G9()
  elif Z3=="isready":
   Q("readyok")
  elif Z3.startswith("position fen"):
   fens=Z3.split(' ')
   position=fens[2].split('/')
   position=21
   for Z2 in fens[2]:
    if Z2=='/':
     position+=2
    else:
     if Z2.isnumeric():
      skip_count=int(Z2)
      while skip_count>0:
       I7.O9(position,'-')
       position+=1
       skip_count-=1
     else:
      I7.O9(position,Z2)
      if Z2.isupper():
       I7.B6+=B[Z2.lower()][position]
       if Z2=='K':
        I7.B4=O8(position)
      else:
       I7.B6-=B[Z2.lower()][abs(position-119)]
       if Z2=='k':
        I7.B5=O8(position)
      position+=1
   for castling in fens[4]:
    if castling=='-':
     I7.B2=[0,0]
     I7.B3=[0,0]
    elif castling=='K':
     I7.B2[1]=1
    elif castling=='Q':
     I7.B2[0]=1
    elif castling=='k':
     I7.B3[1]=1
    elif castling=='q':
     I7.B3[0]=1
   I7.B7=fens[5]
   I7.K3=I7.C6()
   I7.K4=I7.C7()
   if len(fens)>6:
    I7.M9=int(fens[6])
    I7.A8=int(fens[7])*2
   if fens[3]=='b':
    I7.A8+=1
  elif Z3.startswith("print"):
   for Z1 in range(12):
    position=Z1*10
    print(I7.A7[position:position+10])
   print(I7.A8,I7.E0(I7.A8%2==0))
  elif Z3.startswith("position startpos"):
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
   UU=20 if J6>200 else 11
   H91.G2=t()+(J6)-1
   J6=max(3,J6/UU)
   H91.G1=t()+J6
   H91.V=0
   F2=None
   start=t()
   for S,F2,T in H91.H1(I7):
    if(H91.G1-t())<1:
     H91.S=3
    if S>=H91.S or t()>H91.G1 or abs(T)>=J:
     break
   Q(f"bestmove {str(F2)}")
 except(KeyboardInterrupt,SystemExit):
  sys.exit()
 except Exception as exc:
  Q(exc)
  raise

