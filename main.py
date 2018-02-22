#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk
import PIL.Image 
import subprocess
import PIL.ImageTk
import math
import random
import time

APP_TITLE = "Drag & Drop Tk Canvas Images"
APP_XPOS = 100
APP_YPOS = 100
APP_WIDTH = 360
APP_HEIGHT = 640
 
IMAGE_PATH = "images/"
 
class CreateCanvasObject(object):
    def __init__(self, canvas, image_name, position):
        self.canvas = canvas
        self.image_name = image_name
        self.position = position
        self.xpos, self.ypos = position['x'], position['y']
        
        im = PIL.Image.open("{}{}".format(IMAGE_PATH, image_name))
        im = im.resize((16, 16))
        self.tk_image = PIL.ImageTk.PhotoImage(im)
        self.image_obj= canvas.create_image(
            self.xpos, self.ypos, image=self.tk_image)
         
        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        self.move_flag = False
         
    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
             
            self.canvas.move(self.image_obj,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
        self.position['x'] = self.mouse_xpos
        self.position['y'] = self.mouse_ypos

 
    def release(self, event):
        self.move_flag = False

                     
class Application(tk.Frame):
 
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)

        self.bt_press = tk.Button(master=self.master, text="press", command=self.submit)
        self.bt_press.pack()

        self.bt_cap = tk.Button(master=self.master, text="cap", command=self.cap_screen)
        self.bt_cap.pack()
 
        self.canvas = tk.Canvas(self, width=APP_WIDTH, height=APP_HEIGHT, bg='blue',
            highlightthickness=0)
        self.canvas.pack()
        self.start_position = {'x': 100, 'y': 100}
        self.stop_position = {'x': 200, 'y': 200}
        self.cap_screen()


    def cap_screen(self):
        subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/screen.png'])
        subprocess.run(['adb', 'pull', '/sdcard/screen.png'])
        self.replace_bg()

    def submit(self):
        self.press()
        time.sleep(0.8)
        self.cap_screen()


    def press(self):
        dist = math.hypot(self.start_position['x']-self.stop_position['x'], self.start_position['y']-self.stop_position['y'])
        dist = int(dist*3.99)
        subprocess.run(['adb', 'shell', 'input', 'touchscreen', 'swipe', 
            '{}'.format(700+random.randint(0,300)), 
            '{}'.format(1000+random.randint(0,300)), 
            '{}'.format(700+random.randint(0,300)), 
            '{}'.format(1000+random.randint(0,300)), 
            '{}'.format(dist)])


    def replace_bg(self):
        im = PIL.Image.open('screen.png') 
        im = im.resize((APP_WIDTH, APP_HEIGHT))
        self.tk_img = PIL.ImageTk.PhotoImage(im)
        self.screen = self.canvas.create_image(APP_WIDTH/2, APP_HEIGHT/2, image=self.tk_img)
         
        self.image_1 = CreateCanvasObject(self.canvas, "start.png", self.start_position)
        self.image_2 =CreateCanvasObject(self.canvas, "stop.png", self.stop_position)


    def close(self):
        print("Application-Shutdown")
        self.master.destroy()
     
def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT+30))
     
    app = Application(app_win).pack(fill='both', expand=True)
     
    app_win.mainloop()
  
  
if __name__ == '__main__':
    main()