#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Game

def minimax(position: Game.Game, depth: int) -> int:
    '''The "max" part of the minimax function

    SixTowers doesn't actually have an opponent (or minimizing players), so
    probing and additional optimizations are not available

    Args:
       position(Game.Game): Game to use to begin testing alternatives
       depth(int): Current depth of the: Current depth of recursion

    Returns:
       number(int): Maximum static evaluation after a testing all alternatives
    '''

    if depth == 0 or position.won():
        return position.static_evaluation()

    max_number = -float('inf')
    
    for possible_move in position.possible_moves():
        position_copy = position.copy()

        if position_copy.move(*possible_move):
            number = minimax(position_copy, depth - 1)

            max_number = max([number, max_number])

    return max_number


max_depth = 1


def main():
    ''' Runs game from stacks.txt file and finds solution

    As i'm still optimizing, I'm printing the game on each step
    '''

    base_game = Game.Game("../input/stacks.txt")

    curr_game = base_game.copy()
    next_game = base_game.copy()

    print("Steps: ")
    step = 0

    used_steps = set()

    while not next_game.won() and step < 29*1.5:
        max_number = -float('inf')
        move_used = None

        #  print(f'{step}', end='\r')
        print(list(curr_game.possible_moves()))
        #  print('[', end='')
        for possible_move in curr_game.possible_moves():
            position_copy = curr_game.copy()

            if position_copy.move(*possible_move):
                number = minimax(position_copy, max_depth)
                #  print(str(number) + ", ", end='')

                if number > max_number and (hash(curr_game), possible_move) not in used_steps:
                    next_game = position_copy.copy()
                    max_number = number
                    move_used = possible_move[:]
        #  print(']')

        used_steps.add((hash(curr_game), move_used))

        print(next_game.static_evaluation())
        curr_game.print_stacks()
        curr_game = next_game.copy()
        step += 1
        print()

        #  if all([(hash(curr_game), p) in used_steps for p in curr_game.possible_moves()]):
            #  print("Ended early!")
            #  break


    print("We won!!! 🎉")
    print(step)
    next_game.print_stacks()


if __name__ == "__main__":
    main()

