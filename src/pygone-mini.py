#!/usr/bin/env pypy3
import math,sys,time
from itertools import chain
A1={'p':100,'r':480,'n':280,'b':320,'q':960,'k':6e4}
A9={'p':[[0]*8,[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0]*8],'n':[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]],'b':[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]],'r':[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]],'q':[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]],'k':[[4,54,47,-99,-99,60,83,-62],[-32,10,45,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[22,30,-3,-14,6,-1,40,26]]}
for S2,_ in A9.items():
 for E24 in range(8):
  for E33 in range(8):
   A9[S2][E24][E33]+=A1[S2]
K5=['P','R','N','B','Q','K']
K6=['p','r','n','b','q','k']
I0=1
Q6=2
Q7=3
MATE_Q7=A1['k']-10*A1['q']
MATE_Q6=A1['k']+10*A1['q']
def B1(Z5):
 return abs((ord(Z5)-96)-1)
def B2(number):
 return chr(number+96)
def N2(Z5):
 print(Z5,flush=1)
def N3():
 return time.perf_counter()
def Q4(L6,L8,P0,L5,Q1,Q2):
 N2("info depth "+L6+" score cp "+L8+" time "+P0+" nodes "+L5+" nps "+Q1+" pv "+Q2)
class H9:
 B3=[]
 B4=0
 C1=[]
 N4=[[],[]]
 Q8=[]
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
  C5=B1(C2[0:1])
  C6=abs(int(C2[1:2])-8)
  C7=B1(C2[2:3])
  C8=abs(int(C2[3:4])-8)
  C9=Z.B3[C6][C5]
  C0=Z.B3[C8][C7]
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
 def D4(Z,C2,Q0=0):
  Z4=H9()
  Z4.B4=Z.B4
  Z4.B3=[x[:]for x in Z.B3]
  Z4.N4=[x[:]for x in Z.N4]
  Z4.Q8=Z.Q8.copy()
  Z4.P2=[x[:]for x in Z.P2]
  Z4.C1=Z.C1.copy()
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
  if Q0:
   Z4.D8()
  Z4.P9=-Z4.P9
  return Z4
 def Q9(Z,C2):
  Q5=0 if Z.B4%2==0 else 7
  C5=B1(C2[0:1])
  C6=abs(int(C2[1:2])-8)
  C7=B1(C2[2:3])
  C8=abs(int(C2[3:4])-8)
  C9=Z.B3[C6][C5]
  C0=Z.B3[C8][C7]
  H2=A9[C9.lower()][abs(C8-Q5)][abs(C7-Q5)]-A9[C9.lower()][abs(C6-Q5)][abs(C5-Q5)]
  if C0!='-':
   H2+=A9[C0.lower()][abs(C8-Q5)][abs(C7-Q5)]
  if(C9 in('K','k')and C2 in('e1g1','e1c1','e8g8','e8c8')):
   if C2[2]=='g':
    H2+=A9['r'][abs(C8-Q5)][abs(C7-1-Q5)]-A9['r'][abs(C8-Q5)][abs(C7+1-Q5)]
   else:
    H2+=A9['r'][abs(C8-Q5)][abs(C7+1-Q5)]-A9['r'][abs(C8-Q5)][abs(C7-2-Q5)]
  elif C9 in('P','p')and C2[2:4]==Z.R7:
   H2+=A9[C9.lower()][abs(C8-Q5)][abs(C7-Q5)]
  if len(C2)>4:
   H2+=A9['q'][abs(C8-Q5)][abs(C7-Q5)]-A9['p'][abs(C8-Q5)][abs(C7-Q5)]
  return H2
 def M6(Z):
  return hash(''.join(list(chain.from_iterable(Z.B3)))+str(Z.B4%2==0))
 def D8(Z,P6=0):
  E7=Z.B4%2==0
  if P6:
   E7=not E7
  N4=[]
  Q8=[]
  P2=[]
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
     for _,E81 in E8.items():
      if E81['E3']in range(8)and E81['E2']in range(8):
       E9=E1[E81['E2']][E81['E3']]
       if E7:
        E0=(E9!='-' and E9.islower())
       else:
        E0=(E9!='-' and E9.isupper())
       F1=B2(E81['E3']+1)+str(abs(E81['E2']-8))
       if E9=='-' or E0:
        N4.append(K7+F1)
       if E0:
        Q8.append(K7+F1)
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
       E0=(E7 and E9 in K6)or(not E7 and E9 in K5)
       if E9=='-' or E0:
        F1=B2(E31+1)+str(abs(E21-8))
        N4.append(K7+F1)
        P2.append(F1)
        if E0:
         Q8.append(K7+F1)
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
       if E7:
        E0=(E9!='-' and E9.islower())
       else:
        E0=(E9!='-' and E9.isupper())
       if E9=='-' or E0:
        F1=B2(F4['E3']+1)+str(abs(F4['E2']-8))
        N4.append(K7+F1)
        if E0:
         Q8.append(K7+F1)
        P2.append(F1)
    if Z1.lower()=='p':
     if E7:
      S3=1
      S4=6
      Q5=-1
      S6=K6
     else:
      S3=6
      S4=1
      Q5=1
      S6=K5
     if E2 in range(1,7)and E1[E2+Q5][E3]=='-':
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
       if F1_Z1=='-' or F1_Z1 in S6 or F1==Z.R7:
        if F1_Z1!='-':
         N4.append(K7+F1+O3)
         Q8.append(K7+F1+O3)
        P2.append(F1)
      if(E3+1)<8:
       F1=B2(E3+2)+str(abs(E2-8+Q5))
       F1_Z1=E1[E2+Q5][E3+1]
       if F1_Z1=='-' or F1_Z1 in S6 or F1==Z.R7:
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
class G4:
 L5=0
 M2=0
 L6=0
 G6=0
 M3={}
 def K3(Z):
  Z.L5=0
  Z.M2=0
  Z.M3={}
 def G71(Z,G9,L6):
  I8=N3()
  H3=-1e8
  H4=1e8
  J3=-1e8
  J4=None
  Z.L6=0
  while L6>0:
   Z.L6+=1
   L6-=1
   (J3,J4)=Z.G7(G9,Z.L6,H3,H4)
   I6=math.ceil(N3()-I8)
   Q1=math.ceil(Z.L5/I6)
   Q4(str(Z.L6),str(math.ceil(J3)),str(I6),str(Z.L5),str(Q1),J4)
  return[J3,J4]
 def G7(Z,G9,L6,H3,H4):
  G0=-1e8
  F41=None
  H2=-1e8
  L6=max(L6,1)
  S1=N3()+5
  for K7 in sorted(G9.D8(),key=G9.Q9,reverse=1):
   Z.L5+=1
   R3=G9.D4(K7,1)
   if R3.I9(G9.B4%2==0):
    continue
   H2=-Z.pvs(R3,-H4,-H3,L6-1)
   if H2>=G0:
    G0=H2
    F41=K7
   if N3()>S1:
    N2("info nodes "+str(Z.L5))
    S1=N3()+5
  return[G0,F41]
 def pvs(Z,G9,H3,H4,L6):
  if L6<1:
   if G9.C1[-1]in G9.Q8[-1]+G9.Q8[-2]:
    return Z.G72(G9,H3,H4,8)
   else:
    return G9.P9
  if G9.P9<=-MATE_Q7:
   return-MATE_Q6
  H31=H3
  J7=Z.M4(G9)
  if J7['M8']>=L6:
   if J7['M0']==I0:
    Z.L5+=1
    return J7['M9']
   if J7['M0']==Q7:
    H3=max(H3,J7['M9'])
   elif J7['M0']==Q6:
    H4=min(H4,J7['M9'])
   if H3>=H4:
    Z.L5+=1
    return J7['M9']
  H2=-1e8
  for K7 in sorted(G9.D8(),key=G9.Q9,reverse=1):
   Z.L5+=1
   R3=G9.D4(K7)
   H2=-Z.pvs(R3,-H3-1,-H3,L6-1)
   if H3<H2<H4:
    H2=-Z.pvs(R3,-H4,-H2,L6-1)
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
  G9.D8()
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
def main():
 G7er=G4()
 H8=H9()
 while 1:
  try:
   Z2=input()
   if Z2=="quit":
    sys.exit()
   elif Z2=="uci":
    N2("pygone 1.1\nuciok")
   elif Z2=="ucinewgame":
    H8=H9()
    G7er.K3()
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
    I4=7
    P8=0
    I5=Z2.split()
    for key,arg in enumerate(I5):
     if arg=='wtime':
      I2=int(I5[key+1])
     elif arg=='btime':
      I3=int(I5[key+1])
    K4=max(40-H8.B4,2)
    I7=1e8
    E7=H8.B4%2==0
    if E7:
     I7=(I2/(K4*1e3))
    else:
     I7=(I3/(K4*1e3))
    G7er.G6=N3()+I7
    if I7<40:
     I4=6
    if I7<20:
     I4=5
    if I7<15:
     I4=4
    if I7<4:
     I4=2
    G7er.L5=0
    G7er.M2=0
    (_,K7)=G7er.G71(H8,I4)
    N2("bestmove "+K7)
  except(KeyboardInterrupt,SystemExit):
   N2('quit')
   sys.exit()
  except Exception as exc:
   N2(exc)
   raise
main()

