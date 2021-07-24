#!/usr/bin/env python3

import serial, getch
#import signal, sys
import time
from unicurses import *
import serialkey_config as cfg



apple_key_mode = False
option_key_mode = False
control_key_mode = False

screen_keyboard_posy = 3   # vertical offset for drawing keyboard
screen_keyboard_posx = 2   # horizontal offset for drawing keyboard
dashboard_pos_y = 16
dashboard_pos_x = 2


if cfg.hagstrom_keynumber_mode:
    from serialkey_codes import asc232_keycodes
    keycodes = asc232_keycodes
if cfg.pi_gadget_mode:
    from serialkey_codes import pi_gadget_keycodes
    keycodes = pi_gadget_keycodes


ser = serial.Serial(cfg.PORT, baudrate=cfg.BAUD, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=1)   # open serial port





key_symbols = ['`','~','!','@','#','$','%','^','&','*','(',')','-','_','=','+','[','{',']','}','\\','|',';',':','\'','\"',',','<','.','>','/','?']

keycap_dict = {          # "keycap" : y row, x column, length
    '[RESET]': [0,0,7],
    '[ESC]': [1,0,5], '1': [1,5,1], '2': [1,7,1],'3': [1,9,1],'4': [1,11,1],'5': [1,13,1],'6': [1,15,1],'7': [1,17,1],'8': [1,19,1],
    '9': [1,21,1],'0': [1,23,1],'-': [1,25,1],'=': [1,27,3],'[D]': [1,29,3],
    '[C]': [1,39,3],'[=]': [1,42,3],'[/]': [1,45,3],'[*]': [1,48,3],

    '[T]': [2,0,3], 'Q': [2,6,1], 'W': [2,8,1],'E': [2,10,1],'R': [2,12,1],'T': [2,14,1],'Y': [2,16,1],'U': [2,18,1],'I': [2,20,1],'O': [2,22,1],'P': [2,24,1],'[': [2,26,1],']': [2,28,1],
    '[7]': [2,39,3],'[8]': [2,42,3],'[9]': [2,45,3],'[+]': [2,48,3],

    '[CTL]': [3,0,5], 'A': [3,7,1], 'S': [3,9,1],'D': [3,11,1],'F': [3,13,1],'G': [3,15,1],'H': [3,17,1],'J': [3,19,1],'K': [3,21,1],'L': [3,23,1],';': [3,25,1],'\'': [3,27,1],'[R]': [3,29,3],
    '[4]': [3,39,3],'[5]': [3,42,3],'[6]': [3,45,3],'[-]': [3,48,3],

    '[S]': [4,0,3], 'Z': [4,8,1], 'X': [4,10,1], 'C': [4,12,1],'V': [4,14,1],'B': [4,16,1],'N': [4,18,1],'M': [4,20,1],',': [4,22,1],'.': [4,24,1],'/': [4,26,1],'[s]': [4,28,3],
    '[1]': [4,39,3],'[2]': [4,42,3],'[3]': [4,45,3],

    '[CL]': [5,0,4], '[O]': [5,4,3], '[A]': [5,7,3], '`': [5,11,1], '[SPACE]': [5,13,7], '\\': [5,21,1], '[<-]': [5,23,4], '[->]': [5,27,4], '[^]': [5,31,3], '[v]': [5,34,3],
    '[ 0 ]': [5,39,5],'[.]': [5,45,3],'[E]': [5,48,3],

    '<MouseKeys>': [7,40,11]
}

keycap_dict_shift = {
    '!': [1,5,1], '@': [1,7,1],'#': [1,9,1],'$': [1,11,1],'%': [1,13,1],'^': [1,15,1],'&': [1,17,1],'*': [1,19,1],'(': [1,21,1],')': [1,23,1],'_': [1,25,1],'+': [1,27,3],
    '{': [2,26,1], '}': [2,28,1],
    ':': [3,25,1], '\"': [3,27,1],
    '<': [4,22,1], '>': [4,24,1],'?': [4,26,1],
    '~': [5,11,1], '|': [5,21,1]
}

# keys that also exist in number pad
numpad_list = {'1','2','3','4','5','6','7','8','9','0','=','/','*','-','+','.'}


