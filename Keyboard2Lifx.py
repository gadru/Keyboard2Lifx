import pygame
import Tkinter
import lifxlan
import traceback

class Keycode2Lifx:
    def __init__(self):
        print "connecting to lifx..."
        self.lifx = lifxlan.LifxLAN()
        self.num_of_lights = len(self.lifx.get_lights())
        print "Found {} light(s).\n".format(self.num_of_lights)
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
            'q' : "red"         ,
            'w' : "blue"        ,
            'e' : "green"       ,
            'r' : "yellow"      ,
            't' : "pink"        ,
            'y' : "cold_white"
        }

    def _keycode_to_color(self,key_name):
        """Convert keycode to color and friendly color name"""
        color_name = None
        try:
            color_name = self.keymap[key_name]
        except KeyError:
            print "Key '%s' is not mapped."%key_name
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
        print "%d bulb%s set to %s."%(self.num_of_lights,plural_s, str(color_name))

    def do(self,keycode):
        """Send the keycode to lifx"""
        color, color_name = self._keycode_to_color(keycode)
        if (color is not None):
            result = self.set_color(color)
            self.alert(color_name)

class Pygame2Lifx:
    def __init__(self):
        self.keycode2lifx = Keycode2Lifx()
        pygame.init()
        pygame.display.set_mode((100, 100))
    def run(self):
        """Listen to keys and send them to all lifx bulbs"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self.keycode2lifx.do(key_name)

class Tkinter2Lifx:
    def __init__(self):
        self.keycode2lifx = Keycode2Lifx()
        self._init_window()
        
    def _init_window(self):
        self.root = Tkinter.Tk()
        self.root.geometry('300x200')
        self.text = Tkinter.Text(self.root, background='black')
        self.text.pack()

    def onKeyPress(self, event):
        self.keycode2lifx.do(event.char.lower())

    def run(self):
        self.root.bind('<KeyPress>', self.onKeyPress)        
        self.root.mainloop()

if __name__== '__main__':
    Tkinter2Lifx().run()
