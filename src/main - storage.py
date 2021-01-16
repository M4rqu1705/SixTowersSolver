#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Game

class Tree:
    
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.children = []

    def __init__(self):
        self.root = self.Node()

    def max_height(self, node=None):
        if node is None:
            node = self.root

        if len(node.children) > 0:
            heights = [self.max_height(child) for child in node.children]

            return max(heights) + 1
        else:
            return 1

    def min_height(self, node=None):
        if node is None:
            node = self.root

        if len(node.children) > 0:
            heights = [self.min_height(child) for child in node.children]

            return min(heights) + 1
        else:
            return 1

    def get_min_height(self, node=None):
        if node is None:
            node = self.root

        if len(node.children) > 0:
            alternatives = [self.get_min_height(child) for child in node.children]

            smallest = None
            best = None
            for alt in alternatives:
                if smallest is None or alt[0][1] < smallest:
                    smallest = alt[0][1]
                    best = [el for el in alt]

            return [(node, best[0][1] + 1)] + best
        else:
            return [(node, 1)]



    def play(self, node = None, depth=3):
        global situations_found

        if depth == 0:
            return

        if node is None:
            node = self.root

        if node.data is None:
            return None
        
        if node.data.won():
            return

        # We only need to move if we haven't won
        for move in node.data.possible_moves():
            newNode = self.Node()
            newNode.data = node.data.copy()
            newNode.data.move(*move)
            node.children.append(newNode)

        for i in range(len(node.children)):
            if node is self.root:
                width = 100
                progress = i / len(node.children)
                progress = int(progress * width)
                message = f'[{"=" * progress}{" " * (width - progress)}]'
                print(message, end='\r')

            self.play(node.children[i], depth - 1)



def main():
    games = Tree()

    games.root.data = Game.Game("stacks.txt")

    games.play(None, 15)

    # Solution found!!
    if games.min_height() < games.max_height():
        print("Solution found!")
        #  print(games.min_height())
        #  print(games.max_height())

        soln = games.get_min_height()

        for sol in soln:
            sol[0].data.print_stacks()

    else:
        print("Solution not found ...")



if __name__ == "__main__":
    main()

