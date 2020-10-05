#!/usr/bin/env pypy3
import math,sys,time
<<<<<<< HEAD
from itertools import chain
A1={'p':100,'r':480,'n':280,'b':320,'q':960,'k':6e4}
A9={'p':(0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0),'n':(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69),'b':(-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10),'r':(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32),'q':(6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42),'k':(4,54,47,-99,-99,60,83,-62,-32,10,45,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-55,-43,-52,-28,-51,-47,-8,-50,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,22,30,-3,-14,6,-1,40,2)}
for set_Z1,set_table in A9.items():
 padE2=lambda E2:(0,)+tuple(x+A1[set_Z1]for x in E2)+(0,)
 A9[set_Z1]=sum((padE2(set_table[i*8:i*8+8])for i in range(8)),())
 A9[set_Z1]=(0,)*20+A9[set_Z1]+(0,)*20
=======
import gc
from itertools import chain
from collections import namedtuple
A1={'pe':100,'p':90,'r':500,'n':320,'b':330,'q':900,'k':2e4,'ke':2e4}
A9={'p':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[0,0,0,20,20,0,0,0],[5,-5,-10,0,0,-10,-5,5],[5,10,10,-20,-20,10,10,5],[0,0,0,0,0,0,0,0]],'pe':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],'n':[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,0,0,0,0,-20,-40],[-30,0,10,15,15,10,0,-30],[-30,5,15,20,20,15,5,-30],[-30,0,15,20,20,15,0,-30],[-30,5,10,15,15,10,5,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]],'b':[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[-10,5,5,10,10,5,5,-10],[-10,0,10,10,10,10,0,-10],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]],'r':[[0,0,0,0,0,0,0,0],[5,10,10,10,10,10,10,5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[0,0,0,5,5,0,0,0]],'q':[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]],'k':[[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-20,-30,-30,-40,-40,-30,-30,-20],[-10,-20,-20,-20,-20,-20,-20,-10],[20,20,-10,-10,-10,-10,20,20],[20,30,10,0,0,10,30,20]],'ke':[[-50,-40,-30,-20,-20,-30,-40,-50],[-30,-20,-10,0,0,-10,-20,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-30,0,0,0,0,-30,-30],[-50,-30,-30,-30,-30,-30,-30,-50]]}
for S2,_ in A9.items():
 for E24 in range(8):
  for E33 in range(8):
   A9[S2][E24][E33]+=A1[S2]
>>>>>>> master
K5=['P','R','N','B','Q','K']
K6=['p','r','n','b','q','k']
I0=1
Q6=2
Q7=3
<<<<<<< HEAD
MATE_Q7=A1['k']-10*A1['q']
MATE_Q6=A1['k']+10*A1['q']
def B1(letter):
 return abs((ord(letter)-96)-1)
def B2(number):
 return chr(number+96)
def N2(letter):
 print(letter,flush=1)
def N3():
 return time.perf_counter()
=======
Q71=A1['k']-10*A1['q']
Q61=A1['k']+10*A1['q']
def B2(Z6):
 return chr(Z6+96)
def N2(Z5):
 print(Z5,flush=1)
>>>>>>> master
def Q4(L6,L8,P0,L5,Q1,Q2):
 N2("info depth "+L6+" score cp "+L8+" time "+P0+" nodes "+L5+" nps "+Q1+" pv "+Q2)
def S9(C2):
 return(abs((ord(C2[0:1])-96)-1),abs(int(C2[1:2])-8),abs((ord(C2[2:3])-96)-1),abs(int(C2[3:4])-8))
class H9:
 B3=''
 B4=0
 C1=[]
<<<<<<< HEAD
 N4=[[],[]]
 Q8=[]
=======
 S8=[]
 N4=[]
>>>>>>> master
 P2=[[],[]]
 O7=[1,1]
 O8=[1,1]
 O9='e1'
 O0='e8'
 P9=0
