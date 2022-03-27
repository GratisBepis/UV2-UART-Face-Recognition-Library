##declarations
#libraries
from m5stack import *
from m5ui import *
from uiflow import *
import json
import uv2lib
src=uv2lib.uv2lib
#variables 
#JSON variable  
msg=None
running=None
prob=None
match_prob=None
name=None
revstr=None
data1=None
#Face and ID 
numID=0
numFace=0
nom=["A","B","C","D"]
fnc_array=["train","stop","reset","save","strt_R"]
##init 
#screen init 
setScreenColor(0x5B8AAE)
title0 = M5Title(title="Demo program V0.1", x=3, fgcolor=0xABD3E1, bgcolor=0x2D7AA9)
#labels init
label_msg = M5TextBox(0, 27, "msg", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_running = M5TextBox(0, 47, "running", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_status= M5TextBox(0, 67, "status", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_prob = M5TextBox(0, 87, "prob", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_match_prob = M5TextBox(0, 107, "match_prob", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_name = M5TextBox(0, 127, "name", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_dbg = M5TextBox(0, 147, "dbg", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

#rectangles init
#they are be above the buttons, with a label in them
#they are used to select a function to execute
rectangleG = M5Rect(35, 187, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrG = M5TextBox(48, 190, fnc_array[0], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
rectangleC = M5Rect(135, 187, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrC = M5TextBox(138, 190, fnc_array[1], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
rectangleD = M5Rect(225, 187, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrD = M5TextBox(228, 190, fnc_array[2], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

#Uart start
#May not be the good 
uart1 = machine.UART(1, tx=17, rx=16)
uart1.init(115200, bits=8, parity=None, stop=1)

#all the used functions that aren't in the library

def menu_refresh():                     #will refresh the menu each time it's used
    rectangleG.setBgColor(0x2D7AA9)     #clean the rectanglle
    rectangleC.setBgColor(0x2D7AA9)
    rectangleD.setBgColor(0x2D7AA9)
    lrG.setText(fnc_array[0])           #set the text to the new element in the array
    lrC.setText(fnc_array[1])
    lrD.setText(fnc_array[2])
    pass

def move_to_left(your_array):           #shift all the array to the right, in a loop fashion 
    tmp = your_array[0]                 #save the 1st element, it will be put in place of the last one
    for i in range(len(your_array)-1):  #for all element in the array minus 1        
        your_array[i]=your_array[i+1]   #replace element n°i by element n°i+1
    your_array[(len(your_array)-1)]=tmp #replace the last element by the first one


def move_to_right(your_array):          #almost the same as above, but the other way around
    tmp = your_array[len(your_array)-1] 
    for i in range(len(your_array)-1):
        your_array[len(your_array)-1-i]=your_array[len(your_array)-i-2]
    your_array[0]=tmp
    

### buttons actions

def buttonA_wasPressed():               #if btnA is pressed 
    move_to_right(fnc_array)            #"move" the array to the right
    menu_refresh()                      #refresh the labels
    label_dbg.setText("A was pressed")  #for debug purposes
    pass


def buttonC_wasPressed():               #almost same thing as above, but the other way around
    move_to_left(fnc_array)
    menu_refresh()
    label_dbg.setText("C was pressed")
    pass 

def buttonB_wasPressed():               #will execute the function of the label in the center
    global numID                        
    #global nom
    label_dbg.setText(fnc_array[1]+" selected")     
    if fnc_array[1]=="train" :                        
        src.face_reco_train(uart1,numID,nom[numID])
        numID+=1
    elif fnc_array[1]=="stop" :
        src.stop_face_reco_train(uart1)
    elif fnc_array[1]=="save" :
        src.face_reco_save_and_run(uart1)
    elif fnc_array[1]=="reset" :
        src.face_reco_reset(uart1)
    elif fnc_array[1]=="face rcgn" :
        src.choose_fnc(uart1,"Face Recognition","")
    pass




def data_ret():
    #retain the previous values, if nothing is read from one element of the data[] array
    #the previous value won't be replaced by an empty string
    #the function could be done with a for loop but then I would have to change a lot of code so it's simpler this way
    if str(data1[0]) :                                  #if the string is not empty                                   
        label_msg.setText("message : "+str(data1[0]))   #set label's text to the new value
    if str(data1[1]) :
        label_running.setText("running : "+str(data1[1]))
    if str(data1[2]) :
        label_status.setText("status : "+str(data1[2]))
    if str(data1[3]) :
        label_prob.setText("face probability : "+str(data1[3]))
    if str(data1[4]) :
        label_match_prob.setText("match probability : "+str(data1[4]))
    if str(data1[5]) :
        label_name.setText("face is "+str(data1[5]))
    if str(data1[6]) :
        label_msg.setText("ERROR :"+str(data1[6]))
    if str(data1[7]) : 
        label_dbg.setText("ERC="+str(data1[7]))
    pass
        
def start_countdown(i) :
    while i>0 : 
        wait(1)
        label_dbg.setText("starting..."+str(i))
        i-=1
    
#wait for the UV2 to start the face recognition function
src.choose_fnc(uart1,"Face Recognition","")
label_dbg.setText("starting...")
start_countdown(10)
label_dbg.setText("started")


while True : 
    #check if a button is pressed
    btnA.wasPressed(buttonA_wasPressed)
    btnB.wasPressed(buttonB_wasPressed)
    btnC.wasPressed(buttonC_wasPressed)
    #try to read data on the uart liaison
    try :
        revstr1=src.uart_read(uart1)
    except:
        pass            
    #try to parse the JSON into an easily accessible array
    try :
        data1=src.get_data(revstr1)       
        data_ret()                      #will only replace the old value if there is a new value
        wait_ms(200)                    #"<<you're too fast, slow down!>>" 
    except : 
        pass

