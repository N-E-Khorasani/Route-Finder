import numpy as np
import math
import copy
from PIL import Image
import PIL


#def transition_model (p,row, col,block,terminal):
c=0
row=4
col=4
terminal=[3,5,11]
good=[11] #+1 terminals for part 2 of question its better to separate them
bad=[3,5]#-1 terminals
pillar=[10]
p=0.8
reward=-0.04
gama=1

def transition_model (p,row,col,terminal,pillar):
    tm = np.zeros(((row*col), 4, (row*col)), dtype=float)
    pp=(1-p)/2
    for j in range(0,4):

        for i in range(0,row*col):

            if (j==0): #up direction
                if ((i-col)>=0): #seperating 4 first states (first row) from rest of them because with up direction agent would stay in that states with p probability
                    tm[i,j,i-col]=p
                    if ((i-1)%col!=col-1): #seperating first column from other columns because if we want to go up there is a p prime probability to go left and we want agent to stay at these sates with going left we dont want it to end up in the last element of the previous row
                        tm[i,j,i-1]=pp #coulmn other than first
                    else: #first column
                        tm[i,j,i]=pp
                    if ((i+1)%col!=0):#seperating last column from others because there is a p prime possibility that with choosing up agent goes right and we want it to stay at those state and does not go to the next row
                        tm[i,j,i+1]=pp
                    else:
                        tm[i,j,i]=pp
                else: #the first row
                    tm[i,j,i]=p
                    if ((i-1)>=0):
                        tm[i,j,i-1]=pp
                    else:
                        tm[i,j,i]=tm[i,j,i]+pp
                    if ((i+1)%col!=0):
                        tm[i,j,i+1]=pp
                    else:
                        tm[i,j,i]=tm[i,j,i]+pp
            if(j==1): #down direction
                if (i+col<(row*col)): #seperating the last row from others
                    tm[i,j,i+col]=p
                    if ((i-1)>=0 and (i-1)%col!=col-1): #seperating the first column from others for going left with p prime probability
                        tm[i,j,i-1]=pp
                    else:
                        tm[i,j,i]+=pp
                    if ((i+1)%col!=0):#seperating the last column from others for going right with p prime probability
                        tm[i,j,i+1]=pp
                    else:
                        tm[i,j,i]+=pp
                else:  #the last row
                    tm[i,j,i]=p
                    if((i-1)%col!=col-1):
                        tm[i,j,i-1]=pp
                    else:
                        tm[i,j,i]+=pp
                    if((i+1)<(row*col)):
                        tm[i,j,i+1]=pp
                    else:
                        tm[i,j,i]+=pp
            if (j==2): #left direction
                if ((i-1)>=0 and (i-1)%col!=col-1):# seperating first column from others for going left.because they have to stay at the same
                    tm[i,j,i-1]=p
                    if (i-col>=0): #seperating first row because with intending left there is a p prime possibility to go up and this row does not have any upper states
                        tm[i,j,i-col]=pp
                    else:
                        tm[i,j,i]+=pp
                    if ((i+col)<(row*col)): #seperating last row
                        tm[i,j,i+col]=pp
                    else:
                        tm[i,j,i]+=pp
                else: #firt column
                    tm[i,j,i]=p
                    if ((i-col)>=0): #seperating first row because in the first row with left p% we remain at the same state and with p prime we remain too so we add p and p prime.because there is a p prime chance that we go up and in the first row and column (0,0) we cant
                        tm[i,j,i-col]+=pp
                    else:
                        tm[i,j,i]+=pp
                    if((i+col)<(row*col)): #seperating last row from others
                        tm[i,j,i+col]+=pp
                    else:
                        tm[i,j,i]+=pp # last row
            if(j==3): #right direction
                if((i+1)%col!=0): #seperating last column from others because with going right we have to stay at the same state
                    tm[i,j,i+1]=p
                    if ((i-col)>=0):#seperating first row from others because we going right there is p prime chance to go up which is a wall
                        tm[i,j,i-col]=pp #other than first row
                    else:
                        tm[i,j,i]=pp #first row
                    if ((i+col)<(row*col)):#seperating last row from others
                        tm[i,j,i+col]=pp #other than last row
                    else:
                        tm[i,j,i]+=pp #last row
                else: #last column
                    tm[i,j,i]=p
                    if((i-col)>0): #seperating first row from others because we going right there is p prime chance to go up which is a wall
                        tm[i,j,i-col]+=pp #other rows
                    else:
                        tm[i,j,i]+=pp #first row in the last column
                    if((i+col)<(row*col)): #seperating the last row from others
                        tm[i,j,i+col]+=pp #other rows
                    else:
                        tm[i,j,i]+=pp #last row

#applying terminals
#if we enter to a terminal we can not go anywhere else so all the s prime from that state would be 0 in every direction

    for i in range(0,(row*col)):
        for k in range(0,len(terminal)):

            if i==terminal[k]:
                tm[i,:,:]=0