<<<<<<< HEAD
 en_passant=''
 def __init__(Z):
  Z.B3=('          ' '          ' ' rnbqkbnr ' ' pppppppp ' ' -------- ' ' -------- ' ' -------- ' ' -------- ' ' PPPPPPPP ' ' RNBQKBNR ' '          ' '          ')
 def B32(Z,B3):
  Z.B3=B3
 def D1(Z,C2):
  put=lambda Z4,i,p:Z4[:i]+p+Z4[i+1:]
  C6=Z.from_coordinate(C2[0:2])
  C8=Z.from_coordinate(C2[2:4])
  C9=Z.B3[C6]
  E7=Z.B4%2==0
  Z.B3=put(Z.B3,C8,C9)
  Z.B3=put(Z.B3,C6,'-')
  set_en_passant=0
  if C9 in('P','p'):
   set_en_passant=abs(C6-C8)==2
   en_passant_Q5=-1 if E7 else 1
   if set_en_passant:
    Z.en_passant=C2[0:1]+str(int(C2[3:4])+en_passant_Q5)
   elif C2[2:4]==Z.en_passant:
    Z.B3=put(Z.B3,C8-en_passant_Q5,'-')
  if not set_en_passant:
   Z.en_passant=''
=======
 R7=''
 def __init__(Z):
  Z.B3=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def B32(Z,B3):
  Z.B3=B3
 def D1(Z,C2):
  (C5,C6,C7,C8)=S9(C2)
  C9=Z.B3[C6][C5]
  E7=Z.B4%2==0
  Z.B3[C8][C7]=C9
  Z.B3[C6][C5]='-'
  R6=0
  if C9 in('P','p'):
   R6=abs(C6-C8)==2
   Q51=-1 if E7 else 1
   if R6:
    Z.R7=C2[0:1]+str(int(C2[3:4])+Q51)
   elif C2[2:4]==Z.R7:
    Z.B3[C8-Q51][C7]='-'
  if not R6:
   Z.R7=''
>>>>>>> master
  if C9 in('K','k'):
   if C9=='K':
    Z.O9=C2[2:4]
   else:
    Z.O0=C2[2:4]
   if C2 in('e1g1','e8g8'):
<<<<<<< HEAD
    Z.B3=put(Z.B3,C8+1,'-')
    Z.B3=put(Z.B3,C6+1,'R' if C9=='K' else 'r')
   elif C2 in('e1c1','e8c8'):
    Z.B3=put(Z.B3,C8-2,'-')
    Z.B3=put(Z.B3,C6-1,'R' if C9=='K' else 'r')
  elif len(C2)>4:
   Z.B3=put(Z.B3,C8,C2[4:5].upper()if E7 else C2[4:5])
 def D4(Z,C2,Q0=0):
  Z4=H9()
  Z4.B4=Z.B4
  Z4.B3=Z.B3
  Z4.N4=[x[:]for x in Z.N4]
  Z4.Q8=Z.Q8.copy()
=======
    Z.B3[C8][C7+1]='-'
    Z.B3[C6][C5+1]='R' if C9=='K' else 'r'
   elif C2 in('e1c1','e8c8'):
    Z.B3[C8][C7-2]='-'
    Z.B3[C6][C5-1]='R' if C9=='K' else 'r'
  elif len(C2)>4:
   Z.B3[C8][C7]=C2[4:5].upper()if E7 else C2[4:5]
 def D4(Z,C2):
  Z4=H9()
  Z4.B4=Z.B4
  Z4.B3=[x[:]for x in Z.B3]
  Z4.N4=Z.N4.copy()
>>>>>>> master
  Z4.P2=[x[:]for x in Z.P2]
  Z4.C1=Z.C1.copy()
  Z4.S8=Z.S8.copy()
  Z4.O7=Z.O7.copy()
  Z4.O8=Z.O8.copy()
  Z4.O9=Z.O9
  Z4.O0=Z.O0
<<<<<<< HEAD
  Z4.en_passant=Z.en_passant
=======
  Z4.R7=Z.R7
>>>>>>> master
  Z4.P9=Z.P9+Z.Q9(C2)
  if 'e1' in C2:
   Z4.O7=[0,0]
  if 'a1' in C2:
   Z4.O7[0]=0
  if 'h1' in C2:
   Z4.O7[1]=0
  if 'e8' in C2:
   Z4.O8=[0,0]
  if 'a8' in C2:
   Z4.O8[0]=0
  if 'h8' in C2:
   Z4.O8[1]=0
  Z4.D1(C2)
  Z4.C1.append(C2)
  Z4.B4+=1
