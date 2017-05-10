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

#variables we need
global player1,fovy,window_width,window_height,window_full_screen,fireSound,mainSound,zombieSound,footSound,world1,yHouse
global sound_BGM,sound_game

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
#all keyboards buttons have value 0 if no button pressed
keyState=[0 for i in range(0,256)]
jum=0

#30ms per frame
time_interval=30
PI=3.14159265359

#intialization of opengl
def init():
	glClearColor(1,1,1,0)
	#glutSetCursor(GLUT_CURSOR_NONE)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1.0])
	glEnable(GL_LIGHT1)
	glLightfv(GL_LIGHT1, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.01, 0.01, 0.01, 1.0])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1.0])
	glDisable(GL_COLOR_MATERIAL)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_BLEND)
	glutIgnoreKeyRepeat( GL_TRUE )
	if(window_full_screen):
		glutFullScreen()

#read setting from file like (the resolution , fovy etc...)
def setting():
	global window_width,window_height,window_full_screen,fovy,sound_BGM,sound_game
	f= open('Option/op.in').read().split()
	window_width=int(f[2])
	window_height=int(f[5])
	window_full_screen=int(f[8])
	fovy=int(f[11])
	sound_BGM=float(f[14])
	sound_game=float(f[17])

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
	print(distance)
	return distance<10


#Window Width = 2.2 , Depth = .2 , Height = 1.8 , Y= 3+0.55
def draw_window(x,y,z,scale,rot=0):
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glRotate(rot,0,1,0)
	glTranslate(x,y,z)
	glEnable(GL_COLOR_MATERIAL) #AFFECT THE QUAD WITH COLOR_MATERIAL
	glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE) #HOW THE QUAD WILL BE AFFECTED WITH COLOR MATERIAL
	glColor4f(0.3,0.3,0.4,0.7)
	glBegin(GL_QUADS)
	glVertex(0,0,0)
	glVertex(0,0,2.2*scale)
	glVertex(0,1.8*scale,2.2*scale)
	glVertex(0,1.8*scale,0)
	glEnd()
	#glColor(.15,.15,.15) #IF YOU WANT TO MAKE THE GAME MORE DARK, TRY THIS
	glDisable(GL_BLEND)
	glDisable(GL_COLOR_MATERIAL)

def display():
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

	glLoadIdentity()
	player1.displayTool()
	if(player1.x>90 and player1.x<95 and player1.z>19 and player1.z<37):
		yHouse=(player1.z-19)*5/6+world1.height(26,5)
	if(not(player1.x>25 and player1.x<115 and player1.z>4 and player1.z<49)):
		player1.jump(world1.height(player1.x,player1.z))
		yHouse=world1.height(player1.x,player1.z)
	else:
		player1.jump(yHouse)
		print("in the house")

	glLoadIdentity()
	glLightfv(GL_LIGHT1, GL_POSITION,  (0, 999, 0, 0))
	glLoadIdentity()

	glTranslate(player1.x-sin(player1.theta), player1.y+sin(player1.thetaUp), player1.z+cos(player1.theta))
	glutWireSphere(0.01,10,10)
	
	#display all texture in the world (like sky)
	glDisable(GL_COLOR_MATERIAL)
	for i in range(len(lisTexture)):
		glLoadIdentity()
		lisTexture[i].disp()
	#display all object in the world
	for i in range(len(lisObjs)):
		glLoadIdentity()
		lisObjs[i][0].disp()
	for i in range(len(lisDoors)):
		glLoadIdentity()
		lisDoors[i][0].dispDoor()
	#display all zombies,make them walk.
	for i in range(len(lisZombies)):
		lisZombies[i].height(world1.height(lisZombies[i].x,lisZombies[i].z))
		lisZombies[i].dist(player1,zombieSound)
		glLoadIdentity()
		lisZombies[i].disp()
		lisZombies[i].walk(player1)
		#if(lisZombies[i].criticalHit()==False):
			#lisZombies[i].hit()
	for i in range(len(lisSpecialDoors)):
		glLoadIdentity()
		lisSpecialDoors[i][0].dispDoor()
		Epressed=near(player1,None,lisSpecialDoors,keyState)
		if(Epressed):
			Pass=displayPass()
			if Pass==lisSpecialDoors[i][2]:
				lisSpecialDoors[i][0].animation=1
				lisSpecialDoors[i][0].radius=-1
			else:
				print("wrong pass")


	glLoadIdentity()	
	draw_window(25.3,22.5,10.9,4.2)
	world1.disp()
	player1.move(keyState,alist1,lisObjs,lisDoors)

	glutSwapBuffers()


	#print(player1.x,player1.z)
	#print((time.time()-t)*1000)

