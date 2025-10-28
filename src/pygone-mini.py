#!/usr/bin/env pypy3
import math,random,sys,time
t=time.time
A={'p':85,'n':295,'b':300,'r':700,'q':1350,'k':32767}
B={'p':(0,0,0,0,0,0,0,0,30,30,30,30,30,30,30,30,8,8,17,26,26,17,8,8,5,5,8,24,24,8,5,5,0,0,0,24,24,0,0,0,5,-5,-8,6,6,-8,-5,5,5,8,8,-22,-22,8,8,5,0,0,0,0,0,0,0,0),'n':(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,8,13,13,8,0,-30,-30,5,13,18,18,13,5,-30,-30,0,13,18,18,13,0,-30,-30,5,7,13,13,7,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-20,-30,-30,-20,-40,-50),'b':(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-40,-10,-10,-40,-10,-20),'r':(10,20,20,20,20,20,20,10,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10,-10,0,0,10,10,10,0,-10),'q':(-40,-20,-20,-10,-10,-20,-20,-40,-20,0,0,0,0,0,0,-20,-20,0,10,10,10,10,0,-20,-10,0,10,10,10,10,0,-10,0,0,10,10,10,10,0,-10,-20,10,10,10,10,10,0,-20,-20,0,10,0,0,0,0,-20,-40,-20,-20,-10,-10,-20,-20,-40),'k':(-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,20,35,0,0,10,35,20)}
for(C,ZI)in B.items():pZ1=lambda Z1:(0,)+tuple(Z2+A[C]for Z2 in Z1)+(0,);B[C]=sum((pZ1(ZI[Z4*8:Z4*8+8])for Z4 in range(8)),());B[C]=(0,)*20+B[C]+(0,)*20
class A6:
	K3='';ZY=0;ZU={};ZV=[];ZW=[];ZX=0;A8=0;A0=[];B2=[1,1];B3=[1,1];B4='e1';B5='e8';B6=0;K4=32;B7='';B73=0;M9=0
	def __init__(Z):
		Z.A7='.....................rnbqkbnr..pppppppp..--------..--------..--------..--------..PPPPPPPP..RNBQKBNR.....................';Z.ZY=0;Z.ZZ()
		for(pos,Z2)in enumerate(Z.A7):
			if Z2 in'prnbqkPRNBQK':Z.ZY^=Z.ZU[Z2,pos]
	def ZZ(Z):
		random.seed(42);ZZ1={}
		for Z2 in'prnbqkPRNBQK':
			for ZZ2 in range(120):ZZ1[Z2,ZZ2]=random.getrandbits(64)
		Z.ZU=ZZ1;Z.ZV=[random.getrandbits(64)for _ in range(4)];Z.ZW=[random.getrandbits(64)for _ in range(8)];Z.ZX=random.getrandbits(64)
	def Y(Z,A1):return Z.O7(A1[0:2]),Z.O7(A1[2:4])
	def O8(Z,O0):return Z.N(O0%10)+str(abs(O0//10-10))
	def O7(Z,Z7):return 10*(abs(int(Z7[1])-8)+2)+(ord(Z7[0])-97)+1
	def O9(Z,pos,new_Z2):
		old_Z2=Z.A7[pos]
		if old_Z2 in'prnbqkPRNBQK':Z.ZY^=Z.ZU[old_Z2,pos]
		if new_Z2 in'prnbqkPRNBQK':Z.ZY^=Z.ZU[new_Z2,pos]
		Z.ZY^=Z.ZW[Z.B73]if Z.B7 else 0;Z.A7=Z.A7[:pos]+new_Z2+Z.A7[pos+1:]
	def I93(Z,Z2):
		if Z2=='k':return[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)]
		elif Z2=='q':return[(0,10),(0,-10),(1,0),(-1,0),(1,10),(1,-10),(-1,10),(-1,-10)]
		elif Z2=='r':return[(0,10),(0,-10),(1,0),(-1,0)]
		elif Z2=='b':return[(1,10),(1,-10),(-1,10),(-1,-10)]
		elif Z2=='n':return[(1,-20),(-1,-20),(2,-10),(-2,-10),(1,20),(-1,20),(2,10),(-2,10)]
		else:return[(0,-10),(1,-10),(-1,-10)]
	def N(Z,O):return chr(O+96)
	def B8(Z,A1):
		l_A7=Z.A7;i=Z.A8%2==0;Z.M9+=1;B0,O=Z.Y(A1);C2=l_A7[B0].lower()
		if l_A7[O]!='-':Z.M9=0
		Z.O9(O,l_A7[B0]);Z.O9(B0,'-');B71=0
		if C2=='p':
			Z.M9=0;B71=abs(B0-O)==20;B72=-1 if i else 1
			if B71:Z.B7=A1[0:1]+str(int(A1[3:4])+B72);Z.B73=ord(A1[0])-ord('a')
			elif A1[2:4]==Z.B7:Z.O9(O-10*B72,'-')
			elif len(A1)>4:Z.O9(O,A1[4:5].upper()if i else A1[4:5])
		elif C2=='k':
			if i:Z.B4=A1[2:4]
			else:Z.B5=A1[2:4]
			if abs(O-B0)==2:Z.O9(O+(1 if O>B0 else-2),'-');Z.O9(B0+(O-B0)//2,'R'if i else'r')
		if not B71:Z.B7='';Z.B73=0
		Z.ZY^=Z.ZX;Z.K3=Z.C6();Z.K4=Z.C7()
	def C4(Z,A1):
		u=Z.P1();u.B6=Z.B6+Z.A4(A1)
		if'e1'in A1:
			for(i,right)in enumerate(u.B2):
				if right:u.ZY^=u.ZV[i]
			u.B2=[0,0]
		elif'a1'in A1:
			if u.B2[0]:u.ZY^=u.ZV[0];u.B2[0]=0
		elif'h1'in A1:
			if u.B2[1]:u.ZY^=u.ZV[1];u.B2[1]=0
		if'e8'in A1:
			for(i,right)in enumerate(u.B3):
				if right:u.ZY^=u.ZV[i+2]
			u.B3=[0,0]
		elif'a8'in A1:
			if u.B3[1]:u.ZY^=u.ZV[2];u.B3[1]=0
		elif'h8'in A1:
			if u.B3[0]:u.ZY^=u.ZV[3];u.B3[0]=0
		u.B8(A1);u.A8+=1;u.B6=-u.B6;u.A0.append(u.K3);return u
	def C5(Z):u=Z.P1();u.A8+=1;u.B6=-Z.B6;return u
	def P1(Z):u=A6();u.A8=Z.A8;u.B4=Z.B4;u.B5=Z.B5;u.K3=Z.K3;u.K4=Z.K4;u.B7=Z.B7;u.M9=Z.M9;u.A7=Z.A7[:];u.A0=Z.A0.copy();u.B2=Z.B2.copy();u.B3=Z.B3.copy();u.ZY=Z.ZY;u.ZU=Z.ZU;u.ZV=Z.ZV;u.ZX=Z.ZX;u.ZW=Z.ZW;return u
	def C7(Z):return 64-Z.K3.count('-')
	def C8(Z):return Z.K4<14 or Z.K4<20 and'q'not in Z.K3.lower()
	def M3(Z,A1):return Z.A4(A1,1)
	def print_u(Z,A7):
		for i in range(12):Z1=A7[i*10:(i+1)*10];print(' '.join(Z1))
	def A4(Z,A1,M4=0):
		i=Z.A8%2==0;l_A7=Z.A7;B0,O=Z.Y(A1);D1=0 if i else 119;to_D1=abs(O-D1);from_D1=abs(B0-D1);d=0;C2=l_A7[B0].lower();D4=l_A7[O].lower()
		if C2!='-':d+=B[C2][to_D1]-B[C2][from_D1]
		if D4!='-':d+=B[D4][to_D1]
		if C2=='p':
			if A1[2:4]==Z.B7:d+=B[C2][to_D1]
			elif len(A1)>4:D7=A1[4:5];d+=B[D7][to_D1]-B['p'][to_D1]
			if Z.ZH(B0):d+=10
			if Z.ZM(B0):d-=15
		elif C2=='k':
			if abs(O-B0)==2:
				if O>B0:d+=B['r'][to_D1-1]-B['r'][to_D1+1]
				else:d+=B['r'][to_D1+1]-B['r'][to_D1-2]
				if M4:d+=60
		return d
	def ZH(Z,O0):
		i=Z.A8%2==0;D11=-10 if i else 10;ZNs=[O0+D11,O0+D11-1,O0+D11+1]
		while 20<=min(ZNs)<=100 and max(ZNs)<=100:
			for pos in ZNs:
				Z2=Z.A7[pos]
				if Z2 in('prnbqk'if i else'PRNBQK'):return 0
			ZNs=[pos+D11 for pos in ZNs]
		return 1
	def ZM(Z,O0):
		i=Z.A8%2==0;D5='P'if i else'p';D11=-10 if i else 10;pos=O0+D11
		while 20<=pos<=100:
			if Z.A7[pos]==D5:return 1
			pos+=D11
		return 0
	def C6(Z):return Z.A7+str(Z.A8%2)
	def N7(Z):return Z.A5(1)
	def A5(Z,N8=0):
		D1=1
		if Z.A8%2==0:i=1;E7=81;E6=31;E5='prnbqk-'
		else:i=0;E7=31;E6=81;E5='PRNBQK-'
		for(O0,Z2)in enumerate(Z.A7):
			if Z2 in'-.'or i==Z2.islower():continue
			E9=Z.O8(O0);K0=Z2.lower()
			if Z2=='p':D1=-1
			if not N8:
				if Z2=='K':
					if Z.B2[0]and Z.A7[96:99]=='--R'and not any(Z.O2(i,Z7)for Z7 in['e1','f1','g1']):yield E9+'g1'
					if Z.B2[1]and Z.A7[91:95]=='R---'and not any(Z.O2(i,Z7)for Z7 in['e1','d1','c1']):yield E9+'c1'
				elif Z2=='k':
					if Z.B3[0]and Z.A7[26:29]=='--r'and not any(Z.O2(i,Z7)for Z7 in['e8','f8','g8']):yield E9+'g8'
					if Z.B3[1]and Z.A7[21:25]=='r---'and not any(Z.O2(i,Z7)for Z7 in['e8','d8','c8']):yield E9+'c8'
				elif K0=='p'and E7<=O0<E7+8 and Z.A7[O0+-10*D1]=='-'and Z.A7[O0+-20*D1]=='-':yield E9+Z.O8(O0+-20*D1)
			for F3 in Z.I93(K0):
				P3=O0+F3[0]+F3[1]*D1
				while 20<P3<99:
					F6=Z.A7[P3]
					if not N8 or N8 and F6 not in'-.':
						F7=Z.O8(P3)
						if K0=='p':
							if O0 in range(E6,E6+8)and F3[0]==0 and F6=='-'or O0 in range(E6,E6+8)and F3[0]!=0 and F6!='-'and F6 in E5:
								for G8 in'qrbn':yield E9+F7+G8
							elif F3[0]==0 and F6=='-'or F3[0]!=0 and F6!='-'and F6 in E5 or F7==Z.B7:yield E9+F7
						elif F6 in E5:yield E9+F7
					if F6!='-'or K0 in'knp':break
					P3=P3+F3[0]+F3[1]*D1
	def E0(Z,i):O1=Z.B4 if i else Z.B5;return Z.O2(i,O1)
	def O2(Z,i,Z7):
		D1=1;E5='PRNBQK-'if i else'prnbqk-';O2=Z.O7(Z7)
		for(O0,Z2)in enumerate(Z.A7):
			if Z2 in'-.'or i==Z2.isupper():continue
			if Z2=='p':D1=-1
			Z2=Z2.lower()
			for F3 in Z.I93(Z2):
				if Z2=='p'and not F3[0]:continue
				P3=O0+F3[0]+D1*F3[1]
				while 20<P3<99:
					F6=Z.A7[P3]
					if F6 in E5 and P3==O2:return 1
					if F6!='-'or Z2 in'knp':break
					P3=P3+F3[0]+D1*F3[1]
		return 0
class F0:
	V=0;S=0;G1=0;G2=0;G3={};ZA=1;ZB=2;ZC=3;ZD=32767
	def R(Z,S,K7,U,V,W,X):print(f"info depth {S} score cp {K7} time {U} nodes {V} nps {W} pv {X}",flush=1)
	def G9(Z):Z.V=0;Z.S=0;Z.G1=0;Z.G2=0;Z.G3.clear()
	def H1(Z,l):
		H2=t();d=l.B6
		for S in range(1,100):
			d=Z.H9(l,S,-Z.ZD,Z.ZD)
			if t()<Z.G2:
				H7=Z.G3.get(l.ZY)
				if H7:H7=H7['N1']
			else:break
			H8=t()-H2;W=math.ceil(Z.V/H8)if H8>0 else 1;pv='';ZP=1;u1=l.C4(H7)
			while ZP<min(6,S):
				ZP+=1;ZQ=Z.G3.get(u1.ZY)
				if not ZQ or not ZQ['N1']:break
				u1=u1.C4(ZQ['N1']);pv+=' '+ZQ['N1']
			Z.R(str(S),str(math.ceil(d)),str(math.ceil(H8*1000)),str(Z.V),str(W),str(H7+pv));yield(S,H7,d)
	def H9(Z,l,S,a,b):
		if t()>Z.G2:return-Z.ZD
		L11=b>a+1;E01=l.E0(l.A8%2==0);S+=E01
		if l.A0.count(l.K3)>2 or l.M9>=100:return 0
		if S<=0:return Z.H93(l,a,b,200)
		e=Z.G3.get(l.ZY,{'M1':2*Z.ZD,'M2':Z.ZB,'M0':-1,'N1':None});Z.V+=1;L2=a
		if e['M0']>=S and e['N1']and not L11:
			if e['M2']==Z.ZA or e['M2']==Z.ZC and e['M1']>=b or e['M2']==Z.ZB and e['M1']<=a:return e['M1']
		if not L11 and not E01 and S<=7 and l.B6>=b+100*S:return l.B6
		if not L11 and not E01 and S<=5:
			ZJ=a-385*S
			if l.B6<=ZJ:
				if S<=2:return Z.H93(l,a,a+1,200)
				d=Z.H93(l,ZJ,ZJ+1,200)
				if d<=ZJ:return d
		T=-Z.ZD-1;d=-Z.ZD;i=l.A8%2==0;L8='RNBQ'if i else'rnbq'
		if not L11 and not E01 and L8 in l.K3:
			d=-Z.H9(l.C5(),S-4,-b,-b+1)
			if d>=b:return b
		if not L11 and not E01 and e['M0']>=S and abs(e['M1'])<Z.ZD and e['N1']:
			d=-Z.H9(l.C4(e['N1']),S-1,-b,-a)
			if d>=b:return b
		I92=0;H7=None
		for F2 in sorted(l.A5(),key=l.M3,reverse=1):
			G7=l.C4(F2)
			if G7.E0(i):continue
			ZK=l.K4==G7.K4;I92+=1;ZL=1
			if not L11 and ZK and S>2 and I92>1:ZL=max(3,math.ceil(math.sqrt(S-1)+math.sqrt(I92-1)))
			if ZL!=1:d=-Z.H9(G7,S-ZL,-a-1,-a)
			if ZL!=1 and d>a or ZL==1 and not(L11 and I92==1):d=-Z.H9(G7,S-1,-a-1,-a)
			if L11 and(I92==1 or d>a):d=-Z.H9(G7,S-1,-b,-a)
			if not H7:H7=F2
			if d>T:
				H7=F2;T=d
				if d>a:
					a=d
					if a>=b:break
		if not I92:return-Z.ZD+l.A8 if E01 else 0
		if t()<Z.G2:
			e['M1']=T
			if H7:e['N1']=H7
			e['M0']=S
			if T<=L2:e['M2']=Z.ZB
			elif T>=b:e['M2']=Z.ZC
			else:e['M2']=Z.ZA
			Z.G3[l.ZY]=e
		else:Z.G3[l.ZY]={'M1':2*Z.ZD,'M2':Z.ZB,'M0':-1,'N1':None}
		return T
	def H93(Z,l,a,b,S):
		if t()>Z.G2:return-Z.ZD
		if l.A0.count(l.K3)>2 or l.M9>=100:return 0
		e=Z.G3.get(l.ZY)
		if e:
			if e['M2']==Z.ZA or e['M2']==Z.ZC and e['M1']>=b or e['M2']==Z.ZB and e['M1']<=a:return e['M1']
		d=l.B6
		if S<=0 or d>=b:return d
		a=max(a,d);I92=0
		for F2 in sorted(l.N7(),key=l.M3,reverse=1):
			G7=l.C4(F2)
			if G7.E0(l.A8%2==0):continue
			if I92==0:Z.V+=1
			I92+=1;d=-Z.H93(G7,-b,-a,S-1)
			if d>a:
				a=d
				if a>=b:return a
		return a
def Q(P):print(P,flush=1)
def main():
	I7=A6();H91=F0()
	while 1:
		try:
			Z3=input()
			if Z3=='quit':sys.exit()
			elif Z3=='uci':Q('pygone 1.6.0\nuciok')
			elif Z3=='ucinewgame':I7=A6();H91.G9()
			elif Z3=='isready':Q('readyok')
			elif Z3.startswith('position'):
				I9=Z3.split();I7=A6()
				for I0 in I9[3:]:I7=I7.C4(I0)
			elif Z3.startswith('go'):
				H91.S=30;J6=1e8;i=I7.A8%2==0;J3=Z3.split()
				for(key,arg)in enumerate(J3):
					if arg=='wtime'and i or arg=='btime'and not i:J6=int(J3[key+1])/1e3
					elif arg=='depth':H91.S=int(J3[key+1])
				H91.G2=t()+max(.75,J6-1);J6=max(2.2,J6/32);H91.G1=t()+J6;H91.V=0;F2=None
				for(S,F2,T)in H91.H1(I7):
					if S>=H91.S or t()>=H91.G1:break
				Q(f"bestmove {str(F2)}")
		except(KeyboardInterrupt,SystemExit):sys.exit()
		except Exception as exc:Q(exc);raise
main()