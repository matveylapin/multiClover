import tkinter as tk
import tkinter.messagebox as mb
import math
from tomlGen import generateFiles

WIDTH = 1000
HEIGHT = 1000

DRONE_SIZE = 300
BASE_SIZE = 250

drones = []

root = tk.Tk()
#pilImage = Image.open("svg/drone.png")
#drone_image = ImageTk.PhotoImage(pilImage)

def drawAllDrones(old_s, new_s):
    drone_canvas.delete('all')
    if len(drones) == 0:
        return
    x0 = sum([i['x'] for i in drones]) / len(drones)
    y0 = sum([i['y'] for i in drones]) / len(drones)

    sort_key = lambda p: math.sqrt( (x0 - p['x'])**2 + (y0 - p['y'])**2 )
    drones.sort(key = sort_key)

    for drone in drones:
        x = drone['x']
        y = drone['y']
        drone_canvas.create_rectangle(x, y, x + old_s, y + old_s,
                            fill='white',
                            outline='white')

    for i, drone in enumerate(drones):
        drone['x'] = math.floor(drone['x'] / old_s) * new_s
        drone['y'] = math.floor(drone['y'] / old_s) * new_s
        x = drone['x']
        y = drone['y']
        drone_canvas.create_rectangle(x+5, y+5, x + new_s - 5, y + new_s - 5,
                            fill='red',
                            outline='white')
        drone_canvas.create_text((x + int(new_s / 2)),
                                 (y + int(new_s /2)),
                                 text = str(i),
                                 font = 'Verdana 12',
                                 fill = 'black')

def updateDroneSize():
    global DRONE_SIZE
    global BASE_SIZE
    temp1 = 0
    temp2 = 0
    try:
        temp1 = int(edtDroneSize.get())
        temp2 = int(edtBaseSize.get())
    except ValueError:
        mb.showerror('Error', 'Value can be only integer!\n Measurements in mm')
    
    if (temp1 <= 0) or (temp2 <= 0):
        mb.showerror('Error', 'Nice joke, drone size <=0\n Good work!!')
    else:
        drawAllDrones(DRONE_SIZE, temp1)
        BASE_SIZE = int(temp2 / math.sqrt(2))
        DRONE_SIZE = int(temp1 / math.sqrt(2))


def getFiles():
    generateFiles([i.copy() for i in drones], DRONE_SIZE, BASE_SIZE)

root.title('Geometry generator')
root.rowconfigure(0, minsize=1000, weight=1)
root.columnconfigure(1, minsize=1000, weight=1)

drone_canvas = tk.Canvas(root,
            bg='white')

control_frame = tk.Frame(root,
            bg='black',
            relief=tk.RAISED)

lable1 = tk.Label(control_frame, text = 'Drone size(mm):', fg = 'white', bg = 'black')
edtDroneSize = tk.Entry(control_frame)
lable2 = tk.Label(control_frame, text = 'Motor base size(mm):', fg = 'white', bg = 'black')
edtBaseSize = tk.Entry(control_frame)
btnApplySize = tk.Button(control_frame, text='Apply', command=updateDroneSize)
btnGenerateFiles = tk.Button(control_frame, text='Generate', command=getFiles)

lable1.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
edtDroneSize.grid(row=1, column=0, sticky="ew", padx=10)
lable2.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
edtBaseSize.grid(row=3, column=0, sticky="ew", padx=10)
btnApplySize.grid(row=4, column=0, padx=10, pady=20)
btnGenerateFiles.grid(row=5, column=0, padx=10, pady=20)
control_frame.grid(row=0, column=0, sticky="ns")
drone_canvas.grid(row=0, column=1, sticky="nsew")


def drawDroneEvent(event):
    global DRONE_SIZE
    x = math.floor(event.x / DRONE_SIZE) * DRONE_SIZE
    y = math.floor(event.y / DRONE_SIZE) * DRONE_SIZE
    if {'x': x, 'y': y} in drones:
        return
    
    drones.append(({'x': x, 'y': y}))

    drawAllDrones(DRONE_SIZE, DRONE_SIZE)

    print('Drone #' + str(len(drones)) + ' added!')

drone_canvas.bind("<Button-1>", drawDroneEvent)

def deleteDrone(event):
    global DRONE_SIZE
    x = math.floor(event.x / DRONE_SIZE) * DRONE_SIZE
    y = math.floor(event.y / DRONE_SIZE) * DRONE_SIZE
    if {'x': x, 'y': y} in drones:
        i = drones.index({'x': x, 'y': y})    
        drones.pop(i)
        drawAllDrones(DRONE_SIZE, DRONE_SIZE)
        print('Drone #' + str(i+1) + ' deleted!')

drone_canvas.bind("<Button-3>", deleteDrone)
root.mainloop()