from .usbswsdk import *
import argparse
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
parser = argparse.ArgumentParser(prog=f'{bcolors.OKCYAN}zuss{bcolors.ENDC}',description=f'{bcolors.OKGREEN}Python sdk for USB Switch{bcolors.ENDC}',epilog=f"{bcolors.OKGREEN}Caution: Please implement only{bcolors.ENDC} {bcolors.WARNING}ONE{bcolors.ENDC} {bcolors.OKGREEN}function each time.{bcolors.ENDC}")
parser.add_argument('-P','--port', type=str, help=f'Port name of USB switch.This arg is {bcolors.WARNING}REQUIRED{bcolors.ENDC} when manipulating the USB Switch')
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-l',action="store_true", help='Print the list of serial COM ports in use.')
parser.add_argument('-V',action="store_true", help='Current USB switch version information.')
parser.add_argument('-r',action="store_true",help='Reboot the USB switch, about 10s.')
parser.add_argument('-s',action="store_true",help='Save configuration into flash')
parser.add_argument('-R',action="store_true",help='Reset configuration')
parser.add_argument('-d',action="store_true",help='Display configuration')
parser.add_argument('--sethost',type=int,help='Set enable host port,input from 1 to 4')
parser.add_argument('--gethost',action="store_true",help='Show currently enabled host port')
parser.add_argument('--setdev',type=int,help='Set enable device port,input from 1 to 4')
parser.add_argument('--getdev',action="store_true",help='Show currently enabled device port')
parser.add_argument('--setrelay',type=int,help='Set Relay Mask, 4bit Mask value, Bit0 to Bit3 stand for Relay1 to Relay4,input from 0 to 15')
parser.add_argument('--getrelay',action="store_true",help='Show currently Relay Mask,Bit0 to Bit3 stand for Relay1 to Relay4')
parser.add_argument('--setpwr',type=int,help='Set Power Supply Mask,Set the Mask of the Device Ports enable to power supply, Bit0 to Bit3 stand for Port1 to Port4.input from 0 to 15')
parser.add_argument('--getpwr',action="store_true",help='Show currently Power Supply Mask')
if __name__ == '__main__':
    args  = parser.parse_args()
    if args.l:
        detect_comports()
    elif args.V:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-V requires -P{bcolors.ENDC}")
        else:
            get_version(args.port)
    elif args.r:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-r requires -P{bcolors.ENDC}")
        else:
            reboot_sys(args.port)
    elif args.s:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-s requires -P{bcolors.ENDC}")
        else:
            save_config(args.port)
    elif args.R:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-R requires -P{bcolors.ENDC}")
        else:
            clr_config(args.port)
    elif args.d:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-d requires -P{bcolors.ENDC}")
        else:
            disp_config(args.port)
    elif args.sethost:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-sethost requires -P{bcolors.ENDC}")
        else:
            set_host_port(args.port, args.sethost)
    elif args.gethost:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-gethost requires -P{bcolors.ENDC}")
        else:
        
            get_host_port(args.port)
    elif args.setdev:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-setdev requires -P{bcolors.ENDC}")
        else:
        
            set_dev_port(args.port, args.setdev)
    elif args.getdev:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-getdev requires -P{bcolors.ENDC}")
        else:
        
            get_dev_port(args.port)
    elif args.setrelay:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-setrelay requires -P{bcolors.ENDC}")
        else:
        
            set_relay_mask(args.port,args.setrelay)
    elif args.getrelay:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-getrelay requires -P{bcolors.ENDC}")
        else:
            get_relay_mask(args.port)
    elif args.setpwr:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-setpwr requires -P{bcolors.ENDC}")
        else:
            set_pwr_mask(args.port,args.setpwr)
    elif args.getpwr:
        if args.port is None:
            parser.error(f"{bcolors.FAIL}-getpwr requires -P{bcolors.ENDC}")
        else:
            get_pwr_mask(args.port)