apple_toggle_key = '\x01'  # x01 = ^A
option_toggle_key = '\x02' # x02 = ^B
control_toggle_key = '\x04' # x04 = ^D
mousekeys_toggle_key = 'KEY_DC' # 'forward' delete, or "delete" in windows

ser.write( [56] ) # clear ASC buffer



def signal_handler(sig, frame):
    print('^C')
    ser.write( keycodes['\x03'] )
#    sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


def refresh_screen(root,character, ordkey):

    # "dashboard"
    root.attroff(curses.color_pair(1))
    root.addstr ((dashboard_pos_y-1),2,"                                             ")
    root.addstr ((dashboard_pos_y-1),2,"Last Key: {" + character + "} ord: " + str(ordkey))
    root.refresh()

    # clear mod key area
    root.hline(dashboard_pos_y, dashboard_pos_x,' ', 80)
    root.hline(dashboard_pos_y+1, dashboard_pos_x, ' ', 80)
    root.hline(dashboard_pos_y+2, dashboard_pos_x, ' ', 80)
    root.hline(dashboard_pos_y+4, dashboard_pos_x, ' ', 80)
    root.hline(dashboard_pos_y+5, dashboard_pos_x, ' ', 80)


def areyousure(root, height, width, begin_y, begin_x, message):
    win = root.newwin(height, width, begin_y, begin_x)

def draw_controls(root, type):
    global keycap_dict

    if type == "gs":
        keycap_guide = """
        [RESET]
        [E] 1 2 3 4 5 6 7 8 9 0 - = [D]   [C][=][/][*]
        [T]  q w e r t y u i o p [ ]      [7][8][9][+]
        [^]   a s d f g h j k l ; ' [R]   [4][5][6][-]
        [S]    z x c v b n m , . / [S]    [1][2][3]
        [CL][O][A]`[SPACE]\[<-][->][v][^] [ 0 ] [.][E]"""


        

    for idx, element in enumerate(keycap_dict):
        root.addstr(keycap_dict[element][0] + screen_keyboard_posy, keycap_dict[element][1] + screen_keyboard_posx, element )

    command_keys = "^] Special Keys / Options"
    root.addstr(screen_keyboard_posy + 9, screen_keyboard_posx +1, command_keys)
    root.refresh()

def highlight_key(window, screen_key, state):

    global keycap_dict
    global keycap_dict_shift

    if screen_key in keycap_dict:
        keydict = keycap_dict
    elif screen_key in keycap_dict_shift:
        keydict = keycap_dict_shift
    else:
        return # key not in keycap lists, can't flash anything

    if state == 'on':
        window.attron(curses.color_pair(1)) # enable inverse
        window.addstr(keydict[screen_key][0] + screen_keyboard_posy, keydict[screen_key][1] + screen_keyboard_posx, screen_key)
        window.attroff(curses.color_pair(1)) # disable inverse

    if state == 'off':
        window.attroff(curses.color_pair(1)) # remove inverse
        window.addstr(keydict[screen_key][0] + screen_keyboard_posy, keydict[screen_key][1] + screen_keyboard_posx, screen_key)

    if state == 'flash':
        window.attron(curses.color_pair(1)) # enable inverse
        window.addstr(keydict[screen_key][0] + screen_keyboard_posy, keydict[screen_key][1] + screen_keyboard_posx, screen_key)
        window.refresh()
        time.sleep(cfg.KEY_DELAY)
        window.attroff(curses.color_pair(1)) # remove inverse
        window.addstr(keydict[screen_key][0] + screen_keyboard_posy, keydict[screen_key][1] + screen_keyboard_posx, screen_key)
            # Check if key is a shifted symbol, if so change it back to unshifted key at that spot
        if keydict == keycap_dict_shift:
            highlight_key(window, '[S]', 'flash')
            highlight_key(window, '[s]', 'flash')
            key_loc = str(keydict[screen_key])
            for key, values in keycap_dict.items():
                hit = str(values)
                if hit == key_loc:
                    window.attroff(curses.color_pair(1)) # remove inverse
                    window.addstr(keycap_dict[key][0] + screen_keyboard_posy, keycap_dict[key][1] + screen_keyboard_posx, key)



    window.refresh()

