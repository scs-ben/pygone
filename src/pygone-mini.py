#!/usr/bin/env pypy3
import math,sys,time
import gc
from itertools import chain
from collections import namedtuple
A1={'pe':180,'p':90,'r':500,'n':320,'b':330,'q':900,'k':2e4,'ke':2e4}
A9={'p':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[0,0,0,20,20,0,0,0],[5,-5,-10,0,0,-10,-5,5],[5,10,10,-20,-20,10,10,5],[0,0,0,0,0,0,0,0]],'pe':[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[5,5,10,25,25,10,5,5],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],'n':[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,0,0,0,0,-20,-40],[-30,0,10,15,15,10,0,-30],[-30,5,15,20,20,15,5,-30],[-30,0,15,20,20,15,0,-30],[-30,5,10,15,15,10,5,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]],'b':[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[-10,5,5,10,10,5,5,-10],[-10,0,10,10,10,10,0,-10],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]],'r':[[0,0,0,0,0,0,0,0],[5,10,10,10,10,10,10,5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[0,0,0,5,5,0,0,0]],'q':[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]],'k':[[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-20,-30,-30,-40,-40,-30,-30,-20],[-10,-20,-20,-20,-20,-20,-20,-10],[20,20,-10,-10,-10,-10,20,20],[20,30,10,0,0,10,30,20]],'ke':[[-50,-40,-30,-20,-20,-30,-40,-50],[-30,-20,-10,0,0,-10,-20,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,30,40,40,30,-10,-30],[-30,-10,20,30,30,20,-10,-30],[-30,-30,0,0,0,0,-30,-30],[-50,-30,-30,-30,-30,-30,-30,-50]]}
for S2,_ in A9.items():
 for E24 in range(8):
  for E33 in range(8):
   A9[S2][E24][E33]+=A1[S2]
K5=['P','R','N','B','Q','K']
K6=['p','r','n','b','q','k']
I0=1
Q6=2
Q7=3
Q71=A1['k']-10*A1['q']
Q61=A1['k']+10*A1['q']
def B2(Z6):
 return chr(Z6+96)
def N2(Z5):
 print(Z5,flush=1)
def Q4(L6,L8,P0,L5,Q1,Q2):
 N2("info depth "+L6+" score cp "+L8+" time "+P0+" nodes "+L5+" nps "+Q1+" pv "+Q2)
def S9(C2):
 return(abs((ord(C2[0:1])-96)-1),abs(int(C2[1:2])-8),abs((ord(C2[2:3])-96)-1),abs(int(C2[3:4])-8))
