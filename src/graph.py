import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from db import Database


class Graph:
    def __init__(self):
        self.db = Database()

    def draw_graph(self):
        self.rounds = self.db.get_round()
        self.scores = self.db.get_score() 

        plt.scatter(self.rounds, self.scores)
        plt.xlabel("rounds")
        plt.ylabel("score")
        plt.show()