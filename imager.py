#!/usr/bin/python3

import tkinter as tk
from PIL import Image
import os


class Window:


    def __init__(self, master):

        master.title('Picture thingy')

        #make gif versions of all the jpg files in directory
        list(map\
        (lambda _: Image.open(_).save(_.replace('jpg', 'gif'), 'gif'),\
        [_ for _ in os.listdir('.') if 'jpg' in _]))

        oldimg = tk.PhotoImage(file='picture.gif')
        oldpic = tk.Label(master, image=oldimg)
        oldpic.oldimg = oldimg
        oldpic.grid(row=0, column=0)

        #make list of tkinter variables for user input
        l_values = []
        for i in range(9):
            l_values.append(tk.StringVar())

        #set up matrix in GUI for user input
        linear = []
        for i in range(9):
            linear.append(tk.Entry(master, width=3))
            linear[i].configure(textvariable = l_values[i])
            linear[i].grid(row=(i//3 + 2), column=i%3 + 2)


        plus = tk.Label(text='+')
        plus.grid(row = 3, column = 5)

        a_values = []
        for i in range(3):
            a_values.append(tk.StringVar())

        affine = []
        for i in range(3):
            affine.append(tk.Entry(master, width=3))
            affine[i].configure(textvariable = a_values[i])
            affine[i].grid(row=i + 2, column=6)



        but_go = tk.Button(master, text="go", \
              command=lambda x=0:process(x))
        but_go.grid(row=0, column=2)

        output_label = tk.Label(master)
        output_label.grid()

        def process(x):
            l_val = []
            for i in range(9):
                try:
                    l_val.append(float(l_values[i].get()))
                except:
                    l_val.append(float(0))

            a_val=[]
            for i in range(3):
                try:
                    a_val.append(int(a_values[i].get()))
                except:
                    a_val.append(0)


            imob = Image.open('picture.jpg')
            w,h = imob.size
            newim = Image.new(imob.mode, imob.size)
            for _ in [(x,y) for x in range(w) for y in range(h)]:


                    #THIS IS WHAT I WANT TO DISPLAY IN GUI!!!!!
                    #AS IT RUNS SO IT COUNTS DOWN
                    print(w - _[0]) #how long this going to take?
                    output_label.config(text="working on {}".format(w - _[0]))
                    output_label.update() # push the change to the screen


                    p = imob.getpixel(_)

                    pnew=(l_val[0]*p[0]+l_val[1]*p[1]+l_val[2]*p[2]+\
                           a_val[0],\
                          l_val[3]*p[0]+l_val[4]*p[1]+l_val[5]*p[2]+\
                           a_val[1],\
                          l_val[6]*p[0]+l_val[7]*p[1]+l_val[8]*p[2]+\
                           a_val[2])

                    pnew=tuple(map(lambda x: int(x), pnew))
                    newim.putpixel(_, pnew) #alternative
            newim.save('here.jpg')
            newim.close()

        def count_label(newpic):

            new = Image.open('here.jpg').save('here.gif', 'gif')
            newimg = tk.PhotoImage(file='here.gif')
            newpic.config(image=newimg)
            newpic.image = newimg

            newpic.after(1000, count_label, newpic)


        newpic = tk.Label(master)
        newpic.grid(row=0, column=1)

        count_label(newpic)

root =  tk.Tk()
Window(root)
root.mainloop()
