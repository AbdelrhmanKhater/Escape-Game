#calculate the collision with walls and objects 
def collision(player,vertex,lisOBJ):
  for i in range (0,len(vertex)-1,2):
    if vertex[i][0]==vertex[i+1][0] and player.z>=min(vertex[i][1],vertex[i+1][1]) and player.z<=max(vertex[i][1],vertex[i+1][1]):
      distance= abs(player.x-vertex[i][0])
      if distance<1:
        return "wall"
    elif vertex[i][1]==vertex[i+1][1] and player.x>=min(vertex[i][0],vertex[i+1][0]) and player.x<=max(vertex[i][0],vertex[i+1][0]):
      distance= abs(player.z-vertex[i][1])
      if distance<1:
        return "wall"

  for i in range(len(lisOBJ)):
    target=lisOBJ[i][0]
    typ=lisOBJ[i][1]
    dist=((player.x-target.x)**2+(player.z-target.z)**2 +(player.y-target.y))**0.5
    if(dist<target.radius):
      return lisOBJ[i]

  return False  

#check if the player near from any tools ?
def near(player,lisTools,keyState):
  for i in range(len(lisTools)):
    target=lisTools[i][0]
    typ=lisTools[i][1]
    dist=((player.x-target.x)**2+(player.z-player.tall-target.z)**2)**0.5
    if(dist<2):
      print("near from ",typ,'\n',"press E to use")
      if(keyState[ord('e')]==1):
        if typ in ['Tank','FlashLight','Gun','Car']:
          #tool.typ=1
          #del lisTools[i]
          break    