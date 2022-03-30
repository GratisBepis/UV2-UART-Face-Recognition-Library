#UV2-UART-Face-Recognition-Library#
#Thomas E. 2022
"""
All the functions in the library : 

send_data()
choose_fnc()
get_data()
uart_read()
face_reco_train()
stop_face_reco_train
face_reco_save_and_run
face_reco_reset
"""

from m5stack import *
from m5ui import *
from uiflow import *
import json



class uv2lib:

    def send_data( uart, uart_data ) :
        """Send_data allows you to send the data you want to the UV2

        :uart is the uart you initialised
        :uart_data is the data you wan to send, must be JSON
        """
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )
        wait_ms(450) 
        
    def choose_fnc( uart, fnc, args ) :
        """ Choose_fnc will send a command to the UV2 to set the running function 

        :uart is the uart you initialised
        :fnc is the function you want to run 
            possible functions are  "Audio FFT", "Camera Stream", "Color Tracker"                  
            "Code Detector", "Face Detector", "Face Recognition", "Lane Line Tracker",              
            "Motion Tracker", "Object Recognition", "Online Classifier",              
            "Shape Detector", "Shape Matching", "Target Tracker"                  
        :args is the argument you want the running function to start with
            For arguments see : https://docs.m5stack.com/en/quick_start/unitv2/base_functions
        """
        uart_data = '{"function":"'+str(fnc)+'","args":"'+str(args)+'"}'
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )
        wait_ms( 450 ) 
            

    def uart_read( uart ) :
        """Read what is on the uart 

        :uart is the uart you initialised
        """
        if uart.any() :
            rev_str = json.loads( ( uart.read() ).decode() )
            return rev_str
        else:
            pass


    def get_data( revstr1 ) :
        """" Function to parse the data read from the UART into an array
        It will look for JSON elements that are outputted by the UV2
        
        :revstr1 is JSON retrieved from the uart 
        """
        #Set all the variables to an empty string
        return_error = 0
        msg = ""
        running = ""
        prob = ""
        match_prob = ""
        name = ""
        status = ""
        error = ""
        return_error = 1         #1
        #return_error is a debug variable
        #message block
        try :
            temp = revstr1[ "msg" ]
            temp = temp.split( ',' )
            msg = temp[ 0 ]
            return_error += 2     #2
        except : 
            pass
        #running block
        try : 
            temp = revstr1[ "running" ]
            temp = temp.split( ',' )
            running = temp[ 0 ]
            return_error += 4     #4
        except : 
            pass
        #status block
        try : 
            temp = revstr1[ "status" ]
            temp = temp.split( ',' )
            status=temp[0]
            return_error+=8     #8
        except : 
            pass
        #error block
        try : 
            temp = revstr1[ "error" ]
            temp = temp.split( ',' )
            error = temp[ 0 ]
            return_error += 16    #16
        except:
            pass
        #face block
        try :
            rev_obj = revstr1[ "face" ]
            for elements in rev_obj:
                name = elements.get( "name" )
                match_prob = elements.get( "match_prob" )
                prob = elements.get( "prob" )
                return_error += 32    #32
        except:
            pass          
        return [ msg , running , status , prob , match_prob , name , error , return_error ]

#face recognition training functions

    def face_reco_train( uart, ID, Name ) :
        """ The function will send a command to the UV2, with an ID and a name
        If a training was started, it will send a JSON message to comfirm it
        Else if the face ID is invalid, it will also send a JSON message informing you that an error occured
        
        :uart is the uart you initialised
        :ID must be set like this : if there is already 2 face saved, new ID must be 2 (so first ID is 0)
        :Name should be in UTF-8 format for best compatibility
        """
        uart_data = '{"config":"Face Recognition","operation":"train","face_id":'+str(ID)+',"name":"'+str(Name)+'"}'
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )

    def stop_face_reco_train( uart ) :
        """Send a command to stop face recognition training
        
        :uart is the uart you initialised        
        """
        uart_data = '{"config":"Face Recognition","operation":"stoptrain"}'
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )
        
    def face_reco_save_and_run( uart ) :
        """Send a command to save your trained faces
        
        :uart is the uart you initialised
        """
        uart_data = '{"config":"Face Recognition","operation":"saverun"}'
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )
        
    def face_reco_reset( uart ) :
        """Send a command to reset your saved faces
        
        :uart is the uart  you initialised
        """
        uart_data = '{"config":"Face Recognition","operation":"reset"}'
        uart.write( str( uart_data ) )
        uart.write( '' + "\r\n" )
