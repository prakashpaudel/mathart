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
##        c.fill(p, [color.rgb.red])
##    elif(col == "green"):
##        c.fill(p, [color.rgb.green])
##    else:
##        c.fill(p, [color.rgb.blue])
    return p

#
def fill_intersection(c,p1,p2,col,i1,i2):

    #Get original segment pieces
    p1a, p1b, p1c = p1.split([0,(p1.arclen()-1)/2,(p1.arclen()-1)/2+1])
    p2a, p2b, p2c = p2.split([0,(p2.arclen()-1)/2,(p2.arclen()-1)/2+1])
    if(i1>5 and i2>5):
        p1_seg = p1b
        p2_seg = p2a
    elif((i1>5 and i2<=5) or (i1<=5 and i2>5)):
        p1_seg = p1b
        p2_seg = p2a
    c.stroke(p1_seg, [color.rgb.red])
    c.stroke(p2_seg, [color.rgb.green])
##    (p1x1,p1y1) = p1.at(0)
##    (p1x2,p1y2) = p1.at(p1.end()-.5)
##    (p2x1,p2y1) = p2.at(0)
##    (p2x2,p2y2) = p2.at(.5)
##    p1_inter = path.line(p1x1,p1y1,p1x2,p1y2)
##    p2_inter = path.line(p2x1,p2y1,p2x2,p2y2)
####    c.stroke(p1_inter, [color.rgb.red])
####    c.stroke(p2_inter, [color.rgb.green])
##    isect_p1, isect_p2 = p1_inter.intersect(p2_inter)
##    p1_len1, p1_len2 = p1_inter.split(isect_p1)
##    p2_len1, p2_len2 = p2_inter.split(isect_p2)
##    
##
####    segment = p1b << p1_len1 << p2_len1 << p2a
##
##    segment = p2_seg << p2_len1 << p1_len1 << p1_seg
##
##    segment.append(path.closepath())
##    
    
##    c.stroke(p1b, [color.rgb.red])
##    c.stroke(p2a, [color.rgb.green])
    
##    c.stroke(segment, [color.cmyk.Yellow])


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

##    c.stroke(pRed, [color.rgb.red])
##    c.stroke(pGreen, [color.rgb.green])

    fill_intersection(c,pRed,pGreen,"yellow",r,g)

    
    
#Main Commands
c = canvas.canvas()
draw_triangle(c,0,0,9,4,1)

c.writeEPSfile()
c.writePDFfile()
