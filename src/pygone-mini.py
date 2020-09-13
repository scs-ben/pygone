#!/usr/bin/env python3
import math
import sys
import time
PIECEPOINTS={'p':100.0,'r':479.0,'n':280.0,'b':320.0,'q':929.0,'k':60000.0}
ATTACKPOINTS={'p':5.0,'r':18.0,'n':10.0,'b':10.0,'q':20.0,'k':30.0}
PPSQT=[[0,0,0,0,0,0,0,0],[78,83,86,73,102,82,85,90],[7,29,21,44,40,31,44,7],[-17,16,-2,15,14,0,15,-13],[-26,3,10,9,6,1,0,-23],[-22,9,5,-11,-10,-2,3,-19],[-31,8,-7,-37,-36,-14,3,-31],[0,0,0,0,0,0,0,0]]
NPSQT=[[-66,-53,-75,-75,-10,-55,-58,-70],[-3,-6,100,-36,4,62,-4,-14],[10,67,1,74,73,27,62,-2],[24,24,45,37,33,41,25,17],[-1,5,31,21,22,35,2,0],[-18,10,13,22,18,15,11,-14],[-23,-15,2,0,2,0,-23,-20],[-74,-23,-26,-24,-19,-35,-22,-69]]
BPSQT=[[-59,-78,-82,-76,-23,-107,-37,-50],[-11,20,35,-42,-39,31,2,-22],[-9,39,-32,41,52,-10,28,-14],[25,17,20,34,26,25,15,10],[13,10,17,23,17,16,0,7],[14,25,24,15,8,25,20,15],[19,20,11,6,7,6,20,16],[-7,2,-15,-12,-14,-15,-10,-10]]
RPSQT=[[35,29,33,4,37,33,56,50],[55,29,56,67,55,62,34,60],[19,35,28,33,45,27,25,15],[0,5,16,13,18,-4,-9,-6],[-28,-35,-16,-21,-13,-29,-46,-30],[-42,-28,-42,-25,-25,-35,-26,-46],[-53,-38,-31,-26,-29,-43,-44,-53],[-30,-24,-18,5,-2,-18,-31,-32]]
QPSQT=[[6,1,-8,-104,69,24,88,26],[14,32,60,-10,20,76,57,24],[-2,43,32,60,72,63,43,2],[1,-16,22,17,25,20,-13,-6],[-14,-15,-2,-5,-1,-10,-20,-22],[-30,-6,-13,-11,-16,-11,-16,-27],[-36,-18,0,-19,-15,-15,-21,-38],[-39,-30,-31,-13,-31,-36,-34,-42]]
KPSQT=[[4,54,47,-99,-99,60,83,-62],[-32,10,55,56,56,55,10,3],[-62,12,-57,44,-67,28,37,-31],[-55,50,11,-4,-19,13,0,-49],[-55,-43,-52,-28,-51,-47,-8,-50],[-47,-42,-43,-79,-64,-32,-29,-32],[-4,3,-14,-50,-57,-18,13,4],[22,30,-3,-14,6,-1,40,26]]
ALLPSGT={'p':PPSQT,'n':NPSQT,'b':BPSQT,'r':RPSQT,'q':QPSQT,'k':KPSQT}
ISUPPER=lambda c:'A'<=c<='Z'
ISLOWER=lambda c:'a'<=c<='z'
def letter_to_number(letter):
 return abs((ord(letter)-96)-1)
def number_to_letter(number):
 return chr(number+96)
