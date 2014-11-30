"""
Graphical User Interface
It creates the main windows and draw a basic graphic structure, using Tk library.

Draws a Panel according with its descriptor file, which contains option names, images, messages, etc.
"""

import Tkinter as tk
import Image as img
import ImageTk as imgtk

class GUI(tk.Tk):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self, master=None):
        tk.Tk.__init__(self)
        self.resizable(width=False, height=False) # Make window not resizable
        self.minsize(width=self.WIDTH, height=self.HEIGHT) # Window size
        # Window at center of screen
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w/2 - self.WIDTH/2
        y = h/2 - self.HEIGHT/2
        self.geometry("%dx%d+%d+%d" % ((self.WIDTH,self.HEIGHT) + (x, y)))

        self.title('Prova') # Window title
        self.configure(background='blue')
        self._draw()

    def _draw(self):
        # grid (table) geometry
        # window frame: 2 rows x 1 columns
        # up frame: 1 row x 1 column
        # bottom frame: 1 row x 4 columns
        self.upFrame = tk.Frame(self, bg='#f00', height=360, width=760) # create frame
        self.upFrame.grid_propagate(False) # size fixed
        self.upFrame.columnconfigure(0, weight=1) # first column takes all space
        self.upFrame.grid(row=0,column=0,padx=20, pady = 20) # show at top
        self.bottomFrame = tk.Frame(self, bg='#0f0', height=160, width=760) # create frame
        self.bottomFrame.grid_propagate(False)# size fixed
        self.bottomFrame.grid(row=1,column=0,padx=20, pady=20) # show at bottom
        # each column take the same space
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.bottomFrame.columnconfigure(2, weight=1)
        self.bottomFrame.columnconfigure(3, weight=1)

        # fill top frame
        self.currentName = tk.Label(self.upFrame, text='VENTILADOR')
        self.currentName.grid(row=0,column=0)
        i = img.open('../resources/vent.jpg').resize((300,300))
        self.currentImg = imgtk.PhotoImage(i)
        tk.Label(self.upFrame, image=self.currentImg).grid(row=1, column=0, sticky=tk.S)

        # fill bottom frame
        tk.Button(self.bottomFrame, text='Quit', command=self.quit).grid(column=0, row=0)
        tk.Button(self.bottomFrame, text='Quit', command=self.quit).grid(column=1, row=0)
        tk.Button(self.bottomFrame, text='Quit', command=self.quit).grid(column=2, row=0)
        tk.Button(self.bottomFrame, text='Quit', command=self.quit).grid(column=3, row=0)

    def show_panel(self, panel):
        raise NotImplementedError

    def update_GUI(self, panel, action):
        raise NotImplementedError

if __name__ == '__main__':
    app = GUI()
    app.mainloop()