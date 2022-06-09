import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from Analyzer import resume_df, df, included_strings  #df is a dataframe containing original user-extraction
from random import choices

"""
This python script imports from other local .py files to draw graphed data
to a tkinter canvas.
"""
class my_App(tk.Frame):
    def __init__(self, master, dataframe, origindf, included):
        super().__init__(master)
        self.master = master
        self.pack()
        self.dataframe = dataframe
        self.origindf = origindf
        self.width =self.winfo_screenwidth()
        self.height = self.winfo_screenheight()*.10 #we wont use a lot of canvas tools, reduce height
        self.handles = []
        self.included = included
        # Create all the widgets we want in
        # our window at the beginning.
        self.create_widgets()

    def create_widgets(self, header=3):
        # Create the widgets we want our window to have at startup.
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, background="white")

        #after the information is collected from draw, write text to the canvas:
        handle = self.canvas.create_text(self.width//2,self.height//2,text=f"It appears your {header} strongest traits are: {tuple(self.dataframe.head(header).index)}.")
        self.handles.append(handle)
        #self.generate listing button
        self.genlisting = tk.Button(text="Generate Word Listing", command=self.genlist)
        self.genlisting.pack()

        handle = self.canvas.create_text(self.width//2,self.height//2+20,text=f"Some words that contributed to this output include {choices(self.included, k=10)}")
        self.handles.append(handle)
        # This 'pack' method packs it into the top-level window.
        self.canvas.pack(fill = "both", expand=1)

        #call the draw function
        self.draw()

    def genlist(self, header=3):
        while len(self.handles) >0:
            h = self.handles.pop(0)
            self.canvas.delete(h)
        h = self.canvas.create_text(self.width//2,self.height//2,text=f"It appears your {header} strongest traits are: {tuple(self.dataframe.head(header).index)}.")
        self.handles.append(h)
        h = self.canvas.create_text(self.width//2,self.height//2+20,text=f"Some words that contributed to this output include {choices(self.included, k=10)})")
        self.handles.append(h)

    #a function that will take the application (self) and draw a dataframe onto the canvas
    def draw(self, inwidth=10, inheight=7):
        #obtain a pie figure
        fig1 = self.dataframe.plot.pie(title="Category Distribution",y="Relative Frequency",autopct="%1.0f%%",legend=False,figsize=(inwidth,inheight)).get_figure()
        #embed figures to TK canvas
        plot1 = FigureCanvasTkAgg(fig1, self)
        plot1.get_tk_widget().grid(row=1,column=1,padx=5,pady=10)

        #obtain a second figure of a bar plot that uses original extract to show frequency of words but only 10 because 200+ is too much to display
        fig2 = self.origindf.head(10).plot.barh(title="Word Distribution",y="Frequency", figsize=(inwidth,inheight), color="black").get_figure()
        plot2 = FigureCanvasTkAgg(fig2, self)
        plot2.get_tk_widget().grid(row=1,column=2,padx=5,pady=10)

#fire up the tk engine
root = tk.Tk()
root.wm_title("Resume Generation")
#init an instance
app = my_App(master=root, dataframe=resume_df, origindf=df, included = included_strings)

#pass control to TK
app.mainloop()
