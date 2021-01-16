#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import os.path


# ---------------------- Block Classes ---------------------------------------

class BlockColors(Enum):
    '''Colors that are available in the game

    Structuring the alternatives as an enum makes some aspects of the code more
    readable
    '''
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
    '''Block class that contains number and color of a block

    Additionally contains some helper methods that will help simplify code later ahead

    Attributes:
       number(int): Contains the number for this block (practically a number from 0 to 6)
       color(BlockColors): Specifies what color this block is
    '''
    __slots__ = ['number', 'color']

    def __init__(self, number: int, color: BlockColors):
        '''Prepares block data

        Number and color will be treated as private data

        Args:
           number(int): This block's number
           color(BlockColors): This block's color

        Raises:
           TypeError: If number is not int or color is not instance of BlockColors
        '''

        if isinstance(number, int) and isinstance(color, BlockColors):
            self.number = number
            self.color = color

        else:
            raise TypeError(f"#{number} is of type {type(number)} and color {color} is of type {type(color)}")

    def isColor(self, color: BlockColors) -> bool:
        '''Checks if this block's color is the specified one

        Args:
           color(BlockColors): Color we want to compare this block's to

        Returns:
           bool: True if this color and the passed color match

        '''
        return color == self.color

    def __int__(self) -> int:
        return self.number

    def __float__(self) -> float:
        return self.number

    def __eq__(self, b2) -> bool:
        if not isinstance(b2, Block):
            raise ValueError(f'Cannot compare {type(b2)} with Block')

        return self.color == b2.color and self.number == b2.number

    def __lt__(self, b2) -> bool:
        if not isinstance(b2, Block):
            raise ValueError(f'Cannot compare {type(b2)} with Block')

        return self.color == b2.color and self.number < b2.number

    def __le__(self, b2) -> bool:
        if not isinstance(b2, Block):
            raise ValueError(f'Cannot compare {type(b2)} with Block')

        return self.color == b2.color and self.number <= b2.number

    def __gt__(self, b2) -> bool:
        if not isinstance(b2, Block):
            raise ValueError(f'Cannot compare {type(b2)} with Block')

        return self.color == b2.color and self.number > b2.number

    def __ge__(self, b2) -> bool:
        if not isinstance(b2, Block):
            raise ValueError(f'Cannot compare {type(b2)} with Block')

        return self.color == b2.color and self.number >= b2.number

    def __add__(self, b2) -> int:
        if isinstance(b2, Block) and self.isColor(b2.color):
            return self.number + b2.number
        elif isinstance(b2, int) or isinstance(b2, float):
            return self.number + b2
        else:
            return 0

    def __sub__(self, b2) -> int:
        if isinstance(b2, Block) and self.isColor(b2.color):
            return self.number - b2.number
        elif isinstance(b2, int) or isinstance(b2, float):
            return self.number - b2
        else:
            return 0

    def __radd__(self, b1) -> int:
        if isinstance(b1, Block) and self.isColor(b1.color):
            return self.number + b1.number
        elif isinstance(b1, int) or isinstance(b1, float):
            return self.number + b1
        else:
            return 0

    def __rsub__(self, b1) -> int:
        if isinstance(b1, Block) and self.isColor(b1.color):
            return b1.number - self.number
        elif isinstance(b1, int) or isinstance(b1, float):
            return b1 - self.number
        else:
            return 0

    def __mul__(self, b2) -> int:
        if isinstance(b2, Block) and self.isColor(b2.color):
            return self.number * b2.number
        elif isinstance(b2, int) or isinstance(b2, float):
            return self.number * b2
        else:
            return 0

    def __truediv__(self, b2) -> int:
        if isinstance(b2, Block) and self.isColor(b2.color):
            return self.number / b2.number
        elif isinstance(b2, int) or isinstance(b2, float):
            return self.number / b2
        else:
            return 0

    def __rmul__(self, b1) -> int:
        if isinstance(b1, Block) and self.isColor(b1.color):
            return self.number * b1.number
        elif isinstance(b1, int) or isinstance(b1, float):
            return self.number * b1
        else:
            return 0

    def __rtruediv__(self, b1) -> int:
        if isinstance(b1, Block) and self.isColor(b1.color):
            return b1.number / self.number
        elif isinstance(b1, int) or isinstance(b1, float):
            return b1 / self.number
        else:
            return 0

    def __str__(self):
        return f"[{self.number},{str(self.color).split('.')[-1]}]"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.color.value * 10 + self.number