<<<<<<< HEAD
  Z4.D8()
  Z4.P9=-Z4.P9
  return Z4
 def nullmove(Z):
  Z4=H9()
  Z4.B4=Z.B4+1
  Z4.C1=Z.C1.copy()
  Z4.B3=Z.B3
  Z4.O7=Z.O7.copy()
  Z4.O8=Z.O8.copy()
  Z4.P9=-Z.P9
  Z4.D8()
  return Z4
 def Q9(Z,C2):
  C6=Z.from_coordinate(C2[0:2])
  C8=Z.from_coordinate(C2[2:4])
  Q5=0 if Z.B4%2==0 else 120
  C9=Z.B3[C6]
  C0=Z.B3[C8]
  H2=A9[C9.lower()][abs(Q5-C8)]-A9[C9.lower()][abs(Q5-C6)]
  if C0!='-':
   H2+=A9[C0.lower()][abs(Q5-C8)]
  if(C9 in('K','k')and C2 in('e1g1','e1c1','e8g8','e8c8')):
   if C2[2]=='g':
    H2+=A9['r'][abs(Q5-C8-1)]-A9['r'][abs(Q5-C8+1)]
   else:
    H2+=A9['r'][abs(Q5-C8+1)]-A9['r'][abs(Q5-C8-2)]
  elif C9 in('P','p')and C2[2:4]==Z.en_passant:
   H2+=A9[C9.lower()][abs(Q5-C8)]
  if len(C2)>4:
   H2+=A9['q'][abs(Q5-C8)]-A9['p'][abs(Q5-C8)]
  return H2
 def D7(Z):
  for E2 in Z.B3.split():
   print(E2)
 def M6(Z):
  return hash(''.join(list(chain.from_iterable(Z.B3)))+str(Z.B4%2==0))
 def get_coordinate(Z,Z4_position):
  Z4_position=abs(119-Z4_position)
  E2=math.floor(Z4_position/10)-1
  E3=abs(10-Z4_position%10)-1
  return B2(E3)+str(E2)
 def from_coordinate(Z,coordinate):
  E3,E2=ord(coordinate[0])-ord('a'),int(coordinate[1])-1
  return 91+E3-10*E2
 def D8(Z,P6=0):
=======
  Z4.S8.append(Z4.M6())
  Z4.P9=-Z4.P9
  return Z4
 def S0(Z):
  Z4=H9()
  Z4.B4=Z.B4+1
  Z4.B3=[x[:]for x in Z.B3]
  Z4.O7=Z.O7.copy()
  Z4.O8=Z.O8.copy()
  Z4.O9=''
  Z4.O0=''
  Z4.R7=''
  Z4.P9=-Z.P9
  return Z4
 def get_R2(Z):
  return 64-(Z.M6()).count('-')
 def Q9(Z,C2):
  E7=Z.B4%2==0
  Q5=0 if E7 else 7
  (C5,C6,C7,C8)=S9(C2)
  H2=0
  C9=Z.B3[C6][C5]
  from_score_Z1=C9.lower()
  if Z.get_R2()<=14:
   if C9.lower()=='k':
    H2+=2
    from_score_Z1='ke'
   if C9.lower()=='p':
    H2+=2
    from_score_Z1='pe'
  C0=Z.B3[C8][C7]
  H2+=A9[from_score_Z1][abs(C8-Q5)][C7]-A9[from_score_Z1][abs(C6-Q5)][C5]
  if C0!='-':
   H2+=A9[C0.lower()][abs(C8-Q5)][C7]
  if C9 in('K','k'):
   if abs(C6-C8)==2:
    if C2[2]=='g':
     H2+=A9['r'][abs(C8-Q5)][C7-1]-A9['r'][abs(C8-Q5)][C7+1]
    else:
     H2+=A9['r'][abs(C8-Q5)][C7+1]-A9['r'][abs(C8-Q5)][C7-2]
  elif C9 in('P','p'):
   p_Q5=-1 if E7 else 1
   p_Z1='P' if E7 else 'p'
   protected_pawns=0
   if C8>0 and C8<7:
    if C7>0:
     protected_pawns+=Z.B3[C8+p_Q5][C7-1]==p_Z1
    if C7<7:
     protected_pawns+=Z.B3[C8+p_Q5][C7+1]==p_Z1
   if protected_pawns>0:
    H2+=10
   if C2[2:4]==Z.R7:
    H2+=A9[from_score_Z1][abs(C8-Q5)][C7]
  if len(C2)>4:
   H2+=A9['q'][abs(C8-Q5)][C7]-A9['p'][abs(C8-Q5)][C7]
  return H2
 def M6(Z):
  return ''.join(list(chain.from_iterable(Z.B3)))+str(Z.B4%2==0)
 def generate_N4(Z,reverse=0):
