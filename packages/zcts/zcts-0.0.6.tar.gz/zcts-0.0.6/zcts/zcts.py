# -----------------------------------------------------------------------------
# - File              converter2000_sdk.py
# - Owner             Zhengkun Li
# - Version           1.0
# - Date              09.06.2021
# - Classification    Python SDK
# - Brief             Python SDK for ZD converter2000
# ----------------------------------------------------------------------------- 

import serial
from serial import Serial
import serial.tools.list_ports as port_list
import time
import colorama
colorama.init()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
################################################################################
# Description : Check serial port                                              #
# Argument: None                                                               #                             
# Returns: The list of serial COM ports in use :list                           #    
################################################################################  
def detect_comports():
    com_ports_details = list(port_list.comports())
    com_ports = []
    for p in com_ports_details:
        print(f"{bcolors.OKGREEN}{p}{bcolors.ENDC}")
        com_ports.append(str(p).split(" ")[0])
    
    return com_ports
################################################################################
# Description : Get Current Version Information                                #
# Argument: serial_num: str                                                    #                             
# Returns: None                                                                #    
# Get the current version information of ZD-Converter2000 software
################################################################################  
def get_sw_version(serial_num: str): 
    time_start=time.time()  
    serialPort = Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<GET_SW_VERSION{}>")
    serialString = ""  # Used to hold data coming over UART
    
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Reboot System                                                  #
# Argument: serial_num: str                                                    #                             
# Returns: None                                                                #    
# Reboot system. After saving configuration, new configuration parameters can only be activated
# when system is rebooted.
################################################################################
def reboot_sys(serial_num: str):
    time_start=time.time() 
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<REBOOT_SYS{}>")
    serialString = ""  # Used to hold data coming over UART

    while 1 :
        time_end=time.time()
        if (time_end-time_start)>20:
            return  
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass
            if "ZD-Converter2000 initialized OK" in serialString:
                return