# ---------------------- Stack Class -----------------------------------------


class Stack:
    '''Class that represents a stack of blocks in the game

    Unlike the Stack Data Structure, it contains some unconventional operations
    and names that help make the main Game functions much shorter and simpler

    Attributes:
       head(Stack.Node): Pointer to the top node of the stack
       height(int): Amount of elements stored in stack
    '''
    __slots__ = ['head', 'height']

    class Node:
        '''Simple Singly Linked List node for Stack

        Attributes:
           next(Stack.Node): Pointer to next node, or None
           value(Block): Instance of the block class
        '''
        __slots__ = ['next', 'value']
        def __init__(self):
            self.next = None
            self.value = None


    def __init__(self):
        self.head = self.Node()
        self.height = 0

    def push(self, element) -> bool:
        '''Add block or other stack at the top of this stack

        Args:
           element(any): Can be a single Block or another Stack of Blocks

        Returns:
           bool: True if operation was successful

        Raises:
           TypeError: When trying to push elements that are not Stacks or Blocks
        '''

        if element is None:
            return False

        elif isinstance(element, Stack):
            temp = Stack()
            while not element.isEmpty():
                temp.push(element.pop())

            while not temp.isEmpty():
                self.push(temp.pop())

            del temp

            return True

        elif isinstance(element, Block):
            newNode = self.Node()
            newNode.value = element

            newNode.next = self.head.next
            self.head.next = newNode

            self.height += 1

            return True

        else:
            raise TypeError(f"Expected either None, Stack or Block. Received {type(element)}")


    def pop(self, n: int = None):
        '''Removes "n" amount of elements from top of stack and returns them as another stack (but in the correct order)

        By default, it implements a more efficient solution, but when an integer
        n is added, it uses a more time-consuming alternative to extract and
        return all the popped elements in the correct order

        Args:
            n(int): Amount of elements to pop from top of stack

        Returns:
            Block or Stack[Block]: Removed elements

        Raises:
            ValueError: When popping more than the available height
        '''
        if self.isEmpty():
            return None

        elif n is None:
            removedNode = self.head.next
            value = removedNode.value

            self.head.next = self.head.next.next

            del removedNode
            self.height -= 1

            return value

        elif isinstance(n, int) or isinstance(n, float):
            if n > self.height:
                raise ValueError(f"Desired {int(n)} exceeds height {self.height}")


            temp = Stack()

            for i in range(int(n)):
                temp.push(self.pop())

            result = Stack()

            while not temp.isEmpty():
                result.push(temp.pop())

            del temp

            return result


    def top(self, n: int = None):
        '''Extracts and returns "n" amount of elements from top of stack (in the correct order)

        By default, it implements a more efficient solution, but when an integer
        n is added, it uses a more time-consuming alternative to extract and
        return all the popped elements in the correct order

        Args:
            n(int): Amount of elements to pop from top of stack

        Returns:
            Block or Stack[Block]: Top elements

        Raises:
            ValueError: When extracting more than the available height
        '''
        if self.isEmpty():
            return None

        elif n is None:
            return self.head.next.value

        elif isinstance(n, int) or isinstance(n, float):
            if n > self.height:
                raise ValueError(f"Desired {int(n)} exceeds height {self.height}")

            copy = self.copy()
            temp = Stack()

            for i in range(int(n)):
                temp.push(copy.pop())

            del copy

            result = Stack()

            while not temp.isEmpty():
                result.push(temp.pop())

            del temp

            return result

    def isEmpty(self) -> bool:
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

    def isValid(self) -> bool:
        '''Checks if the stack of blocks is valid

        Returns:
           bool: True if the following blocks are the same color and wider than the previous ones
        '''
        copy = self.copy()

        count = 1
        while copy.height > 1 and copy.pop() < copy.top():
            count += 1

        return self.height == count

    def isConsecutive(self) -> bool:
        '''Checks if the stack of blocks is consecutive

        Returns:
           bool: True if the following blocks are the same color and follows the
           correct sequence after the previous one (1, 2, 3, etc.)
        '''
        copy = self.copy()

        count = 1
        while copy.height > 1 and copy.pop() - copy.top() == -1:
            count += 1

        return self.height == count


    def __str__(self) -> str:
        copy = self.copy()

        elements = list()

        while not copy.isEmpty():
            elements.append(copy.pop())

        return '[' + ', '.join([str(el) for el in elements]) + ']'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        copy = self.copy()

        total = 0

        while not copy.isEmpty():
            total += hash(copy.pop())
            total *= 100

        return total