>>>>>>> master
  E7=Z.B4%2==0
  if reverse:
   E7=not E7
  N4=[]
<<<<<<< HEAD
  Q8=[]
  P2=[]
  E1=Z.B3
  for E2,Z1 in enumerate(E1):
   if Z1.isspace()or Z1=="-" or(E7 and Z1 in K6)or(not E7 and Z1 in K5):
    continue
   K7=Z.get_coordinate(E2)
   if Z1.lower()in('b','r','q','k'):
    F7={1:-10,2:+10,3:-1,4:+1,5:-11,6:+11,7:-9,8:+9,}
    for key,F8 in F7.items():
     if(key<=4 and Z1.lower()=='b')or(key>=5 and Z1.lower()=='r'):
      continue
     E21=E2+F8
     while E21>=21 and E21<99:
      E9=E1[E21]
      E0=(E7 and E9 in K6)or(not E7 and E9 in K5)
      if Z1.lower()=='k':
       if E7:
        if Z.O7[1]and K7=='e1' and E1[96:99]=='--R' and not any(coordinate in Z.P2[1]for coordinate in['e1','f1','g1']):
         N4.append(K7+'g1')
        if Z.O7[0]and K7=='e1' and E1[91:95]=='R---' and not any(coordinate in Z.P2[1]for coordinate in['e1','d1','c1']):
         N4.append(K7+'c1')
       else:
        if Z.O8[1]and K7=='e8' and E1[26:29]=='--r' and not any(coordinate in Z.P2[0]for coordinate in['e8','f8','g8']):
         N4.append(K7+'g8')
        if Z.O8[0]and K7=='e8' and E1[21:25]=='r---' and not any(coordinate in Z.P2[0]for coordinate in['e8','d8','c8']):
         N4.append(K7+'c8')
      if E9=='-' or E0:
       F1=Z.get_coordinate(E21)
       N4.append(K7+F1)
       P2.append(F1)
       if E0:
        Q8.append(K7+F1)
        break
      else:
       break
      if Z1.lower()=='k':
       break
      E21+=F8
   if Z1.lower()=='n':
    F3={1:E2-21,2:E2-19,3:E2-12,4:E2-8,5:E2+8,6:E2+12,7:E2+19,8:E2+21,}
    for _,F4 in F3.items():
     if F4>=21 and F4<99:
      E9=E1[F4]
      if E7:
       E0=(E9!='-' and E9.islower())
      else:
       E0=(E9!='-' and E9.isupper())
      if E9=='-' or E0:
       F1=Z.get_coordinate(F4)
       N4.append(K7+F1)
       if E0:
        Q8.append(K7+F1)
       P2.append(F1)
   if Z1.lower()=='p':
    if E7:
     N9=81
     N0=31
     Q5=-10
     Z1_set=K6
    else:
     N9=31
     N0=81
     Q5=10
     Z1_set=K5
    O3=''
    if E2 in range(N0,N0+10):
     O3='q'
    if E1[E2+Q5]=='-':
     N4.append(K7+Z.get_coordinate(E2+Q5)+O3)
     if E2 in range(N9,N9+10)and E1[E2+2*Q5]=='-':
      N4.append(K7+Z.get_coordinate(E2+2*Q5))
    if E1[E2+Q5+1]=='-':
     F1=Z.get_coordinate(E2+Q5+1)
     F1_Z1=E1[E2+Q5+1]
     if F1_Z1=='-' or F1_Z1 in Z1_set or F1==Z.en_passant:
      if F1_Z1!='-':
       N4.append(K7+F1+O3)
       Q8.append(K7+F1+O3)
      P2.append(F1)
    if E1[E2+Q5-1]=='-':
     F1=Z.get_coordinate(E2+Q5-1)
     F1_Z1=E1[E2+Q5-1]
     if F1_Z1=='-' or F1_Z1 in Z1_set or F1==Z.en_passant:
      if F1_Z1!='-':
       N4.append(K7+F1+O3)
       Q8.append(K7+F1+O3)
      P2.append(F1)
  Z.Q8.append(Q8)
  Z.N4[0 if E7 else 1]=N4
  Z.P2[0 if E7 else 1]=P2
  return N4
 def I9(Z,E7):
  if E7:
   return Z.O9 in Z.P2[1]
  return Z.O0 in Z.P2[0]