################################################################################
# Description : Save Configuration into Flash                                  #
# Argument: serial_num: str                                                    #                             
# Returns: Save status: bool                                                   # 
# • Save the configuration into ZD-Converter2000’s internal flash memory. Next time when system
# starts up, the configuration will be loaded automatically from flash memory and activated.
# • Notice: if newly settings are not saved by SAVE_CONFIG command, these settings will be lost
# when system is rebooted.
################################################################################     
def save_config(serial_num: str):
    time_start=time.time() 
    res = False
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<SAVE_CONFIG{}>")
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>3:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[SAVE_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Clear Configuration in Flash                                   #
# Erase the configuration in ZD-Converter2000’s internal flash memory          #  
# Argument: serial_num: str                                                    #                             
# Returns: Clear status:bool                                                   #    
# Erase the configuration in ZD-Converter2000’s internal flash memory.
################################################################################   
def clear_config(serial_num: str):
    time_start=time.time() 
    res = False
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<CLEAR_CONFIG{}>")
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[CLEAR_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass


################################################################################
# Description : Display Current Configuration in Ram                           #
# Argument: serial_num: str                                                    #                             
# Returns: Display result: bool                                                #  
# Display the current configuration parameters, including newly settings which are not in flash
# Memory  
################################################################################
def disp_config(serial_num: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<DISP_CONFIG{}>")
    res = False
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[DISP_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Display Port Status                                     #
# Argument: serial_num: str                                                    #                             
# Returns: Display result: bool                                                #    
# Show the status of ZD-Converter2000’s four ethernet ports Speed, Role, Link up Status etc
################################################################################
def disp_port_status(serial_num: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<DISP_PORT_STATUS{}>")
    res = False
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[DISP_PORT_STATUS{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Display Statistics Information                                 #
# Argument: serial_num: str                                                    #                             
# Returns: Display result: bool                                                #    
# Show the Statistics Information of BRR and ETH Ports, include the number of transmitted and
# received frames, transmitted, and received bytes, counts transmitted and received multicast
# frames, broadcast frames, counts the transmitted and received number of frames which were
# dropped.
################################################################################
def disp_port_statistics(serial_num: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<DISP_PORT_STATISTICS{}>")
    res = False
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[DISP_PORT_STATISTICS{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass
################################################################################
# Description : Set Operation Mode                                             #
# Argument: serial_num: str, 1~4 : int           0: mode 0; 1: mode 1          #  
#                                                2: mode 2; 3: mode 3          #                             
# Returns: Set enable port of Device status: bool                              #  
# • Set the configuration of operation mode.
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued.  
################################################################################    
def set_op_mode(serial_num: str,value:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if value not in [0,1,2,3]:
        print(f"Input value:{value} error! Valid options: 0: mode 0; 1: mode 1; 2: mode 2; 3: mode 3")
        return False
    serialPort.write( bytes(f"<SET_OP_MODE{{{value}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False 
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_OP_MODE{{{value}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get Operation Mode                                             #
# Argument: serial_num: str                                                    #                             
# Returns:  Currently Operation Mode:list( enable:int, config:int,status:int ) #  
# enable 0: Manual Mode 1: Program Mode  
# config -1: default 0: mode 0; 1: mode 1 2: mode 2; 3: mode 3
# status 0: mode 0; 1: mode 12: mode 2; 3: mode 3
################################################################################  
def get_op_mode(serial_num: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( b"<GET_OP_MODE{}>")
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_OP_MODE{" in serialString:   
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_OP_MODE{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
                
            except:
                pass  
################################################################################
# Description : Set ETH Speed                                                  #
# Argument: serial_num: str, port : int, speed:int                             #                             
# Returns: Set ETH Speed  result: bool                                         #    
# • Set the Configuration of ETH Speed
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued.
################################################################################  
def set_eth_speed(serial_num: str,port:int,speed:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if speed not in [100,1000]:
        print(f"Input speed:{speed} error! Valid options: 100: 100M; 1000: 1000M")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: ETH 1; 2: ETH 2(GE)")
        return False
    serialPort.write( bytes(f"<SET_ETH_SPEED{{{port},{speed}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_ETH_SPEED{{{port},{speed}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  
################################################################################
# Description :  Get ETH Speed                                           #
# Argument: serial_num: str, port:int                                                    #                             
# Returns:  list of the Configuration of ETH Speed in Ram and current Setting: list                            #    
################################################################################  
def get_eth_speed(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_ETH_SPEED{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_ETH_SPEED{" in serialString:   
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_ETH_SPEED{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

################################################################################
# Description : Set ETH Operator of Force Down                                                 #
# Argument: serial_num: str, port : int, com:int                             #                             
# Returns: Set ETH Operator of Force Down result: bool                                         #    
# • Set the Operator of Force Down
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued
################################################################################  
def set_eth_down(serial_num: str,port:int,com:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if com not in [0,1]:
        print(f"Input com:{com} error! Valid options: 0: not down; 1: down")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: ETH 1; 2: ETH 2(GE)")
        return False
    serialPort.write( bytes(f"<SET_ETH_DOWN{{{port},{com}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_ETH_DOWN{{{port}, {com}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get ETH Operator of Force Down                                         #
# Argument: serial_num: str, port : int                                                      #                             
# Returns:  list of Currently ETH Operator of Force Down  :list                              #    
################################################################################  
def get_eth_down(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_ETH_DOWN{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_ETH_DOWN{" in serialString:  
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_ETH_DOWN{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Set BRR Speed                                                  #
# Argument: serial_num: str, port : int, speed:int                             #                             
# Returns: Set BRR Speed result: bool                                         #    
# • Set the Configuration of BRR Speed
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued.
################################################################################  
def set_brr_speed(serial_num: str,port:int,speed:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if speed not in [100,1000]:
        print(f"Input speed:{speed} error! Valid options: 100: 100M; 1000: 1000M")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: BRR 1; 2: BRR 2")
        return False
    serialPort.write( bytes(f"<SET_BRR_SPEED{{{port},{speed}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_BRR_SPEED{{{port},{speed}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  

################################################################################
# Description :  Get BRR Speed                                         #
# Argument: serial_num: str, port:int                                                    #                             
# Returns:   list ofCurrently Get BRR Speed: list                               #    
################################################################################  
def get_brr_speed(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_BRR_SPEED{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_BRR_SPEED{" in serialString:   
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_BRR_SPEED{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

################################################################################
# Description : Set BRR Operator of Force Down                                                #
# Argument: serial_num: str, port : int, com:int                             #                             
# Returns: Set BRR Operator of Force Down result: bool                                         #    
# • Set the Operator of Force Down
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued
################################################################################  
def set_brr_down(serial_num: str,port:int,com:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if com not in [0,1]:
        print(f"Input com:{com} error! Valid options: 0: not down; 1: down")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: BRR 1; 2: BRR 2")
        return False
    serialPort.write( bytes(f"<SET_BRR_DOWN{{{port},{com}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_BRR_DOWN{{{port}, {com}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get BRR Operator of Force Down                                         #
# Argument: serial_num: str, port : int                                                      #                             
# Returns:  • Get the Configuration of the Operator of Force Down in Ram and current Link Status of BRR                              #    
################################################################################  
def get_brr_down(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_BRR_DOWN{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_BRR_DOWN{" in serialString:
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_BRR_DOWN{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Set BRR Role                                                 #
# Argument: serial_num: str, port : int, com:int                             #                             
# Returns: Set BRR Role result: bool                                         #    
# • Set the Configuration of BRR Role
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued
################################################################################  
def set_brr_role(serial_num: str,port:int,com:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if com not in [0,1]:
        print(f"Input com:{com} error! Valid options: 0: master; 1: slave")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: BRR 1; 2: BRR 2")
        return False
    serialPort.write( bytes(f"<SET_BRR_ROLE{{{port},{com}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_BRR_ROLE{{{port}, {com}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get BRR Role                                         #
# Argument: serial_num: str, port : int                                                      #                             
# Returns:  • Get the Configuration of BRR Role and current Role status                           #    
################################################################################  
def get_brr_role(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_BRR_ROLE{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_BRR_ROLE{" in serialString:               
                for i in range(0,3):
                    res[i] = serialString.lstrip('[GET_BRR_ROLE{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Set BRR Mode                                                #
# Argument: serial_num: str, port : int, com:int                             #                             
# Returns: Set BRR Mode result: bool                                         #    
# • Set the Configuration of BRR mode
# • Notice: this setting can only be persistent after SAVE_CONFIG command is issued
################################################################################  
def set_brr_mode(serial_num: str,port:int,com:int): 
    time_start=time.time()
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if com not in [0,1]:
        print(f"Input com:{com} error! Valid options: 0: ieee-compliant; 1: legacy")
        return False
    elif port not in [1,2]:
        print(f"Input port number:{port} error! Valid options: 1: BRR 1; 2: BRR 2")
        return False
    serialPort.write( bytes(f"<SET_BRR_MODE{{{port},{com}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_BRR_MODE{{{port}, {com}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get BRR mode                                         #
# Argument: serial_num: str, port : int                                                      #                             
# Returns:  • Get the Configuration of BRR mode and current mode status                           #    
################################################################################  
def get_brr_mode(serial_num: str,port:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=serial_num, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(bytes(f"<GET_BRR_MODE{{{port}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = [-1,-1,-1]
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>0.5:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_BRR_MODE{" in serialString:               
                # res = serialString.lstrip('Return: [GET_BRR_MODE{').rstrip('}]')[0]
                for i in range(0,3):

                    res[i] = serialString.lstrip('[GET_BRR_MODE{').rstrip("}]\r\n").split(",")[i]

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 