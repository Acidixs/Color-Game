import tkinter as tk
import random
import time
import threading

class App:
    def __init__(self, master):
        self.master = master
        master.title = "color game"
        master.bind("<Return>", self.start)
        master.geometry("400x400")
        self.score = 0
        self.highscore = 0
        self.timer = 30
        self.create_widgets(root)
        self.set_darkmode()
        
    def create_widgets(self, master):
        self.colors = ["blue", "green", "yellow", "orange", "blue", "pink", "violet", "black", "white", "brown"]

        self.highscoreLabel = tk.Label(master, text=f"Highscore: {self.highscore}", font=("verdana, 10"))
        self.highscoreLabel.pack()

        self.scoreLabel = tk.Label(master, text=f"score: {self.score}", font=("verdana", 12))
        self.scoreLabel.pack()
        
        self.timeLabel = tk.Label(master, text=f"Time left: {self.timer}")
        self.timeLabel.pack()

        self.intstructions = tk.Label(master, text="Press enter to start!")
        self.intstructions.config(fg="green", font=("verdana", 18))
        self.intstructions.pack()

        self.label = tk.Label(master, text=random.choice(self.colors), fg=random.choice(self.colors),
                              font=("verdana", 14))

        self.inp = tk.Entry(master)

    def set_darkmode(self):
        self.master.config(bg="#212526")
        self.highscoreLabel.config(bg="#212526", fg="white")
        self.scoreLabel.config(bg="#212526", fg="white")
        self.timeLabel.config(bg="#212526", fg="white")
        self.intstructions.config(bg="#212526")
        self.master.update()

    def game_over(self):
        return self.timer == 0


    def end_game(self):
        print("game ended!")
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
  
        if self.timer == 30:
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
        self.timer = 30
        self.score = 0
        self.timeLabel.config(text=f"Time left: {self.timer}")
        self.label.pack_forget()
        self.inp.pack_forget()
        self.timeLabel.update()
        self.scoreLabel.config(text=f"score: {self.score}", font=("verdana", 12))
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
    app = App(root)
    root.mainloop()
