from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
#our models
from Loader import *
from Player import *
from Texture import *
from Collision import *
from Zombie import *
from Object import *
from World import *
#some extra libraries
from math import *
import sys, pygame,os,numpy,time
#comen
#variables we need
global player1,fovy,window_width,window_height,fullscreen,fireSound,windSound,zombieSound,footSound,world1,yHouse
global paused,sound_BGM,sound_game,worldAudio,houseAudio,houseMusic,windSound,doorSound,doorSlam

paused=0
paused_settings=0

white=[1,1,1]
blue=[1,0,0]
blue=[0,0,1]
green=[0,1,0]
bSize=[0.35,0.35,0.35,0.35,0.35]
bColor=[white,white,white,white,white]


alist1=[#horizontal walls
		[0,0],[1,0],
		[2,0],[18,0],
		[0,4],[6,4],
		[6,6],[13,6],
		[15,3],[18,3],
		[15,6],[18,6],
		[0,9],[2,9],
		[4,9],[18,9],
		#vertical
		[0,0],[0,9],
		[6,0],[6,1.5],
		[6,2.5],[6,7],
		[6,8],[6,9],
		[13,0],[13,1.5],
		[13,2.5],[13,7],
		[13,8],[13,9],
		[15,0],[15,1],
		[15,2],[15,4],
		[15,5],[15,7],
		[15,8],[15,9],
		[18,0],[18,9],
		#staris
		[14,3],[14,7]
		]


lisZombies=[]
lisTexture=[]
lisObjs=[]
lisTools=[]
lisDoors=[]
lisSpecialDoors=[]
lisHouse=[]
#all keyboards buttons have value 0 if no button pressed
keyState=[0 for i in range(0,256)]


#30ms per frame
time_interval=30
PI=3.14159265359

pauseimage_id,pauseimage=0,0
#intialization of opengl

def texInit(name,id):
	global pauseimage_id,pauseimage
	imgload=pygame.image.load(name) #LOAD IMAGE
	imgdata=pygame.image.tostring(imgload,"RGB",1) #CONVERT IMAGE TO RAW DATA
	width=imgload.get_width()
	height=imgload.get_height()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[id]) #GIVE IT AN ID THEN SET PARAMETERS
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,imgdata)
	#ASSING THE IMAGE TO A 2D TEXTURE WITH THE GIVEN SPECIFICATIONS ^


def init1():
	global pauseimage_id,pauseimage
	glClearColor(1,1,1,0)
	#glutSetCursor(GLUT_CURSOR_NONE)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.2, 0.2, 0.2, 1.0])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1.0])
	glEnable(GL_LIGHT1)
	glLightfv(GL_LIGHT1, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.01, 0.01, 0.01, 1.0])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1.0])
	glDisable(GL_COLOR_MATERIAL)

	pauseimage_id=glGenTextures(2)
	texInit("Menu\Images\Paused.jpg",0)
	pauseimage=glGenLists(1) #GENERATE A GL.LIST THAT APPLIES ANY GIVEN TEXTURE
	glNewList(pauseimage,GL_COMPILE) #COMPLIE THE LIST -- BEGIN
	glEnable(GL_TEXTURE_2D) 
	glBegin(GL_QUADS) #DRAWING TEXTURES ON QUADS
	glTexCoord(0,0)
	glVertex2d(0,0)
	glTexCoord(1,0)
	glVertex2d(1280,0)
	glTexCoord(1,1)
	glVertex2d(1280,720)
	glTexCoord(0,1)
	glVertex2d(0,720)
	glEnd() #END DRAWING
	glDisable(GL_TEXTURE_2D)
	glEndList() #END THE LIST

	glEnable(GL_DEPTH_TEST)
	#glShadeModel(GL_SMOOTH)
	glEnable(GL_BLEND)
	glutIgnoreKeyRepeat( GL_TRUE )
	if(fullscreen):
		glutFullScreen()