def display_mod_key_menu(root):

    keypress = 'none'
    root.addstr(dashboard_pos_y, dashboard_pos_x, "0)Send ^] 1)Apple  2)Option  3)Control")
    root.addstr(dashboard_pos_y+1, dashboard_pos_x, "4)GS-CPnl 5)Reset  6)Reboot  7)Power Off/On  8)Clear Buffer")
    root.addstr(dashboard_pos_y+2, dashboard_pos_x, "e)//e reset  E)//e reboot")
    root.addstr(dashboard_pos_y+4, dashboard_pos_x, "USB Sync Control: S)Switch USB +)Add USB -)Remove USB R)Reset")
    choice = root.getkey()
    if choice == '1':
        keypress = apple_toggle_key

    elif choice == '2':
        keypress = option_toggle_key
 
    elif choice == '3':
        keypress = control_toggle_key

    elif choice == '4':
        ser.write([ keycodes['control'][0], keycodes['Apple'][0], keycodes['Esc'][0], keycodes['Esc'][1], keycodes['Apple'][1], keycodes['control'][1] ])

    elif choice == '5':
        ser.write([ keycodes['control'][0], keycodes['PrtSc'][0], keycodes['PrtSc'][1], keycodes['control'][1] ]) # wombat ctl-reset

    elif choice == '6':  # WOMBAT Warm Boot Salute
        ser.write([ keycodes['control'][0], keycodes['Apple'][0], keycodes['PrtSc'][0] ]) # send control - apple - prtsc 
        time.sleep(.5)
        ser.write([ keycodes['PrtSc'][1] ]) # release prtsc after 1 second
        ser.write([ keycodes['control'][1], keycodes['Apple'][1] ]) # now release control and apple
        time.sleep(.5)
        ser.write([ keycodes['control'][0], keycodes['Apple'][0] ]) # now HOLD control and apple
        time.sleep(.5)
        ser.write([ keycodes['control'][1], keycodes['Apple'][1] ]) # now release control and apple

    elif choice == '7':
        # Send commands to PDU, coming later
        pass

    elif choice == '8':
        ser.write([keycodes['ClrBuffer'][0]]) # clear buffer

    elif choice == '9':
        keypress = mousekeys_toggle_key

    elif choice == '0':
       # print(keycodes['control'][0], keycodes[']'][0])
       # ser.write ([  keycodes['control'][0] , keycodes[']'][0] , keycodes[']'][1], keycodes['control'][1] ])  # send actual ^]
       keypress = "^]"

    elif choice == 'e':   # send ctrl - Break to RESET  for Ian Kim //e PS/2 adapter
         ser.write([ keycodes['control'][0], keycodes['Break'][0] ])
         ser.write([ keycodes['Break'][1], keycodes['control'][1] ])

    elif choice == 'E':   # send ctrl - apple- Break  to REBOOT for Ian Kim //e PS/2 adapter
         ser.write([ keycodes['control'][0], keycodes['Apple'][0], keycodes['Break'][0] ])
         time.sleep(.5)
         ser.write([ keycodes['Break'][1], keycodes['control'][1], keycodes['Apple'][1] ])       

    elif choice == 'b':  # send Break key alone
         ser.write([ keycodes['Break'][0], keycodes['Break'][1] ])

    elif choice.lower() == 's':  # switch USB device
         root.addstr(dashboard_pos_y+5, dashboard_pos_x, "Device #? (0 for all) ")
         device_choice = root.getkey()
         try:
            val = int(device_choice)        # be sure it's a # input
            ser.write([ keycodes['num*'][0] ])   # hold numberpad * key
            time.sleep(.3)
            ser.write ([ keycodes['num'+str(device_choice)][0] ]) # press key for new choice
            ser.write ([ keycodes['num'+str(device_choice)][1] ]) # release key for new choice
            time.sleep(.3)
            ser.write([ keycodes['num*'][1] ])   # release numberpad * key
         except ValueError:      # must be a number
            pass

    elif choice.lower() == '-':  # remove USB device
         root.addstr(dashboard_pos_y+5, dashboard_pos_x, "Device #? ")
         device_choice = root.getkey()
         try:
            val = int(device_choice)        # be sure it's a # input
            ser.write([ keycodes['num-'][0] ])   # hold numberpad - key
            time.sleep(.3)
            ser.write ([ keycodes['num'+str(device_choice)][0] ]) # press key for new choice
            ser.write ([ keycodes['num'+str(device_choice)][1] ]) # release key for new choice
            time.sleep(.3)
            ser.write([ keycodes['num-'][1] ])   # release numberpad - key
         except ValueError:      # must be a number
            pass

    elif choice.lower() == '+':  # add USB device
         root.addstr(dashboard_pos_y+5, dashboard_pos_x, "Device #? ")
         device_choice = root.getkey()
         try:
            val = int(device_choice)        # be sure it's a # input
            ser.write([ keycodes['num+'][0] ])   # hold numberpad + key
            time.sleep(.3)
            ser.write ([ keycodes['num'+str(device_choice)][0] ]) # press key for new choice
            ser.write ([ keycodes['num'+str(device_choice)][1] ]) # release key for new choice
            time.sleep(.3)
            ser.write([ keycodes['num+'][1] ])   # release numberpad + key
         except ValueError:      # must be a number
            pass

    elif choice.lower() == 'r':  # Reset USB controller
         root.addstr(dashboard_pos_y+5, dashboard_pos_x, "Sending *-F11")
         ser.write([ keycodes['num*'][0] ])   # hold numberpad * key
         time.sleep(.3)
         ser.write ([ keycodes['F11'][0] ])  # F11
         ser.write ([ keycodes['F11'][1] ])  # release F11
         time.sleep(.3)
         ser.write([ keycodes['num*'][1] ])   # release numberpad * key

    elif choice.lower() == 'l':  # Light status      
         ser.write([ keycodes['light_status'][0] ]) 
         light_response = ser.read(1)
         root.addstr(dashboard_pos_y+5, dashboard_pos_x, "Result: " + str(light_response))
         ser.write([keycodes['ClrBuffer'][0]]) # clear buffer
         time.sleep(.3)

    else: 
         keypress = ""



    return keypress


    

