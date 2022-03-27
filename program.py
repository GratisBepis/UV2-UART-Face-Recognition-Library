###declarations
##libraries
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
inB=0
#Face and ID 
numID=0
namearr=["Albert","Betty","Charles","David","Elvis","Frederik"]
fnc_array=["train","stop","reset","save","rcgn"]

##init 
#screen init 
setScreenColor(0x5B8AAE)
title0 = M5Title(title="Demo program V0.1", x=3, fgcolor=0xABD3E1, bgcolor=0x2D7AA9)

#labels init
label_msg = M5TextBox(0, 27, "msg", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_running = M5TextBox(0, 67, "running", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_status= M5TextBox(0, 87, "status", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_prob = M5TextBox(0, 107, "prob", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_match_prob = M5TextBox(0, 127, "match_prob", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_name = M5TextBox(0, 147, "name", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
label_dbg = M5TextBox(0, 167, "dbg", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)

#rectangles init
#they are be above the buttons, with a label in them
#they are used to select a function to execute
rectangleG = M5Rect(40, 190, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrG = M5TextBox(40, 192, fnc_array[0], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
rectangleC = M5Rect(130, 190, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrC = M5TextBox(130, 192, fnc_array[1], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
rectangleD = M5Rect(220, 190, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrD = M5TextBox(220, 192, fnc_array[2], lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
#those are for the training functions, they alllow you to select a name 
RectangleName = M5Rect(210, 110, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrN = M5TextBox(210, 112, namearr[numID] , lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
RectangleID = M5Rect(210, 150, 60, 20, 0x2D7AA9, 0x0C6BA7)
lrI = M5TextBox(210, 152, str(numID), lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
#hide them in the first place, they will be shown when they are needed 
RectangleName.hide()
RectangleID.hide()
lrN.hide()
lrI.hide()

#Uart start
#May not be the pin you have to use 
uart1 = machine.UART(1, tx=17, rx=16)

uart1.init(115200, bits=8, parity=None, stop=1)
##all the used functions that aren't in the library
def menu_refresh():                     #will refresh the menu each time the function is called
    rectangleG.setBgColor(0x2D7AA9)     #clean the rectangles
    rectangleC.setBgColor(0x2D7AA9)
    rectangleD.setBgColor(0x2D7AA9)
    lrG.setText(fnc_array[0])           #set the text to the new element in the array
    lrC.setText(fnc_array[1])
    lrD.setText(fnc_array[2])
    pass

def move_to_left(your_array):           #shift all the array to the left, in a loop fashion 
    tmp = your_array[0]                 #save the 1st element, it will be put in place of the last one
    for i in range(len(your_array)-1):  #for all element in the array minus 1        
        your_array[i]=your_array[i+1]   #replace element n°i by element n°i+1
    your_array[(len(your_array)-1)]=tmp #replace the last element by the first one

def move_to_right(your_array):          #almost the same as above, but the other way around
    tmp = your_array[len(your_array)-1] 
    for i in range(len(your_array)-1):
        your_array[len(your_array)-1-i]=your_array[len(your_array)-i-2]
    your_array[0]=tmp

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
        label_prob.setText("face probability : "+str(round(float(data1[3]),2)))
    if str(data1[4]) :
        label_match_prob.setText("match probability : "+str(round(float(data1[4]),2)))
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

#buttons actions

def buttonA_wasPressed():               #if btnA is pressed 
    if inB==1 :                         #if you pressed btnB before to start training 
        global numID                    #this will make you select which face you want
        if numID==0:
            numID=(len(namearr)-1)
        else :
            numID-=1
        lrN.setText(str(namearr[numID]))
        lrI.setText(str(numID))
    else :    
        move_to_right(fnc_array)            #"move" the array to the right
        menu_refresh()                      #refresh the labels
    label_dbg.setText("A was pressed")  #for debug purposes
    pass

def buttonC_wasPressed():               #almost same thing as above, but the other way around
    global inB                         
    if inB==1 : 
        global numID                        
        if numID==(len(namearr)-1):
            numID=0
        else :
            numID+=1
        lrN.setText(str(namearr[numID]))
        lrI.setText(str(numID))
    else :
        move_to_left(fnc_array)
        menu_refresh()
    label_dbg.setText("C was pressed")
    pass 

def buttonB_wasPressed():               #if you want to start training a face it will ask you which one you want
    global inB                          #else it will execute the function of the center's label  
    if inB==1 :                         #if inB = 1, it means you already selected the training function 
        src.face_reco_train(uart1,numID,namearr[numID]) #send the command to start the training
        RectangleName.hide()                            #and hide both labels and rectangles
        RectangleID.hide()                              #plus affect 0 to inB
        lrN.hide()
        lrI.hide()
        inB=0
    else :
        if fnc_array[1]=="train" :                        
            RectangleName.show()
            RectangleID.show()
            lrN.show()
            lrI.show()
            inB=1
        elif fnc_array[1]=="stop" :
            src.stop_face_reco_train(uart1)
        elif fnc_array[1]=="save" :
            src.face_reco_save_and_run(uart1)
        elif fnc_array[1]=="reset" :
            src.face_reco_reset(uart1)
        elif fnc_array[1]=="rcgn" :
            src.choose_fnc(uart1,"Face Recognition","")
    pass

###End of declarations    
###Program  
##Start 
#wait for the UV2 to start the face recognition function
src.choose_fnc(uart1,"Face Recognition","")
label_dbg.setText("starting...")
start_countdown(10)
label_dbg.setText("started")
##While loop start 
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