class H9:
 B3=[]
 B4=0
 C1=[]
 S8=[]
 N4=[[],[]]
 P2=[[],[]]
 O7=[1,1]
 O8=[1,1]
 O9='e1'
 O0='e8'
 P9=0
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
  if C9 in('K','k'):
   if C9=='K':
    Z.O9=C2[2:4]
   else:
    Z.O0=C2[2:4]
   if C2 in('e1g1','e8g8'):
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
  Z4.N4=[x[:]for x in Z.N4]
  Z4.P2=[x[:]for x in Z.P2]
  Z4.C1=Z.C1.copy()
  Z4.S8=Z.S8.copy()
  Z4.O7=Z.O7.copy()
  Z4.O8=Z.O8.copy()
  Z4.O9=Z.O9
  Z4.O0=Z.O0
  Z4.R7=Z.R7
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
  Z4.S8.append(Z4.M6())
  Z4.P9=-Z4.P9
  return Z4
 def S0(Z):
  Z4=H9()
  Z4.B4=Z.B4+1
  Z4.B3=[x[:]for x in Z.B3]
  Z4.N4=[x[:]for x in Z.N4]
  Z4.P2=[x[:]for x in Z.P2]
  Z4.C1=Z.C1.copy()
  Z4.S8=Z.S8.copy()
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
  C9=Z.B3[C6][C5]
  from_score_Z1=C9.lower()
  if Z.get_R2()<=16 and C9.lower()=='k':
   from_score_Z1='ke'
  if Z.get_R2()<=16 and C9.lower()=='p':
   from_score_Z1='pe'
  C0=Z.B3[C8][C7]
  H2=A9[from_score_Z1][abs(C8-Q5)][C7]-A9[from_score_Z1][abs(C6-Q5)][C5]
  if C0!='-':
   H2+=A9[C0.lower()][abs(C8-Q5)][C7]
  if C9 in('K','k'):
   if abs(C6-C8)==2:
    if C2[2]=='g':
     H2+=A9['r'][abs(C8-Q5)][C7-1]-A9['r'][abs(C8-Q5)][C7+1]
    else:
     H2+=A9['r'][abs(C8-Q5)][C7+1]-A9['r'][abs(C8-Q5)][C7-2]
  elif C9 in('P','p')and C2[2:4]==Z.R7:
   H2+=A9[from_score_Z1][abs(C8-Q5)][abs(C7-Q5)]
  if len(C2)>4:
   H2+=A9['q'][abs(C8-Q5)][C7]-A9['p'][abs(C8-Q5)][C7]
  return H2
 def R5(Z):
  E7=Z.B4%2==0
  Z1='P' if E7 else 'p'
  H2=0
  for E3 in range(8):
   E34=0
   for E2 in range(8):
    if Z.B3[E2][E3]==Z1:
     E34+=1
   if E34>1:
    H2-=(E34-1)*5
  return H2
 def M6(Z,T8=1):
  return ''.join(list(chain.from_iterable(Z.B3)))+str(Z.B4%2==0)
 def D8(Z,R7=0):
  E7=Z.B4%2==0
  if R7:
   E7=not E7
  N4=[]
  P2=[]
  R8=['p','r','n','b','q','k','-']
  if not E7:
   R8=['P','R','N','B','Q','K','-']
  E1=Z.B3
  for E2 in range(8):
   for E3 in range(8):
    Z1=E1[E2][E3]
    if Z1=="-" or(E7 and Z1 in K6)or(not E7 and Z1 in K5):
     continue
    K7=B2(E3+1)+str(abs(E2-8))
    if Z1.lower()=='k':
     E8={1:{'E3':(E3+0),'E2':(E2+1)},2:{'E3':(E3+0),'E2':(E2-1)},3:{'E3':(E3+1),'E2':(E2+0)},4:{'E3':(E3-1),'E2':(E2+0)},5:{'E3':(E3+1),'E2':(E2+1)},6:{'E3':(E3+1),'E2':(E2-1)},7:{'E3':(E3-1),'E2':(E2+1)},8:{'E3':(E3-1),'E2':(E2-1)},}
     if E7:
      if Z.O7[1]and K7=='e1' and ''.join(E1[7][5:8])=='--R' and not any(Z6 in Z.P2[1]for Z6 in['e1','f1','g1']):
       N4.append(K7+'g1')
      if Z.O7[0]and K7=='e1' and ''.join(E1[7][0:4])=='R---' and not any(Z6 in Z.P2[1]for Z6 in['e1','d1','c1']):
       N4.append(K7+'c1')
     else:
      if Z.O8[1]and K7=='e8' and ''.join(E1[0][5:8])=='--r' and not any(Z6 in Z.P2[0]for Z6 in['e8','f8','g8']):
       N4.append(K7+'g8')
      if Z.O8[0]and K7=='e8' and ''.join(E1[0][0:4])=='r---' and not any(Z6 in Z.P2[0]for Z6 in['e8','d8','c8']):
       N4.append(K7+'c8')
     past_N4=Z.N4[E7]
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
     if E7:
      S3=1
      S4=6
      Q5=-1
     else:
      S3=6
      S4=1
      Q5=1
     if E2 in range(1,7)and E2!=S3 and E1[E2+Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+Q5)))
     if E2==S4 and E1[E2+Q5][E3]=='-' and E1[E2+2*Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+2*Q5)))
     if E2==S3 and E1[E2+Q5][E3]=='-':
      N4.append(K7+B2(E3+1)+str(abs(E2-8+Q5))+'q')
     if((E3-1)>=0 and(E2+Q5)in range(8))or((E3+1)<8 and(E2+Q5)in range(8)):
      O3=''
      if E2==S3:
       O3='q'
      if(E3-1)>=0:
       F1=B2(E3)+str(abs(E2-8+Q5))
       F1_Z1=E1[E2+Q5][E3-1]
       if F1_Z1 in R8:
        if F1_Z1!='-' or F1==Z.R7:
         N4.append(K7+F1+O3)
        P2.append(F1)
      if(E3+1)<8:
       F1=B2(E3+2)+str(abs(E2-8+Q5))
       F1_Z1=E1[E2+Q5][E3+1]
       if F1_Z1 in R8:
        if F1_Z1!='-' or F1==Z.R7:
         N4.append(K7+F1+O3)
        P2.append(F1)
  Z.N4[0 if E7 else 1]=N4
  Z.P2[0 if E7 else 1]=P2
  return N4
 def I9(Z,E7):
  if E7:
   return Z.O9 in Z.P2[1]
  return Z.O0 in Z.P2[0]
