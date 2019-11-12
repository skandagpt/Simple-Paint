# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:19:43 2019

@author: Skandagpt
"""

from tkinter import *
from tkinter.colorchooser import askcolor
import sys



class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    DEFAULT_NUM = 0
    
    sys.setrecursionlimit(10000)
    
    def __init__(self,master):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)
        
        self.master=master
        self.square_button = Button(self.root, text = 'square', command = self.draw_square)
        self.square_button.grid(row = 1 , column = 1)
    
        self.line_button = Button(self.root, text = 'line', command = self.draw_line)
        self.line_button.grid(row = 1 , column = 0)
        
        self.circle_button = Button(self.root, text = 'circle/ellipse', command = self.draw_circle)
        self.circle_button.grid(row = 1 , column = 2)
        
        self.triangle_button = Button(self.root, text = 'TRIANGLE', command = self.draw_triangle)
        self.triangle_button.grid(row = 1 , column = 3)
        
        self.fill_color_button = Button(self.root, text = 'Fill Color', command = self.fill_color)
        self.fill_color_button.grid(row = 1 , column = 4)
        
        self.c = Canvas(self.root, bg='white', width=1000, height=600)
        self.c.grid(row=2, columnspan=5)
        
        self.setup()
        
        self.root.mainloop()
        

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.DEFAULT_NUM = 0
        
    
    def use_pen(self):
        self.activate_button(self.pen_button)
        
       

    def use_brush(self):
        self.activate_button(self.brush_button)
        self.origin()

    def choose_color(self):
#        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
    
    def draw_square(self):
        self.DEFAULT_NUM = 1
        self.c.bind("<ButtonPress-1>",self.on_button_press)
        self.c.bind("<ButtonRelease-1>",self.on_button_release)
        self.eraser_on = True
        
    def draw_line(self):
        self.DEFAULT_NUM = 2
        self.c.bind("<ButtonPress-1>",self.on_button_press)
        self.c.bind("<ButtonRelease-1>",self.on_button_release)
        self.eraser_on = True
    
    def draw_circle(self):
        self.DEFAULT_NUM = 3
        self.c.bind("<ButtonPress-1>",self.on_button_press)
        self.c.bind("<ButtonRelease-1>",self.on_button_release)
        self.eraser_on = True
    
    def draw_triangle(self):
        self.DEFAULT_NUM = 4
        self.c.bind("<ButtonPress-1>",self.on_button_press)
        self.c.bind("<ButtonRelease-1>",self.on_button_release)
        
        self.eraser_on = True
    
    def fill_color(self):
        self.c.bind("<ButtonPress-1>",self.get_coord)
        self.floodFill(self.x,self.y)
    
    def get_coord(self,event):
        self.x= event.x
        self.y= event.y
        
    
    def getColour(self , x , y ):
        overlapping = self.c.find_overlapping(x, y, x, y)
        if overlapping:
           return( self.c.itemcget(overlapping[0], "fill"))
           
    def floodFill(self,x,y):
        col=self.getColour(x,y)       
        if col != self.color:
            self.c.create_line(x,y,x,y,fill = self.color)
            self.floodFill(x+1, y+1)
            self.floodFill(x-1, y-1)
            self.floodFill(x-1, y+1)
            self.floodFill(x+1, y-1)
            self.floodFill(x+1, y)
            self.floodFill(x-1, y)
            self.floodFill(x, y+1)
            self.floodFill(x, y-1)
             
    
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        self.c.bind("<ButtonPress-1>",self.on_button_press)
        x2,y2 = x1+x0/20 , y1+y0/20
        x3,y3 = x1-x0/20 , y1 -y0/20
        
        if self.DEFAULT_NUM == 1:
              self.c.create_rectangle(x0,y0,x1,y1,outline = self.color,width = self.choose_size_button.get())
        elif self.DEFAULT_NUM == 2:
            self.c.create_line(x0,y0,x1,y1,fill = self.color,width = self.choose_size_button.get())
        elif self.DEFAULT_NUM == 3:
            self.c.create_oval(x0,y0,x1,y1,outline = self.color, width = self.choose_size_button.get())
        elif self.DEFAULT_NUM == 4:
            self.c.create_polygon(x0,y0,x2,y2,x3,y3,outline = self.color,fill = "WHITE",width = self.choose_size_button.get())
        col = self.color
        self.setup()
        self.color = col
        
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode
        

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y
       

    def reset(self, event):
        self.old_x, self.old_y = None, None
        

    

if __name__ == '__main__':
    root = Tk()
    Paint(root)
