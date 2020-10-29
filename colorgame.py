import tkinter as tk
import random
import time

class App:
    def __init__(self, master, score=0, timer=30):
        self.master = master
        master.title = "color game"
        master.bind("<Return>", self.start)
        master.geometry("400x400")
        self.score = score
        self.timer = timer
        self.create_widgets(root)
        
    def create_widgets(self, master):
        self.colors = ["blue", "green", "yellow", "orange", "blue", "pink", "violet", "black", "white", "brown"]

        self.scoreLabel = tk.Label(master, text=f"score: {self.score}", font=("verdana", 12))
        self.scoreLabel.pack()
        
        self.timeLabel = tk.Label(master, text=f"Time left: {self.timer}")
        self.timeLabel.pack()

        self.intstructions = tk.Label(master, text="Press return to start!")
        self.intstructions.config(fg="cyan", font=("verdana", 18))
        self.intstructions.pack()

        self.label = tk.Label(master, text=random.choice(self.colors), fg=random.choice(self.colors),
                              font=("verdana", 14))

        self.inp = tk.Entry(master)

    def start(self, event):
  
        self.label.pack()
        self.inp.pack()
        self.next_color()
        
  
        if self.timer == 30:
            self.countdown()

            

    def next_color(self):
    
        user_input = self.inp.get()
        color = self.label.cget("fg")
        self.inp.focus()

        if user_input == "":
            print("Field cannot be empty!")
        
        else:
        
            print(f"User guess: {user_input}, color: {color}")

            if user_input == color:
                print("correct!")
                self.score += 1
                self.scoreLabel.config(text=f"score: {self.score}")

            self.label.config(text=random.choice(self.colors), fg=random.choice(self.colors))

            self.inp.delete(0, 'end')
    
    def countdown(self):
        while self.timer > 0:
            self.timer -= 1
            self.timeLabel.config(text=f"Time left: {self.timer}")
            time.sleep(1)
            
        
    
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()
