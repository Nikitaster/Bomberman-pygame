import tkinter as tk


def openFile():
    exec(open('C:\\Users\\Дом\\PycharmProjects\\bomberman\\run.py').read())


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='New Window', width=25, command=openFile)
        self.button1.pack()
        self.frame.pack()


def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()


if __name__ == '__main__':
    main()
