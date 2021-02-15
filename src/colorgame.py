import tkinter as tk
import random
import time
import threading
from datetime import datetime
import json
from db import Database
from graph import Graph

class Game:
    def __init__(self, master):
        self.master = master
        master.title = "color game"
        master.bind("<Return>", self.start)
        master.bind("<Escape>", self.resetGame)
        master.geometry("400x400")
        self.score = 0
        self.highscore = self.get_highscore()
        self.timer = self.get_timer()
        self.timerRunning = False
        self.sunIcon = tk.PhotoImage(file=r"img/sun.png").subsample(20, 20)
        self.moonIcon = tk.PhotoImage(file=r"img/moon.png").subsample(20, 20)
        self.mainframe = tk.Frame(root)
        self.mainframe.pack()
        self.secondframe = tk.Frame(root)

        self.redXIcon = tk.PhotoImage(file=r"img/red-x.png").subsample(12, 12)
        self.greenCheckMarkIcon = tk.PhotoImage(file=r"img/green-checkmark.png").subsample(10, 10)
        self.canvas = tk.Canvas(self.mainframe, bg="#212526", width=100, height=100, highlightthickness=0)
        self.canvas.pack(side="bottom", pady=10)

        self.graph = Graph()
        self.db = Database()


        self.create_widgets(root)
        self.set_darkmode()

    def draw_x(self):
        image = self.canvas.create_image(50, 50, anchor="s", image=self.redXIcon)
        self.canvas.itemconfigure(image, state="normal")
        time.sleep(0.5)
        self.canvas.itemconfigure(image, state="hidden")
        return 

    def draw_checkmark(self):
        image = self.canvas.create_image(50, 50, anchor="s", image=self.greenCheckMarkIcon)
        self.canvas.itemconfigure(image, state="normal")
        time.sleep(0.5)
        self.canvas.itemconfigure(image, state="hidden")
        return



    def toggle_settings(self):
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


    def set_timer(self):
        time = int(self.timeEntry.get())
        self.save_timer(time)
        self.update_timer()

    def update_timer(self):
        self.timer = self.get_timer()
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

        self.toggleSettings = tk.Button(master, text="settings", command=self.toggle_settings)
        self.toggleSettings.pack(side="bottom", anchor="s", padx=5, pady=5)

        self.inp = tk.Entry(self.mainframe)
        self.settingsTitle = tk.Label(self.secondframe, text="Settings", font=("verdana", 12))
        self.settingsTitle.pack(pady=5)
        self.setTimeLabel = tk.Label(self.secondframe, text="Enter the time") 
        self.setTimeLabel.pack()
        self.timeEntry = tk.Entry(self.secondframe)
        self.timeEntry.pack(pady=5)
        self.saveBtn = tk.Button(self.secondframe, text="Save", command=self.set_timer)
        self.saveBtn.pack(pady=5)

        self.graphButton = tk.Button(self.secondframe, text="Show graph", command=self.graph.draw_graph)
        self.graphButton.pack(pady=5)


    def set_darkmode(self):
        self.master.config(bg="#212526")
        self.highscoreLabel.config(bg="#212526", fg="white")
        self.scoreLabel.config(bg="#212526", fg="white")
        self.timeLabel.config(bg="#212526", fg="white")
        self.intstructions.config(bg="#212526")
        self.label.config(bg="#212526")
        self.theme.config(text="light mode", image=self.sunIcon, command=self.set_lightmode)
        self.settingsTitle.config(bg="#212526", fg="white")
        self.canvas.config(bg="#212526")
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
        self.settingsTitle.config(bg="#f9f9f9", fg="black")
        self.canvas.config(bg="#f9f9f9")
        self.master.update()

        self.mainframe.config(bg="#f9f9f9")
        self.secondframe.config(bg="#f9f9f9")
        self.mainframe.update()
        self.secondframe.update()


    def save_score_local(self, score):
        time = str((datetime.today().replace(microsecond=0)))
        with open("scores.txt", "a+") as f:
            f.write(f"{time} | Score: {score} \n")

    def save_score_db(self, score):
        self.db.add_score(score)


    def game_over(self):
        return self.timer == 0


    def end_game(self):
        print("game ended!")

        if self.score != 0:
            self.save_score_local(self.score)
            self.save_score_db(self.score)
            self.update_highscore()
            print("penis")
        self.resetGame(event=True)


    def start(self, event):
        if self.game_over():
            self.end_game()
        else:
            self.label.pack()
            self.inp.pack()
            self.next_color()
            self.intstructions.pack_forget()

            if not self.timerRunning:
                self.timerRunning = True
                # TimerLoop = TimerThread(self.countdown).create_thread()
                # TimerLoop.start()

                TimerLoop = threading.Thread(target=self.countdown)
                TimerLoop.start()
            
    def correct_answer(self, inp, color):
        return inp == color

    def update_score(self):
        self.score += 1
        self.scoreLabel.config(text=f"score: {self.score}")

    def hasNumbers(self, inp):
        return any(char.isdigit() for char in inp)

    def invalid_input(self, inp):
        if inp == "" or inp == None or self.hasNumbers(inp):
            print("(!) Invalid input!")
            return True
        else:
            return False


    def next_color(self):
        user_input = self.inp.get()
        color = self.label.cget("fg")
        self.inp.focus()

        if self.invalid_input(user_input):
            return

        if self.correct_answer(user_input, color):
            self.update_score()
            show_checkmark = threading.Thread(target=self.draw_checkmark)
            show_checkmark.start()
        else:
            show_x = threading.Thread(target=self.draw_x)
            show_x.start()

        # picks new color and resets input field
        self.label.config(text=random.choice(self.colors), fg=random.choice(self.colors))
        self.inp.delete(0, 'end')
    

    def countdown(self):
        while self.timer > 0 and self.timerRunning == True:
            self.timer -= 1
            self.timeLabel.config(text=f"Time left: {self.timer}")
            self.timeLabel.update()
            time.sleep(1)
        self.end_game()
        print("Thread stopped!")
        return 
    
    def stop_countdown(self):
        self.timerRunning = False


    def resetGame(self, event):
        self.stop_countdown()
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

            stats = {"highscore": self.highscore}
            with open("stats.json", "w+") as f:
                json.dump(stats, f, indent=4)

    def get_highscore(self):
        with open("stats.json", "r") as f:
            stats = json.load(f)
            return stats["highscore"]
           

class TimerThread(threading.Thread):
    def __init__(self, function):
        threading.Thread.__init__(self)
        self.function = function

    def create_thread(self):
        return threading.Thread(target=self.function)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
