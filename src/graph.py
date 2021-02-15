import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from db import Database


class Graph:
    def __init__(self):
        self.db = Database()

    def draw_graph(self):
        rounds = self.db.get_round()
        scores = self.db.get_score()

        print(rounds, scores) 

        plt.scatter(rounds, scores)
        plt.xlabel("rounds")
        plt.ylabel("score")
        plt.show()