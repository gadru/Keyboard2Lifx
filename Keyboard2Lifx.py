from __future__ import print_function

try:
    import pygame
except ImportError:
    pygame = None
    import Tkinter

import lifxlan
import traceback
import sys

class Keyname2Lifx:
    def __init__(self):
        print("connecting to lifx...")
        self.lifx = lifxlan.LifxLAN()
        self.num_of_lights = len(self.lifx.get_lights())
        print("Found {} light(s).\n".format(self.num_of_lights))
        #Define colro friendly names.
        self.colors = {
            "red"       : lifxlan.RED           ,
            "orange"    : lifxlan.ORANGE        ,
            "yellow"    : lifxlan.YELLOW        ,
            "green"     : lifxlan.GREEN         ,
            "cyan"      : lifxlan.CYAN          ,
            "blue"      : lifxlan.BLUE          ,
            "purple"    : lifxlan.PURPLE        ,
            "pink"      : lifxlan.PINK          ,
            "white"     : lifxlan.WHITE         ,
            "cold_white": lifxlan.COLD_WHITE    ,
            "warm_white": lifxlan.WARM_WHITE    ,
            "gold"      : lifxlan.GOLD
        }
        #Map the keys to colors.
        self.keymap = {
            'w'         :   "cyan"        ,
            'a'         :   "pink"        ,
            's'         :   "blue"        ,
            'd'         :   "cold_white"  ,
            'f'         :   "warm_white"  ,
            'g'         :   "gold"        ,
            'm'         :   "gold"        ,
            'up'        :   "red"         ,
            'down'      :   "purple"      ,
            'left'      :   "green"       ,
            'right'     :   "orange"      ,
            'space'     :   "yellow"      
        }

    def _keyname_to_color(self,key_name):
        """Convert key name to color and friendly color name"""
        color_name = None
        try:
            color_name = self.keymap[key_name]
        except KeyError:
            print("Key '%s' is not mapped."%key_name)
        color = self.colors.get(color_name)
        return color,color_name
    
    def set_color(self,color):
        """Pass the instruction to the bulbs"""
        try:
            self.lifx.set_color_all_lights(color, rapid=True)
            return True
        except Exception as error:
            traceback.print_exc()
    def alert(self,color_name):
        """Alert the user that the change has been performed."""
        plural_s = "" if self.num_of_lights==1 else "s"
        print("%d bulb%s set to %s."%(self.num_of_lights,plural_s, str(color_name)))

    def do(self,key_name):
        """Send the key name to lifx"""
        color, color_name = self._keyname_to_color(key_name)
        if (color is not None):
            result = self.set_color(color)
            self.alert(color_name)

if pygame is not None:
    class Pygame2Lifx:
        def __init__(self):
            self.keyname2lifx = Keyname2Lifx()
            pygame.init()
            pygame.display.set_mode((300, 200))
            self.running = False
        def run(self):
            """Listen to keys and send them to all lifx bulbs"""
            self.running = True
            try:
                while self.running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                        if event.type == pygame.KEYDOWN:
                            key_name = pygame.key.name(event.key).lower()
                            self.keyname2lifx.do(key_name)
                pygame.quit()
            except SystemExit:
                pygame.quit()

if pygame is None:
    class Tkinter2Lifx:
        def __init__(self):
            self.keyname2lifx = Keyname2Lifx()
            self._init_window()
            
        def _init_window(self):
            self.root = Tkinter.Tk()
            self.root.geometry('300x200')
            self.text = Tkinter.Text(self.root, background='black')
            self.text.pack()

        def _onKeyPress(self, event):
            self.keyname2lifx.do(event.char.lower())

        def run(self):
            """Listen to keys and send them to all lifx bulbs"""
            self.root.bind('<KeyPress>', self._onKeyPress)        
            self.root.mainloop()

if __name__== '__main__':
    #Prefare 
    try:
        Keyboard2Lifx = Pygame2Lifx
    except:
        print("""Couldn't find pygame ,only alphanumeric(a-z,A-Z,0-9) buttons will be supported.""")
        Keyboard2Lifx = Tkinter2Lifx
    Keyboard2Lifx().run()