#applying wall to the map

    for k in range (0,len(pillar)):
        print(pillar[k],"pilare k")
        for j in range(0, 4):
            for i in range(0,(row*col)):
                if ((i-col)==pillar[k] and ((i-col) not in terminal)): #if we were in the below state of the wall
                    # for example if we wanted to go up and there was no wall we would go there by p% chance but now by choosing up we will remain at the same state because
                    # the upper one is a wall so we add the percentage of going up without the wall to the remaining at the same state and we set the percentage
                    #of going up to zero . we implement same concept for other state around the wall too

                    tm[i,j,i]+=tm[i,j,pillar[k]]
                    tm[i,j,pillar[k]]=0
                if  ((i+col)==pillar[k] and ((i+col) not in terminal)):# if we were in the upper state of the wall
                    tm[i, j, i] += tm[i, j, pillar[k]]
                    tm[i, j, pillar[k]] = 0
                if ((i +1) == pillar[k] and ((i +1) not in terminal)): #if we were in the left state of the wall
                    tm[i, j, i] += tm[i, j, pillar[k]]
                    tm[i, j, pillar[k]] = 0
                if ((i -1) == pillar[k] and ((i -1) not in terminal)):#if we were in the right state of the wall
                    tm[i, j, i] += tm[i, j, pillar[k]]
                    tm[i, j, pillar[k]] = 0


    return tm

tm=transition_model(p,row,col,terminal,pillar)
print("up","\n",tm[:,0,:])
print("**********************************************************************************")
print("down","\n",tm[:,1,:])
print("**********************************************************************************")
print("left","\n",tm[:,2,:])
print("**********************************************************************************")
print("right","\n",tm[:,3,:])

#part 2 of problem 6

def value_iteration (transition_model,gama,reward,row,col,good_termianl,bad_terminal,wall):
    #initialize u with 0 and +1 and -1 for terminals
    u=np.zeros(((row*col),),dtype=float)
    for item in bad_terminal:
        u[item]=-1
    for item in good_termianl:
        u[item] = 1
    for item in wall:
        u[item] = 0

    tm=transition_model

    #save the initial u
    b = np.zeros(((row * col),), dtype=float)
    for item in bad_terminal:
        b[item] = -1
    for item in good_termianl:
        b[item] = 1
    for item in wall:
        b[item] = 0

    u_list = []

    temp=[]
    cnt=0
    u_list.append(b)

    while(True):
        #print("baaadi",cnt)

        for i in range(0,(row*col)): #for all the states
            #setting the utility for terminals and walls
            if (i in bad_terminal):
                u[i]=-1
            elif(i in good_termianl):
                u[i]=1
            elif(i in wall):
                u[i]=0
            else:

                for j in range(0,4): #for every direction [up,down,left,right]
                    c=0
                    for k in range(0,(row*col)): #for every s prime

                        c+=tm[i,j,k]*u[k] #multiply every s prime probability in its correspond utility
                    temp.append(c)

                u[i]=reward+(gama*max(temp)) #choosing the max value which comes from one of the direction. we dont want direction in this part we will save it in the next part of question
                temp = []
        u_list.append(copy.copy(u)) #saving utilities so we can subtract the last two and see the difference.
        myu=u_list[-1]
        dif = np.abs(np.subtract(myu,b)) #subtract two last utility
        maxElement = np.max(dif)#choose the element with max value because if the max value is less that 1e-6 all of them would be less and we can say that we reach to convergence
        #print("max element",maxElement)
        cnt += 1
        u_list=[]
        if maxElement<1e-20: # we check that whether we reach to the convergence or not if yes, we will break and be out of while loop

            break
        else:

            temporary=myu #update the u
            b=temporary


    print("true utility of states:","\n",u.reshape(row,col))
    return u


true_utility=value_iteration(tm,gama,reward,row,col,good,bad,pillar)

def optimal_policy (transition_model,true_utility,row,col,good_terminal,bad_terminal,wall):
    temp=[]
    multi=row*col
    max_index=np.zeros((multi,),dtype=object)

    for i in range(0,(row*col)): #for all the states
        for j in range(0,4):# for all the actions {up,down,left,right}
            c=0
            for k in range(0,(row*col)): #for every s'
                c+=transition_model[i,j,k]*true_utility[k] #multiply every s prime probability in its correspond true utility
            temp.append(c) # save the C so after finishing second for (action for) we can choose the index which has max value



        max_index[i]=temp.index(max(temp))# this time we dont want the max value we want the action which causes the max value
        temp=[]
    #setting for the termianls and walls
    for item in good_terminal:
        max_index[item]='G'
    for item in bad_terminal:
        max_index[item] = 'B'
    for item in wall:
        max_index[item] = 'W'

    return max_index

optimal_pol=optimal_policy(tm,true_utility,row,col,good,bad,pillar)
optimal_pol=optimal_pol.reshape((row,col))
print("optimal policy is :","\n",optimal_pol)

#drawing the optimal policy with Pillow library PIL
image_list=[]
#adding and editing the pictures of arrows

right=Image.open(("right-b.png.jpg"))
up=right.rotate(90)
left=up.rotate(90)
down=left.rotate(90)
posone=Image.open("posone.png")
negone=Image.open("minusone.png")
wall=Image.open("brown.jpg")
image_list.append(up)
image_list.append(down)
image_list.append(left)
image_list.append(right)

#setting the size of new image
h=row*100
w=col*100
new_im = Image.new('RGB', (w,h))

#drawing the optimal policy
for i in range(0,row):
    for j in range(0,col):
        for k in range(0,4):

            if optimal_pol[i][j]==k: #if it was one of the direction bring its correspond from list of image for example fourth elemet of image list is the picture of right arrow anf the our fourth action is also right
                new_im.paste(image_list[k],(j*100,i*100))
        if optimal_pol[i][j]=='G':# if it was good terminals upload the picture of positive one
            new_im.paste(posone,(j*100,i*100))
        if optimal_pol[i][j] == 'W':#if it was walls upload the picture of wall (brown square)
            new_im.paste(wall, (j * 100, i * 100))
        if optimal_pol[i][j] == 'B':#if it was bad terminals upload the picture of negative one
            new_im.paste(negone, (j * 100, i * 100))

new_im.show()


