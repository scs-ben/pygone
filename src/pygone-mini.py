#!/usr/bin/env pypy3
import copy,math,sys,time
A1={'p':100,'r':480,'n':280,'b':320,'q':960,'k':6e4}
A3=[[0]*8,[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0]*8]
A4=[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]]
A5=[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]]
A6=[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]]
A7=[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]]
A8=[[4,54,47,-99,-99,60,83,-62],[-32,10,45,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[22,30,-3,-14,6,-1,40,26]]
A9={'p':A3,'n':A4,'b':A5,'r':A6,'q':A7,'k':A8}
K5=['P','R','N','B','Q','K']
K6=['p','r','n','b','q','k']
def B1(letter):
 return abs((ord(letter)-96)-1)
def B2(number):
 return chr(number+96)
def N2(letter):
 print(letter,flush=True)
def N3():
 return time.perf_counter()
class H9:
 B3=[]
 B4=0
 C1=[]
 D9=[]
 D0=[]
 white_castling=[True,True]
 black_castling=[True,True]
 def K3(Z):
  Z.B31()
  Z.B4=0
  Z.C1=[]
  Z.D9=[]
  Z.D0=[]
  Z.white_castling=[True,True]
  Z.black_castling=[True,True]
 def B31(Z):
  Z.B3=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def B32(Z,state):
  Z.B3=state
 def D1(Z,C2,C3=0,C4=0,C91='',C01=''):
  C5=B1(C2[0:1])
  C6=abs(int(C2[1:2])-8)
  C7=B1(C2[2:3])
  C8=abs(int(C2[3:4])-8)
  C9=Z.B3[C6][C5]
  C0=Z.B3[C8][C7]
  E7=Z.B4%2==0
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
    Z.B3[C8][C7-1]='-'
   else:
    Z.B3[C8][C7+2]='-'
   Z.B3[C6][C5+D2]='R' if C9=='K' else 'r'
   Z.B3[C8][C7]='K' if C9=='K' else 'k'
   Z.B3[C8][C7+D2]='-'
   return[C9,C0]
  D3=""
  if len(C2)>4:
   D3=C2[4:5]
  if(C9 in('P','p')and C0=='-' and C2[0:1]!=C2[2:3]and len(C91)==0 and len(C01)==0):
   Z.B3[C6][C5]='-'
   Z.B3[C8][C7]=C9
   Z.B3[C6][C7]='-'
  elif(C9 in('K','k')and C2 in('e1g1','e1c1','e8g8','e8c8')):
   Z.B3[C6][C5]='-'
   if C2[2]=='g':
    Z.B3[C8][C7+1]='-'
    Z.B3[C6][C5+1]='R' if C9=='K' else 'r'
   else:
    Z.B3[C8][C7-2]='-'
    Z.B3[C6][C5-1]='R' if C9=='K' else 'r'
   Z.B3[C8][C7]=C9
  else:
   if len(C01)==0:
    Z.B3[C6][C5]='-'
   else:
    Z.B3[C6][C5]=C01
   if D3!="":
    if E7:
     Z.B3[C8][C7]=D3.upper()
    else:
     Z.B3[C8][C7]=D3
   else:
    if len(C91)==0:
     Z.B3[C8][C7]=C9
    else:
     Z.B3[C8][C7]=C91
  return[C9,C0]
 def D4(Z,C2):
  board=H9()
  board.B4=Z.B4
  board.B3=[x[:]for x in Z.B3]
  board.D9=Z.D9
  board.D0=Z.D0
  board.C1=Z.C1.copy()
  board.white_castling=Z.white_castling
  board.black_castling=Z.black_castling
  if C2 is not None:
   if 'e1' in C2:
    board.white_castling=[False,False]
   if 'a1' in C2:
    board.white_castling[0]=False
   if 'h1' in C2:
    board.white_castling[1]=False
   if 'e8' in C2:
    board.black_castling=[False,False]
   if 'a8' in C2:
    board.black_castling[0]=False
   if 'h8' in C2:
    board.black_castling[1]=False
   board.D1(C2)
   board.C1.append(C2)
  board.B4+=1
  return board
 def M6(Z):
  N1=''
  for i in range(8):
   for j in range(8):
    N1+=Z.B3[i][j]
  return N1+str(Z.B4%2==0)
 def D8(Z):
  E7=Z.B4%2==0
  yield None
  N4=[]
  N7=[]
  if(E7):
   Z.D9=[]
  else:
   Z.D0=[]
  E1=Z.B3.copy()
  for E2 in range(8):
   for E3 in range(8):
    Z1=E1[E2][E3]
    if Z1=="-" or(E7 and Z1 in K6)or(not E7 and Z1 in K5):
     continue
    K7=B2(E3+1)+str(abs(E2-8))
    if Z1.lower()=='k':
     E8={1:{'E3':(E3+0),'E2':(E2+1)},2:{'E3':(E3+0),'E2':(E2-1)},3:{'E3':(E3+1),'E2':(E2+0)},4:{'E3':(E3-1),'E2':(E2+0)},5:{'E3':(E3+1),'E2':(E2+1)},6:{'E3':(E3+1),'E2':(E2-1)},7:{'E3':(E3-1),'E2':(E2+1)},8:{'E3':(E3-1),'E2':(E2-1)},}
     if E7:
      if Z.white_castling[1]and K7=='e1' and E1[7][5]=='-' and E1[7][6]=='-' and E1[7][7]=='R':
       yield(K7+'g1')
      if Z.white_castling[0]and K7=='e1' and E1[7][1]=='-' and E1[7][2]=='-' and E1[7][3]=='-' and E1[7][0]=='R':
       yield(K7+'c1')
     else:
      if Z.black_castling[0]and K7=='e8' and E1[0][1]=='-' and E1[0][2]=='-' and E1[0][3]=='-' and E1[0][0]=='r':
       yield(K7+'c8')
      if Z.black_castling[1]and K7=='e8' and E1[0][5]=='-' and E1[0][6]=='-' and E1[0][7]=='r':
       yield(K7+'g8')
     for _,E81 in E8.items():
      if E81['E3']in range(8)and E81['E2']in range(8):
       E9=E1[E81['E2']][E81['E3']]
       if E7:
        E0=(E9!='-' and E9.islower())
       else:
        E0=(E9!='-' and E9.isupper())
       F1=B2(E81['E3']+1)+str(abs(E81['E2']-8))
       if E9=='-' or E0:
        yield(K7+F1)
    if Z1.lower()=='p':
     if E7:
      if E2>1 and E1[E2-1][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-9)))
      if E2==6 and E1[E2-1][E3]=='-' and E1[E2-2][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-10)))
      if E2==1 and E1[E2-1][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-9))+'q')
      if((E3-1)>=0 and(E2-1)>=0)or((E3+1)<8 and(E2-1)>=0):
       O3=''
       if E2==1:
        O3='q'
       if(E3-1)>=0 and E1[E2-1][E3-1]!='-' and E1[E2-1][E3-1].islower():
        F1=B2(E3)+str(abs(E2-9))
        N7.append(E1[E2-1][E3-1])
        yield(K7+F1+O3)
       if(E3+1)<8 and E1[E2-1][E3+1]!='-' and E1[E2-1][E3+1].islower():
        F1=B2(E3+2)+str(abs(E2-9))
        N7.append(E1[E2-1][E3+1])
        yield(K7+F1+O3)
     else:
      if E2<6 and E1[E2+1][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-7)))
      if E2==1 and E1[E2+1][E3]=='-' and E1[E2+2][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-6)))
      if E2==6 and E1[E2+1][E3]=='-':
       yield(K7+B2(E3+1)+str(abs(E2-7))+'q')
      if((E3-1)>=0 and(E2+1)<8)or((E3+1)<8 and(E2+1)<8):
       O3=''
       if E2==6:
        O3='q'
       if(E3+1)<8 and E1[E2+1][E3+1]!='-' and E1[E2+1][E3+1].isupper():
        F1=B2(E3+2)+str(abs(E2-7))
        N7.append(E1[E2+1][E3+1])
        yield(K7+F1+O3)
       if(E3-1)>=0 and E1[E2+1][E3-1]!='-' and E1[E2+1][E3-1].isupper():
        F1=B2(E3)+str(abs(E2-7))
        N7.append(E1[E2+1][E3-1])
        yield(K7+F1+O3)
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
        yield(K7+F1)
        if E0:
         N7.append(E9)
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
        yield(K7+F1)
        if E0:
         N7.append(E9)
         break
       else:
        break
       E21+=F8['E23']
       E22+=F8['E24']
 def I9(Z,E7):
  if E7:
   return 'K' in Z.D0
  else:
   return 'k' in Z.D9
 def G3(Z):
  K0=0
  for table in range(64):
   E2=math.floor(table/8)
   E3=table%8
   Z1=Z.B3[E2][E3]
   E7=Z1.isupper()
   if Z1!='-':
    if E7:
     K0+=A1[Z1.lower()]
     K0+=(A9[Z1.lower()][E2][E3]/50)
    else:
     K0-=A1[Z1]
     K0-=(A9[Z1][abs(E2-7)][abs(E3-7)]/50)
  return K0
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
 def G71(Z,G9,L6,I7):
  I8=N3()
  Z.G6=N3()+I7
  H3=-1e8
  J3=0
  J4=None
  initial_score=G9.G3()
  Z.L6=1
  while L6>1:
   Z.L6+=1
   L6-=1
   (J3,J4)=Z.aspiration_window(G9,Z.L6,J3)
   I6=math.ceil(N3()-I8)
   v_nps=math.ceil(Z.L5/I6)
   Z.print_stats(str(Z.L6),str(math.ceil(J3)),str(I6),str(Z.L5),str(v_nps),J4)
  return[J3,J4]
 def print_stats(Z,L6,L8,v_time,L5,v_nps,v_pv):
  N2("info depth "+L6+" score cp "+L8+" time "+v_time+" nodes "+L5+" nps "+v_nps+" pv "+v_pv)
 def aspiration_window(Z,G9,L6,initial_score):
  H3=-1e8
  H4=1e8
  L9=10
  depth=L6
  if depth>3:
   H3=max(-1e8,initial_score-L9)
   H4=min(1e8,initial_score+L9)
  H2=-1e8
  local_move=None
  while True:
   (H2,local_move)=Z.G7(G9,depth,H3,H4)
   if H2>H3 and H2<H4:
    N2("info nodes "+str(Z.L5))
   if H2>H3 and H2<H4:
    return[H2,local_move]
   if H2<=H3:
    H4=(H3+H4)/2
    H3=max(-1e8,H3-L9)
    depth=L6
   elif H2>=H4:
    H4=min(1e8,H4+L9)
    depth=min(1,depth-min(1e8,H2)/2)
   L9=L9+L9/2
 def G7(Z,G9,L6,H3,H4):
  G0=-1e8
  F41=None
  H2=-1e8
  E7=G9.B4%2==0
  L6=max(L6,1)
  for K7 in G9.D8():
   if K7 is None:
    continue
   Z.L5+=1
   H2=-Z.pvs(G9.D4(K7),-H4,-H3,L6-1)
   if H2>=G0:
    G0=H2
    F41=K7
  return[G0,F41]
 def M4(Z,G9):
  M5=G9.M6()
  if M5 not in Z.M3:
   Z.M3[M5]={'M8':0,'M9':-1e5,'M0':2}
  return Z.M3[M5]
 def store_tt(Z,G9,J7):
  M5=G9.M6()
  if len(Z.M3)>1e7:
   Z.M3.clear()
  Z.M3[M5]=J7
 def pvs(Z,G9,H3,H4,L6):
  E7=G9.B4%2==0
  K0=G9.G3()
  if K0>=5e4:
   return 1e8 if E7 else-1e8
  if L6<1:
   return K0 if E7 else-K0
  H3_orig=H3
  J7=Z.M4(G9)
  if J7['M8']>=L6:
   if J7['M0']==I0:
    Z.L5+=1
    return J7['M9']
   elif J7['M0']==LOWER:
    H3=max(H3,J7['M9'])
   elif J7['M0']==UPPER:
    H4=min(H4,J7['M9'])
   if H3>=H4:
    Z.L5+=1
    return J7['M9']
  H2=-1e8
  for K7 in G9.D8():
   Z.L5+=1
   H2=-Z.pvs(G9.D4(K7),-H3-1,-H3,L6-1)
   if H2>H3 and H2<H4:
    H2=-Z.pvs(G9.D4(K7),-H4,-H2,L6-1)
   H3=max(H3,H2)
   if H3>=H4:
    break
  J7['M9']=H3
  if H3<=H3_orig:
   J7['M0']=UPPER
  elif H3>=H4:
   J7['M0']=LOWER
  else:
   J7['M0']=I0
  J7['M8']=L6
  Z.store_tt(G9,J7)
  return H3