def displayPass():
	s=input("enter the pass:")
	return s

def Timer(v): 
	display() 
	glutTimerFunc(time_interval,Timer,1)

#call function if any key pressed 
def keyDown(key,xx,yy):
	global player1,jum,keyState
	if(key==b" ") and jum==0:
		player1.jumping=1
	keyState[ord(key.decode('unicode_escape'))]=1

#call function when the key is (up) (no presse)
def keyUp(key,xx,yy):
	global keyStates
	keyState[ord(key.decode('unicode_escape'))]=0

#used for special key like SHIFT
def specialKey(key,xx,yy):
	global player1, keyState
	keyState[112]=not keyState[112]

#get the mouse position in the screen 
def mouseMove(x,y):
	global window_height,window_width,PI
	if(x<2):
		glutWarpPointer( window_width-2 , y )
	if(x>window_width-2):
		glutWarpPointer(2,y)

	player1.theta=(PI*x)/683-PI
	player1.thetaUp=-(PI*y)/768+PI/2

#get the mouse click 
def mouseShoot(key,state,x,y):
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

def main():
	t=time.time()#to calculate time needed to load the game

	global player1,lisTexture,fireSound,mainSound,zombieSound,footSound,world1,alist1,yHouse,lisSpecialDoors
	pygame.init()
	setting()
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(window_width,window_height)
	glutInitWindowPosition(0,0)
	glutCreateWindow(b"WAR")
	init()

	for i in range(len(alist1)):
		alist1[i][0]=alist1[i][0]*5+25
		alist1[i][1]=alist1[i][1]*5+4

	
	print(alist1)
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


	for i in range(1,11):#24
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

	world1=world('world.png',-1000,-1000)
	world1.render(8,500)
	yHouse=world1.height(26,5)
	lisTexture.append(obje([OBJ("House.obj",False,"Models/House/")],0,[25,world1.height(25,4)+0.1,4],-1,0.05,0))


	Dlis=[OBJ("Door1.obj",False,"Models/Door1/")]
	#first door
	lisDoors.append([obje(Dlis,0,[32.5,world1.height(32.5,4),4],3,0.05,0,0,1),"Door"])
	#first floor doors
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4),14],3,0.05,90,0,1),"Door"])
	lisSpecialDoors.append([obje(Dlis,0,[90,world1.height(32.5,4),14],3,0.05,90,1,0),"Door","HELP!"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),11.5],3,0.05,90,0,1),"Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),26.5],3,0.05,90,0,1),"Door"])
	lisDoors.append([obje(Dlis,0,[100,world1.height(32.5,4),41.5],3,0.05,90,0,1),"Door"])
	#second floor doors
	lisSpecialDoors.append([obje(Dlis,0,[100,world1.height(32.5,4)+15,41.5],3,0.05,90,0,0),"Door","Done"])
	lisDoors.append([obje(Dlis,0,[90,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"Door"])
	lisDoors.append([obje(Dlis,0,[55,world1.height(32.5,4)+15,41.5],3.5,0.05,90,1,1),"Door"])


	#create some sound
	fireSound=pygame.mixer.Sound("Sounds/gun_fire.wav")
	fireSound.set_volume(sound_game)

	mainSound=pygame.mixer.Sound("Sounds/mainSound.wav")
	mainSound.set_volume(sound_BGM)

	zombieSound=pygame.mixer.Sound("Sounds/zombieSound.wav")
	
	footSound=pygame.mixer.Sound("Sounds/FootStep.wav")
	footSound.set_volume(sound_game)
	mainSound.play(20)#play the mainSound 20 times 





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

main()