=======
  P2=[]
  R8=['p','r','n','b','q','k','-']
  if not E7:
   R8=['P','R','N','B','Q','K','-']
  E1=Z.B3
  for E2 in range(8):
   for E3 in range(8):
    Z1=E1[E2][E3]
    if Z1=="-" or(E7 and Z1.islower())or(not E7 and Z1.isupper()):
     continue
    K7=B2(E3+1)+str(abs(E2-8))
    if Z1.lower()=='k':
     E8={1:{'E3':(E3+0),'E2':(E2+1)},2:{'E3':(E3+0),'E2':(E2-1)},3:{'E3':(E3+1),'E2':(E2+0)},4:{'E3':(E3-1),'E2':(E2+0)},5:{'E3':(E3+1),'E2':(E2+1)},6:{'E3':(E3+1),'E2':(E2-1)},7:{'E3':(E3-1),'E2':(E2+1)},8:{'E3':(E3-1),'E2':(E2-1)},}
     if E7:
      if Z.O7[1]and K7=='e1' and ''.join(E1[7][5:8])=='--R' and not any(Z6 in Z.P2[0]for Z6 in['e1','f1','g1']):
       N4.append(K7+'g1')
      if Z.O7[0]and K7=='e1' and ''.join(E1[7][0:4])=='R---' and not any(Z6 in Z.P2[0]for Z6 in['e1','d1','c1']):
       N4.append(K7+'c1')
     else:
      if Z.O8[1]and K7=='e8' and ''.join(E1[0][5:8])=='--r' and not any(Z6 in Z.P2[1]for Z6 in['e8','f8','g8']):
       N4.append(K7+'g8')
      if Z.O8[0]and K7=='e8' and ''.join(E1[0][0:4])=='r---' and not any(Z6 in Z.P2[1]for Z6 in['e8','d8','c8']):
       N4.append(K7+'c8')
     for _,E81 in E8.items():
      if E81['E3']in range(8)and E81['E2']in range(8):
       E9=E1[E81['E2']][E81['E3']]
       F1=B2(E81['E3']+1)+str(abs(E81['E2']-8))
       if E9 in R8:
        N4.append(K7+F1)
       P2.append(F1)
    if Z1.lower()in('b','r','q'):
     F7={1:{'E3':E3,'E2':(E2-1),'E32':0,'E23':-1},2:{'E3':E3,'E2':(E2+1),'E32':0,'E23':1},3:{'E3':(E3-1),'E2':E2,'E32':-1,'E23':0},4:{'E3':(E3+1),'E2':E2,'E32':1,'E23':0},5:{'E3':(E3-1),'E2':(E2-1),'E32':-1,'E23':-1},6:{'E3':(E3+1),'E2':(E2+1),'E32':1,'E23':1},7:{'E3':(E3-1),'E2':(E2+1),'E32':-1,'E23':1},8:{'E3':(E3+1),'E2':(E2-1),'E32':1,'E23':-1},}
     for key,F8 in F7.items():
      if(key<=4 and Z1.lower()=='b')or(key>=5 and Z1.lower()=='r'):
       continue
      E21=F8['E2']
      E31=F8['E3']
      while E21 in range(8)and E31 in range(8):
       E9=E1[E21][E31]
       if E9 in R8:
        F1=B2(E31+1)+str(abs(E21-8))
        N4.append(K7+F1)
        P2.append(F1)
        if E9!='-':
         break
       else:
        break
       E21+=F8['E23']
       E31+=F8['E32']
    if Z1.lower()=='n':
     F3={1:{'E3':(E3+1),'E2':(E2-2)},2:{'E3':(E3-1),'E2':(E2-2)},3:{'E3':(E3+2),'E2':(E2-1)},4:{'E3':(E3-2),'E2':(E2-1)},5:{'E3':(E3+1),'E2':(E2+2)},6:{'E3':(E3-1),'E2':(E2+2)},7:{'E3':(E3+2),'E2':(E2+1)},8:{'E3':(E3-2),'E2':(E2+1)}}
     for _,F4 in F3.items():
      if F4['E3']in range(8)and F4['E2']in range(8):
       E9=E1[F4['E2']][F4['E3']]
       if E9 in R8:
        F1=B2(F4['E3']+1)+str(abs(F4['E2']-8))
        N4.append(K7+F1)
        P2.append(F1)
    if Z1.lower()=='p':
     S3=1
     S4=6
     Q5=-1
     if not E7:
      S3=6
      S4=1
      Q5=1
     if E1[E2+Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+Q5)))
     if E2==S4 and E1[E2+Q5][E3]=='-' and E1[E2+2*Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+2*Q5)))
     if E2==S3 and E1[E2+Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+Q5))+'q')
     if E2+Q5 in range(8)and 1<=E3<7:
      O3=''
      if E2==S3:
       O3='q'
      if E3>0:
       F1=B2(E3)+str(abs(E2-8+Q5))
       F1_Z1=E1[E2+Q5][E3-1]
       if F1_Z1 in R8:
        if F1_Z1!='-' or F1==Z.R7:
         N4.append(K7+F1+O3)
        P2.append(F1)
      if E3<7:
       F1=B2(E3+2)+str(abs(E2-8+Q5))
       F1_Z1=E1[E2+Q5][E3+1]
       if F1_Z1 in R8:
        if F1_Z1!='-' or F1==Z.R7:
         N4.append(K7+F1+O3)
        P2.append(F1)
  Z.N4=N4
  Z.P2[E7]=P2
  return N4
 def I9(Z,E7):
  if E7:
   return Z.O9 in Z.P2[not E7]
  return Z.O0 in Z.P2[not E7]
