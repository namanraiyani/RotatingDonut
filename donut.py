import math 
import numpy as np
import time
import sys

def rotate(x, y, z, ax, ay, az):
    ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
    rotation_matrix = [
        [math.cos(ay) * math.cos(az), math.cos(az) * math.sin(ax) * math.sin(ay) - math.cos(ax) * math.sin(az), math.sin(ax) * math.sin(az) + math.cos(ax) * math.cos(az) * math.sin(ay)],
        [math.cos(ay) * math.sin(az), math.cos(ax) * math.cos(az) + math.sin(ax) * math.sin(ay) * math.sin(az), math.cos(ax) * math.sin(ay) * math.sin(az) - math.cos(az) * math.sin(ax)],
        [-math.sin(ay),               math.cos(ay) * math.sin(ax),                                                math.cos(ax) * math.cos(ay)]
    ]
    return [round(coord, 12) for coord in np.dot(rotation_matrix, [x, y, z])]

def project(x, y, z, width, height, scale = 150, distance = 10):
    aspect_ratio=2
    return [int(((width/2) + (x*scale*aspect_ratio) / (z+distance))), int((height/2) - (y*scale / (z+distance)))]

def make_donut(R, r):
    coords = []
    for theta in np.arange(0, 2*math.pi, 0.25):
        for phi in np.arange(0, 2*math.pi, 0.09):
            x = (R + r*math.sin(theta))*math.cos(phi)
            y = (R + r*math.sin(theta))*math.sin(phi)
            z = r*math.cos(theta)

            nx = math.cos(theta)*math.cos(phi)
            ny = math.cos(theta)*math.sin(phi)
            nz = math.sin(theta)
            coords.append([[x,y,z], [nx,ny,nz]])
    return coords

def rotate_point_and_normal(pos, normal, ax,ay,az):
    rotated_pos=rotate(pos[0],pos[1],pos[2], ax,ay,az)
    rotated_normal=rotate(normal[0],normal[1],normal[2],ax,ay,az)
    return [rotated_pos, rotated_normal]

def get_distances(coords, light_source):
    lx,ly,lz = light_source
    return [(x,y,z,(lx-x)**2 + (ly-y)**2 + (lz-z)**2) for x,y,z in coords]

def get_ascii(d):
    shades = ".:=+*0@#"
    ind = int(d * (len(shades)-1)) 
    ind = max(0, min(ind, len(shades)-1))
    return shades[ind]

def shade_points(coords,screen):
    light_dir = np.array(light_source)
    for (pos, normal) in coords:
        x,y,z=pos
        nx,ny,nz=normal
        norm_vec=np.array([nx,ny,nz])
        norm_vec/=np.linalg.norm(norm_vec)

        light_vec=(light_dir-np.array([x,y,z]))*2
        light_vec /= np.linalg.norm(light_vec)
        intensity = np.dot(light_vec, norm_vec)
        brightness=max(0,min(intensity,1))
        x,y=project(x,y,z,width,height)
        if 0<=y<height and 0<=x<width:
            screen[y][x] = get_ascii(brightness)
    return screen

R = 1.25
r = 0.5
R, r = 1, 0.45
width = 225
height = 65
light_source = [2,-0.75,1]

def main():
    coords = make_donut(R, r)
    while True:
        print("\033[H", end='') 
        screen = [[' ']*width for _ in range(height)]
        screen = shade_points(coords,screen)
        output = '\n'.join(''.join(row) for row in screen)
        sys.stdout.write(output)
        sys.stdout.flush()
        for i in range(len(coords)):
            coords[i] = rotate_point_and_normal(coords[i][0],coords[i][1],12,6,5)
        time.sleep(1/40)
if __name__=="__main__":
    main()
