from tkinter import *
import math


class threeSplitTree(object):
    def __init__(self,level):
        self.level = level

    def drawBranch(self,canvas,xtop,ytop,xbottom,ybottom,height,width=10,color="#947A6F"):
        canvas.create_line(xtop,ytop,xbottom,ybottom,fill=color,width=width)

    def drawTree(self,canvas,height,level,xtop,ytop,xbottom,ybottom,width=10,color="#947A6F"):
        if (level<=0):
            return
        else:
            self.drawBranch(canvas,xtop,ytop,xbottom,ybottom,height,width,color)
            height = height/2
            branch1dx = height / 2
            branch1dy = height / (2 * 3**0.5)
            self.drawTree(canvas,height,level-1,xtop-branch1dx,ytop-branch1dy,xtop,ytop,width/2,color)
            branch2dy = height * math.cos(10)
            branch2dx = (height**2 - branch2dy**2)**0.5
            self.drawTree(canvas,height,level-1,xtop-branch2dx,ytop+branch2dy,xtop,ytop,width/2,color)
            branch3dx = (height**2)/2
            branch3dy = height * math.sin(10)
            self.drawTree(canvas,height,level-1,xtop+branch1dx,ytop-branch1dy,xtop,ytop,width/2,color)
            self.drawTree(canvas,height,level-1,xtop+branch2dx,ytop+branch3dy,xtop,ytop,width/2,color)
