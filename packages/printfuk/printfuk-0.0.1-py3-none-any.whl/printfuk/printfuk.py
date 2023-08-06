import random
import subprocess
import time
global chars
chars = [chr(x) for x in range(32,592)]+[chr(x) for x in range(647,670)]+[chr(x) for x in range(688,767)]+[chr(x) for x in range(880,1024)]+[chr(x) for x in range(7936,8191)]
def getRandomChar():
	global chars
	x= random.randint(0,int(len(chars)*1.02))
	if x>=len(chars):
		return ""
	c= chars[x]
	return c
def __break(S,color=88,cmod=0.5):
	i=random.randint(0,100)
	n = 0;
	N=len(S)*cmod
	while i>=5 and n<=N:
		c = getRandomChar()
		i = random.randint(0,len(S)-1)
		
		S=S[:i]+c+S[i+1:]
		n+=1
		i=random.randint(0,100)
	strEffect = u"\u001b[38;5;"+color+"m\033[5m"
	reset = "\u001b[0m"
	return strEffect+S+reset
def __printHelper(S):
	subprocess.run(["echo", "-ne",S])
def print(*args,**kwargs):
	_string = args[0]
	if len(args)>1:
		for s in args[1:]:
			_string+=" "+s
	delay=.1
	end="\n"
	color=88
	startAfter=0
	maxCharMod=.5

	if "delay" in kwargs:
		delay = kwargs['delay']
	if "color" in kwargs:
		color = kwargs['color']
	color=str(color)
	if "startAfter" in kwargs:
		startAfter = kwargs['startAfter']
	if "maxCharMod" in kwargs:
		maxCharMod = kwargs['maxCharMod']
	if "end" in kwargs:
		end = kwargs['end']

	if delay<0:
		delay=0.1	
	if maxCharMod>1:
		maxCharMod=1
	if maxCharMod<=0:
		maxCharMod=0.5

	if len(end)>1:
		end=__break(end,color,maxCharMod)

	
	S = ""
	i=0
	st=""
	if delay>0:
		j=0
		for x in _string:
			j+=1
			S+=x
			if i>=startAfter:
				st=__break(S,color,maxCharMod)
			if j==len(_string):
				subprocess.run(["echo", "-ne",st])
			else:
				subprocess.run(["echo", "-ne",st+'\r'])
		
			time.sleep(delay)
		subprocess.run(["echo", "-ne",end])
	else:
		st=__break(_string,color,maxCharMod)
		subprocess.run(["echo", "-ne",st])
		subprocess.run(["echo", "-ne",end])
#print('test','string',delay=0.01,end='\n')
