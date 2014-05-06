from pyx import *
from math import *
# Global Constants

s = 1.0
h = (sqrt(3)/2)*s
hCenter = h/3
hCornerCenter = 2*h/3
bend = h/4

#Create individual rgb triagnles with 6 inputs: c,x,y,col,o,i
# c is the canvas
# the x and y coordinates of the center of the triangle
# col is the color of the triangle (red,green or blue)
# o is the orientation of the triangle (0-2) (where 0=0 degrees, 1=120 degrees, 2=240 degrees)
# i is the intensity of the color (0-9) (higher number = brighter)
def draw_rgb(c,x,y,col,o,i):
    iIncrement = bend/5  #length increment for each level change in intensity

    yOffset = (i*iIncrement)-bend

    p = path.path(path.moveto(x,y), path.rmoveto(0,yOffset),
                  path.rlineto(.5,-yOffset-hCenter), path.rlineto(-1,0),
                  path.closepath())
    t = trafo.trafo()
    t = t.rotated(o*120)
    p = p.transformed(t)
    
##    if(col == "red"):
##        c.stroke(p, [color.rgb.red])
##    elif(col == "green"):
##        c.stroke(p, [color.rgb.green])
##    else:
##        c.stroke(p, [color.rgb.blue])
    return p

#
def fill_intersection(c,p1,p2,col,i1,i2):
    p1a, p1b, p1c = p1.split([0,.5,p1.end()-.5])
    p2a, p2b, p2c = p2.split([0,.5,p2.end()-.5])
    if(i1>5 and i2>5):
        p1_inter = p1a
        p2_inter = p2b
    elif((i1>5 and i2<=5) or (i1<=5 and i2>5)):
        p1_inter = p1b
        p2_inter = p2b
    isects_p1, isect_p2 = p1_inter.intersect(p2_inter)
    arc1, arc2 = circle.split(isects_circle)
    if arc1.arclen() < arc2.arclen():
        arc = arc1
    else:
        arc = arc2
         
    isects_line.sort()
    line1, line2, line3 = line.split(isects_line)
    segment = line2 << arc

#Draw a complete triangle pixel given c,x,y,r,g,b
#Where c is the canvas
#x,y are the coordinates of the center of the triangle
#r,g,b are the degree of red,blue and green in the triangle
#these should be a number between 0-9
def draw_triangle(c,x,y,r,g,b):
    #draws main triangle outline and fill
    pMain = path.path(path.moveto(x,y+hCornerCenter), path.lineto(x+.5,y-hCenter),
                      path.lineto(x-.5,y-hCenter), path.closepath())
    c.stroke(pMain, [deco.filled([color.grey(0)])])

    #draw r,g,b triangles
    pRed = draw_rgb(c,x,y,"red",0,r)
    pGreen = draw_rgb(c,x,y,"green",1,g)
    pBlue = draw_rgb(c,x,y,"blue",2,b)

    fill_intersection(c,pRed,pGreen,"yellow",r,g)

    
    
#Main Commands
c = canvas.canvas()
draw_triangle(c,0,0,9,5,9)

c.writeEPSfile()
c.writePDFfile()
