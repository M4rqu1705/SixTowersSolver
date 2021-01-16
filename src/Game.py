#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


# ---------------------- Block Classes ---------------------------------------

class BlockColors(Enum):
    Magenta = 1
    Red = 2
    Yellow = 3
    Green = 4
    Cyan = 5
    Indigo = 6

colors_abbrev = {
        'M': BlockColors.Magenta,
        'R': BlockColors.Red,
        'Y': BlockColors.Yellow,
        'G': BlockColors.Green,
        'C': BlockColors.Cyan,
        'I': BlockColors.Indigo
        }


class Block:
    __slots__ = ['number', 'color']

    def __init__(self, number: int, color: Enum):
        if isinstance(number, int) and isinstance(color, BlockColors):
            self.number = number
            self.color = color
        else:
            raise TypeError(f"#{number} is of type {type(number)} and color {color} is of type {type(color)}")

    def __str__(self):
        return f"[{self.number},{str(self.color).split('.')[-1]}]"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.color.value * 10 + self.number


# ---------------------- Stack Class -----------------------------------------


class Stack:
    __slots__ = ['head', 'height']

    class Node:
        __slots__ = ['next', 'value']
        def __init__(self):
            self.next = None
            self.value = None


    def __init__(self):
        self.head = self.Node()
        self.height = 0


    def push(self, element):
        if element is None:
            return False

        # push stack right on top without altering order
        elif isinstance(element, Stack):
            temp = Stack()
            while not element.isEmpty():
                temp.push(element.pop())

            while not temp.isEmpty():
                self.push(temp.pop())

            del temp

        elif isinstance(element, Block):
            newNode = self.Node()
            newNode.value = element

            newNode.next = self.head.next
            self.head.next = newNode

            self.height += 1

            return True

        else:
            raise TypeError(f"Expected either None, Stack or Block. Received {type(element)}")

    def pop(self):
        if self.isEmpty():
            return None

        else:
            removedNode = self.head.next
            value = removedNode.value

            self.head.next = self.head.next.next

            del removedNode
            self.height -= 1

            return value

    def top(self):
        if self.isEmpty():
            return None
        else:
            return self.head.next.value

    def isEmpty(self):
        return self.height == 0

    def clear(self):
        while not self.isEmpty():
            self.pop()

    def copy(self):
        tempStack = Stack()
        copy = Stack()

        # Transfer all contents of self to a tempStack
        while not self.isEmpty():
            tempStack.push(self.pop())

        # Transfer all contents back to self, but also to copy
        while not tempStack.isEmpty():
            self.push(tempStack.top())
            copy.push(tempStack.pop())

        return copy

    def __str__(self):
        copy = self.copy()

        elements = list()

        while not copy.isEmpty():
            elements.append(copy.pop())

        return '[' + ', '.join([str(el) for el in elements]) + ']'

    def __repr__(self):
        return str(self)

    
    def __hash__(self):
        copy = self.copy()

        total = 0

        while not copy.isEmpty():
            total += hash(copy.pop())
            total *= 100

        return total


# ---------------------- Game Class ------------------------------------------