# ---------------------- Game Class ------------------------------------------


class Game:
    '''Game class, which tries to implement a simple version of SixTowers

    It does so by validating moves before performing them, and making sure to
    comply with all the basic game rules.

    Attributes:
       stacks: list of Stacks of Blocks with the current game arrangement
    '''
    __slots__ = ['stacks']

    def __init__(self, param = None):

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
        '''Helper function to help fill the stacks attribute with the contents of a file

        Args:
           file_name(str): Name of the file from which the data will be extracted

        Raises:
           ValueError: When file_name file is not found

        '''
        if not os.path.exists(file_name):
            return ValueError(f"Cannot find file {file_name}")

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


    def is_valid_move(self, src: int, dest: int, src_height: int) -> bool:
        '''Checks if move from src to dest with src_height is valid based on game rules

        This function bascally establishes the game's rules

        Args:
           src(int): Index of source stack in stacks array
           dest(int): Index of destination stack in stacks array
           src_height(int): Height of the source array to be moved

        Returns:
           bool: True if move complies with game rules

        Raises:
           ValueError: If inputs exceed stack size of height
        '''

        if src < 0 or src >= len(self.stacks) or dest < 0 or dest >= len(self.stacks):
            raise ValueError(f"Expected src {src} -> dest {dest} to be within bounds (0-7)")
            #  return False

        if src_height > self.stacks[src].height:
            raise ValueError(f"Expected src_height {src_height} to be <= stack height {self.stacks[src].height}")

        elif src_height == 0:
            raise ValueError(f"Expected src_height to be greater than 0")


        # If the specified source is not consecutive (even if it were valid)
        # We canot split a stack that is not consecutive
        if not self.stacks[src].top(src_height).isConsecutive():
            return False

        # Cannot split up a stack that is consecutive "mid-way"
        if self.stacks[src].height > src_height and self.stacks[src].top(src_height + 1).isConsecutive():
            return False

        copy = self.stacks[src].top(src_height)
        while copy.height > 1:
            copy.pop()
        bottom_src_block = copy.top()


        # Empty slots are more than capable of holding any valid stack. However,
        # I'm making a custom rule to prevent some moves
        if self.stacks[dest].height == 0:

           # Prevent any block coming from empty source to moving to empty destination
            if src_height == self.stacks[src].height:
                return False

            return True

        # Otherwise, compare the bottom of the src stack with the destination stack
        elif bottom_src_block < self.stacks[dest].top():
            return True

        return False


    def move(self, src: int, dest: int, src_height: int) -> bool:
        '''Perform a move action from origin to destination with specific height

        Args:
           src(int): Index of source stack in stacks array
           dest(int): Index of destination stack in stacks array
           src_height(int): Height of the source array to be moved

        Returns:
           bool: True if operation was successful
        '''

        if not self.is_valid_move(int(src), int(dest), int(src_height)):
            return False

        self.stacks[dest].push(self.stacks[src].pop(src_height))

        return True


    def possible_moves(self):
        '''Python generator that returns all possible moves one by one

        Returns:
           (src, dest, height): Source, destination indices and height of stack
           to be used with the ::meth::Game.Game.move() method
        '''

        for src in range(len(self.stacks)):

            # Do not consider removing elements from empty stacks
            if self.stacks[src].height == 0:
                continue

            for dest in range(len(self.stacks)):
                # Do not consider staying the same place
                if src == dest:
                    continue

                if self.stacks[src].height > 1:
                    # Check all potential heights
                    for height in range(1, self.stacks[src].height + 1):
                        if self.is_valid_move(src, dest, height):
                            yield (src, dest, height)

                        # !! End height loop early whenever possible
                        elif not self.stacks[src].top(height).isConsecutive():
                            continue

                else:
                    if self.is_valid_move(src, dest, 1):
                        yield (src, dest, 1)


    def won(self) -> bool:
        '''Checks if game fulfills winning condition

        Returns:
           bool: True if game fulfills winning condition
        '''
        stacks = [s.copy() for s in self.stacks]

        # Elements must be in ascending order with the correct color
        for stack in stacks:
            if stack.height == 0:
                continue
            elif not(stack.height == 7 and stack.isConsecutive()):
                return False

        return True


    def static_evaluation(self) -> int:
        '''Evaluates game state and returns a number

        The bigger the number of the game evaluation, the closer the game is to
        the winning state.

        196 * 6 towers = 1176 corresponds to the winning game

        Formula:
           stack.height * sum(map(lambda x: x.number + 1, stack)) -
            missing.height * sum(map(lambda x: x.number + 1, missing))

           If stack is consecutive, missing.height = 0 and result will simply
           be the first term (sum of elements offset by 1 multiplied by its height)

           If stack is valid, we need to extract the missing terms and
            proceed with calculations. The subtraction will help penalize
            valid, but not consecutive stacks

        Returns:
           int: Static evaluation of current game state
        '''
        total = 0

        for stack in self.stacks:
            # Empty stacks MUST be ignored
            if stack is None or stack.height == 0:
                continue


            # There will not be any missing elements if the full stack is consecutive
            if stack.isConsecutive():
                top = stack.top() + 1
                bottom = top + stack.height - 1

                # Adding all the elements of the *consecutive* stack offsetting all elements by 1
                stack_sum = (bottom*bottom + int(bottom) - top*top + int(top)) / 2

                total += stack.height * stack_sum

                continue


            for height in range(stack.height, 1, -1):
                if stack.top(height).isValid():
                    missing_sum = 0
                    missing_height = 0

                    stack_sum = 0
                    stack_height = height

                    copy = stack.top(height)
                    while copy.height > 1:
                        prev = copy.pop()
                        curr = copy.top()

                        stack_sum += prev + 1

                        if curr - prev > 1:
                            '''
                            If prev = 2 and curr = 6, then end = curr - 1, start = prev + 1

                            But because of the +1 offset ...
                                end = curr, start = prev + 2

                            height = end - (start + 1) = end - start - 1

                            AND

                            sum = end * (end + 1) / 2 - (start - 1) * start / 2

                                => curr * (cur + 1) / 2 - (prev + 1) * (prev + 2) / 2

                                => 1/2 * (curr*curr + curr - prev*prev - 3*prev - 2)
                            '''

                            missing_height += curr - prev - 1
                            missing_sum += (curr*curr + int(curr) - prev*prev - prev*3 - 2) / 2

                    stack_sum += copy.pop() + 1

                    total += stack_height * stack_sum - missing_height * missing_sum

                    break


        return int(total)


    def copy(self):
        '''Make game copy and return it

        Basically just clones stack attribute

        Returns:
           Game: Copy of current game

        '''
        return Game([s.copy() for s in self.stacks])


    def print_stacks(self):
        '''Print all stacks in a visually-appealing format

        This format sort of ressembles the actual game
        '''

        stacks = [s.copy() for s in self.stacks]

        max_height = max([s.height for s in stacks])
        message = ""

        for row in range(max_height):
            for column in range(len(stacks)):
                if row >= max_height - stacks[column].height:
                    temp = str(stacks[column].pop())[1:-1].split(",")
                    message += f" {temp[0], temp[1][0]} "
                else:
                    message += " "*12

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
    root_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    os.chdir(root_dir)

    game = Game("input/simp2.txt")
    game.print_stacks()
    print(game.static_evaluation())

if __name__ == "__main__":
    main()