def send_key(root):
    height, width = root.getmaxyx()
    apple_key_mode = False
    option_key_mode = False
    control_key_mode = False
    mousekeys_mode = False
    numpad_mode = False

    mod_menu_key = '\x1d' # ^]

    while 1:
        try:


            
            input_keypress = root.getkey()
            display_key = input_keypress  # key to display to user
            use_keycode = input_keypress  # "key" to look up for sending serial commands

            try:       
                key = ord(str(input_keypress))
            except:
                key = 'unknown'

            
            root.hline(height-1, 0, ' ',80)
         

# KEY TRANSLATE
    
    # Visible keys read by string

            if input_keypress == ' ':   #space
                highlight_key(root, '[SPACE]', 'flash')
                display_key = '[SPACE]'
            if input_keypress == 'KEY_LEFT':
                highlight_key(root, '[<-]', 'flash')
            if input_keypress == 'KEY_RIGHT':
                highlight_key(root, '[->]', 'flash')
            if input_keypress == 'KEY_UP':
                highlight_key(root, '[^]', 'flash')  
            if input_keypress == 'KEY_DOWN':
                highlight_key(root, '[v]', 'flash') 
            if input_keypress == 'KEY_BACKSPACE':               # raspberry pi workaround
                highlight_key(root, '[D]', 'flash')
                display_key = '[Del]'
                key = ''
                ser.write([ keycodes['\x7f'][0],keycodes['\x7f'][1] ])
                continue


            # numpad?
            if input_keypress in numpad_list:
                if numpad_mode == True:
                    use_keycode = 'num' + str(input_keypress)
                    display_key = 'numpad' + str(input_keypress)
                    highlight_key(root, '[' + str(input_keypress) + ']', 'flash')
                    ser.write([ keycodes[use_keycode][0], keycodes[use_keycode][1] ])
                    input_keypress = "handled"


    # "Invisible" keys read by ord
            if str(key) == '9':     #TAB
                highlight_key(root, '[T]', 'flash')
                display_key = '[Tab]'
                use_keycode = '\t'
            if str(key) == '127':    #DEL
                highlight_key(root, '[D]', 'flash')
                display_key = '[Del]'
            if str(key) == '10':    #RETURN
                highlight_key(root, '[R]', 'flash')
                display_key = '[Return]'
                use_keycode = '\n'
            if str(key) == '27': 
               display_key = '[ESC]'
               use_keycode = 'Esc'
            if str(key) == '30':      # Ctrl - 6 for vidHD
                display_key = '^6'
                highlight_key(root, '6', 'flash')
                highlight_key(root, '[CTL]', 'flash')
                ser.write([ keycodes['control'][0], keycodes['6'][0] ])
                ser.write([ keycodes['control'][1], keycodes['6'][1] ])
                


               
            if input_keypress == mod_menu_key:
                input_keypress = display_mod_key_menu(root)  # display mod menu window which may return a new input keypress          

            # Flash typed keys on and off
            if input_keypress != 'handled':
                if input_keypress == '^]':
                    screen_key = "]"
                    highlight_key(root, screen_key, 'flash')
                    highlight_key(root, "[CTL]", 'flash')
                elif input_keypress.isalpha() or input_keypress.isdigit() or input_keypress in key_symbols:
                  screen_key = input_keypress.upper()
                  highlight_key(root, screen_key[0], 'flash' )


            refresh_screen(root,display_key, key)   # update on screen keyboard



            if input_keypress == mousekeys_toggle_key:
                mousekeys_mode^=True # toggle mousekeys mode
                if mousekeys_mode == True:
                    ser.write([ keycodes['shiftL'][0], keycodes['Apple'][0], keycodes['clear'][0] ])
                    ser.write([ keycodes['shiftL'][1], keycodes['Apple'][1], keycodes['clear'][1] ])
                    highlight_key(root, '<MouseKeys>', 'on')
                    numpad_mode = True  
                elif mousekeys_mode == False:
                    ser.write([ keycodes['shiftL'][0], keycodes['Apple'][0], keycodes['clear'][0] ])
                    ser.write([ keycodes['shiftL'][1], keycodes['Apple'][1], keycodes['clear'][1] ])
                    highlight_key(root, '<MouseKeys>', 'off')
                    numpad_mode = False


                    

            if input_keypress == apple_toggle_key:
                apple_key_mode^=True       #  toggle apple mode
                if apple_key_mode == True:
                    ser.write ( [keycodes['Apple'][0]]  ) # "hold" left win (open apple)
                    highlight_key(root, '[A]', 'on')
                elif apple_key_mode == False:
                    ser.write ( [keycodes['Apple'][1]] ) # release left win (open apple)
                    highlight_key(root, '[A]', 'off')
                input_keypress = "handled"    
            if input_keypress == option_toggle_key:
                option_key_mode^=True       #  toggle option mode
                if option_key_mode == True:
                    ser.write ( [keycodes['option'][0]] ) # "hold" left alt (option)
                    highlight_key(root, '[O]', 'on')
                elif option_key_mode == False:
                    ser.write ( [keycodes['option'][1]] ) # release left alt (option)
                    highlight_key(root, '[O]', 'off')
                input_keypress = "handled"
            if input_keypress == control_toggle_key:
                control_key_mode^=True       #  toggle control mode
                if control_key_mode == True:
                    ser.write ( [keycodes['control'][0]] ) # "hold" left control
                    highlight_key(root, '[CTL]', 'on')
                elif control_key_mode == False:
                    ser.write ( [keycodes['control'][1]] ) # release left control
                    highlight_key(root, '[CTL]', 'off')
                input_keypress = "handled"

                

    # Generic Send Key               
            if input_keypress != "handled":
                ser.write( keycodes[use_keycode] ) # write pressed key

            if str(key) == '10':            # key was return? we need to delay
                time.sleep(cfg.RETURN_DELAY)


            if input_keypress == '^C':
                continue

            root.attroff(curses.color_pair(1)) # remove inverse
            root.hline(dashboard_pos_y, dashboard_pos_x, ' ',80)
            root.refresh()

        except Exception as e:
          # root.attroff(curses.color_pair(1))
            height, width = root.getmaxyx()
            if str(key) == '31' or input_keypress == 'KEY_RESIZE' :
                root.hline(height-1, 0, ' ',80)  # clear error line
            else:
                continue   #  root.addstr(height-1,0, ("Error: " + str(e) ) + "                      ")


def main(root):
    stdscr = initscr()
    curses.curs_set(0)  # disable cursor
    curses.use_default_colors()   # Allow default terminal background color
    curses.init_pair(1, curses.COLOR_BLACK,COLOR_WHITE)  
    root.clear()
    draw_controls(root,"gs")
    send_key(root)

curses.wrapper(main)

if __name__ == "__main__":
     main()