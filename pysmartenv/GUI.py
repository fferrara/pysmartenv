"""
Graphical User Interface
It creates the main windows and draw a basic graphic structure, using Tk library.

Draws a Panel according with its descriptor file, which contains option names, images, messages, etc.
"""

import Tkinter as tk
import Image as img
import ImageTk as imgtk
import panel


class GUI(tk.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, master=None):
        tk.Tk.__init__(self)
        self.resizable(width=False, height=False)  # Make window not resizable
        self.minsize(width=self.WIDTH, height=self.HEIGHT)  # Window size
        # Window at center of screen
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w / 2 - self.WIDTH / 2
        y = h / 2 - self.HEIGHT / 2
        self.geometry("%dx%d+%d+%d" % ((self.WIDTH, self.HEIGHT) + (x, y)))

        self.title('Prova')  # Window title
        self._draw()

    def _draw(self):
        # grid (table) geometry
        # window frame: 2 rows x 1 columns
        # up frame: 1 row x 1 column
        # bottom frame: 1 row x 4 columns
        self.upFrame = tk.Frame(self, height=360, width=760)  # create frame
        self.upFrame.grid_propagate(False)  # size fixed
        self.upFrame.columnconfigure(0, weight=1)  # first column takes all space
        self.upFrame.grid(row=0, column=0, padx=20, pady=20)  # show at top
        self.bottomFrame = tk.Frame(self, height=160, width=760)  # create frame
        self.bottomFrame.grid_propagate(False)  # size fixed
        self.bottomFrame.grid(row=1, column=0, padx=20, pady=20)  # show at bottom
        # each column take the same space
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.bottomFrame.columnconfigure(2, weight=1)
        self.bottomFrame.columnconfigure(3, weight=1)

    def show_panel(self, panel):
        # fill bottom frame
        self.littleimg = [None] * len(panel.options)
        self.optionLabels = [None] * len(panel.options)
        for i in range(len(panel.options)):
            # create and visualize option label
            self.optionLabels[i] = tk.Label(self.bottomFrame, text=panel.options[i].name)
            self.optionLabels[i].grid(column=i, row=0)
            # create and visualize option icon
            icon = img.open(panel.options[i].imgFile).resize((100, 100), img.ANTIALIAS)
            self.littleimg[i] = imgtk.PhotoImage(icon)
            tk.Label(self.bottomFrame, image=self.littleimg[i]).grid(row=1, column=i, sticky=tk.S)

        # call update_GUI to fill the top frame, showing currently selected option
        self.update_GUI(panel)


    def update_GUI(self, panel):
        currentOption = panel.currentOption
        # fill top frame
        tk.Label(self.upFrame, text=currentOption.name).grid(row=0, column=0)
        I = img.open(currentOption.imgFile).resize((300, 300), img.ANTIALIAS)
        self.currentImg = imgtk.PhotoImage(I)
        self.currentImgLabel = tk.Label(self.upFrame, image=self.currentImg)
        self.currentImgLabel.grid(row=1, column=0, sticky=tk.S)

        for label in self.optionLabels:
            if label['text'] == currentOption.name:
                label.configure(bd = 10)
                label.configure(relief = 'ridge')
                label.configure(fg = '#f00')
            else:
                label.configure(bd = 2)
                label.configure(relief = 'flat')
                label.configure(fg = '#000')

        self.after(500, self.update_GUI, panel)

# Test class
if __name__ == '__main__':
    from threading import Thread
    from time import sleep

    def threaded_function(arg):
        sleep(2)
        arg.currentOption = arg.options[1]
        sleep(2)
        arg.currentOption = arg.options[2]
        sleep(2)
        arg.currentOption = arg.options[3]

    app = GUI()
    jsonFile = '../resources/sala.panel'
    panel = panel.Panel(jsonFile)

    thread = Thread(target = threaded_function, args = (panel, ))
    thread.start()

    app.show_panel(panel)
    app.mainloop()

