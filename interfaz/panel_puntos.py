from tkinter import *
import numpy as np

class PanelPuntos(Frame):

    def __init__(self, pInterfaz):
        super(PanelPuntos, self).__init__(master=pInterfaz)
        self.interfaz = pInterfaz
        self.configure(background='#212946')

        # labels
        label_list = ["P", "Q", "R", "S", "T"]

        self.variables_a, self.variables_b = self.interfaz.updatePoints()

        Label(self, text="P",background='#212946',foreground='#08F7FE', font=('calibri', 12, 'bold')).grid(row=0, column=1)

        self.p_a = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.p_a.grid(row=1, column=1)
        self.p_a.insert(0,self.variables_a[0])

        self.p_b = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.p_b.grid(row=2, column=1)
        self.p_b.insert(0,self.variables_b[0])

        Label(self, text="Q",background='#212946',foreground='#08F7FE', font=('calibri', 12, 'bold')).grid(row=0, column=2)

        self.q_a = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.q_a.grid(row=1, column=2)
        self.q_a.insert(0,self.variables_a[1])

        self.q_b = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.q_b.grid(row=2, column=2)
        self.q_b.insert(0,self.variables_b[1])


        Label(self, text="R",background='#212946',foreground='#08F7FE', font=('calibri', 12, 'bold')).grid(row=0, column=3)

        self.r_a = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.r_a.grid(row=1, column=3)
        self.r_a.insert(0,self.variables_a[2])

        self.r_b = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.r_b.grid(row=2, column=3)
        self.r_b.insert(0,self.variables_b[2])

        Label(self, text="S",background='#212946',foreground='#08F7FE', font=('calibri', 12, 'bold')).grid(row=0, column=4)

        self.s_a = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.s_a.grid(row=1, column=4)
        self.s_a.insert(0,self.variables_a[3])

        self.s_b = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.s_b.grid(row=2, column=4)
        self.s_b.insert(0,self.variables_b[3])

        Label(self, text="T",background='#212946',foreground='#08F7FE', font=('calibri', 12, 'bold')).grid(row=0, column=5)

        self.t_a = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.t_a.grid(row=1, column=5)
        self.t_a.insert(0,self.variables_a[4])

        self.t_b = Entry(master=self, background='#212946', foreground='#dad0c0',
                                      insertbackground='#dad0c0', width=4, highlightbackground="#F5D300",
                                      highlightcolor="#F5D300", highlightthickness=1, relief="solid")
        self.t_b.grid(row=2, column=5)
        self.t_b.insert(0,self.variables_b[4])


        Label(self, text="a_i",background='#212946', foreground='#FE53BB', font=('calibri', 12, 'bold')).grid(row=1, column=0)
        Label(self, text="b_i",background='#212946', foreground='#FE53BB', font=('calibri', 12, 'bold')).grid(row=2, column=0)