class Z:
 board_AH=[]
 played_move_count=0
 white_valid_AI=[]
 black_valid_AI=[]
 white_attack_locations=''
 black_attack_locations=''
 white_king_location='e1'
 black_king_location='e8'
 S=[]
 last_move=''
 nodes=0
 depth=0
 def __init__(self):
  self.set_default_board_AH()
  self.played_move_count=0
  self.white_valid_AI=[]
  self.black_valid_AI=[]
  self.white_attack_zs=[]
  self.black_attack_zs=[]
  self.white_attack_locations=''
  self.black_attack_locations=''
 def set_default_board_AH(self):
  self.board_AH=[['r','n','b','q','k','b','n','r'],['p']*8,['-']*8,['-']*8,['-']*8,['-']*8,['P']*8,['R','N','B','Q','K','B','N','R']]
 def set_board_AH(self,AH):
  self.board_AH=AH
 def make_move(self,uci_coordinate):
  from_letter_number=letter_to_number(uci_coordinate[0:1])
  from_number=abs(int(uci_coordinate[1:2])-8)
  to_letter_number=letter_to_number(uci_coordinate[2:3])
  to_number=abs(int(uci_coordinate[3:4])-8)
  from_z=self.board_AH[from_number][from_letter_number]
  to_z=self.board_AH[to_number][to_letter_number]
  a=""
  if len(uci_coordinate)>4:
   a=uci_coordinate[4:5]
  if(from_z in('P','p')and to_z=='-' and uci_coordinate[0:1]!=uci_coordinate[2:3]):
   self.board_AH[from_number][from_letter_number]='-'
   self.board_AH[to_number][to_letter_number]=from_z
   self.board_AH[from_number][to_letter_number]='-'
  elif(from_z in('K','k')and uci_coordinate in('e1g1','e1c1','e8g8','e8c8')):
   self.board_AH[from_number][from_letter_number]='-'
   if uci_coordinate[2]=='g':
    self.board_AH[to_number][to_letter_number+1]='-'
    if self.played_move_count%2==0:
     self.board_AH[from_number][from_letter_number+1]='R'
    else:
     self.board_AH[from_number][from_letter_number+1]='r'
   else:
    self.board_AH[from_number][to_letter_number-2]='-'
    if self.played_move_count%2==0:
     self.board_AH[from_number][from_letter_number-1]='R'
    else:
     self.board_AH[from_number][from_letter_number-1]='r'
   if self.played_move_count%2==0:
    self.board_AH[from_number][to_letter_number]='K'
   else:
    self.board_AH[from_number][to_letter_number]='k'
  else:
   self.board_AH[from_number][from_letter_number]='-'
   if a!="":
    if self.played_move_count%2==0:
     self.board_AH[to_number][to_letter_number]=a.upper()
    else:
     self.board_AH[to_number][to_letter_number]=a
   else:
    self.board_AH[to_number][to_letter_number]=from_z
  self.S.append(uci_coordinate)
  self.played_move_count+=1
 def show_board(self):
  for i in range(8):
   for j in range(8):
    print(self.board_AH[i][j],end=" ")
   print()
 def get_valid_AI(self):
  white_valid_AI=[]
  black_valid_AI=[]
  white_attack_zs=[]
  black_attack_zs=[]
  self.white_attack_locations=''
  self.black_attack_locations=''
  eval_AH=self.board_AH.copy()
  for t in range(8):
   for u in range(8):
    z=eval_AH[t][u]
    if z=="-":
     continue
    white_start_coordinate=number_to_letter(u+1)+str(abs(t-8))
    black_start_coordinate=number_to_letter(u+1)+str(abs(t-8))
    if z in('k','K'):
     if z=='K':
      is_white=True
      self.white_king_location=white_start_coordinate
     else:
      is_white=False
      self.black_king_location=black_start_coordinate
     king_AI={1:{'u':(u+0),'t':(t+1)},2:{'u':(u+0),'t':(t-1)},3:{'u':(u+1),'t':(t+0)},4:{'u':(u-1),'t':(t+0)},5:{'u':(u+1),'t':(t+1)},6:{'u':(u+1),'t':(t-1)},7:{'u':(u-1),'t':(t+1)},8:{'u':(u-1),'t':(t-1)},}
     if is_white:
      if white_start_coordinate=='e1' and eval_AH[7][5]=='-' and eval_AH[7][6]=='-' and eval_AH[7][7]=='R':
       white_valid_AI.append(white_start_coordinate+'g1')
      if white_start_coordinate=='e1' and eval_AH[7][1]=='-' and eval_AH[7][2]=='-' and eval_AH[7][3]=='-' and eval_AH[7][0]=='R':
       white_valid_AI.append(white_start_coordinate+'c1')
     else:
      if black_valid_AI=='e8' and eval_AH[0][1]=='-' and eval_AH[0][1]=='-' and eval_AH[0][2]=='-' and eval_AH[0][0]=='r':
       black_valid_AI.append(black_start_coordinate+'c8')
      if black_valid_AI=='e8' and eval_AH[0][5]=='-' and eval_AH[0][6]=='-' and eval_AH[0][7]=='r':
       black_valid_AI.append(black_start_coordinate+'g8')
     for n_move in king_AI.items():
      if(n_move['u']>=0 and n_move['u']<=7 and n_move['t']>=0 and n_move['t']<=7):
       eval_z=eval_AH[n_move['t']][n_move['u']]
       if is_white:
        can_capture=(eval_z!='-' and eval_z.ISLOWER())
       else:
        can_capture=(eval_z!='-' and eval_z.ISUPPER())
       dest=number_to_letter(n_move['u']+1)+str(abs(n_move['t']-8))
       if eval_z=='-' or can_capture:
        if is_white:
         white_valid_AI.append(white_start_coordinate+dest)
        else:
         black_valid_AI.append(black_start_coordinate+dest)
       if can_capture:
        if is_white:
         white_attack_zs.append([eval_z,z])
         self.white_attack_locations+=dest
        else:
         black_attack_zs.append([eval_z,z])
         self.black_attack_locations+=dest
    if z in('p','P'):
     if z=='P':
      if t>1 and eval_AH[t-1][u]=='-':
       white_valid_AI.append(white_start_coordinate+number_to_letter(u+1)+str(abs(t-9)))
      if t==6 and eval_AH[t-1][u]=='-' and eval_AH[t-2][u]=='-':
       white_valid_AI.append(white_start_coordinate+number_to_letter(u+1)+str(abs(t-10)))
      if t==1 and eval_AH[t-1][u]=='-':
       white_valid_AI.append(white_start_coordinate+number_to_letter(u+1)+str(abs(t-9))+'q')
      if((u-1)>=0 and(t-1)>=0)or((u+1)<8 and(t-1)>=0):
       prom=''
       if t==1:
        prom='q'
       if(u-1)>=0 and eval_AH[t-1][u-1]!='-' and eval_AH[t-1][u-1].ISLOWER():
        white_valid_AI.append(white_start_coordinate+number_to_letter(u)+str(abs(t-9))+prom)
        self.white_attack_locations+=number_to_letter(u)+str(abs(t-9))
        white_attack_zs.append([eval_AH[t-1][u-1],z])
       if(u+1)<8 and eval_AH[t-1][u+1]!='-' and eval_AH[t-1][u+1].ISLOWER():
        white_valid_AI.append(white_start_coordinate+number_to_letter(u+2)+str(abs(t-9))+prom)
        self.white_attack_locations+=number_to_letter(u+2)+str(abs(t-9))
        white_attack_zs.append([eval_AH[t-1][u+1],z])
     else:
      if t<6 and eval_AH[t+1][u]=='-':
       black_valid_AI.append(black_start_coordinate+number_to_letter(u+1)+str(abs(t-7)))
      if t==1 and eval_AH[t+1][u]=='-' and eval_AH[t+2][u]=='-':
       black_valid_AI.append(black_start_coordinate+number_to_letter(u+1)+str(abs(t-6)))
      if t==6 and eval_AH[t+1][u]=='-':
       black_valid_AI.append(black_start_coordinate+number_to_letter(u+1)+str(abs(t-7))+'q')
      if((u-1)>=0 and(t+1)<8)or((u+1)<8 and(t+1)<8):
       prom=''
       if t==6:
        prom='q'
       if(u+1)<8 and eval_AH[t+1][u+1]!='-' and eval_AH[t+1][u+1].ISUPPER():
        black_valid_AI.append(black_start_coordinate+number_to_letter(u+2)+str(abs(t-7))+prom)
        self.black_attack_locations+=number_to_letter(u+2)+str(abs(t-7))
        black_attack_zs.append([eval_AH[t+1][u+1],z])
       if(u-1)>=0 and eval_AH[t+1][u-1]!='-' and eval_AH[t+1][u-1].ISUPPER():
        black_valid_AI.append(black_start_coordinate+number_to_letter(u)+str(abs(t-7))+prom)
        self.black_attack_locations+=number_to_letter(u)+str(abs(t-7))
        black_attack_zs.append([eval_AH[t+1][u-1],z])
    if z in('n','N'):
     is_white=(z=='N')
     night_AI={1:{'u':(u+1),'t':(t-2)},2:{'u':(u-1),'t':(t-2)},3:{'u':(u+2),'t':(t-1)},4:{'u':(u-2),'t':(t-1)},5:{'u':(u+1),'t':(t+2)},6:{'u':(u-1),'t':(t+2)},7:{'u':(u+2),'t':(t+1)},8:{'u':(u-2),'t':(t+1)},}
     for n_move in night_AI.items():
      if n_move['u']>=0 and n_move['u']<=7 and n_move['t']>=0 and n_move['t']<=7:
       eval_z=eval_AH[n_move['t']][n_move['u']]
       if is_white:
        can_capture=(eval_z!='-' and eval_z.ISLOWER())
       else:
        can_capture=(eval_z!='-' and eval_z.ISUPPER())
       if eval_z=='-' or can_capture:
        dest=number_to_letter(n_move['u']+1)+str(abs(n_move['t']-8))
        if is_white:
         white_valid_AI.append(white_start_coordinate+dest)
         if can_capture:
          self.white_attack_locations+=dest
          white_attack_zs.append([eval_z,z])
        else:
         black_valid_AI.append(black_start_coordinate+dest)
         if can_capture:
          self.black_attack_locations+=dest
          black_attack_zs.append([eval_z,z])
    if z in('r','R')or z in('q','Q'):
     is_white=z in('R','Q')
     horizontal_AI={1:{'u':u,'t':(t-1),'s':0,'r':-1},2:{'u':u,'t':(t+1),'s':0,'r':1},3:{'u':(u-1),'t':t,'s':-1,'r':0},4:{'u':(u+1),'t':t,'s':1,'r':0}}
     for _,h_move in horizontal_AI.items():
      temp_t=h_move['t']
      temp_col=h_move['u']
      while temp_t in range(8)and temp_col in range(8):
       eval_z=eval_AH[temp_t][temp_col]
       can_capture=(is_white and eval_z!='-' and eval_z.ISLOWER())or(not is_white and eval_z!='-' and eval_z.ISUPPER())
       if eval_z=='-' or can_capture:
        dest=number_to_letter(temp_col+1)+str(abs(temp_t-8))
        if is_white:
         white_valid_AI.append(white_start_coordinate+dest)
         if can_capture:
          self.white_attack_locations+=dest
          white_attack_zs.append([eval_z,z])
        else:
         black_valid_AI.append(black_start_coordinate+dest)
         if can_capture:
          self.black_attack_locations+=dest
          black_attack_zs.append([eval_z,z])
        if can_capture:
         break
       else:
        break
       temp_t+=h_move['r']
       temp_col+=h_move['s']
    if z in('b','B')or z in('q','Q'):
     is_white=z in('B','Q')
     diag_AI={1:{'u':(u-1),'t':(t-1),'s':-1,'r':-1},2:{'u':(u+1),'t':(t+1),'s':1,'r':1},3:{'u':(u-1),'t':(t+1),'s':-1,'r':1},4:{'u':(u+1),'t':(t-1),'s':1,'r':-1}}
     for _,d_move in diag_AI.items():
      temp_t=d_move['t']
      temp_col=d_move['u']
      while temp_t in range(8)and temp_col in range(8):
       eval_z=eval_AH[temp_t][temp_col]
       can_capture=(is_white and eval_z!='-' and eval_z.ISLOWER())or(not is_white and eval_z!='-' and eval_z.ISUPPER())
       if eval_z=='-' or can_capture:
        dest=number_to_letter(temp_col+1)+str(abs(temp_t-8))
        if is_white:
         white_valid_AI.append(white_start_coordinate+dest)
         if can_capture:
          self.white_attack_locations+=dest
          white_attack_zs.append([eval_z,z])
        else:
         black_valid_AI.append(black_start_coordinate+dest)
         if can_capture:
          self.black_attack_locations+=dest
          black_attack_zs.append([eval_z,z])
        if can_capture:
         break
       else:
        break
       temp_t+=d_move['r']
       temp_col+=d_move['s']
  sep=''
  if self.played_move_count%2==0:
   move_copy=white_valid_AI.copy()
   move_string=sep.join(black_valid_AI)
   for move in move_copy:
    override_remove=((move=='e1g1' and('e1' in move_string or 'f1' in move_string or 'g1' in move_string))or(move=='e1c1' and('e1' in move_string or 'd1' in move_string or 'c1' in move_string)))
    if override_remove:
     try:
      white_valid_AI.remove(move)
     except Exception:
      continue
  else:
   move_copy=black_valid_AI.copy()
   move_string=sep.join(white_valid_AI)
   for move in move_copy:
    override_remove=((move=='e8g8' and('e8' in move_string or 'f8' in move_string or 'g8' in move_string))or(move=='e8c8' and('e8' in move_string or 'd8' in move_string or 'c8' in move_string)))
    if override_remove:
     try:
      black_valid_AI.remove(move)
     except Exception:
      continue
  self.white_valid_AI=white_valid_AI
  self.black_valid_AI=black_valid_AI
  self.white_attack_zs=white_attack_zs
  self.black_attack_zs=black_attack_zs
  return{'white_valid_AI':white_valid_AI,'black_valid_AI':black_valid_AI}
 def get_side_AI(self,is_white):
  if is_white:
   return self.white_valid_AI.copy()
  return self.black_valid_AI.copy()
 def board_evaluation(self):
  b_eval=0
  for t in range(8):
   for u in range(8):
    z=self.board_AH[t][u]
    is_white=z.ISUPPER()
    if z!='-':
     if is_white:
      b_eval+=PIECEPOINTS[z.lower()]
      b_eval+=(ALLPSGT[z.lower()][t][u]/10)
     else:
      b_eval-=PIECEPOINTS[z]
      b_eval-=(ALLPSGT[z][abs(t-7)][abs(u-7)]/10)
  return b_eval
 def A7_root(self,depth,local_board,max_time):
  lgl_mvs=local_board.get_side_AI(local_board.played_move_count%2==0)
  poss_mvs=lgl_mvs
  if len(poss_mvs)==1:
   local_board.depth=1
   return[local_board.board_evaluation(),poss_mvs[0]]
  is_maxing_white=(local_board.played_move_count%2==0)
  global_score=-50000 if is_maxing_white else 50000
  chosen_move=None
  original_AH=[x[:]for x in local_board.board_AH]
  local_board.depth=depth
  max_time=max_time/len(poss_mvs)
  for move in poss_mvs:
   local_board.nodes+=1
   local_board.make_move(move)
   local_start_time=time.perf_counter()+max_time
   local_score=self.A7(depth-1,-50000,50000,local_board,local_start_time,move)
   if is_maxing_white and local_score>global_score:
    global_score=local_score
    chosen_move=move
   elif not is_maxing_white and local_score<global_score:
    global_score=local_score
    chosen_move=move
   local_board.set_board_AH([x[:]for x in original_AH])
   local_board.played_move_count-=1
  GAMEBOARD.last_move=chosen_move
  return[global_score,chosen_move]
 def A7(self,depth,AM,AN,local_board,end_time,last_move):
  is_maxing_white=(local_board.played_move_count%2==0)
  local_board.get_valid_AI()
  poss_mvs=local_board.get_side_AI(is_maxing_white)
  local_start_time=time.perf_counter()
  if depth==0 or local_start_time>=end_time or len(poss_mvs)==0:
   AP=0
   if last_move==GAMEBOARD.last_move:
    if is_maxing_white:
     AP=-30.0
    else:
     AP=30.0
   return local_board.board_evaluation()+AP
  initial_score=local_board.board_evaluation()
  if(is_maxing_white and initial_score<-50000)or(not is_maxing_white and initial_score>50000):
   return local_board.board_evaluation()
  original_AH=[x[:]for x in local_board.board_AH]
  best_score=-50000 if is_maxing_white else 50000
  for move in poss_mvs:
   local_board.nodes+=1
   local_board.make_move(move)
   local_score=self.A7(depth-1,AM,AN,local_board,end_time,move)
   if is_maxing_white:
    best_score=max(best_score,local_score)
    AM=max(AM,best_score)
   else:
    best_score=min(best_score,local_score)
    AN=min(AN,best_score)
   local_board.set_board_AH([x[:]for x in original_AH])
   local_board.played_move_count-=1
   if AN<=AM:
    break
  return best_score
