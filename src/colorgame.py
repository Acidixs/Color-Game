import tkinter as tk
import random
import time
import threading
from datetime import datetime
import json

class Game:
    def __init__(self, master):
        self.master = master
        master.title = "color game"
        master.bind("<Return>", self.start)
        master.geometry("400x400")
        self.score = 0
        self.highscore = 0
        self.timer = self.get_timer()
        self.sunIcon = tk.PhotoImage(file=r"img/sun.png").subsample(20, 20)
        self.moonIcon = tk.PhotoImage(file=r"img/moon.png").subsample(20, 20)
        self.mainframe = tk.Frame(root)
        self.mainframe.pack()
        self.secondframe = tk.Frame(root)
        self.create_widgets(root)
        self.set_darkmode()


    def enter_settings(self):
        if self.mainframe.winfo_ismapped():
            self.mainframe.pack_forget()
            self.secondframe.pack()
        else:
            self.secondframe.pack_forget()
            self.mainframe.pack()

    def save_timer(self, timer):
        settings = {"timer": timer}
        with open("settings.json", "w+") as f:
            json.dump(settings, f, indent=4)

    def get_timer(self):
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data["timer"]


    # # settings frame
    def set_timer(self):
        time = int(self.timeEntry.get())
        self.save_timer(time)
        self.update_timer()

    def update_timer(self):
        self.timeLabel.config(text=f"Time left: {self.timer}")
        self.timeLabel.update()


    def create_widgets(self, master):
        self.colors = ["blue", "green", "yellow", "orange", "blue", "pink", "violet", "black", "white", "brown"]

        self.theme = tk.Button(master, text="light theme", image=self.sunIcon, command=self.set_lightmode, compound="left")
        self.theme.pack(side="bottom", anchor="s", padx=5, pady=5)

        self.highscoreLabel = tk.Label(self.mainframe, text=f"Highscore: {self.highscore}", font=("verdana", 12))
        self.highscoreLabel.pack()

        self.scoreLabel = tk.Label(self.mainframe, text=f"Score: {self.score}", font=("verdana", 12))
        self.scoreLabel.pack()
        
        self.timeLabel = tk.Label(self.mainframe, text=f"Time left: {self.timer}", font=("verdana", 12))
        self.timeLabel.pack()

        self.intstructions = tk.Label(self.mainframe, text="Press enter to start!")
        self.intstructions.config(fg="green", font=("verdana", 18))
        self.intstructions.pack()

        self.label = tk.Label(self.mainframe, text=random.choice(self.colors), fg=random.choice(self.colors),
                              font=("verdana", 14))

        self.enterSettings = tk.Button(master, text="settings", command=self.enter_settings)
        self.enterSettings.pack(side="bottom", anchor="s", padx=5, pady=5)

        self.inp = tk.Entry(self.mainframe)


        self.setTimeLabel = tk.Label(self.secondframe, text="enter the time") 
        self.setTimeLabel.pack()
        self.timeEntry = tk.Entry(self.secondframe)
        self.timeEntry.pack()
        self.saveBtn = tk.Button(self.secondframe, text="save", command=self.set_timer)
        self.saveBtn.pack()


    def set_darkmode(self):
        self.master.config(bg="#212526")
        self.highscoreLabel.config(bg="#212526", fg="white")
        self.scoreLabel.config(bg="#212526", fg="white")
        self.timeLabel.config(bg="#212526", fg="white")
        self.intstructions.config(bg="#212526")
        self.label.config(bg="#212526")
        self.theme.config(text="light mode", image=self.sunIcon, command=self.set_lightmode)
        self.master.update()

        self.mainframe.config(bg="#212526")
        self.secondframe.config(bg="#212526")
        self.mainframe.update()
        self.secondframe.update()

    def set_lightmode(self):
        self.master.config(bg="#f9f9f9")
        self.highscoreLabel.config(bg="#f9f9f9", fg="black")
        self.scoreLabel.config(bg="#f9f9f9", fg="black")
        self.timeLabel.config(bg="#f9f9f9", fg="black")
        self.intstructions.config(bg="#f9f9f9")
        self.label.config(bg="#f9f9f9")
        self.theme.config(text="dark mode", image=self.moonIcon, command=self.set_darkmode)
        self.master.update()

        self.mainframe.config(bg="#f9f9f9")
        self.secondframe.config(bg="#f9f9f9")
        self.mainframe.update()
        self.secondframe.update()


    def save_score(self, score):
        time = str((datetime.today().replace(microsecond=0)))
        with open("scores.txt", "a+") as f:
            f.write(f"{time} | Score: {score} \n")


    def game_over(self):
        return self.timer == 0


    def end_game(self):
        print("game ended!")
        self.save_score(self.score)
        self.update_highscore()
        self.resetGame()


    def start(self, event):
        if self.game_over():
            self.end_game()
        else:
            self.label.pack()
            self.inp.pack()
            self.next_color()
            self.intstructions.pack_forget()
  
        if self.timer == self.get_timer():
            threading.Thread(target=self.countdown).start()
            

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
            self.timeLabel.update()
            time.sleep(1)
        self.end_game()
    

    def resetGame(self):
        self.timer = self.get_timer()
        self.score = 0
        self.timeLabel.config(text=f"Time left: {self.timer}")
        self.label.pack_forget()
        self.inp.pack_forget()
        self.timeLabel.update()
        self.scoreLabel.config(text=f"Score: {self.score}", font=("verdana", 12))
        self.scoreLabel.update()
        self.intstructions.pack()
        time.sleep(1)
    
    
    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.highscoreLabel.config(text=f"Highscore: {self.highscore}")
            self.highscoreLabel.update()
           
    
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
