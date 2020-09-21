#!/usr/bin/env pypy3
import math,sys,time
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
 B5=[]
 B6=[]
 B7=''
 B8=''
 B9='e1'
 B0='e8'
 C11=[]
 C1=[]
 def K3(Z):
  Z.B31()
  Z.B4=0
  Z.B5=[]
  Z.B6=[]
  Z.D9=[]
  Z.D0=[]
  Z.B7=''
  Z.B8=''
  Z.B9='e1'
  Z.B0='e8'
  Z.C11=[]
  Z.C1=[]
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
  (C9,C0)=Z.D1(C2)
  Z.C1.append(C2)
  Z.C11.append([C2,C9,C0])
  Z.B4+=1
  Z.D8()
 def D6(Z):
  Z.C1.pop()
  F81=Z.C11.pop()
  C2=F81[0]
  C9=F81[1]
  C0=F81[2]
  C4=C2 in('e1g1','e1c1','e8g8','e8c8')and C9 in('K','k')
  Z.B4-=1
  Z.D1(C2[2:4]+C2[0:2],len(C2)>4,C4,C9,C0)
 def M6(Z):
  N1=''
  for i in range(8):
   for j in range(8):
    N1+=Z.B3[i][j]
  return N1
 def D8(Z):
  E7=Z.B4%2==0
  N4=[]
  N7=[]
  N5=''
  if(E7):
   Z.B5=[]
   Z.D9=[]
   Z.B7=''
  else:
   Z.B6=[]
   Z.D0=[]
   Z.B8=''
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
      Z.B9=K7
      if K7=='e1' and E1[7][5]=='-' and E1[7][6]=='-' and E1[7][7]=='R':
       N4.append(K7+'g1')
      if K7=='e1' and E1[7][1]=='-' and E1[7][2]=='-' and E1[7][3]=='-' and E1[7][0]=='R':
       N4.append(K7+'c1')
     else:
      Z.B0=K7
      if K7=='e8' and E1[0][1]=='-' and E1[0][2]=='-' and E1[0][3]=='-' and E1[0][0]=='r':
       N4.append(K7+'c8')
      if K7=='e8' and E1[0][5]=='-' and E1[0][6]=='-' and E1[0][7]=='r':
       N4.append(K7+'g8')
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
        N7.append([E9,Z1,K7+F1])
        N5+=F1
    if Z1.lower()=='p':
     if E7:
      if E2>1 and E1[E2-1][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-9)))
      if E2==6 and E1[E2-1][E3]=='-' and E1[E2-2][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-10)))
      if E2==1 and E1[E2-1][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-9))+'q')
      if((E3-1)>=0 and(E2-1)>=0)or((E3+1)<8 and(E2-1)>=0):
       O3=''
       if E2==1:
        O3='q'
       if(E3-1)>=0 and E1[E2-1][E3-1]!='-' and E1[E2-1][E3-1].islower():
        F1=B2(E3)+str(abs(E2-9))
        N4.append(K7+F1+O3)
        N5+=F1
        N7.append([E1[E2-1][E3-1],Z1,K7+F1+O3])
       if(E3+1)<8 and E1[E2-1][E3+1]!='-' and E1[E2-1][E3+1].islower():
        F1=B2(E3+2)+str(abs(E2-9))
        N4.append(K7+F1+O3)
        N5+=F1
        N7.append([E1[E2-1][E3+1],Z1,K7+F1+O3])
     else:
      if E2<6 and E1[E2+1][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-7)))
      if E2==1 and E1[E2+1][E3]=='-' and E1[E2+2][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-6)))
      if E2==6 and E1[E2+1][E3]=='-':
       N4.append(K7+B2(E3+1)+str(abs(E2-7))+'q')
      if((E3-1)>=0 and(E2+1)<8)or((E3+1)<8 and(E2+1)<8):
       O3=''
       if E2==6:
        O3='q'
       if(E3+1)<8 and E1[E2+1][E3+1]!='-' and E1[E2+1][E3+1].isupper():
        F1=B2(E3+2)+str(abs(E2-7))
        N4.append(K7+F1+O3)
        N5+=F1
        N7.append([E1[E2+1][E3+1],Z1,K7+F1+O3])
       if(E3-1)>=0 and E1[E2+1][E3-1]!='-' and E1[E2+1][E3-1].isupper():
        F1=B2(E3)+str(abs(E2-7))
        N4.append(K7+F1+O3)
        N5+=F1
        N7.append([E1[E2+1][E3-1],Z1,K7+F1+O3])
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
         N5+=F1
         N7.append([E9,Z1,K7+F1])
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
        N4.append(K7+F1)
        if E0:
         N5+=F1
         N7.append([E9,Z1,K7+F1])
         break
       else:
        break
       E21+=F8['E23']
       E22+=F8['E24']
  if(E7):
   Z.B5=N4
   Z.B7=N5
   Z.D9=N7
  else:
   Z.B6=N4
   Z.B8=N5
   Z.D0=N7
  F0=''.join(Z.C1)
  if E7:
   F9=Z.B5.copy()
   M1=''.join(Z.B6.copy())
   for K7 in F9:
    G1=((K7=='e1g1' and('e1' in F0 or 'h1' in F0 or 'e1' in M1 or 'f1' in M1 or 'g1' in M1))or(K7=='e1c1' and('e1' in F0 or 'a1' in F0 or 'c1' in M1 or 'd1' in M1 or 'e1' in M1)))
    if G1:
     try:
      Z.B5.remove(K7)
     except Exception:
      continue
  else:
   F9=Z.B6.copy()
   M1=''.join(Z.B5.copy())
   for K7 in F9:
    G1=((K7=='e8g8' and('e8' in F0 or 'h8' in F0 or 'e8' in M1 or 'f8' in M1 or 'g8' in M1))or(K7=='e8c8' and('e8' in F0 or 'a8' in F0 or 'c8' in M1 or 'd8' in M1 or 'e8' in M1)))
    if G1:
     try:
      Z.B6.remove(K7)
     except Exception:
      continue
 def I9(Z,E7):
  if E7:
   for(K8,K9,_)in Z.D0:
    if K8=='K':
     return 1
   return 0
  else:
   for(K8,K9,_)in Z.D9:
    if K8=='k':
     return 1
   return 0
 def G2(Z,E7):
  if E7:
   return Z.B5
  return Z.B6
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
  Z.L6=0
  while L6>0:
   Z.L6+=1
   L6-=1
   (J3,J4)=Z.G7(G9,Z.L6)
   I6=math.ceil(N3()-I8)
   v_nps=math.ceil(Z.L5/I6)
   Z.print_stats(str(Z.L6),str(math.ceil(J3)),str(I6),str(Z.L5),str(v_nps),J4)
   if N3()>=Z.G6 or L6<1:
    break
  return[J3,J4]
 def print_stats(Z,L6,L8,v_time,L5,v_nps,v_pv):
  N2("info depth "+L6+" score cp "+L8+" time "+v_time+" nodes "+L5+" nps "+v_nps+" pv "+v_pv)
 def G7(Z,G9,L6):
  G0=-1e8
  F41=None
  H2=-1e8
  H3=-1e8
  H4=1e8
  E7=G9.B4%2==0
  G9.D8()
  H1=G9.G2(E7)
  L6=max(L6,1)
  for K7 in H1:
   Z.L5+=1
   G9.D4(K7)
   if not G9.I9(E7):
    H2=-Z.pvs(G9,-H4,-H3,L6-1)
    if H2>=G0:
     G0=H2
     F41=K7
   G9.D6()
  return[G0,F41]
 def M4(Z,G9):
  M5=G9.M6()
  if M5 not in Z.M3:
   Z.M3[M5]={'M8':0,'M9':-1e5,'M0':2}
  return Z.M3[M5]
 def store_tt(Z,G9,J7):
  M5=G9.M6()
  if len(Z.M3)>1e7:
   print('bucket dump')
   Z.M3={}
  Z.M3[M5]=J7
 def pvs(Z,G9,H3,H4,L6):
  E7=G9.B4%2==0
  G9.D8()
  H1=G9.G2(E7)
  if len(H1)==0 or L6<=0:
   K0=G9.G3()
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
  for K7 in H1:
   Z.L5+=1
   G9.D4(K7)
   if not G9.I9(E7):
    H2=-Z.pvs(G9,-H3-1,-H3,L6-1)
    if H2>H3 and H2<H4:
     H2=-Z.pvs(G9,-H4,-H2,L6-1)
   G9.D6()
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
H8=H9()
H8.K3()
def main():
 G7er=G4()
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
     H8.D4(F42)
   elif Z2.startswith("go"):
    I2=1e8
    I3=1e8
    I4=8
    I5=Z2.split()
    for key,arg in enumerate(I5):
     if arg=='wtime':
      I2=int(I5[key+1])
     if arg=='btime':
      I3=int(I5[key+1])
     if arg=='depth':
      I4=int(I5[key+1])
    K4=max(40-H8.B4,2)
    I7=1e8
    E7=H8.B4%2==0
    if E7:
     I7=I2/(K4*1e3)
    else:
     I7=I3/(K4*1e3)
    if I7<15:
     I4=5
    if I7<4:
     I7=2
     I4=4
    G7er.L5=0
    G7er.M2=0
    (score,K7)=G7er.G71(H8,I4,I7)
    N2("bestmove "+K7)
  except(KeyboardInterrupt,SystemExit):
   N2('quit')
   sys.exit()
  except Exception as exc:
   N2(exc)
   raise
main()