class Game:
    __slots__ = ['stacks']

    def __init__(self, param: None):

        if isinstance(param, str):
            self.stacks = [Stack() for _ in range(8)]
            self.parse_from_file(param)
        elif isinstance(param, list) and isinstance(param[0], Stack):
            self.stacks = param
        elif isinstance(param, Game):
            self = Game.copy()
        else:
            raise TypeError("Expected list of stacks or string with filename")


    def parse_from_file(self, file_name: str):
        with open(file_name, 'r') as fp:
            lines = fp.readlines()
            # Add blocks to stacks from bottom to top
            for line in lines:
                blocks = line.split(",")

                for column, block in enumerate(blocks):
                    block = block.strip()

                    # If valid, create block and add to stacks
                    if block == "00":
                        continue

                    block = Block(
                            int( block[0] ),
                            colors_abbrev[ str( block[1] ).upper() ]
                            )
                    self.stacks[column].push(block)


    @staticmethod
    def invert_stack(S):
        copy = S.copy()
        inverted = Stack()
        while not copy.isEmpty():
            inverted.push(copy.pop())

        return inverted

    @classmethod
    def extract_from_stack(cls, S, amount: int):
        copy = S.copy()
        
        if S.height < amount:
            raise ValueError(f"Cannot extract {amount} from Stack with height {S.height}")

        temp = Stack()
        for i in range(amount):
            temp.push(copy.pop())

        return cls.invert_stack(temp)
    
    @staticmethod
    def is_consecutive_stack(S) -> bool:
        copy = S.copy()

        if copy.height <= 1:
            return True
        else:
            curr_block = copy.pop()

            while copy.height >= 1:

                conditions = [
                        isinstance(curr_block, Block),
                        isinstance(copy.top(), Block),
                        curr_block.color == copy.top().color,
                        copy.top().number - curr_block.number == 1
                        ]
                if not all(conditions):
                    return False
                else:
                    curr_block = copy.pop()

            return True

    @staticmethod
    def is_valid_stack(S) -> bool:
        copy = S.copy()

        if copy.height <= 1:
            return True
        else:
            curr_block = copy.pop()

            while copy.height >= 1:

                conditions = [
                        isinstance(curr_block, Block),
                        isinstance(copy.top(), Block),
                        curr_block.color == copy.top().color,
                        copy.top().number > curr_block.number
                        ]
                if not all(conditions):
                    return False
                else:
                    curr_block = copy.pop()

            return True


    def is_valid_move(self, src: int, src_height: int, dest: int) -> bool:
        if src < 0 or src >= len(self.stacks) or dest < 0 or dest >= len(self.stacks) or src_height > self.stacks[src].height:
            raise ValueError(f"Expected src {src} of height {src_height} -> dest {dest} to be within bounds (0-7)")
            #  return False

        # Extract specified source
        source = self.extract_from_stack(self.stacks[src], src_height)

        if not self.is_consecutive_stack(source):
            return False


        # Do not "break off" already consecutive towers
        if src_height + 1 <= self.stacks[src].height:
            # Extract specified source. However, it is in inverted order
            copy = self.extract_from_stack(self.stacks[src], src_height + 1)

            if self.is_consecutive_stack(copy):
                return False


        dest_block = self.stacks[dest].top()

        inverted_source = self.invert_stack(source)

        # Empty slots are more than capable of holding any valid stack. However,
        # I'm making a custom rule to prevent this
        if self.stacks[dest].height == 0:
           # Just prevent any block coming from empty source to moving to empty destination
            if src_height == self.stacks[src].height:
                return False
            return True

        # Otherwise, compare the bottom of the src stack with the destination stack
        elif inverted_source.top().color == dest_block.color and inverted_source.top().number < dest_block.number:
            return True

        return False


    def move(self, src: int, src_height: int, dest: int) -> bool:
        if not self.is_valid_move(int(src), int(src_height), int(dest)):
            return False

        # push top src_height blocks of src to a src stack
        temp = Stack()
        source = Stack()
        for i in range(src_height):
            temp.push(self.stacks[src].pop())
        while not temp.isEmpty():
            source.push(temp.pop())
        del temp

        self.stacks[dest].push(source)

        return True


    def possible_moves(self):
        for src in range(len(self.stacks)):
            # Do not consider removing elements from empty stacks
            if self.stacks[src].height == 0:
                continue

            for dest in range(len(self.stacks)):
                # Do not consider staying the same
                if src == dest:
                    continue

                if self.stacks[src].height > 1:
                    for height in range(1, self.stacks[src].height + 1):
                        if self.is_valid_move(src, height, dest):
                            yield (src, height, dest)
                elif self.stacks[src].height == 1:
                    if self.is_valid_move(src, 1, dest):
                        yield (src, 1, dest)


    def won(self):
        stacks = [s.copy() for s in self.stacks]

        colors_seen = set()
    
        # Elements must be in ascending order with the correct color
        for stack in stacks:
            while stack.height > 1:
                prev = stack.pop()
                curr = stack.top()

                colors_seen.add(prev.color)

                if prev.color != curr.color or prev.number > curr.number:
                    return False

        # Elements must occupy least amount of space possible
        occupied_stacks = sum([int(stack.height > 0) for stack in stacks])
        if len(colors_seen) != occupied_stacks:
            return False

        return True


    def static_evaluation(self) -> int:
        total = 0

        for stack in self.stacks:

            # Use "temporary" total value to only take into account value for
            # this stack in later calculations
            curr_total = 0

            if not stack.isEmpty():
                stack = stack.copy()

                # Check for stacks in consecutive order
                for i in range(stack.height-1, -1, -1):
                    if self.is_consecutive_stack(self.extract_from_stack(stack, i)):
                        curr_total += i
                        break

                # Use a multiplier for sequences (to motivate getting stacks)
                if curr_total == 7:
                    curr_total = 10000

                elif curr_total >= 1:
                    ns = stack.top().number
                    ne = stack.top().number + curr_total
                    curr_total = (ne*ne + ne - ns*ns + ns) / 2
                    curr_total *= 100


                # Check for stacks in valid order
                else:
                    for i in range(stack.height-1, -1, -1):
                        if self.is_valid_stack(self.extract_from_stack(stack, i)):
                            curr_total += i
                            break

                    # Use a multiplier for sequences (to motivate getting stacks)
                    if curr_total == 7:
                        curr_total = 100

                    elif curr_total >= 1:
                        ns = stack.top().number
                        ne = stack.top().number + curr_total
                        curr_total = (ne*ne + ne - ns*ns + ns) / 2



                #  # Reward stacks in valid order
                #  for i in range(stack.height-1, -1, -1):
                    #  if self.is_valid_stack(self.extract_from_stack(stack, i)):
                        #  curr_total += i
                        #  break

                #  # Reward stacks with 6's at the bottom
                #  if self.is_valid_stack(stack) and self.invert_stack(stack).top().number == 6:
                    #  curr_total *= 10

                #  # Heavily penalize lonely blocks
                #  if stack.height == 1:
                    #  curr_total = 0
                #  elif stack.height == 2:
                    #  curr_total /= 1000
                #  elif stack.height == 3:
                    #  curr_total /= 100


                total += curr_total

        return int(total)


    def copy(self):
        return Game([s.copy() for s in self.stacks])


    def print_stacks(self):
        stacks = [s.copy() for s in self.stacks]

        max_height = max([s.height for s in stacks])
        message = ""

        for row in range(max_height):
            for column in range(len(stacks)):
                if row >= max_height - stacks[column].height:
                    temp = str(stacks[column].pop())[1:-1].split(",")
                    message += f" {temp[0], temp[1][0:3]} "
                else:
                    message += " "*14

            message += "\n"

        print(message)


    def __hash__(self):
        total = 2166136261

        for stack in self.stacks:
            total *= 16777619
            total ^= hash(stack)
            # A little extra just to prevent numbers from getting tooo big
            total % int(1E19)

        return total





def main():
    game1 = Game("simp2.txt")
    game2 = Game("simp2.txt")
    game3 = Game("simp2.txt")

    game1.print_stacks()
    print(game1.move(0, 1, 5))
    print(game1.static_evaluation())
    game1.print_stacks()

    game2.print_stacks()
    print(game2.move(4, 1, 5))
    print(game2.static_evaluation())
    game2.print_stacks()

    game3.print_stacks()
    print(game3.move(4, 1, 0))
    print(game3.static_evaluation())
    game3.print_stacks()

    #  game = Game("simp2.txt")
    #  game.print_stacks()
    #  print(game.static_evaluation())
    #  breakpoint()

if __name__ == "__main__":
    main()

