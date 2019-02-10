from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import csv
global my_images

def accessibility(row):
    if (row[7] == 'Yes'):
        wheelchairLabel.config(fg='green',text='YES')
    elif (row[7] == 'No'):
        wheelchairLabel.config(fg='red', text='NO')
    else:
        wheelchairLabel.config(fg='orange')

    if (row[8] == 'Yes'):
        elevatorLabel.config(fg='green',text='YES')
    elif (row[8] == 'No'):
        elevatorLabel.config(fg='red', text='NO')
    else:
        elevatorLabel.config(fg='orange')

    if (row[9] == 'Yes'):
        parkingLabel.config(fg='green',text='YES')
    elif (row[9] == 'No'):
        parkingLabel.config(fg='red', text='NO')
    else:
        parkingLabel.config(fg='orange')

    if (row[10] == 'Yes'):
        rideshareLabel.config(fg='green',text='YES')
    elif (row[10] == 'No'):
        rideshareLabel.config(fg='red', text='NO')
    else:
        rideshareLabel.config(fg='orange')

    if (row[11] == 'Yes'):
        transitLabel.config(fg='green',text='YES')
    elif (row[11] == 'No'):
        transitLabel.config(fg='red', text='NO')
    else:
        transitLabel.config(fg='orange')

    if (row[12] == 'Yes'):
        washroomLabel.config(fg='green',text='YES')
    elif (row[12] == 'No'):
        washroomLabel.config(fg='red', text='NO')
    else:
        washroomLabel.config(fg='orange')

def thebindinggoat(event, x):
    row = returnEventData(x)
    v.set(row[6])
    canvas.pack()
    im = Image.open(row[13])
    im = im.resize((300, 200), Image.ANTIALIAS)
    my_images = []
    my_images.append(ImageTk.PhotoImage(im))
    my_image_number = 0

    image_on_canvas = canvas.create_image(0, 0, anchor=NW, image=my_images[my_image_number])
    canvas.itemconfig(image_on_canvas, image=my_images[my_image_number])
    canvas.image = my_images[my_image_number]
    accessibility(row)

def returnEventData(x):
    with open('events.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0;
        for row in reader:
            if (i != (x)):
                i = i + 1
                continue
            else:
                return row
def captureNum(x):
    return lambda ev: thebindinggoat(ev, x)

root = Tk()
root.geometry("800x600")
root.title("Social Calendar")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)

left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
container = Frame(left, borderwidth=2, relief="solid")
box1 = Frame(right, borderwidth=2, relief="solid", width=100, height=100)
box2 = Frame(right, borderwidth=2, relief="solid")

box11 = Frame(box2, borderwidth=2, relief="solid")
box3 = Frame(box11, borderwidth=2, relief="solid")
box4 = Frame(box11, borderwidth=2, relief="solid")
box5 = Frame(box11, borderwidth=2, relief="solid")

box9 = Frame(box2, borderwidth=2, relief="solid")
box6 = Frame(box9, borderwidth=2, relief="solid")
box7 = Frame(box9, borderwidth=2, relief="solid")
box8 = Frame(box9, borderwidth=2, relief="solid")

w = Label(left, text="List of Activities")
w.pack();


color='brown'
canv = Canvas(left, bg=color, relief=SUNKEN)
canv.config(width=300, height=200)
canv.config(scrollregion=(0,0,300, 1000))
canv.config(highlightthickness=0)

sbar = Scrollbar(left)
sbar.config(command=canv.yview)
canv.config(yscrollcommand=sbar.set)
sbar.pack(side=RIGHT, fill=Y)
canv.pack(side=LEFT, expand=YES, fill=BOTH)
with open('events.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0;
    for row in reader:
        print(row)
        if (i == 0):
            i=i+1
            continue
        block = Frame(canv, borderwidth=2, relief='solid')
        block.columnconfigure(0, weight=1)
        w = Frame(block)
        w.pack(expand=True, fill="both", padx=10, pady=15, side="top");
        name = Label(w, text="Event Name: {}".format(row[0]))
        name.pack( side="top", fill="x",expand=True)
        location = Label(w, text="Location: {}".format(row[1]))
        location.pack(side="left", fill="x", expand=True)
        time = Label(w, text="Time: {}".format(str(row[2]) + " - " + str(row[3])))
        time.pack(side="right", fill="x", expand=True)

        block.bind("<Button-1>", captureNum(i))
        location.bind("<Button-1>",captureNum(i))
        name.bind("<Button-1>",captureNum(i) )
        time.bind("<Button-1>",captureNum(i) )

        canv.create_window((0, (i*90 - 70)), window=block, anchor="nw", tags="frame", width=480)
        i += 1

label8 = Label(right, text="About the Event")
label8.pack()

v = StringVar()
label4 = Label(box1, textvariable=v, wraplength=280 ).pack()

label9 = Label(right, text="Key Information")

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
box1.pack(expand=True, fill="both", padx=5, pady=5)
box1.pack_propagate(0)
canvas = Canvas(box1, width=200, height=150)
label9.pack()
box2.pack(expand=True, fill="both", padx=5, pady=5)
box2.pack_propagate(0)
box9.pack(expand=True, fill="x", padx=5, pady=5)
box11.pack(expand=True, fill="x", padx=5, pady=5)


box3.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label9 = Label(box3, text="Wheelchairs")
wheelchairLabel = Label(box3, text="")
box4.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label10 = Label(box4, text="Elevator")
elevatorLabel = Label(box4, text="")
box5.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label11 = Label(box5, text="Close Parking")
parkingLabel = Label(box5, text="")
box6.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label12 = Label(box6, text="Rideshare")
rideshareLabel = Label(box6, text="")
box7.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label13 = Label(box7, text="Transit")
transitLabel = Label(box7, text="")
box8.pack(expand=True, fill="x", padx=5, pady=5, side=LEFT)
label14 = Label(box8, text="Washrooms")
washroomLabel = Label(box8, text="")




label9.pack()
label10.pack()
label11.pack()
label12.pack()
label13.pack()
label14.pack()


wheelchairLabel.pack()
parkingLabel.pack()
rideshareLabel.pack()
transitLabel.pack()
washroomLabel.pack()
elevatorLabel.pack()



root.mainloop()
