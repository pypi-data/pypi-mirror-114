from wordhuntanagram.matrices import Matrix
from wordhuntanagram.base import WordBase



class WordHunt(WordBase): 

    def __init__(self, n_column:int=None, n_rows:int=None, matrix:Matrix=None, args:list[str]=None, auto_input:bool=True):
        if matrix is None:
            if not auto_input:
                pass
            else:
                args = []
            super().__init__(n_column*n_rows, state='wordhunt', force_state=True, auto_input=auto_input, split=(n_column, n_rows), args=args)
        else:
            super().__init__(word_matrix=matrix)
                
    def hunt(self) -> None:
        # start_with 3 letter words
        matrix = self._matrix
        # pick a point and use that point to find words
        for column in range(matrix.len_column()):
            for row in range(matrix.len_row()):
                self.walk_ordered([[[row, column]]])

    def make_matrix(self, args):
        i = 0
        for column in range(self._matrix.len_column()):
            for row in range(self._matrix.len_row()):
                self._matrix.insert(column, row, args[i])
                i += 1

    def is_word(self, word, words):
        return word in words
        
    def walk(self, path):
        word = ""
        for step in path:
            word += self._matrix.index(step[0], step[1])
        return word

    def is_in_trie(self, word, path):
        trie = self.root
        for letter in word:
            if letter in trie:
                trie = trie[letter]
            else:
                return False
        if trie['isWord']:
            self.words[word] = path
        return True

    def walk_ordered(self, paths, new_paths=None, index=0, trie=None):
        if not new_paths:
            new_paths = []
        if not trie:
            trie = self.root
        for path in paths:
            word_initial = self.walk(path)
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_path = [path[-1][0]+direction[0], path[-1][1]+direction[1]]
                if 0 <= new_path[0] < self._matrix.len_column() and 0 <= new_path[1] < self._matrix.len_row() and new_path not in path:
                    path_moved = path + [new_path]
                    word = word_initial + self._matrix.index(*new_path)
                    if self.is_in_trie(word, path_moved):
                        new_paths.append(path_moved)
                    else:
                        pass
        if new_paths:
            paths += self.walk_ordered(new_paths, index=index+1)
        return paths
        
    def get_word(self, path):
        return self._matrix.index(path[0], path[1])

        


