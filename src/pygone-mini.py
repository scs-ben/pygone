#!/usr/bin/env pypy3
import math,sys,time
t=time.time
A={'p':100,'n':320,'b':325,'r':500,'q':975,'k':32767}
B={'p':(0,0,0,0,0,0,0,0,20,20,20,20,20,20,20,20,8,8,8,8,8,8,8,8,6,6,6,6,6,6,6,6,0,0,0,4,4,0,0,0,2,-2,-2,3,3,-2,-2,2,2,4,4,-8,-8,4,4,2,0,0,0,0,0,0,0,0),'n':(-20,-16,-12,-12,-12,-12,-16,-20,-16,-8,2,2,2,2,-8,-16,-8,4,5,6,6,5,4,-8,0,4,6,8,8,6,4,0,0,4,6,8,8,6,4,0,-8,4,5,5,5,5,4,-8,-16,-8,0,2,2,0,-8,-16,-20,-16,-12,-12,-12,-12,-16,-20),'b':(-8,-4,-4,-4,-4,-4,-4,-8,-4,0,0,0,0,0,0,-4,-4,0,2,4,4,2,0,-4,0,2,2,4,4,2,2,0,0,0,4,4,4,4,0,0,-4,4,4,4,4,4,4,-4,-4,2,0,0,0,0,2,-4,-8,-4,-4,-4,-4,-4,-4,-8),'r':(0,0,0,0,0,0,0,0,2,4,4,4,4,4,4,2,-4,0,2,2,2,2,0,-4,-2,0,2,2,2,2,0,-2,0,0,2,2,2,2,0,-2,-4,2,2,2,2,2,0,-4,-2,0,0,2,0,2,0,-2,0,0,0,2,2,0,0,0),'q':(-8,-4,-4,-2,-2,-4,-4,-8,-4,6,6,6,6,6,6,-4,-4,4,4,4,4,4,4,-4,-2,2,2,2,2,2,2,-2,-2,2,2,2,2,2,2,-2,-4,2,2,2,2,2,2,-4,-4,0,2,0,0,0,0,-4,-8,-4,-4,-2,-2,-4,-4,-8),'k':(-20,-16,-12,-8,-8,-12,-16,-20,-4,-4,-2,0,0,-2,-4,-4,-4,0,8,12,12,8,0,-4,-4,0,12,16,16,12,0,-4,-4,0,12,16,16,12,0,-4,-4,0,8,12,12,8,0,-4,8,8,-16,-16,-16,-16,8,8,0,4,8,0,0,4,8,0)}
for C,set_board in B.items():
 prow=lambda row:(0,)+tuple(piece+A[C]for piece in row)+(0,)
 B[C]=sum((prow(set_board[column*8:column*8+8])for column in range(8)),())
 B[C]=(0,)*20+B[C]+(0,)*20
H=1
K=2
L=3
J=A['k']
PROTECTED_PAWN_VALUE=4
STACKED_PAWN_VALUE=20
KING_SAFETY=25
M={'k':[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)],'q':[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)],'r':[(0,10),(0,-10),(1,0),(-1,0)],'b':[(1,10),(1,-10),(-1,10),(-1,-10)],'n':[(1,-20),(-1,-20),(2,-10),(-2,-10),(1,20),(-1,20),(2,10),(-2,10)],'p':[(0,-10),(1,-10),(-1,-10)]}
def N(O):
 return chr(O+96)
def Q(P):
 print(P,flush=True)
def R(S,v_score,U,V,W,X):
 Q(f"info depth {S} score cp {v_score} time {U} nodes {V} nps {W} pv {X}")
def Y(A1):
 return(coordinate_to_position(A1[0:2]),coordinate_to_position(A1[2:4]))
