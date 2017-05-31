#!/usr/bin/python3

import tkinter as tk
from PIL import Image, ImageTk
import os

def all_jpg_to_gif():
    for filename in os.listdir('.'):
        basename, ext = os.path.splitext(filename)
        if ext.lower() in ('.jpg', '.jpeg'):
            Image.open(filename).save(basename+'.gif')

class Matrix(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.l_values = []
        for i in range(9):
            ent = tk.Entry(self, width=3)
            row, column = divmod(i, 3)
            ent.grid(row=row, column=column)
            self.l_values.append(ent)

        plus = tk.Label(self, text='+')
        plus.grid(row = 1, column = 3)

        self.affine = []
        for i in range(3):
            ent = tk.Entry(self, width=3)
            ent.grid(row=i, column=4)
            self.affine.append(ent)

    def convert_values(self, data_list):
        '''converts a list of Entry widgets to floats'''
        data = []
        for ent in data_list:
            try:
                data.append(float(ent.get()))
            except ValueError:
                data.append(0)
        return data

    def get_l_values(self):
        return self.convert_values(self.l_values)

    def get_affine(self):
        return self.convert_values(self.affine)

class Window(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        master.title('Picture thingy')

        # make gif versions of all the jpg files in directory
        # all_jpg_to_gif() # uncomment this line if you really want this functionality

        self.oldimg = Image.open('picture.jpg')
        oldimg = ImageTk.PhotoImage(self.oldimg)
        oldpic = tk.Label(self, image=oldimg)
        oldpic.oldimg = oldimg
        oldpic.grid(row=0, column=0, rowspan=3)

        self.newpic = tk.Label(self)
        self.newpic.grid(row=0, column=1, rowspan=3)
        self.update_output(Image.open('here.jpg'))

        self.mat = Matrix(self)
        self.mat.grid(row=0, column=3)

        but_go = tk.Button(self, text="go", command=self.process)
        but_go.grid(row=1, column=3)

        self.output_label = tk.Label(self, text="Press go")
        self.output_label.grid(row=2, column=3)

    def process(self):
        l_val = self.mat.get_l_values()
        a_val = self.mat.get_affine()

        w,h = self.oldimg.size
        newim = Image.new(self.oldimg.mode, self.oldimg.size)
        for x in range(w):
            self.output_label.config(text="working on {}".format(w - x))
            self.output_label.update() # push the change to the screen
            for y in range(h):
                p = self.oldimg.getpixel((x,y))

                pnew=(l_val[0]*p[0]+l_val[1]*p[1]+l_val[2]*p[2]+a_val[0],
                      l_val[3]*p[0]+l_val[4]*p[1]+l_val[5]*p[2]+a_val[1],
                      l_val[6]*p[0]+l_val[7]*p[1]+l_val[8]*p[2]+a_val[2])

                pnew=tuple(map(int, pnew))
                newim.putpixel((x,y), pnew) #alternative
        newim.save('here.jpg')
        self.update_output(newim)

    def update_output(self, new_data):
        newimg = ImageTk.PhotoImage(new_data)
        self.newpic.config(image=newimg)
        self.newpic.image = newimg

def main():
    root = tk.Tk()
    win = Window(root)
    win.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