#read setting from file like (the resolution , fovy etc...)
def setting():
	global window_width,window_height,fullscreen,fovy,sound_BGM,sound_game
	f= open('Option/op.in').read().split()
	window_width=int(f[2])
	window_height=int(f[5])
	fullscreen=int(f[8])
	fovy=int(f[11])
	sound_BGM=int(f[14])
	sound_game=int(f[17])


def displayPause():
	global current_H,current_W,white,blue,blue,bColor,bSize
	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,1280,0,720,-3,3)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)
	drawTextB(bColor[0], "SAVE GAME", 128, 345.6, bSize[0])
	drawTextB(bColor[1], "LOAD GAME", 128, 288, bSize[1])
	drawTextB(bColor[2], "SETTINGS", 128, 230.4, bSize[2])
	drawTextB(bColor[3], "EXIT",  128, 172.8, bSize[3])
	glColor(1,1,1)
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)
	glutSwapBuffers()

def displaySettings():
	global bColor,bSize,white,blue,blue
	global current_W,current_H,fullscreen,sound_game,sound_BGM,bSound1,bSound2
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,1280,0,720,-3,3)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)

	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)
	glBindTexture(GL_TEXTURE_2D, pauseimage_id[0])
	glCallList(pauseimage)

	drawTextB([.5,.5,.6], "SETTINGS", 128, 450, 0.3)
	drawTextB([.4,.4,.4], "GRAHPICS", 128, 345.6, 0.4)
	if fullscreen:
		drawTextB(bColor[1], "FULLSCREEN", 128, 288, bSize[1])
	else:
		drawTextB(bColor[1], "WINDOWED", 128, 288, bSize[1])
	drawTextB(bColor[2], "MUSIC: "+str(sound_BGM), 128, 230.4, bSize[2])
	drawTextB(bColor[3], "SOUNDS: "+str(sound_game), 128, 172.8, bSize[3])
	drawTextB(bColor[4], "BACK", 128, 115.2, bSize[4])
	glColor(1,1,1)

	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)

	bSound1.set_volume(.01*sound_game)
	bSound2.set_volume(.01*sound_game)
	fireSound.set_volume(0.1*sound_game)
	windSound.set_volume(0.04*sound_BGM)
	houseMusic.set_volume(0.02*sound_BGM)
	zombieSound.set_volume(0.1*sound_game)
	footSound.set_volume(0.1*sound_game)
	doorSound.set_volume(0.1*sound_game)
	doorSlam.set_volume(0.1*sound_game)

	opfile=open('Option/op.in','r')
	setOp=opfile.read().split()
	setOp[8]=str(fullscreen)
	setOp[14]=str(sound_BGM)
	setOp[17]=str(sound_game)
	opfile=open('Option/op.in','w')
	for item in setOp:
		opfile.write(str(item))
		opfile.write(" ")
	opfile.close()
	glutSwapBuffers()

#detect if bullet collied with zombie ?
def bullet(player, enemy):
	#direction of bullet
	xd=-sin(player.theta)
	yd=sin(player.thetaUp)
	zd=cos(player.theta)

	#position of the player
	xs=player.x
	ys=player.y
	zs=player.z

	#position of the enemy 
	xc=enemy.x
	yc=enemy.y+7
	zc=enemy.z

	#r is the raidus of sphere which we check if we collied with it ? sphere==zombie's head
	r=0.5
	#calculation
	a=xd**2+yd**2+zd**2
	b = 2*(xd*(xs-xc)+ yd*(ys-yc) + zd*(zs-zc))
	c = (xs-xc)**2 + (ys-yc)**2 + (zs-zc)**2 - r**2
	M= b**2 - 4*a*c

	return M> 0

def axe(player,enemy):
	distance=((enemy.x-player.x)**2+(enemy.y-player.y+player.tall)**2+(enemy.z-player.z)**2)**0.5
	return distance<10


