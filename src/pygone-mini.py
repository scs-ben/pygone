#!/usr/bin/env pypy3
import gc,math,sys,time
import itertools
import re
from itertools import count
from collections import namedtuple
piece={'P':100,'N':280,'B':320,'R':479,'Q':929,'K':60000}
pst={'P':(0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0),'N':(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69),'B':(-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10),'R':(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32),'Q':(6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42),'K':(4,54,47,-99,-99,60,83,-62,-32,10,55,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-55,-43,-52,-28,-51,-47,-8,-50,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,17,30,-3,-14,6,-1,40,18),}
for k,table in pst.items():
 padrow=lambda row:(0,)+tuple(x+piece[k]for x in row)+(0,)
 pst[k]=sum((padrow(table[i*8:i*8+8])for i in range(8)),())
 pst[k]=(0,)*20+pst[k]+(0,)*20
N,E,S,W=-10,1,10,-1
directions={'P':(N,N+N,N+W,N+E),'N':(N+N+E,E+N+E,E+S+E,S+S+E,S+S+W,W+S+W,W+N+W,N+N+W),'B':(N+E,S+E,S+W,N+W),'R':(N,E,S,W),'Q':(N,E,S,W,N+E,S+E,S+W,N+W),'K':(N,E,S,W,N+E,S+E,S+W,N+W)}
MATE_LOWER=piece['K']-10*piece['Q']
MATE_UPPER=piece['K']+10*piece['Q']
A1,H1,A8,H8=91,98,21,28
initial=('         \n' '         \n' ' rnbqkbnr\n' ' pppppppp\n' ' ........\n' ' ........\n' ' ........\n' ' ........\n' ' PPPPPPPP\n' ' RNBQKBNR\n' '         \n' '         \n')
WHITE_PIECES=['P','R','N','B','Q','K']
BLACK_PIECES=['p','r','n','b','q','k']
TTEXACT=1
TTLOWER=2
TTUPPER=3
isupper=lambda c:'A'<=c<='Z'
islower=lambda c:'a'<=c<='z'
def letter_to_number(letter):
 return abs((ord(letter)-96)-1)
def number_to_letter(number):
 return chr(number+96)
def print_to_terminal(letter):
 print(letter,flush=1)
def get_perf_counter():
 return time.perf_counter()