def position_to_coordinate(board_position):
 return N(board_position%10)+str(abs(board_position//10-10))
def coordinate_to_position(coordinate):
 return 10*(abs(int(coordinate[1])-8)+2)+(ord(coordinate[0])-97)+1
class A6:
 K3=''
 A8=0
 A0=[]
 B2=[True,True]
 B3=[True,True]
 B4='e1'
 B5='e8'
 B6=0
 K4=32
 B7=''
 move_counter=0
 def __init__(self):
  self.A7=('..........' '..........' '.rnbqkbnr.' '.pppppppp.' '.--------.' '.--------.' '.--------.' '.--------.' '.PPPPPPPP.' '.RNBQKBNR.' '..........' '..........')
 def mutate_board(self,board_position,piece):
  self.A7=self.A7[:board_position]+piece+self.A7[board_position+1:]
 def B8(self,A1):
  is_white=self.A8%2==0
  self.move_counter+=1
  (B0,O)=Y(A1)
  C2=self.A7[B0].lower()
  if self.A7[O]!='-':
   self.move_counter=0
  self.mutate_board(O,self.A7[B0])
  self.mutate_board(B0,'-')
  B71=False
  if C2=='p':
   self.move_counter=0
   B71=abs(B0-O)==20
   B72=-1 if is_white else 1
   if B71:
    self.B7=A1[0:1]+str(int(A1[3:4])+B72)
   elif A1[2:4]==self.B7:
    self.mutate_board(O-10*B72,'-')
   elif len(A1)>4:
    self.mutate_board(O,A1[4:5].upper()if is_white else A1[4:5])
  elif C2=='k':
   if is_white:
    self.B4=A1[2:4]
   else:
    self.B5=A1[2:4]
   if abs(O-B0)==2:
    self.mutate_board(O+(1 if O>B0 else-2),'-')
    self.mutate_board(B0+((O-B0)//2),'R' if is_white else 'r')
  if not B71:
   self.B7=''
  self.K3=self.C6()
  self.K4=self.C7()
 def C4(self,A1):
  board=self.board_copy()
  board.B6=self.B6+self.A4(A1)
  if 'e1' in A1:
   board.B2=[False,False]
  elif 'a1' in A1:
   board.B2[0]=False
  elif 'h1' in A1:
   board.B2[1]=False
  if 'e8' in A1:
   board.B3=[False,False]
  elif 'a8' in A1:
   board.B3[0]=False
  elif 'h8' in A1:
   board.B3[1]=False
  board.B8(A1)
  board.A8+=1
  board.B6=-board.B6
  board.A0.append(board.K3)
  return board
 def C5(self):
  board=self.board_copy()
  board.A8+=1
  board.B6=-self.B6
  return board
 def board_copy(self):
  board=A6()
  board.A8=self.A8
  board.B4=self.B4
  board.B5=self.B5
  board.K3=self.K3
  board.K4=self.K4
  board.B7=self.B7
  board.move_counter=self.move_counter
  board.A7=self.A7
  board.A0=self.A0.copy()
  board.B2=self.B2.copy()
  board.B3=self.B3.copy()
  return board
 def C7(self):
  return 64-self.K3.count('-')
 def C8(self):
  return self.K4<14 or(self.K4<20 and 'q' not in self.K3.lower())
 def move_sort(self,A1):
  return self.A4(A1,True)
 def A4(self,A1,sorting=False):
  is_white=self.A8%2==0
  D1=0 if is_white else 119
  D11=-10 if is_white else 10
  D5='P' if is_white else 'p'
  C8=self.C8()
  (B0,O)=Y(A1)
  local_score=0
  C2=self.A7[B0].lower()
  D4=self.A7[O].lower()
  local_score+=B[C2][abs(O-D1)]- B[C2][abs(B0-D1)]
  if D4!='-':
   local_score+=B[D4][abs(O-D1)]
   if not C8 and D4=='p':
    local_score+=self.E11(A1,self.A7[O],-D11)
   if sorting and C2=='q' and D4=='p':
    local_score-=100
  if C2=='p':
   if A1[2:4]==self.B7:
    local_score+=B[C2][abs(O-D1)]
   elif len(A1)>4:
    D7=A1[4:5]
    local_score+=B[D7][abs(O-D1)]- B['p'][abs(O-D1)]
   if not C8:
    local_score+=self.E11(A1,D5,D11)
  elif C2=='k':
   if abs(O-B0)==2:
    if O>B0:
     local_score+=B['r'][abs(O-D1)-1]- B['r'][abs(O-D1)+1]
    else:
     local_score+=B['r'][abs(O-D1)+1]- B['r'][abs(O-D1)-2]
    if sorting:
     local_score+=KING_SAFETY
  if not C8:
   local_score+=self.king_safety(A1,is_white,D11)
  return local_score
 def E11(self,A1,D5,D11):
  D61=self.protected_pawn_count(D5,D11)
  pawn_board=self.board_copy()
  pawn_board.B8(A1)
  D6=pawn_board.protected_pawn_count(D5,D11)
  return(D6-D61)*PROTECTED_PAWN_VALUE 
 def protected_pawn_count(self,D5,D11):
  D6=0
  for board_position,piece in enumerate(self.A7):
   if piece==D5:
    D6+=self.protected_pawn(board_position,D11,D5)
  return D6
 def protected_pawn(self,board_position,D11,D5):
  return D5 in(self.A7[board_position-D11+1],self.A7[board_position-D11-1])
 def king_safety(self,A1,is_white,D11):
  king_position=coordinate_to_position(self.B4 if is_white else self.B5)
  pieces='P' if is_white else 'p'
  D61=0
  c_string=self.A7[(king_position+D11-1):(king_position+D11+2)]+ self.A7[(king_position+2*D11-1):(king_position+2*D11+2)]
  D61=c_string.count(pieces)
  pawn_board=self.board_copy()
  pawn_board.B8(A1)
  D6=0
  c_string=pawn_board.A7[(king_position+D11-1):(king_position+D11+2)]+ pawn_board.A7[(king_position+2*D11-1):(king_position+2*D11+2)]
  D6=c_string.count(pieces)
  return(D6-D61)*KING_SAFETY
 def C6(self):
  return self.A7+ str(self.A8%2)
 def generate_valid_captures(self):
  return self.A5(True)
 def A5(self,captures_only=False):
  D1=1
  if self.A8%2==0:
   is_white=True
   E7=81
   E6=31
   E5='prnbqk-'
  else:
   is_white=False
   E7=31
   E6=81
   E5='PRNBQK-'
  for board_position,piece in enumerate(self.A7):
   if piece in "-." or is_white==piece.islower():
    continue
   E9=position_to_coordinate(board_position)
   piece_lower=piece.lower()
   if piece=='p':
    D1=-1
   if not captures_only:
    if piece=='K':
     if self.B2[1]and self.A7[96:99]=='--R' and not any(self.attack_position(is_white,coordinate)for coordinate in['e1','f1','g1']):
      yield E9+'g1'
     if self.B2[0]and self.A7[91:95]=='R---' and not any(self.attack_position(is_white,coordinate)for coordinate in['e1','d1','c1']):
      yield E9+'c1'
    elif piece=='k':
     if self.B3[1]and self.A7[26:29]=='--r' and not any(self.attack_position(is_white,coordinate)for coordinate in['e8','f8','g8']):
      yield E9+'g8'
     if self.B3[0]and self.A7[21:25]=='r---' and not any(self.attack_position(is_white,coordinate)for coordinate in['e8','d8','c8']):
      yield E9+'c8'
    elif piece_lower=='p' and E7<=board_position<E7+8 and self.A7[board_position+-10*D1]=='-' and self.A7[board_position+-20*D1]=='-':
     yield E9+position_to_coordinate(board_position+-20*D1)
   for F3 in M[piece_lower]:
    to_position=board_position+F3[0]+(F3[1]*D1)
    while 20<to_position<99:
     F6=self.A7[to_position]
     if not captures_only or(captures_only and F6 not in '-.'):
      F7=position_to_coordinate(to_position)
      if piece_lower=='p':
       if(board_position in range(E6,E6+8)and F3[0]==0 and F6=='-')or (board_position in range(E6,E6+8)and F3[0]!=0 and F6!='-' and F6 in E5):
        for G8 in 'qrbn':
         yield E9+F7+G8
       else:
        if(F3[0]==0 and F6=='-')or (F3[0]!=0 and F6!='-' and F6 in E5)or F7==self.B7:
         yield E9+F7
      elif F6 in E5:
       yield E9+F7
     if F6!='-' or piece_lower in 'knp':
      break
     to_position=to_position+F3[0]+(F3[1]*D1)
 def E0(self,is_white):
  king_position=self.B4 if is_white else self.B5
  return self.attack_position(is_white,king_position)
 def attack_position(self,is_white,coordinate):
  D1=1
  E5='PRNBQK-' if is_white else 'prnbqk-'
  attack_position=coordinate_to_position(coordinate)
  for board_position,piece in enumerate(self.A7):
   if piece in "-." or is_white==piece.isupper():
    continue
   if piece=='p':
    D1=-1
   piece=piece.lower()
   for F3 in M[piece]:
    if piece=='p' and not F3[0]:
     continue
    to_position=board_position+F3[0]+(D1*F3[1])
    while 20<to_position<99:
     F6=self.A7[to_position]
     if F6 in E5 and to_position==attack_position:
      return True
     if F6!='-' or piece in 'knp':
      break
     to_position=to_position+F3[0]+D1*F3[1]
  return False
class F0:
 V=0
 S=0
 G1=0
 G2=0
 G3={}
 def G9(self):
  self.V=0
  self.S=0
  self.G1=0
  self.G2=0
  self.G3.clear()
 def H1(self,local_board):
  H2=t()
  local_score=local_board.B6
  for S in range(1,100):
   local_score=self.H9(local_board,S,-J,J)
   if t()<self.G2:
    H7=self.G3.get(local_board.K3)
    if H7:
     H7=H7['tt_move']
   else:
    break
   H8=t()-H2
   W=math.ceil(self.V/H8)if H8>0 else 1
   R(str(S),str(math.ceil(local_score)),str(math.ceil(H8)),str(self.V),str(W),str(H7))
   yield S,H7,local_score
 def H9(self,local_board,S,alpha,beta):
  if t()>self.G2:
   return-J
  self.V+=1
  is_pv_node=beta>alpha+1
  E01=local_board.E0(local_board.A8%2==0)
  S+=E01 
  if S<=0:
   return self.H93(local_board,alpha,beta,10)
  tt_entry=self.G3.get((local_board.K3),{'tt_value':2*J,'tt_flag':K,'tt_depth':-1,'tt_move':None})
  if tt_entry['tt_move']and(local_board.A0.count(local_board.K3)>2 or local_board.move_counter>=100):
   return 0
  mating_value=J-S
  if mating_value<beta:
   beta=mating_value
   if alpha>=mating_value:
    return mating_value
  mating_value=-J+S
  if mating_value>alpha:
   alpha=mating_value
   if beta<=mating_value:
    return mating_value
  original_alpha=alpha
  if tt_entry['tt_depth']>=S and tt_entry['tt_move']and not is_pv_node:
   if tt_entry['tt_flag']==H or (tt_entry['tt_flag']==L and tt_entry['tt_value']>=beta)or (tt_entry['tt_flag']==K and tt_entry['tt_value']<=alpha):
    return tt_entry['tt_value']
  if not is_pv_node and not E01 and S<=7 and local_board.B6>=beta+(80*S):
   return local_board.B6
  if not is_pv_node and not E01 and S<=5:
   cut_boundary=alpha-(340*S)
   if local_board.B6<=cut_boundary:
    if S<=2:
     return self.H93(local_board,alpha,alpha+1,6)
    local_score=self.H93(local_board,cut_boundary,cut_boundary+1,6)
    if local_score<=cut_boundary:
     return local_score
  T=-J-1
  local_score=-J
  is_white=local_board.A8%2==0
  pieces='RNBQ' if is_white else 'rnbq'
  if not is_pv_node and not E01 and pieces in local_board.K3:
   local_score=-self.H9(local_board.C5(),S-4,-beta,-beta+1)
   if local_score>=beta:
    return beta
  if not is_pv_node and not E01 and tt_entry['tt_depth']>=S and abs(tt_entry['tt_value'])<J and tt_entry['tt_move']:
   local_score=-self.H9(local_board.C4(tt_entry['tt_move']),S-2,-beta,-alpha)
   if local_score>=beta:
    return beta
  I92=0
  H7=None
  for F2 in sorted(local_board.A5(),key=local_board.move_sort,reverse=True):
   G7=local_board.C4(F2)
   if G7.E0(is_white):
    continue
   is_quiet=local_board.K4==G7.K4
   I92+=1
   r_depth=1
   if(not is_pv_node and is_quiet and S>2 and I92>1):
    r_depth=max(3,math.ceil(math.sqrt(S-1)+math.sqrt(I92-1)))
   if r_depth!=1:
    local_score=-self.H9(G7,S-r_depth,-alpha-1,-alpha)
   if(r_depth!=1 and local_score>alpha)or(r_depth==1 and not(is_pv_node and I92==1)):
    local_score=-self.H9(G7,S-1,-alpha-1,-alpha)
   if is_pv_node and(I92==1 or local_score>alpha):
    local_score=-self.H9(G7,S-1,-beta,-alpha)
   if not H7:
    H7=F2
   if local_score>T:
    H7=F2
    T=local_score
    if local_score>alpha:
     alpha=local_score
     if alpha>=beta:
      break
  if not I92:
   return-J if E01 else 0
  if t()<self.G2:
   tt_entry['tt_value']=T
   if H7:
    tt_entry['tt_move']=H7
   tt_entry['tt_depth']=S
   if T<=original_alpha:
    tt_entry['tt_flag']=K
   elif T>=beta:
    tt_entry['tt_flag']=L
   else:
    tt_entry['tt_flag']=H
   self.G3[local_board.K3]=tt_entry
  else:
   self.G3[local_board.K3]={'tt_value':2*J,'tt_flag':K,'tt_depth':-1,'tt_move':None}
  return T
 def H93(self,local_board,alpha,beta,S):
  if t()>self.G2:
   return-J
  self.V+=1
  if local_board.A0.count(local_board.K3)>2 or local_board.move_counter>=100:
   return 0
  tt_entry=self.G3.get(local_board.K3)
  if tt_entry:
   if tt_entry['tt_flag']==H or (tt_entry['tt_flag']==L and tt_entry['tt_value']>=beta)or (tt_entry['tt_flag']==K and tt_entry['tt_value']<=alpha):
    return tt_entry['tt_value']
  local_score=local_board.B6
  if S<=0 or local_score>=beta:
   return local_score
  alpha=max(alpha,local_score)
  for F2 in sorted(local_board.generate_valid_captures(),key=local_board.move_sort,reverse=True):
   G7=local_board.C4(F2)
   if G7.E0(local_board.A8%2==0):
    continue
   local_score=-self.H93(G7,-beta,-alpha,S-1)
   if local_score>alpha:
    alpha=local_score
    if alpha>=beta:
     return alpha
  return alpha
def main():
 I7=A6()
 H91=F0()
 while 1:
  try:
   line=input()
   if line=="quit":
    sys.exit()
   elif line=="uci":
    Q("pygone 1.4\nuciok")
   elif line=="ucinewgame":
    I7=A6()
    H91.G9()
   elif line=="isready":
    Q("readyok")
   elif line.startswith("position"):
    I9=line.split()
    I7=A6()
    for I0 in I9[3:]:
     I7=I7.C4(I0)
   elif line.startswith("go"):
    H91.S=30
    J6=1e8
    is_white=I7.A8%2==0
    J3=line.split()
    for key,arg in enumerate(J3):
     if arg=='wtime' and is_white or arg=='btime' and not is_white:
      J6=int(J3[key+1])/1e3
     elif arg=='depth':
      H91.S=int(J3[key+1])
    H91.G2=t()+max(0.75,J6-1)
    J6=max(2.2,J6/18)
    H91.G1=t()+J6
    H91.V=0
    F2=None
    for S,F2,T in H91.H1(I7):
     if S>=H91.S or t()>=H91.G1:
      break
    Q(f"bestmove {str(F2)}")
  except(KeyboardInterrupt,SystemExit):
   sys.exit()
  except Exception as exc:
   Q(exc)
   raise
main()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
