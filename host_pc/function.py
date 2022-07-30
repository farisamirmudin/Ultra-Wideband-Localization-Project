import numpy as np
from sympy import *
from sympy.geometry import *
import matplotlib.pyplot as plt

def solve(point, distance):
    circles={}
    min_r = min(distance)
    for i in range (0, len(point)):
        circles[f'c{i}'] = Circle(point[i], distance[i])
        if distance[i] == min_r:
            str = f'c{i}'
            smallest_circle = circles[str]
    i_dict = {}
    i = 0
    for key1 in circles:
        for key2 in circles:
            if key1 != key2 and (f"{key1}_{key2}" and f"{key2}_{key1}") not in i_dict.keys():
                poc = intersection(circles[key1], circles[key2])
                if poc:
                    i_dict[f"{key1}_{key2}"] = poc
    length = len(i_dict)
    if length == 1:
        # print("Closest Point Algorithm")
        segments = {}
        for key in i_dict:
            if str not in key:
                for p in i_dict[key]:
                    dist = smallest_circle.center.distance(p)
                    segments[dist] = Segment(smallest_circle.center, p)
        min_dist = min(list(segments))
        pos =  intersection(segments[min_dist], smallest_circle)[0]

    if length == 2:
        # print("Small Circle Intersection")
        poc = list(i_dict.values())
        cross_i = {}
        for p1 in poc[0]:
            for p2 in poc[1]:
                cross_i[p1.distance(p2)] = [p1, p2]
        min_dist = min(list(cross_i))
        for point in cross_i[min_dist]:
            if not intersection(point,smallest_circle):
                segment = Segment(smallest_circle.center, point)
                pos = intersection(segment, smallest_circle)[0]
                break

    if length == 3:
        segment=[]
        j = 0
        for key in i_dict:
            poc = i_dict[key]
            segment.append(Segment(poc[j], poc[j+1]))
        concurrent = Segment.are_concurrent(segment[0], segment[1], segment[2])
        if concurrent:
            # print("Line Intersection Algorithm")
            pos = intersection(segment[0], segment[1])[0]
        else:
            # print("Comparison Approach of Intersection Distances")
            poc = []
            for key in i_dict:
                if str in key:
                    poc.extend(i_dict[key])
            d1 = poc[0].distance(poc[2])
            d2 = poc[1].distance(poc[3])
            if d1 < d2:
                pos = poc[0].midpoint(poc[2])
            else:
                pos = poc[1].midpoint(poc[3])

    return np.array([pos.x, pos.y])

def trilateration(points, distances, dim):
    with open('abc_param.txt', 'r') as f:
        lines = f.readlines()
        a=float(lines[0][4:])
        b=float(lines[1][4:])
        c=float(lines[2][4:])
    if dim == 3:
        p1,p2,p3,p4 = np.array(points)
        r1,r2,r3,r4 = np.array(distances)
    else:
        p1,p2,p3 = np.array(points)
        r1,r2,r3 = np.array(distances)
    e_x=(p2-p1)/np.linalg.norm(p2-p1)
    i=np.dot(e_x,(p3-p1))
    e_y=(p3-p1-(i*e_x))/(np.linalg.norm(p3-p1-(i*e_x)))
    e_z=np.cross(e_x,e_y)
    d=np.linalg.norm(p2-p1)
    j=np.dot(e_y,(p3-p1))
    x=((r1**2)-(r2**2)+(d**2))/(2*d)
    y=(((r1**2)-(r3**2)+(i**2)+(j**2))/(2*j))-((i/j)*(x))
    if dim == 2:
        ans1=p1+(x*e_x)+(y*e_y)
        return ans1
    z1=np.sqrt(max(0, r1**2-x**2-y**2))
    z2=-z1
    ans1=p1+(x*e_x)+(y*e_y)+(z1*e_z)
    ans2=p1+(x*e_x)+(y*e_y)+(z2*e_z)
    multp_z = lambda x:a*x**2+b*x+c
    ans1[2] = multp_z(ans1[2])
    return ans1
    # dist1=np.linalg.norm(p4-ans1)
    # dist2=np.linalg.norm(p4-ans2)
    # if np.abs(r4-dist1)<np.abs(r4-dist2):
    #     return ans1
    # else:
    #     return ans2

    
    