R9=9e5
T2=namedtuple('T2','lower upper')
>>>>>>> master
class G4:
 L5=0
 L6=0
 G6=0
 M3={}
 tt_Z3={}
 def K3(Z):
  Z.L5=0
<<<<<<< HEAD
  Z.M2=0
  Z.M3={}
 def G71(Z,G9,L6):
  I8=N3()
  H3=-1e8
  H4=1e8
  J3=-1e8
  J4=None
=======
>>>>>>> master
  Z.L6=0
  Z.G6=0
  Z.M3.clear()
  Z.tt_Z3.clear()
 def G71(Z,G9):
  I8=time.time()
  initial_move=Z.tt_Z3.get(G9.M6())
  if initial_move:
   if initial_move in('e1c1','e1g1','e8c8','e8g8')and G9.I9(G9.B4%2==0):
    Z.tt_Z3[G9.M6()]=None
  for L6 in range(1,100):
   lower_Z9=-Q61
   upper_Z9=Q61
   while lower_Z9<upper_Z9-10:
    score_cutoff=(lower_Z9+upper_Z9+1)//2
    H2=Z.G7(G9,score_cutoff,L6)
    if H2>=score_cutoff:
     lower_Z9=H2
    if H2<score_cutoff:
     upper_Z9=H2
   Z.G7(G9,lower_Z9,L6)
   best_move=Z.tt_Z3.get(G9.M6())
   score=Z.M3.get((G9.M6(),L6,1)).lower
   I6=time.time()-I8
   Q1=math.ceil(Z.L5/I6)