#Window Width = 2.2 , Depth = .2 , Height = 1.8 , Y= 3+0.55
def draw_window(x,y,z,scale,rot=0):

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glRotate(rot,0,1,0)
	glTranslate(x,y,z)
	glDisable(GL_LIGHTING)
	#glEnable(GL_COLOR_MATERIAL) #AFFECT THE QUAD WITH COLOR_MATERIAL
	#glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE) #HOW THE QUAD WILL BE AFFECTED WITH COLOR MATERIAL
	glColor4f(0.3,0.3,0.4,0.7)
	glBegin(GL_QUADS)
	glVertex(0,0,0)
	glVertex(0,0,2.2*scale)
	glVertex(0,1.8*scale,2.2*scale)
	glVertex(0,1.8*scale,0)
	glEnd()
	#glColor(0,0,0) #IF YOU WANT TO MAKE THE GAME MORE DARK, TRY THIS
	glDisable(GL_BLEND)
	glEnable(GL_LIGHTING)
	#glColor4f(1,1,1,0)

	glDisable(GL_COLOR_MATERIAL)

LastFps=0
def display():
	global houseAudio,worldAudio,houseMusic,windSound,LastFps
	global current_H,current_W
	t=time.time()#store the time when we enter the function (to calculate the amount of time this function needs)
	global player1,yHouse
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	player1.updateCamera()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glLightfv(GL_LIGHT0, GL_POSITION,  (player1.x, player1.y, player1.z,1))
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 25)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [-sin(player1.theta), sin(player1.thetaUp), cos(player1.theta)])
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT,20)

	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)

	glDisable(GL_LIGHT0)
	glLoadIdentity()
	player1.displayTool()
	if(player1.x>90 and player1.x<95 and player1.z>19 and player1.z<37):
		yHouse=(player1.z-19)*5/6+world1.height(26,5)
	if(not(player1.x>25 and player1.x<115 and player1.z>4 and player1.z<49)):
		player1.jump(world1.height(player1.x,player1.z))
		yHouse=world1.height(player1.x,player1.z)
		if not worldAudio:
			houseMusic.fadeout(3000)
			windSound.play(loops=-1,fade_ms=3000)
			worldAudio=1
			houseAudio=0
	else:
		if keyState[ord("f")]:
			glEnable(GL_LIGHT0)
		player1.jump(yHouse)
		print("in the house")
		if not houseAudio:
			windSound.fadeout(3000)
			houseMusic.play(loops=-1,fade_ms=3000)
			worldAudio=0
			houseAudio=1


	glLoadIdentity()
	glLightfv(GL_LIGHT1, GL_POSITION,  (0, 999, 0, 0))

	
	#display all texture in the world (like sky)
	glDisable(GL_COLOR_MATERIAL)

	for i in range(len(lisTexture)):
		glLoadIdentity()
		glColor(1,1,1)
		glDisable(GL_LIGHTING)
		lisTexture[i].disp()
		glEnable(GL_LIGHTING)

	for i in range(len(lisHouse)):
		glLoadIdentity()
		lisHouse[i].disp()
	#display all object in the world
	for i in range(len(lisObjs)):
		glLoadIdentity()
		lisObjs[i][0].disp()
	for i in range(len(lisDoors)):
		glLoadIdentity()
		lisDoors[i][0].dispDoor(doorSound)
	#display all zombies,make them walk.
	for i in range(len(lisZombies)):
		lisZombies[i].height(world1.height(lisZombies[i].x,lisZombies[i].z))
		lisZombies[i].dist(player1,zombieSound)
		glLoadIdentity()
		lisZombies[i].disp()
		lisZombies[i].walk(player1)
		#if(lisZombies[i].criticalHit()==False):
			#lisZombies[i7].hit()

	for i in range(len(lisSpecialDoors)):
		glLoadIdentity()
		lisSpecialDoors[i][0].dispDoor(doorSound)
		Epressed=near(player1,None,lisSpecialDoors,keyState)
		if(Epressed):
			Pass=displayPass()
			if Pass==lisSpecialDoors[i][2]:
				lisSpecialDoors[i][0].animation=1
				lisSpecialDoors[i][0].radius=-1
			else:
				Text("wrong pass")
				


	glLoadIdentity()
	draw_window(25.3,22.5,10.9,4.2)

	world1.disp()
	player1.move(keyState,alist1,lisObjs,lisDoors,lisSpecialDoors)

	Text(str(int(1/(time.time()-t))),-0.96,0.92,0.0005,2,1,0,0)
	glutSwapBuffers()
	if fullscreen:
		glutFullScreen()
	else:
		glutPositionWindow(20,30)
		glutReshapeWindow(window_width, window_height)
	#print(player1.x,player1.z)
	
	print(str(int((1/(time.time()-t)+LastFps)/2)))
	LastFps=int((1/(time.time()-t)+LastFps)/2)
	#print((time.time()-t)*1000)

