from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 

from math import *
class zombie:
	def __init__(self,health=100,OBJ1=None,lis=[0,0,0],raidus=5,scale=1,rotate=0,zombieSound=None):
		self.CurrentOBJ=OBJ1
		self.OBJ1=OBJ1

		self.tall=-1

		self.x=lis[0]
		self.y=lis[1]
		self.z=lis[2]

		self.raidus=raidus
		self.scale=scale
		self.rotate=rotate
		
		self.health=health
		self.zombieSound=zombieSound
		self.animation=0
		self.i=0

	def height(self,height):
		self.y=height+self.tall

	#calculate the distance betwwen zombie and the player 
	#if the zombie is too close play some SOUND !!! :D 
	def dist(self,player,zombieSound):
		distance=((self.x-player.x)**2+(self.y-player.y+player.tall)**2+(self.z-player.z)**2)**0.5

		if(distance<self.raidus):
			if(self.animation==0):
				zombieSound.play()
			self.animation=1
			if(distance<3):
				return True		#mean player died
		return False			#mean player didn't die

	#display the zombie and make appropriate translation and ....
	def disp(self):
		glTranslate(self.x,self.y,self.z)
		glScale(self.scale,self.scale,self.scale)
		glRotate(self.rotate,0,1,0)
		glTranslate(14,0,0)
		if(self.i>=len(self.CurrentOBJ)):
					self.i=30
		glCallList(self.CurrentOBJ[self.i].gl_list)
		if(self.animation==1):
			self.i+=1

	#make the zombie to walk toward the player
	def walk(self,player):
		theta=0
		if(player.x-self.x<0 and player.z-self.z<0):
			theta=180
		elif(player.x-self.x<0):
			theta=360
		elif(player.z-self.z<0):
			theta=180

		if(self.z-player.z != 0):
			self.rotate=atan((player.x-self.x)/(player.z-self.z))*180/3.14-90+theta
		if(self.animation):
			if(self.x>player.x+0.1):
				self.x-=0.1
			elif(self.x<player.x-0.1):
				self.x+=0.1
			if(self.z>player.z+0.1):
				self.z-=0.1
			elif(self.z<player.z-0.1):
				self.z+=0.1

	def walk2(self,player):
		#self.rotate=atan((self.x-player.x)/(self.z-player.z))*180/3.14-90
		if(self.animation):
			if(self.x>player.x+0.1):
				self.x+=1
			elif(self.x<player.x-0.1):
				self.x-=1
			if(self.z>player.z+0.1):
				self.z+=1
			elif(self.z<player.z-0.1):
				self.z-=1