I0=1
UPPER=2
LOWER=3
def main():
 G7er=G4()
 H8=H9()
 H8.K3()
 while 1:
  try:
   Z2=input()
   if Z2=="quit":
    sys.exit()
   elif Z2=="uci":
    N2("pygone 1.0\nuciok")
   elif Z2=="ucinewgame":
    H8.K3()
    G7er.K3()
   elif Z2=="isready":
    N2("readyok")
   elif Z2.startswith("position"):
    Z3=Z2.split()
    H8.K3()
    for F42 in Z3[3:]:
     H8=H8.D4(F42)
   elif Z2.startswith("go"):
    I2=1e8
    I3=1e8
    I4=8
    input_depth=0
    I5=Z2.split()
    for key,arg in enumerate(I5):
     if arg=='wtime':
      I2=int(I5[key+1])
     elif arg=='btime':
      I3=int(I5[key+1])
     elif arg=='depth':
      I4=int(I5[key+1])
     elif arg=='infinite':
      input_depth=30
    K4=max(40-H8.B4,2)
    I7=1e8
    E7=H8.B4%2==0
    if E7:
     I7=I2/(K4*1e3)
    else:
     I7=I3/(K4*1e3)
    if I7<15:
     I4=6
    if I7<4:
     I7=2
     I4=4
    I4=max(input_depth,I4)
    G7er.L5=0
    G7er.M2=0
    (score,K7)=G7er.G71(H8,I4,I7)
    (score,K7)=G7er.G7(H8,I4,score-10,score+10)
    N2("bestmove "+K7)
  except(KeyboardInterrupt,SystemExit):
   N2('quit')
   sys.exit()
  except Exception as exc:
   N2(exc)
   raise
main()

