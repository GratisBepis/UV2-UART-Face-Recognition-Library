##UV2-UART-Face-Recognition-Library##
#Thomas E. 2022
# uart_read()
# choose_fnc()
# get_data()
# face_reco_train()
# face_reco_save_and_run
# face_reco_reset

##declarations 
#libraries
from m5stack import *
from m5ui import *
from uiflow import *
import json
class uv2lib:
   




##send whatever data you want to the UV 
    def choose_fnc(uart,fnc,args,uart_data):
        uart.write(str(uart_data))
        uart.write(''+"\r\n")
        wait_ms(450)
        pass
    
    
##chose the function you want to use 
    def choose_fnc(uart,fnc,args):
        uart_data='{"function":"'+str(fnc)+'","args":"'+str(args)+'"}'
        uart.write(str(uart_data))
        uart.write(''+"\r\n")
        wait_ms(450)
        pass
    
##possible function are :       |   For arguments see : https://docs.m5stack.com/en/quick_start/unitv2/base_functions
#Audio FFT                      
#Camera Stream                  
#Color Tracker                  
#Code Detector                  
#Face Detector                  
#Face Recognition               
#Lane Line Tracker              
#Motion Tracker                 
#Object Recognition             
#Online Classifier              
#Shape Detector                 
#Shape Matching                 
#Target Tracker                 


##get the data on an uart 
    def uart_read(uart):
        if uart.any():
            wait_ms(100)
            rev_str=json.loads((uart.read()).decode())
            return rev_str
        else:
            pass

##function to parse the data read from the UART into an array
#It will look for JSON elements that are outputted by the UV2
#It needs the JSON retrieved from the uart 
    def get_data(revstr1):
        #Set all the variables to an empty string
        #And return_error is a debug variable
        return_error=0
        msg=""
        running=""
        prob=""
        match_prob=""
        name=""
        status=""
        error=""
        return_error=1              #1
        #message block
        try :
            temp=revstr1["msg"]
            temp=temp.split(',')
            msg=temp[0]
            return_error+=2     #2
        except : 
            pass
        #running block
        try : 
            temp=revstr1["running"]
            temp=temp.split(',')
            running=temp[0]
            return_error+=4     #4
        except : 
            pass
        #status block
        try : 
            temp=revstr1["status"]
            temp=temp.split(',')
            status=temp[0]
            return_error+=8     #8
        except : 
            pass
        #error block
        try : 
            temp=revstr1["error"]
            temp=temp.split(',')
            error=temp[0]
            return_error+=16    #16
        except:
            pass
        #face block
        try :
            rev_obj=revstr1["face"]
            for elements in rev_obj:
                name=elements.get("name")
                match_prob=elements.get("match_prob")
                prob=elements.get("prob")
                return_error+=32    #32
        except:
            pass          


        return [msg,running,status,prob,match_prob,name,error,return_error]

        
##face recognition training
#the function will send a command to the UV2, with the an ID and a name
#IDs must be set like this :
#if there is already 2 face saved, new ID must be 2
#Name should be in UTF-8 format for best compatibility
#If a taining was started, it will send a JSON message to comfirm it
#Else if the face ID is invalid, it will also send a JSON message informing you that an error occured

    def face_reco_train(uart,ID,Name):
        uart_data='{"config":"Face Recognition","operation":"train","face_id":'+str(ID)+',"name":"'+str(Name)+'"}'
        uart.write(str(uart_data))
        uart.write(''+"\r\n")


##stop face recognition training 
#The functions will send a command to the UV2 to stop the training


    def stop_face_reco_train(uart):
        uart_data='{"config":"Face Recognition","operation":"stoptrain"}'
        uart.write(str(uart_data))
        uart.write(''+"\r\n")
        pass
##save your trained faces
    def face_reco_save_and_run(uart):
        uart_data='{"config":"Face Recognition ","operation":"saverun"}'
        uart.write(str(uart_data))
        uart.write(''+"\r\n")
        pass

#reset your saved faces
    def face_reco_reset(uart):
        uart_data='{"config":"Face Recognition","operation":"reset"}'
        uart.write(str(uart_data))
        uart.write(''+"\r\n")
        pass



