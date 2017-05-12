from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
def drawText(string, x, y):
  glLineWidth(2)
  glColor(1,1,1)  # Yellow Color

  glTranslate(x-len(string)/50,y,0)
  glScale(0.0005,0.0005,1)
  string = string.encode() # conversion from Unicode string to byte string
  for c in string:
    glutStrokeCharacter(GLUT_STROKE_ROMAN , c )   
def Text(s):
  glMatrixMode(GL_PROJECTION)
  glPushMatrix()
  glLoadIdentity()
  glOrtho(-1,1,-1,1,-1,1)
  glMatrixMode(GL_MODELVIEW)
  glPushMatrix()
  glLoadIdentity()
  glDisable(GL_LIGHTING)
  drawText(s, 0,0)
  glEnable(GL_LIGHTING)
  glMatrixMode(GL_PROJECTION)
  glPopMatrix()
  glMatrixMode(GL_MODELVIEW)
  glPopMatrix()
#calculate the collision with walls and objects 
def collision(player,vertex,lisOBJ,lisDoors):
  for i in range (0,len(vertex)-1,2):
    if vertex[i][0]==vertex[i+1][0] and player.z>=min(vertex[i][1],vertex[i+1][1]) and player.z<=max(vertex[i][1],vertex[i+1][1]):
      distance= abs(player.x-vertex[i][0])
      if distance<1:
        Text("collieding with wall")
        return True
    elif vertex[i][1]==vertex[i+1][1] and player.x>=min(vertex[i][0],vertex[i+1][0]) and player.x<=max(vertex[i][0],vertex[i+1][0]):
      distance= abs(player.z-vertex[i][1])
      if distance<1:
        Text("collieding with wall")
        return True

  for i in range(len(lisOBJ)):
    target=lisOBJ[i][0]
    typ=lisOBJ[i][1]
    dist=((player.x-target.x)**2+(player.z-target.z)**2 +(player.y-player.tall-target.y)**2)**0.5
    if(dist<target.radius):
      Text("collieding woth "+typ)
      return True

  for i in range(len(lisDoors)):
    target=lisDoors[i][0]
    typ=lisDoors[i][1]
    if target.radius==-1:
      continue
    typ=lisDoors[i][1]
    dist=((player.x-target.x)**2+(player.z-target.z)**2 +(player.y-player.tall-1-target.y)**2)**0.5
    if(dist<target.radius):

      return True

  return False  

#check if the player near from any tools ?
def near(player,lisTools,lisDoors,keyState):
  for i in range(len(lisDoors)):
    target=lisDoors[i][0]
    if target.radius==-1:
      continue
    typ=lisDoors[i][1]
    dist=((player.x-target.x)**2+(player.z-target.z)**2+(player.y-player.tall-0.5-target.y)**2)**0.5
    if(dist<target.radius+0.5):
      Text("press E to "+typ)
      if(keyState[ord('e')]):
        if not target.doorKey:
          return True
        else:
          target.animation=1
          target.radius=-1
          break    