class Position(namedtuple('Position','board score wc bc ep kp')):
 def gen_moves(self):
  for i,p in enumerate(self.board):
   if not p.isupper():continue
   for d in directions[p]:
    for j in count(i+d,d):
     q=self.board[j]
     if q.isspace()or q.isupper():break
     if p=='P' and d in(N,N+N)and q!='.':break
     if p=='P' and d==N+N and(i<A1+N or self.board[i+N]!='.'):break
     if p=='P' and d in(N+W,N+E)and q=='.' and j not in(self.ep,self.kp,self.kp-1,self.kp+1):break
     yield(i,j)
     if p in 'PNK' or q.islower():break
     if i==A1 and self.board[j+E]=='K' and self.wc[0]:yield(j+E,j+W)
     if i==H1 and self.board[j+W]=='K' and self.wc[1]:yield(j+W,j+E)
 def rotate(self):
  return Position(self.board[::-1].swapcase(),-self.score,self.bc,self.wc,119-self.ep if self.ep else 0,119-self.kp if self.kp else 0)
 def nullmove(self):
  return Position(self.board[::-1].swapcase(),-self.score,self.bc,self.wc,0,0)
 def move(self,move):
  i,j=move
  p,q=self.board[i],self.board[j]
  put=lambda board,i,p:board[:i]+p+board[i+1:]
  board=self.board
  wc,bc,ep,kp=self.wc,self.bc,0,0
  score=self.score+self.value(move)
  board=put(board,j,board[i])
  board=put(board,i,'.')
  if i==A1:wc=(False,wc[1])
  if i==H1:wc=(wc[0],False)
  if j==A8:bc=(bc[0],False)
  if j==H8:bc=(False,bc[1])
  if p=='K':
   wc=(False,False)
   if abs(j-i)==2:
    kp=(i+j)//2
    board=put(board,A1 if j<i else H1,'.')
    board=put(board,kp,'R')
  if p=='P':
   if A8<=j<=H8:
    board=put(board,j,'Q')
   if j-i==2*N:
    ep=i+N
   if j==self.ep:
    board=put(board,j+S,'.')
  return Position(board,score,wc,bc,ep,kp).rotate()
 def value(self,move):
  i,j=move
  p,q=self.board[i],self.board[j]
  score=pst[p][j]-pst[p][i]
  if q.islower():
   score+=pst[q.upper()][119-j]
  if abs(j-self.kp)<2:
   score+=pst['K'][119-j]
  if p=='K' and abs(i-j)==2:
   score+=pst['R'][(i+j)//2]
   score-=pst['R'][A1 if j<i else H1]
  if p=='P':
   if A8<=j<=H8:
    score+=pst['Q'][j]-pst['P'][j]
   if j==self.ep:
    score+=pst['P'][119-(j+S)]
  return score
class Search:
 nodes=0
 end_time=0
 v_depth=0
 tt_bucket={}
 def iterative_search(self,position,v_depth,move_time):
  start_time=time.perf_counter()
  self.end_time=time.perf_counter()+move_time
  self.v_depth=0
  local_score=-1e9
  local_move=None
  alpha=-1e8
  beta=1e8
  while True:
   self.v_depth+=1
   v_depth-=1
   (iterative_score,iterative_move)=-self.negascout(position,-beta,-alpha,self.v_depth)
   if iterative_score>local_score:
    local_score=iterative_score
    local_move=mrender(position,iterative_move)
   elapsed_time=math.ceil(get_perf_counter()-start_time)
   nps=math.ceil(self.v_nodes/elapsed_time)
   print_to_terminal("info depth "+str(self.v_depth)+" score cp "+str(math.ceil(local_score))+" time "+str(elapsed_time)+" nodes "+str(self.v_nodes)+" nps "+str(nps)+" pv "+str(local_move))
   if get_perf_counter()>=self.end_time or v_depth<1:
    break
  return[local_score,local_move]
 def negascout(self,position,alpha,beta,depth):
  if depth<0:
   return position.score
  b=beta
  second_search=False
  for s_move in position.gen_moves():
   t=-self.negascout(position.move(s_move),-b,-alpha,depth-1)
   if t>alpha and t<beta and second_search:
    t=-self.negascout(position.move(s_move),-beta,-alpha,depth-1)
   second_search=True
   alpha=max(alpha,t)
   if alpha>=beta:
    return alpha
   b=alpha+1
  return alpha
 def tt_lookup(self,position):
  board_string=position.board+str(get_color(position))
  if board_string not in self.tt_bucket:
   self.tt_bucket[board_string]={'tt_depth':0,'tt_value':-1e5,'tt_flag':2}
 def store_tt(self,position,tt_entry):
  board_string=position.board+str(get_color(position))
  if len(self.tt_bucket)>1e7:
   self.tt_bucket={}
  self.tt_bucket[board_string]=tt_entry
 def negamax(self,position,alpha,beta,v_depth):
  alpa_orig=alpha
  if v_depth<=0:
   return position.score
  value=-1e8
  for s_move in position.gen_moves():
   self.v_nodes+=1
   local_score=-self.negamax(position.move(s_move),-beta,-alpha,v_depth-1)
   alpha=max(local_score,alpha)
   if self.v_nodes%1e5==0:
    print_to_terminal("info nodes "+str(self.v_nodes)+" tthits "+str(self.v_tthits))
   if alpha>=beta:
    break
  return alpha
WHITE=0
BLACK=1
gc.enable()
def parse(c):
 fil,rank=ord(c[0])-ord('a'),int(c[1])-1
 return A1+fil-10*rank
def mparse(color,move):
 m=(parse(move[0:2]),parse(move[2:4]))
 return m if color==WHITE else(119-m[0],119-m[1])
def render(i):
 rank,fil=divmod(i-A1,10)
 return chr(fil+ord('a'))+str(-rank+1)
def mrender(pos,m):
 p='q' if A8<=m[1]<=H8 and pos.board[m[0]]=='P' else ''
 m=m if get_color(pos)==WHITE else(119-m[0],119-m[1])
 return render(m[0])+render(m[1])+p
def get_color(pos):
 return BLACK if pos.board.startswith('\n')else WHITE
def renderFEN(pos,half_move_clock=0,full_move_clock=1):
 color='wb'[get_color(pos)]
 if get_color(pos)==BLACK:
  pos=pos.rotate()
 board='/'.join(pos.board.split())
 board=re.sub(r'\.+',(lambda m:str(len(m.group(0)))),board)
 castling=''.join(itertools.compress('KQkq',pos.wc[::-1]+pos.bc))or '-'
 ep=sunfish.render(pos.ep)if not pos.board[pos.ep].isspace()else '-'
 clock='{} {}'.format(half_move_clock,full_move_clock)
 return ' '.join((board,color,castling,ep,clock))
def main():
 hist=[Position(initial,0,(True,True),(True,True),0,0)]
 searcher=Search()
 while True:
  try:
   line=input()
   if line=="quit":
    sys.exit()
   elif line=="uci":
    print("pygone 1.0 by rcostheta")
    print("uciok")
   elif line=="print":
    print(renderFEN(hist[-1],len(hist),math.ceil(len(hist)/2)))
   elif line=="ucinewgame":
    hist=[Position(initial,0,(True,True),(True,True),0,0)]
    gc.collect()
   elif line=="isready":
    print("readyok")
   elif line.startswith("position"):
    color=WHITE
    moves=line.split()
    hist=[Position(initial,0,(True,True),(True,True),0,0)]
    for position_move in moves[3:]:
     hist.append(hist[-1].move(mparse(color,position_move)))
     color=1-color
   elif line.startswith("go"):
    white_time=1000000
    black_time=1000000
    go_depth=8
    args=line.split()
    for key,arg in enumerate(args):
     if arg=='wtime':
      white_time=int(args[key+1])
     if arg=='btime':
      black_time=int(args[key+1])
     if arg=='depth':
      go_depth=int(args[key+1])
    time_move_calc=max(40-len(hist),2)
    time_move_calc=40
    if len(hist)>38:
     time_move_calc=2
    else:
     time_move_calc=40-len(hist)
    is_white=len(hist)%2==0
    if is_white:
     move_time=white_time/(time_move_calc*1e3)
    else:
     move_time=black_time/(time_move_calc*1000)
    move_time-=3
    if move_time<8:
     move_time=8
    if move_time<10 and go_depth>4:
     go_depth=4
    searcher.v_nodes=0
    searcher.v_tthits=0
    start_time=get_perf_counter()
    (score,s_move)=searcher.iterative_search(hist[-1],go_depth,move_time)
    print_to_terminal("bestmove "+s_move)
  except(KeyboardInterrupt,SystemExit):
   print('quit')
   sys.exit()
  except Exception as exc:
   print(exc)
   raise
main()

