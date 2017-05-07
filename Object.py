from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 

class obje:
	def __init__(self,OBJ=None,lis=[0,0,0],raidus=0.5,scale=1,rotate=0):
		self.OBJ=OBJ

		self.x=lis[0]
		self.y=lis[1]
		self.z=lis[2]

		self.raidus=raidus
		self.scale=scale
		self.rotate=rotate
		
		self.animation=1
		self.i=0

	def updatePosition(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z

	def setHeight(self,height):
		self.height=height


	def disp(self):
		glTranslate(self.x,self.y,self.z)
		glScale(self.scale,self.scale,self.scale)
		glRotate(self.rotate,0,1,0)
		if(self.i>=len(self.OBJ)):
			self.i=0
		glCallList(self.OBJ[self.i].gl_list)
		if(self.animation==1):
			self.i+=1