<<<<<<< HEAD
   Q4(str(Z.L6),str(math.ceil(J3)),str(I6),str(Z.L5),str(Q1),J4)
  return[J3,J4]
 def G7(Z,G9,L6,H3,H4):
  G0=-1e8
  F41=None
  H2=-1e8
  L6=max(L6,1)
  print_time=N3()+5
  for K7 in sorted(G9.D8(),key=G9.Q9,reverse=1):
   Z.L5+=1
   R3=G9.D4(K7,1)
   if R3.I9(G9.B4%2==0):
    continue
   H2=-Z.pvs(R3,-H4,-H3,L6-1)
   if H2>=G0:
    G0=H2
    F41=K7
   if N3()>print_time:
    N2("info nodes "+str(Z.L5))
    print_time=N3()+5
  return[G0,F41]
 def pvs(Z,G9,H3,H4,L6):
  L6=max(0,L6)
  if L6<1 or G9.P9>(H4+60*L6):
   if G9.C1[-1]in G9.Q8[-1]:
    return Z.G72(G9,H3,H4,8)
   else:
    return G9.P9
  if G9.P9<=-MATE_Q7:
   return-MATE_Q6
  H31=H3
  J7=Z.M4(G9)
  if J7['M8']>=L6:
   if J7['M0']==I0:
    return J7['M9']
   if J7['M0']==Q7:
    H3=max(H3,J7['M9'])
   elif J7['M0']==Q6:
    H4=min(H4,J7['M9'])
   if H3>=H4:
    return J7['M9']
  H2=-1e8
  Z1s='RBNQ' if G9.B4%2==0 else 'rnbq'
  if any(Z1 in G9.B3 for Z1 in Z1s):
   H3=max(H3,-Z.pvs(G9.nullmove(),-H4,-H3,L6-3))
  for K7 in sorted(G9.D8(),key=G9.Q9,reverse=1):
   Z.L5+=1
   H2=-Z.pvs(G9.D4(K7,1),-H3-1,-H3,L6-1)
   if H3<H2<H4:
    H2=-Z.pvs(G9.D4(K7,1),-H4,-H2,L6-1)
   H3=max(H3,H2)
   if H3>=H4:
    break
  J7['M9']=H3
  if H3<=H31:
   J7['M0']=Q6
  elif H3>=H4:
   J7['M0']=Q7
  else:
   J7['M0']=I0
  J7['M8']=L6
  Z.R2(G9,J7)
  return H3
 def G72(Z,G9,H3,H4,L6):
  if L6<=0 or len(G9.Q8[-1])==0:
   return G9.P9
  if G9.P9<=-MATE_Q7:
   return-MATE_Q6
  if G9.P9>=H4:
   return H4
  H3=max(G9.P9,H3)
  H2=-1e8
  for K7 in G9.Q8[-1]:
   Z.L5+=1
   H2=-Z.G72(G9.D4(K7),-H4,-H3,L6-1)
   if H2>=H4:
    return H4
   H3=max(H2,H3)
  return H3
 def M4(Z,G9):
  M5=G9.M6()
  if M5 not in Z.M3:
   Z.M3[M5]={'M8':0,'M9':-1e5,'M0':2}
  return Z.M3[M5]
 def R2(Z,G9,J7):
  M5=G9.M6()
  if len(Z.M3)>1e7:
   Z.M3.clear()
  Z.M3[M5]=J7
