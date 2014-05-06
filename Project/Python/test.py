from pyx import *
from math import *
# Global Constants

s = 1.0
h = (sqrt(3)/2)*s
hCenter = h/3
hCornerCenter = 2*h/3
bend = h/4

def get_color(col):
    if(col == "black"):
        return color.rgb.black
    elif(col == "white"):
        return color.rgb.white
    elif(col == "grey"):
        return color.rgb.gray
    elif(col == "red"):
        return color.rgb.red
    elif(col == "green"):
        return color.rgb.green
    elif(col == "blue"):
        return color.rgb.blue
    elif(col == "yellow"):
        return color.cmyk.Yellow
    elif(col == "cyan"):
        return color.cmyk.Cyan
    elif(col == "magenta"):
        return color.cmyk.Magenta

#Create individual rgb triagnles with 6 inputs: c,x,y,col,o,i
# c is the canvas
# the x and y coordinates of the center of the triangle
# col is the color of the triangle (red,green or blue)
# o is the orientation of the triangle (0-2) (where 0=0 degrees, 1=120 degrees, 2=240 degrees)
# i is the intensity of the color (0-9) (higher number = brighter)
# it returns the path of the triangle
def draw_rgb(c,x,y,col,o,i):
    iIncrement = bend/5  #length increment for each level change in intensity

    yOffset = (i*iIncrement)-bend

    p = path.path(path.moveto(x,y), path.rmoveto(0,yOffset),
                  path.rlineto(.5,-yOffset-hCenter), path.rlineto(-1,0),
                  path.closepath())
    
    #apply rotation transformation
    t = trafo.trafo()
    t1 = trafo.trafo()
    t = t.translated(-x,-y)
    t = t.rotated(o*120)
    p = p.transformed(t)
    t1 = t1.translated(x,y)
    p = p.transformed(t1)

    #fill path
    c.stroke(p, [get_color(col)])
    
    return p

#
def fill_intersection(c,p1,p2,col,i1,i2):

    #Define line segments
    p1_diagonal = (p1.arclen()-1)/2
    p2_diagonal = (p2.arclen()-1)/2
    p1a, p1b, p1c = p1.split([0,p1_diagonal,p1_diagonal+1])
    p2a, p2b, p2c = p2.split([0,p2_diagonal,p2_diagonal+1])

    #For all
    (p1x1,p1y1) = p1.at(0)        
    (p2x1,p2y1) = p2.at(0)
    
    if(i1>5 and i2>5):
        (p1x2,p1y2) = p1.at(p1_diagonal+1)
        (p2x2,p2y2) = p2.at(p2_diagonal)
    elif(i1>5 and i2<=5 and i1+i2>10):
        (p1x2,p1y2) = p1.at(p1_diagonal)
        (p2x2,p2y2) = p2.at(p2_diagonal)
    elif(i1<=5 and i2>5 and i1+i2>10):
        (p1x2,p1y2) = p1.at(p1_diagonal+1)
        (p2x2,p2y2) = p2.at(p2_diagonal+1)
    else:
        return
    
    p1_seg = p1b
    p2_seg = p2a
    p1_inter = path.line(p1x1,p1y1,p1x2,p1y2)
    p2_inter = path.line(p2x1,p2y1,p2x2,p2y2)

##    c.stroke(p1_seg, [color.rgb.red])
##    c.stroke(p2_seg, [color.rgb.green])
##    c.stroke(p1_inter, [color.rgb.red])
##    c.stroke(p2_inter, [color.rgb.green])

    #split on intersection point
    isect_p1, isect_p2 = p1_inter.intersect(p2_inter)
    p1_len1, p1_len2 = p1_inter.split(isect_p1)
    p2_len1, p2_len2 = p2_inter.split(isect_p2)

    #form intersecting path
    if(i1>5 and i2>5):
        segment = p2_seg << p2_len1 << p1_len1 << p1_seg
        return p2_len1 << p1_len1
    elif(i1>5 and i2<=5):
        segment = p2_seg << p2_len1 << p1_len2
        return p2_len1
    elif(i1<=5 and i2>5):
        segment =  p1_seg << p1_len1 << p2_len2
        return p1_len1
    segment.append(path.closepath())

    #fill new path
    c.fill(segment, [get_color(col)])

def fill_intersections(c,p1,p2,p3,r,g,b):
    #fill 2-triangle overlaps and get intersection points
    seg1 = fill_intersection(c,p1,p2,"yellow",r,g)
    seg2 = fill_intersection(c,p2,p3,"cyan",g,b)
    seg3 = fill_intersection(c,p3,p1,"magenta",b,r)

    #all three overlap case
    #Define line segments
    p1_diagonal = (p1.arclen()-1)/2
    p2_diagonal = (p2.arclen()-1)/2
    p3_diagonal = (p3.arclen()-1)/2
    
    
##    if(r+g>10 and g+b>10 and b+r>10):
##        if(r>5):
##            if(g>5):
##                if(b>5):
##                    segment = seg1 << seg2 << seg3
##                else:
##                    segment = seg1 << 
                
        
        
        p1a, p1b = p1.split([isect3b,p1.arclen()-isect1a])
        p2a, p2b = p2.split([isect1b,p2.arclen()-isect2a])
        p3a, p3b = p3.split([isect2b,p3.arclen()-isect3a])
        segment = p1b << p2b << p3b
        segment.append(path.closepath())
        #fill new path
        c.fill(segment, [get_color("white")])
    else:
        return

#Draw a complete triangle pixel given c,x,y,r,g,b
#Where c is the canvas
#x,y are the coordinates of the center of the triangle
#r,g,b are the degree of red,blue and green in the triangle
#these should be a number between 0-9
def draw_triangle(c,x,y,r,g,b):
    #draws main triangle outline and fill
    pMain = path.path(path.moveto(x,y+hCornerCenter), path.lineto(x+.5,y-hCenter),
                      path.lineto(x-.5,y-hCenter), path.closepath())
    c.stroke(pMain, [deco.filled([get_color("black")])])

    #draw r,g,b triangles
    pRed = draw_rgb(c,x,y,"red",0,r)
    pGreen = draw_rgb(c,x,y,"green",1,g)
    pBlue = draw_rgb(c,x,y,"blue",2,b)

##    fill_intersections(c,pRed,pGreen,pBlue,r,g,b)
    
    
#Main Commands
c = canvas.canvas()

###All possible values
##count =0
##for i in range(1,9):
##    for j in range(1,9):
##        for k in range(1,9):
##            draw_triangle(c,count % 12,floor(count/12),i,j,k)
##            count +=1

draw_triangle(c,0,0,9,9,9)

c.writeEPSfile()
c.writePDFfile()
