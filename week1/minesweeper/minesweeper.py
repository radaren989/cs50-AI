import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cells) != self.count:
            return set()

        return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count != 0:
            return set()

        return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # add cell to made moves
        self.moves_made.add(cell)

        # mark cell as safe
        self.mark_safe(cell)
        
        #create matrix with cells that adjancent to cell
        cellSet = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            if i < 0 or i >= self.height:
                continue
            
            for j in range(cell[1] - 1, cell[1] + 2):
                if j < 0 or j >= self.width or (cell[0] == i and cell[1] == j):
                    continue
                
                cellSet.add((i,j))

        #print(f"CellSet: {cellSet}")
        final_set = set()
        count_copy = count
        for cell in cellSet:
            if cell in self.mines:
                count_copy -= 1
            elif cell not in self.safes | self.mines:
                final_set.add(cell)

        #print(f"final_set: {final_set}")
        # create new sentence and add to KB
        new_sentence = Sentence(final_set, count_copy)
        if len(final_set) > 0:
            self.knowledge.append(new_sentence)
        
        # If sentence has no mine then it means all cells are safe therefore mark them as safe
        copy_cells = new_sentence.known_mines().copy()
        #print(f"known mines: {copy_cells}")
        #print(f"self mines: {self.mines}")
        for cell in copy_cells:
            self.mark_mine(cell)

        # If sentence count is equal to set size, it means all cells are mines therefore mark them mine
        copy_cells = new_sentence.known_safes().copy()
        #print(f"known safe: {copy_cells}")
        #print(f"self safes: {self.safes}")
        for cell in copy_cells:
            self.mark_safe(cell)

        #print(f"new sentence {new_sentence}")
        # Iterate over a copy of self.knowledge :to avoid modifying the list during iteration
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence2.cells > sentence1.cells:
                    sentence2.cells -= sentence1.cells
                    sentence2.count -= sentence1.count

                elif sentence2.cells < sentence1.cells:
                    sentence1.cells -= sentence2.cells
                    sentence1.count -= sentence2.count

                copy_cells = sentence1.known_mines().copy()
                for cell in copy_cells:
                    self.mark_mine(cell)

                copy_cells = sentence2.known_mines().copy()
                for cell in copy_cells:
                    self.mark_mine(cell)

                copy_cells = sentence1.known_safes().copy()
                for cell in copy_cells:
                    self.mark_safe(cell)

                copy_cells = sentence2.known_safes().copy()
                for cell in copy_cells:
                    self.mark_safe(cell)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        not_moved_safes = self.safes - self.moves_made 
        #print(f"not moved safes: {not_moved_safes}")
        return not_moved_safes.pop() if len(not_moved_safes) > 0 else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        not_moved = {(i, j) for i in range(0, self.height) for j in range(0, self.width)}
        not_moved -= self.moves_made
        not_moved -= self.mines

        not_moved = list(not_moved)

        if not_moved:
            return random.choice(not_moved)