=======
   Q4(str(L6),str(math.ceil(score)),str(math.ceil(I6)),str(Z.L5),str(Q1),str(best_move))
   yield L6,best_move,score
 def G7(Z,G9,score_cutoff,L6,parent_G7=1,root=1):
  Z.L5+=1
  L6=max(0,L6)
  if G9.P9<=-Q71:
   return-Q61
  if not root and G9.S8.count(G9.M6())>=2:
   return 0
  J7=Z.M3.get((G9.M6(),L6,root),T2(-Q61,Q61))
  if J7.lower>=score_cutoff and(not root or Z.tt_Z3.get(G9.M6())is not None):
   return J7.lower
  if J7.upper<score_cutoff:
   return J7.upper
  def Z3():
   current_R2=G9.get_R2()
   if L6==0:
    yield None,G9.P9
   killer=Z.tt_Z3.get(G9.M6())
   if killer:
    killer_score=G9.Q9(killer)
    killer_Z4=G9.D4(killer)
    if L6>0 or killer_score>800 or current_R2!=killer_Z4.get_R2():
     yield killer,-Z.G7(killer_Z4,1-score_cutoff,L6-1,root=0)
   for K7 in sorted(G9.generate_N4(),key=G9.Q9,reverse=parent_G7):
    current_move_score=G9.Q9(K7)
    moved_Z4=G9.D4(K7)
    moved_R2=moved_Z4.get_R2()
    if L6>0 or current_move_score>800 or current_R2!=moved_R2:
     yield K7,-Z.G7(moved_Z4,1-score_cutoff,L6-1,root=0)
  best_score=-Q61
  for K7,H2 in Z3():
   best_score=max(best_score,H2)
   if best_score>=score_cutoff:
    if parent_G7:
     Z.tt_Z3[G9.M6()]=K7
    break
  if best_score<score_cutoff and best_score<0 and L6>0:
   is_dead=lambda G9:any(G9.Q9(m)>=Q71 for m in G9.generate_N4())
   if all(is_dead(G9.D4(m))for m in G9.generate_N4()):
    I9=is_dead(G9.S0())
    best_score=-Q61 if I9 else 0
  if best_score>=score_cutoff:
   Z.M3[G9.M6(),L6,root]=T2(best_score,J7.upper)
  if best_score<score_cutoff:
   Z.M3[G9.M6(),L6,root]=T2(J7.lower,best_score)
  return best_score
>>>>>>> master
def main():
 H8=H9()
<<<<<<< HEAD
=======
 G7er=G4()
>>>>>>> master
 while 1:
  try:
   Z2=input()
   if Z2=="quit":
    sys.exit()
   elif Z2=="uci":
    N2("pygone 1.3\nuciok")
   elif Z2=="ucinewgame":
    H8=H9()
    G7er.K3()
    gc.collect()
   elif Z2=="isready":
    N2("readyok")
   elif Z2.startswith("position"):
    Z3=Z2.split()
    H8=H9()
    for F42 in Z3[3:]:
     H8=H8.D4(F42)
    H8.generate_N4()
    H8.generate_N4(1)
   elif Z2.startswith("go"):
    I2=1e8
    I3=1e8
    G7er.L6=30
    I5=Z2.split()
    for key,arg in enumerate(I5):
     if arg=='wtime':
      I2=int(I5[key+1])
     elif arg=='btime':
      I3=int(I5[key+1])
     elif arg=='depth':
      G7er.L6=int(I5[key+1])
    K4=max(40-H8.B4,2)
    I7=1e8
    E7=H8.B4%2==0
    I7=(I3/20000)
    if E7:
<<<<<<< HEAD
     I7=(I2/(K4*1e3))
    else:
     I7=(I3/(K4*1e3))
    G7er.G6=N3()+I7
    I4=max(P8,I4)
    print(I7)
    if I7<30:
     I4=5
    if I7<7:
     I4=4
    if I7<4:
     I4=3
    G7er.L5=0
    G7er.M2=0
    (_,K7)=G7er.G71(H8,I4)
=======
     I7=(I2/20000)
    if H8.B4<13:
     I7+=10
    I7=max(I7,3)
    G7er.G6=time.time()+I7-1
    G7er.L5=0
    K7=None
    start=time.time()
    for _depth,K7,score in G7er.G71(H8):
     if H8.B4>13 and(G7er.G6-time.time())<25:
      G7er.L6=5
     if H8.B4>13 and(G7er.G6-time.time())<4:
      G7er.L6=3
     if _depth>=G7er.L6 or time.time()>G7er.G6:
      break
>>>>>>> master
    N2("bestmove "+K7)
    if len(G7er.tt_Z3)>R9:
     G7er.tt_Z3.clear()
    if len(G7er.M3)>R9:
     G7er.M3.clear()
  except(KeyboardInterrupt,SystemExit):
   N2('quit')
   sys.exit()
  except Exception as exc:
   N2(exc)
   raise
main()