def drawTextB(lis, string,x,y,textsize=0.35):
	glLineWidth(4)
	glLoadIdentity()
	glColor(lis[0],lis[1],lis[2]) #GIVEN THE COLOR IN A LIST
	glTranslate(x,y,1)
	glScale(textsize,textsize,textsize)
	string=string.encode()
	for char in string:
		glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, char)

def drawText(string, x, y,scale=0.0005,w=2,r=0,g=0,b=0):
	glLineWidth(w)
	glColor(r,g,b)  # Yellow Color
	glTranslate(x-len(string)/50,y,0)
	glScale(scale,scale,1)
	string = string.encode() # conversion from Unicode string to byte string
	for c in string:
		glutStrokeCharacter(GLUT_STROKE_ROMAN , c )  


def Text(s,x=0,y=0,scale=0.0005,w=2,r=0,g=0,b=0):
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(-1,1,-1,1,-1,1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	glDisable(GL_LIGHTING)
	drawText(s,x,y,scale,w,r,g,b)
	glEnable(GL_LIGHTING)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()

def displayPass():
	s=input("enter the pass:")
	return s

def Timer(v):
	global paused
	if paused and not paused_settings:
		glDisable(GL_LIGHTING)
		displayPause()
	elif paused and paused_settings:
		glDisable(GL_LIGHTING)
		displaySettings()
	else:
		glEnable(GL_LIGHTING)
		display()
	glutTimerFunc(time_interval,Timer,1)

#call function if any key pressed 
def keyDown(key,xx,yy):
	global window_height,window_width,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2
	global player1,jum,keyState,paused


	if not paused:
		if key==b"\x1b":
			paused=1
		if(key==b" "):
			player1.jumping=1
		if (key==b"f"):
			keyState[ord(key.decode('unicode_escape'))]=not keyState[ord(key.decode('unicode_escape'))]
		else:
			keyState[ord(key.decode('unicode_escape'))]=1

	else:
		if key==b"\x1b":
			paused=0
		if not paused_settings:
			if key==b'\r': #ENTER BUTTON \r
				if bColor[0]==blue:
					print("SAVE GAME")
				if bColor[1]==blue:
					print("LOAD GAME")
				if bColor[2]==blue:
					paused_settings=1
				if bColor[3]==blue:
					sys.exit()

		else:
			bSound2.play()
			if key==b'\r':
				if bColor[1]==blue:
					if fullscreen:
						fullscreen=0
					else:
						fullscreen=1
				if bColor[2]==blue:
					if sound_BGM==100:
						sound_BGM=0
					else:
						sound_BGM+=10
				if bColor[3]==blue:
					if sound_game==100:
						sound_game=0
					else:
						sound_game+=10
				if bColor[4]==blue:
					paused_settings=0


#call function when the key is (up) (no presse)
def keyUp(key,xx,yy):
	global keyStates
	if not paused:
		if key != b"f":
				keyState[ord(key.decode('unicode_escape'))]=0

#used for special key like SHIFT

currentButton=0 #CURRENT BUTTON SELECTED BY KEYBOARD
upArrow,downArrow=101,103 #VALUES FOR UP AND DOWN ARROW
def specialKey(key,xx,yy):
	global bColor,currentButton,upArrow,downArrow
	global window_height,window_width,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2
	global player1, keyState

	if not paused:
		keyState[112]=not keyState[112]
	else:
		if not paused_settings:

			if key==upArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==0:
					currentButton=3
				else:
					currentButton-=1
				bColor=[white,white,white,white,white]
				bSize[currentButton]=0.4
				bColor[currentButton]=blue
				

			elif key==downArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==3 or currentButton==4:
					currentButton=0
				else:
					currentButton+=1
				bColor=[white,white,white,white,white]
				bColor[currentButton]=blue
				bSize[currentButton]=0.4
				

		else:
			#SETTINGS
			if key==upArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==1:
					currentButton=4
				else:
					currentButton-=1
				bColor=[white,white,white,white,white]
				bSize[currentButton]=0.4
				bColor[currentButton]=blue
				

			elif key==downArrow:
				bSound1.play()
				bSize[currentButton]=0.35
				if currentButton==4:
					currentButton=1
				else:
					currentButton+=1
				bColor=[white,white,white,white,white]
				bColor[currentButton]=blue
				bSize[currentButton]=0.4

#get the mouse position in the screen 
def mouseMove(x,y):
	global window_height,window_width,PI,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2

	if paused:
		y=current_H-y #LET THE MOUSE COORDINATES START FROM BOTTOM LEFT NOT TOP LEFT
		y=y*window_height/current_H #FIXING THE MOUSE SCREEN AREA IF RESIZED
		x=x*window_width/current_W

		#RESET BUTTONS TO DEFAULTS IF NO HIGHLIGHTED
		bColor=[white,white,white,white,white]
		bSize=[0.35,0.35,0.35,0.35,0.35]
		#CHECK IF THE MOUSE IS NOW HIGHLIGHTING ANY BUTTON
		if (x>=128*window_width/1280 and x<=420*window_width/1280): #NEWGAME
			if(y<390*window_height/720 and y>345*window_height/720):
					bColor[0]=blue
					bSize[0]=0.4
		
		if (x>=128*window_width/1280 and x<=460*window_width/1280): #LOADGAME
			if(y<330*window_height/720 and y>285*window_height/720):
					bColor[1]=blue
					bSize[1]=0.4
					
		if (x>=128*window_width/1280 and x<=430*window_width/1280): #SETTINGS
			if(y<275*window_height/720 and y>230*window_height/720):
					bColor[2]=blue
					bSize[2]=0.4
					
		if (x>=128*window_width/1280 and x<=400*window_width/1280): #CblueITS
			if(y<215*window_height/720 and y>170*window_height/720):
					bColor[3]=blue
					bSize[3]=0.4
					
		if (x>=128*window_width/1280 and x<=300*window_width/1280): #EXIT
			if(y<160*window_height/720 and y>115*window_height/720):
					bColor[4]=blue
					bSize[4]=0.4
	else:
		if(x<2):
			glutWarpPointer( window_width-2 , y )
		if(x>window_width-2):
			glutWarpPointer(2,y)

		player1.theta=(PI*x)/683-PI
		player1.thetaUp=-(PI*y)/768+PI/2

#get the mouse click 
def mouseShoot(key,state,x,y):
	global window_height,window_width,PI,current_H,current_W
	global bSize,bColor,blue,white,blue,current_H,current_W,bSound1,bSound2
	global paused_settings,bColor,blue
	global fullscreen,sound_game,sound_BGM,bSound1,bSound2
	if paused:
		if not paused_settings:
			if bColor[0]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					print("SAVE GAME")
					bSound2.play()
			if bColor[1]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					print("LOAD GAME")
					bSound2.play()
			if bColor[2]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					paused_settings=1
			if bColor[3]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					sys.exit()

		else: #SETTTINGS
			if bColor[1]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if fullscreen:
						fullscreen=0
					else:
						fullscreen=1
			if bColor[2]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if sound_BGM==100:
						sound_BGM=0
					else:
						sound_BGM+=10
			if bColor[3]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					if sound_game==100:
						sound_game=0
					else:
						sound_game+=10
			if bColor[4]==blue:
				if key==GLUT_LEFT_BUTTON and state==GLUT_UP:
					bSound2.play()
					paused_settings=0


	else:
		if(key==0 and state==0 and player1.animation==0):
			player1.animation=1
			if(player1.t==0):
				fireSound.stop()
				fireSound.play()
				for i in range(len(lisZombies)):
					if(bullet(player1,lisZombies[i]) ):
						del lisZombies[i]#die
						break
			else:
				for i in range(len(lisZombies)):
					print(axe(player1,lisZombies[i]))
					print(lisZombies[i].health)
					if(axe(player1,lisZombies[i])):
						lisZombies[i].health-=50
					if(lisZombies[i].health<0):
						del lisZombies[i]
						break

		if((key==3 or key==4 )and state==0):
			player1.updateTool()
			#get next gun
			#play voice

def main1():
	t=time.time()#to calculate time needed to load the game
	global current_H,current_W
	global player1,lisTexture,fireSound,windSound,zombieSound,footSound,world1,alist1,yHouse,lisSpecialDoors,lisHouse
	global sound_BGM,sound_game,worldAudio,houseAudio,houseMusic,windSound,doorSound,doorSlam,bSound2,bSound1
	pygame.init()
	setting()
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	#glutInitWindowSize(window_width,window_height)
	#glutInitWindowPosition(0,0)
	#glutCreateWindow(b"WAR")
	init1()

	current_W=glutGet(GLUT_WINDOW_WIDTH)
	current_H=glutGet(GLUT_WINDOW_HEIGHT)

	for i in range(len(alist1)):
		alist1[i][0]=alist1[i][0]*5+25
		alist1[i][1]=alist1[i][1]*5+4

	
	Zlis=[]
	G1lis=[]
	G2lis=[]
	M1lis=[]
	M2lis=[]

	'''for i in range(1,115,2):#115
		sr="Monster_"
		ss=""
		for j in range(0,5-int(log10(i))):
			ss+=str(0)
		sr+=ss+str(i)+".obj"

		Zlis.append(sr)
	Zlis=[OBJ(Zlis[i],False,"Models/MonsterLowQ/Low/") for i in range (len(Zlis))]'''

	for i in range(1,11):#11
		sr="Gun_"
		ss=""
		for j in range(0,5-int(log10(i))):
			ss+=str(0)
		sr+=ss+str(i)+".obj"

		G1lis.append(sr)
	G1lis=[OBJ(G1lis[i],False,"Models/Gun/") for i in range (len(G1lis))]


	for i in range(1,15):#24
		sr="Axe_"
		ss=""
		for j in range(0,5-int(log10(i))):
			ss+=str(0)
		sr+=ss+str(i)+".obj"

		M1lis.append(sr)
	M1lis=[OBJ(M1lis[i],False,"Models/Axe/") for i in range (len(M1lis))]

	

	#create zombies
	#lisZombies.append(zombie(100,Zlis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[-30,0,-30],30,0.5,-90))
	#lisZombies.append(zombie(100,Zlis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[10,0,10],30,0.5,-90))
	#lisZombies.append(zombie(100,Zlis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[-20,0,-20],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[30,0,0],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[0,0,50],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[1,0,1],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[5,0,30],30,0.5,-90))
	#lisZombies.append(zombie(100,alis,[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[OBJ("Monster_000001.obj",False,"Models/MonsterLowQ/Low/")],[0,0,30],30,0.5,-90))

	#create the SKY
	

	lisTexture.append(texture('nightsky_up.jpg',[[-1,10000,-1],[-1,10000,1],[1,10000,1],[1,10000,-1]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_up.jpg',[[-1000,1000,-1000],[-1000,1000,1000],[1000,1000,1000],[1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_ft.jpg',[[-1000,1000,1000],[-1000,-1000,1000],[1000,-1000,1000],[1000,1000,1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_lf.jpg',[[1000,1000,1000],[1000,-1000,1000],[1000,-1000,-1000],[1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_bk.jpg',[[1000,1000,-1000],[1000,-1000,-1000],[-1000,-1000,-1000],[-1000,1000,-1000]],[[1,0],[0,0],[0,1],[1,1]],1))
	lisTexture.append(texture('nightsky_rt.jpg',[[-1000,1000,-1000],[-1000,-1000,-1000],[-1000,-1000,1000],[-1000,1000,1000]],[[1,0],[0,0],[0,1],[1,1]],1))

	world1=world('world.png',-500,-500)
	world1.render(4,100)
	yHouse=world1.height(26,5)
	lisHouse.append(obje([OBJ("House.obj",False,"Models/House/")],0,[25,world1.height(25,4)+0.1,4],-1,0.05,0))


	Dlis=[OBJ("Door1.obj",False,"Models/Door1/")]
	#first door
	lisDoors.append([obje(Dlis,0,[32.5,world1.height(32.5,4),4],3,0.05,0,0,1),"open the Door"])
	#first floor doors
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4),14],3,0.05,90,0,1),"open the Door"])
	lisSpecialDoors.append([obje(Dlis,0,[90,world1.height(32.5,4),14],3,0.05,90,1,0),"write the password","HELP!"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),11.5],3,0.05,90,0,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),26.5],3,0.05,90,0,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),41.5],3,0.05,90,0,1),"open the Door"])
	#second floor doors
	lisSpecialDoors.append([obje(Dlis,0,[100,world1.height(32.5,4)+15,41.5],3,0.05,90,0,0),"write the password","Done"])
	lisDoors.append([obje(Dlis,0,[90,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"open the Door"])
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"open the Door"])


	#create some sound
	fireSound=pygame.mixer.Sound("Sounds/gun_fire.wav")
	fireSound.set_volume(0.1*sound_game)

	windSound=pygame.mixer.Sound("Sounds/Wind.wav")
	windSound.set_volume(0.04*sound_BGM)
	windSound.play(-1)
	worldAudio=1

	houseMusic=pygame.mixer.Sound("Sounds/Nightmare.wav")
	houseMusic.set_volume(0.02*sound_BGM)
	houseAudio=0

	zombieSound=pygame.mixer.Sound("Sounds/zombieSound.wav")
	zombieSound.set_volume(0.1*sound_game)

	footSound=pygame.mixer.Sound("Sounds/FootStep.wav")
	footSound.set_volume(0.1*sound_game)

	doorSound=pygame.mixer.Sound("Sounds/DoorOpen.wav")
	doorSound.set_volume(0.1*sound_game)

	doorSlam=pygame.mixer.Sound("Sounds/DoorSlam.wav")
	doorSlam.set_volume(0.1*sound_game)

	bSound1=pygame.mixer.Sound("Menu\Audio\ButtonScroll.wav")
	bSound2=pygame.mixer.Sound("Menu\Audio\ButtonSelect.wav")

	player1=player(fovy,window_width,window_height,footSound,[G1lis,M1lis])


	glutKeyboardFunc(keyDown)
	glutKeyboardUpFunc(keyUp)
	glutSpecialFunc(specialKey)
	glutPassiveMotionFunc(mouseMove)
	glutMouseFunc(mouseShoot)
	glutDisplayFunc(display)
	glutTimerFunc(time_interval,Timer,1)
	
	print((time.time()-t)*1000)#print the time needed to load 
	glutMainLoop()

if __name__=="__main__":
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1366,768)
	glutInitWindowPosition(0,0)
	glutCreateWindow(b"WAR")
	main1()