GAMEBOARD=Z()
while True:
 try:
  LINE=input()
  if LINE=="quit":
   sys.exit()
  elif LINE=="uci":
   print("pygone 1.0 by rcostheta")
   print("uciok")
  elif LINE=="ucinewgame":
   GAMEBOARD=Z()
   GAMEBOARD.played_move_count=0
  elif LINE=="eval":
   GAMEBOARD.get_valid_AI()
   GAMEBOARD.get_side_AI(1)
   print(GAMEBOARD.board_evaluation())
   GAMEBOARD.show_board()
  elif LINE=="isready":
   print("readyok")
  elif LINE.startswith("position"):
   MOVES=LINE.split()
   OFFSETMOVES=GAMEBOARD.played_move_count+3
   for position_move in MOVES[OFFSETMOVES:]:
    GAMEBOARD.make_move(position_move)
    OFFSETMOVES+=1
   GAMEBOARD.played_move_count=(OFFSETMOVES-3)
  elif LINE.startswith("go"):
   GOBOARD=Z()
   GOBOARD.set_board_AH([x[:]for x in GAMEBOARD.board_AH.copy()])
   GOBOARD.played_move_count=GAMEBOARD.played_move_count
   GOBOARD.get_valid_AI()
   WHITETIME=300
   BLACKTIME=300
   GODEPTH=3
   ARGS=LINE.split()
   for x,arg in enumerate(ARGS):
    if arg=='wtime':
     WHITETIME=int(ARGS[x+1])
    if arg=='btime':
     BLACKTIME=int(ARGS[x+1])
   TIMEMOVECALC=40
   if GAMEBOARD.played_move_count>38:
    TIMEMOVECALC=2
   else:
    TIMEMOVECALC=40-GAMEBOARD.played_move_count
   if GAMEBOARD.played_move_count%2==0:
    MOVETIME=WHITETIME/(TIMEMOVECALC*1000)
   else:
    MOVETIME=BLACKTIME/(TIMEMOVECALC*1000)
   MOVETIME-=3
   if MOVETIME<5:
    MOVETIME=5
   STARTTIME=time.perf_counter()
   (SCORE,MOVE)=GOBOARD.A7_root(GODEPTH,GOBOARD,MOVETIME)
   ELAPSEDTIME=math.ceil(time.perf_counter()-STARTTIME)
   NPS=math.ceil(GOBOARD.nodes/ELAPSEDTIME)
   print("info depth "+str(GOBOARD.depth)+" score cp "+str(math.ceil(SCORE))+" time "+str(ELAPSEDTIME)+" nodes "+str(GOBOARD.nodes)+" nps "+str(NPS)+" pv "+MOVE)
   print("bestmove "+MOVE)
 except(KeyboardInterrupt,SystemExit):
  print('quit')
  sys.exit()
 except Exception as exc:
  print(exc)
  raise