R9=9e5
R0=115
T1=15
T2=namedtuple('T2','value depth flag')
class G4:
 L5=0
 L6=0
 G6=0
 M3={}
 tt_Z3={}
 G73=0
 def K3(Z):
  Z.L5=0
  Z.L6=0
  Z.G6=0
  Z.M3.clear()
  Z.tt_Z3.clear()
 def G71(Z,G9):
  I8=time.time()
  last_score=-Q61
  for L6 in range(1,100):
   H3=-Q61
   if L6>5:
    H3=max(H3,last_score)
   score=Z.G7(G9,H3,Q61,L6)
   last_score=max(score,last_score)
   T5=Z.tt_Z3[G9.M6()]
   I6=time.time()-I8
   Q1=math.ceil(Z.L5/I6)
   Q4(str(L6),str(math.ceil(score)),str(math.ceil(I6)),str(Z.L5),str(Q1),str(T5))
   yield L6,T5,score
 def G7(Z,G9,H3,H4,L6,q_count=0,root=1):
  Z.L5+=1
  H31=H3
  is_pv_node=H3!=H4-1
  L6=max(0,L6)
  is_I9=G9.I9(G9.B4%2!=0)
  if not root and G9.S8.count(G9.M6())>2:
   return 0
  if G9.P9<=-Q71:
   return-Q61
  J7=Z.M3.get((G9.M6(),L6,root),T2(-Q61,L6,Q7))
  if J7.flag==I0:
   return J7.value
  if J7.flag==Q7:
   H3=max(H3,J7.value)
  elif J7.flag==Q6:
   H4=min(H4,J7.value)
  if H3>=H4:
   return J7.value
  local_eval=J7.value if J7.value>-Q61 else G9.P9
  if not is_pv_node and not is_I9 and L6<=6 and(local_eval-85*L6>H4):
   return local_eval
  if L6==0:
   return G9.P9
  best_score=-Q61
  played_Z3=0
  current_R2=G9.get_R2()
  H2=-1e8
  if L6>0:
   H2=-Z.G7(G9.S0(),-H4,-H3,L6-3,root=0)
  killer=Z.tt_Z3.get(G9.M6())
  if killer:
   killer_Z4=G9.D4(killer)
   if L6>0 and current_R2==killer_Z4.get_R2():
    H2=max(H2,-Z.G7(killer_Z4,-H4,-H3,L6-1,root=0))
   elif current_R2!=killer_Z4.get_R2():
    H2=max(H2,-Z.G72(killer_Z4,-H4,-H3,8))
  for K7 in sorted(G9.D8(),key=G9.Q9,reverse=1):
   current_move_score=G9.Q9(K7)
   moved_Z4=G9.D4(K7)
   moved_Z4.D8()
   moved_R2=moved_Z4.get_R2()
   if moved_Z4.I9(moved_Z4.B4%2!=0)or current_move_score<=-Q61:
    continue
   played_Z3+=1
   if current_R2!=moved_R2:
    H2=max(H2,-Z.G72(moved_Z4,-H4,-H3,8))
   elif L6>0:
    H2=max(H2,-Z.G7(moved_Z4,-H3-1,-H3,L6-1,root=0))
    if H2>H3:
     H2=max(H2,-Z.G7(moved_Z4,-H4,-H3,L6-1))
   if H2>best_score:
    best_score=H2
    Z.tt_Z3[G9.M6()]=K7
   H3=max(H3,H2)
   if H3>=H4:
    break;
  if L6>0 and played_Z3==0:
   return-Q61 if is_I9 else 0
  if best_score<=H31:
   flag=Q6
  elif best_score>=H4:
   flag=Q7
  else:
   flag=I0
  Z.M3[G9.M6(),L6,root]=T2(best_score,L6,flag)
  return best_score
 def G72(Z,G9,H3,H4,L6):
  Z.L5+=1
  if L6<=0:
   return G9.P9
  if G9.P9<=-Q71:
   return-Q61
  if G9.P9>=H4:
   return H4
  H3=max(G9.P9,H3)
  current_R2=G9.get_R2()
  H2=-1e8
  for K7 in G9.D8():
   moved_Z4=G9.D4(K7)
   moved_R2=moved_Z4.get_R2()
   if moved_R2==current_R2:
    continue
   H2=-Z.G72(G9.D4(K7),-H4,-H3,L6-1)
   if H2>=H4:
    return H4
   H3=max(H2,H3)
  return H3
def main():
 H8=H9()
 G7er=G4()
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
    H8.D8(1)
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
     I7=(I2/20000)
    if H8.B4<13:
     I7+=10
    I7=max(I7,3)
    if I7<=4:
     G7.L6=3
    G7er.G6=time.time()+I7-2
    G7er.L5=0
    K7=None
    start=time.time()
    for _depth,K7,score in G7er.G71(H8):
     if _depth>=G7er.L6 or time.time()>G7er.G6:
      break
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

