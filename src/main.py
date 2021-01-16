#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Game

def minimax(position, depth, alpha=-float('inf'), beta=float('inf'), maximizing_player=True):
    if depth == 0 or position.won():
        return position.static_evaluation()

    if maximizing_player:

        max_number = -float('inf')
        
        for possible_move in position.possible_moves():
            position_copy = position.copy()

            if position_copy.move(*possible_move):
                number = minimax(position_copy, depth - 1, alpha, beta)

                max_number = max([number, max_number])

                alpha = max([alpha, number])

                if beta <= alpha:
                    break

        return max_number




max_depth = 3


def main():

    base_game = Game.Game("stacks.txt")

    curr_game = base_game.copy()
    next_game = base_game.copy()

    print("Steps: ")
    step = 0

    used_steps = set()

    while not next_game.won() and step < 50:
        max_number = -float('inf')
        max_height = -float('inf')
        move_used = None

        #  print(f'{step}', end='\r')
        print(list(curr_game.possible_moves()))
        #  print('[', end='')
        for possible_move in curr_game.possible_moves():
            position_copy = curr_game.copy()

            if position_copy.move(*possible_move):
                number = minimax(position_copy, max_depth)
                #  print(str(number) + ", ", end='')

                if number >= max_number and (hash(curr_game), possible_move) not in used_steps:
                    next_game = position_copy.copy()
                    max_number = number
                    max_height = possible_move[1]
                    move_used = possible_move[:]
        #  print(']')

        used_steps.add((hash(curr_game), move_used))

        print(next_game.static_evaluation())
        curr_game.print_stacks()
        curr_game = next_game.copy()
        step += 1
        print()

        if all([(hash(curr_game), p) in used_steps for p in curr_game.possible_moves()]):
            print("Ended early!")
            break


    #  print(curr_game.static_evaluation())
    #  curr_game.print_stacks()
    #  print(list(curr_game.possible_moves()))

    #  curr_game.move(0, 1, 4)
    #  print(curr_game.static_evaluation())
    #  curr_game.print_stacks()
    #  print(list(curr_game.possible_moves()))

    #  curr_game.move(4, 2, 0)
    #  print(curr_game.static_evaluation())
    #  curr_game.print_stacks()
    #  print(list(curr_game.possible_moves()))
    print(step)


    #  for sol in soln:
        #  sol[0].data.print_stacks()


if __name__ == "__main__":
    main()

