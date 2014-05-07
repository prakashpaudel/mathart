from pyx import *
from math import *

# Global Constants
s = 1.0
h = (sqrt(3)/2)*s
hCenter = h/3
hCornerCenter = 2*h/3
bend = h/3
L = 10

def get_color(col):
    if(col == "black"):
        return color.rgb.black
    elif(col == "white"):
        return color.rgb.white
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
    c.fill(p, [get_color(col)])
    
    return p

def make_line(p, start, end):
    (px1,py1) = p.at(start)        
    (px2,py2) = p.at(end)
    return path.line(px1,py1,px2,py2)

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
    elif(i1>5 and i2<=5 and i1-i2<7 and i1+i2>L):
        (p1x2,p1y2) = p1.at(p1_diagonal)
        (p2x2,p2y2) = p2.at(p2_diagonal)
    elif(i1<=5 and i2>5 and i2-i1<7 and i1+i2>L):
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
    elif(i1>5 and i2<=5):
        segment = p2_seg << p2_len1 << p1_len2
    elif(i1<=5 and i2>5):
        segment =  p1_seg << p1_len1 << p2_len2

    segment.append(path.closepath())

    #fill new path
    c.fill(segment, [get_color(col)])

    return p1_seg, p1_len1, p1_len2, p2_seg, p2_len1, p2_len2

def middle_intersection_helper(c, path1a, path1b, path2a, path2b, path3a, path3b):
    p1_inter = path1a
    a_p1_len1 = path1b
    p2_inter = path2a
    a_p2_len1 = path2b
    b_p2_len1 = path3a
    c_p1_len1 = path3b


    #split1
    isect_p1, isect_p2 = p1_inter.intersect(a_p1_len1)
    p1_len1, p1_len2 = p1_inter.split(isect_p1)
    p2_len1, p2_len2 = a_p1_len1.split(isect_p2)


    #split2
    isect_p3, isect_p4 = p2_inter.intersect(a_p2_len1)
    p3_len1, p3_len2 = p2_inter.split(isect_p3)
    p4_len1, p4_len2 = a_p2_len1.split(isect_p4)

    #segment construction and fill
    segment1 = b_p2_len1 << p4_len2
    segment2 = p2_len2 << c_p1_len1
    segment1.append(path.closepath())
    segment2.append(path.closepath())
    c.fill(segment1, [get_color("white")])
    c.fill(segment2, [get_color("white")])

def fill_intersections(c,p1,p2,p3,r,g,b):
    #fill 2-triangle overlaps and get intersection points
    fill_intersection(c,p1,p2,"yellow",r,g)
    fill_intersection(c,p2,p3,"cyan",g,b)
    fill_intersection(c,p3,p1,"magenta",b,r)

    #all three overlap case
    #Define line segments
    p1_diagonal = (p1.arclen()-1)/2
    p2_diagonal = (p2.arclen()-1)/2
    p3_diagonal = (p3.arclen()-1)/2
    p1a, p1b, p1c = p1.split([0,p1_diagonal,p1_diagonal+1])
    p2a, p2b, p2c = p2.split([0,p2_diagonal,p2_diagonal+1])
    p3a, p3b, p3c = p3.split([0,p3_diagonal,p3_diagonal+1])

    if(fabs(r-g)<7 and r+g>L and fabs(g-b)<7 and g+b>L and fabs(b-r)<7 and b+r>L):
        a_p1_seg, a_p1_len1, a_p1_len2, a_p2_seg, a_p2_len1, a_p2_len2 = fill_intersection(c,p1,p2,"yellow",r,g)
        b_p1_seg, b_p1_len1, b_p1_len2, b_p2_seg, b_p2_len1, b_p2_len2 = fill_intersection(c,p2,p3,"cyan",g,b)
        c_p1_seg, c_p1_len1, c_p1_len2, c_p2_seg, c_p2_len1, c_p2_len2 = fill_intersection(c,p3,p1,"magenta",b,r)

        if(r>5 and g>5 and b>5):
            segment = a_p2_len1 << a_p1_len1 << c_p2_len1 << c_p1_len1 << b_p2_len1 << b_p1_len1
            c.fill(segment, [get_color("white")])
        elif(b<=5):
            p1_inter = make_line(p3a,0, p3_diagonal)
            p2_inter = make_line(p3b,0, p3_diagonal)
            middle_intersection_helper(c, p1_inter, a_p1_len1, p2_inter, a_p2_len1, b_p2_len1, c_p1_len1)
        elif(g<=5):
            p1_inter = make_line(p2a,0, p2_diagonal)
            p2_inter = make_line(p2b,0, p2_diagonal)
            middle_intersection_helper(c, p1_inter, c_p1_len1, p2_inter, c_p2_len1, a_p2_len1, b_p1_len1)
        elif(r<=5):
            p1_inter = make_line(p1a,0, p1_diagonal)
            p2_inter = make_line(p1b,0, p1_diagonal)
            middle_intersection_helper(c, p1_inter, b_p1_len1, p2_inter, b_p2_len1, c_p2_len1, a_p1_len1)
                

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

    fill_intersections(c,pRed,pGreen,pBlue,r,g,b)
    
    
#Main Commands
c = canvas.canvas()

#All possible values
count=0
for i in range(0,L):
    for j in range(0,L):
        for k in range(0,L):
##            print(i,j,k,count)
            draw_triangle(c,count % L,floor(count/L),i,j,k)
            count +=1

##draw_triangle(c,0,0,9,9,9)
##draw_triangle(c,1,0,9,9,4)
##draw_triangle(c,2,0,9,4,9)
##draw_triangle(c,3,0,4,9,9)

c.writeEPSfile()
c.writePDFfile()
