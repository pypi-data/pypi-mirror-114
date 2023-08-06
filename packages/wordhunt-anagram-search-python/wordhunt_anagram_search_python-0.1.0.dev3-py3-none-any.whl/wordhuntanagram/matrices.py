class Matrix:
    def __init__(self, M=None, j=None, i=None, args=None):
        if args is None:
            args = []
        self.__column_number = j
        self.__row_number = i
        if i is not None:
            self.__row_number = i
        elif j is not None:
            self.__column_number = j
            self.__mat = [[0] * self.__row_number for _ in range(self.__column_number)]
        if self.__row_number is not None and self.__column_number is not None and len(args) != 0:
            t = 0
            self.__mat = [[0] * self.__row_number for _ in range(self.__column_number)]
            for m in range(self.__column_number):
                for n in range(self.__row_number):
                    self.__mat[m][n] = args[t]
                    t += 1
        elif self.__row_number is not None and self.__column_number is not None and len(args) == 0:
            self.__mat = [[0] * self.__row_number for _ in range(self.__column_number)]
            for m in range(self.__column_number):
                for n in range(self.__row_number):
                    print("Enter value indexed ", m+1, " x ", n+1)
                    self.__mat[m][n] = eval(input(""))
        elif M is not None:
            self.__mat = M
            self.__row_number = len(M[0])
            self.__column_number = len(M)
        else:
            self.__row_number = 3
            self.__column_number = 3
            self.__mat = [[0] * self.__row_number for _ in range(self.__column_number)]

    def __eq__(self, other):
        return isinstance(other, Matrix) and self.__mat == other.__mat

    def __hash__(self):
        return hash(self)

    def __repr__(self):
        return '\n'.join([''.join(['{:10}'.format(item) for item in row])
                         for row in self.return_matrix()])

    def __mul__(self, other):
        if isinstance(other, Matrix) and self.__row_number == other.__column_number:
            result = [[sum(am * bm for am, bm in zip(A_row, B_col))
                       for B_col in zip(*other.return_matrix())]
                      for A_row in self.return_matrix()]
            return Matrix(result)

    def __add__(self, other):
        result = [[0] * self.__row_number for _ in range(self.__column_number)]
        if isinstance(other, Matrix) and self.__row_number == other.__row_number and self.__column_number == \
                other.__column_number:
            for j in range(self.__column_number):
                for i in range(self.__row_number):
                    result[j][i] = self.return_matrix()[j][i] + other.return_matrix()[j][i]
            return Matrix(result)

    def __sub__(self, other):
        result = [[0] * self.__row_number for _ in range(self.__column_number)]
        if isinstance(other, Matrix) and self.__row_number == other.__row_number and self.__column_number == \
                other.__column_number:
            for j in range(self.__column_number):
                for i in range(self.__row_number):
                    result[j][i] = self.return_matrix()[j][i] - other.return_matrix()[j][i]
            return Matrix(result)

    def mul(self, scalar):
        result = [[0] * self.__row_number for _ in range(self.__column_number)]
        for j in range(self.__column_number):
            for i in range(self.__row_number):
                result[j][i] = self.return_matrix()[j][i] * scalar
        return Matrix(result)

    def div(self, scalar):
        result = [[0] * self.__row_number for _ in range(self.__column_number)]
        for j in range(self.__column_number):
            for i in range(self.__row_number):
                result[j][i] = self.return_matrix()[j][i] / scalar
        return Matrix(result)

    def insert(self, column, row, value):
        self.__mat[column][row] = value
    
    def index(self, column, row):
        return self.__mat[row][column]

    def mix_matrix(self):
        return Matrix(mix_matrix(self.return_matrix()))

    def determinant(self):
        return det(self.return_matrix())

    def upper_triangular_matrix(self):
        return Matrix(upper_t_m(self.return_matrix()))

    def matrix_minor(self, i, j):
        return Matrix(minor_(self.return_matrix(), i, j))

    def len_column(self):
        return self.__column_number

    def eigenvalues(self):
        return ei_gen_v(self.return_matrix())

    def len_row(self):
        return self.__row_number

    def return_matrix(self):
        return self.__mat

    def as_list(self):
        pass

    def as_string(self, flatten=False):
        if not flatten:
            new = [[] * self.len_row() for _ in range(self.len_column())]
            for index_j in range(self.len_column()):
                for index_i in range(self.len_row()):
                    new[index_j][index_i] = str(self.index(index_j, index_i))
        else:
            new = ''
            for index_j in range(self.len_column()):
                for index_i in range(self.len_row()):
                    new += str(self.index(index_j, index_i))
        return new

    def identity(self):
        result = [[0] * self.__row_number for _ in range(self.__column_number)]
        for j in range(self.__column_number):
            result[j][j] = 1
        return Matrix(result)

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def swap_matrix(self, row1, row2):
        return Matrix(swap(self.return_matrix(), row1, row2))

    def rr_matrix(self):
        return Matrix(echelon(self.return_matrix()))

    def m_inverse(self):
        return Matrix(inv(self.return_matrix()))

    def extract_matrix(self, index_j, index_i, size_h, size_w):
        return Matrix(ext_m(self.return_matrix(), index_j, index_i, size_h, size_w))

    def transpose(self):
        return Matrix(transpose(self.return_matrix()))

    def add_column(self, list_of_r=None):
        if list_of_r is not None:
            return Matrix(add_column(self.return_matrix(), list_of_r))
        else:
            list_of_r = []
            for i in range(len(self.return_matrix())):
                print("Enter element for row ", i)
                list_of_r.append(eval(input()))
            return Matrix(add_column(self.return_matrix(), list_of_r))

    def manual_swap(self, j, i, j1, i1):
        return Matrix(swap1(self.return_matrix(), j, i, j1, i1))


def minor_(m, j, i):
    k = m[:j] + m[j+1:]
    j = []
    for row in k:
        j.append(row[:i] + row[i+1:])
    return j


def row_mat(m, j):
    return m[j]


def column_mat(m, i, j):
    return [m[col+j][i] for col in range(len(m)-j)]


def upper_t_m(m):
    mat_copy = m.copy()
    for col_ in range(len(m)-1):
        for row_ in range(col_+1, len(m)):
            if mat_copy[col_][col_] == 0:
                mat_copy = swap(mat_copy, col_, row_)
        else:
            break
    for j in range(len(m[0])-1):
        for i in range(j+1, len(m)):
            if mat_copy[j][j] != 0:
                prime = mat_copy[i][j] / mat_copy[j][j]
                col_ = [prime*elem for elem in mat_copy[j]]
                row3 = [row2-row1 for row2, row1 in zip(mat_copy[i], col_)]
                mat_copy[i] = row3
    return mat_copy


def ei_gen_v(m):
    li = []
    mat = upper_t_m(m.copy())
    for i in range(len(m)):
        li.append(mat[i][i])
    return li


def det(m):
    if len(m) == len(m[0]):
        dm = upper_t_m(m.copy())
        d = 1
        for i in range(len(m)):
            d *= dm[i][i]
        return d
    else:
        return 'No Determinant'


def swap(m, j1, j2):
    m[j1], m[j2] = m[j2], m[j1]
    return m


def inv(m):
    result_matrix = [[0]*len(m[0]) for _ in range(len(m))]
    determinant_of_mat = det(m.copy())
    if determinant_of_mat != 0:
        for j in range(len(m)):
            for i in range(len(m[0])):
                result_matrix[i][j] = (-1)**((i+j) % 2) * det(minor_(m.copy(), j, i)) / determinant_of_mat
        return result_matrix
    else:
        return 'No Inverse'


def transpose(m):
    rez = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    return rez


def ext_m(m, j, i, size_h, size_w):
    extracted_col = m[j:size_h+j]
    extracted_elem = []
    for row in extracted_col:
        row = row[i:size_w+i]
        extracted_elem.append(row)
    return extracted_elem


def add_column(original, new):
    m = original.copy()
    if len(original) == len(new):
        for i in range(len(original)):
            m[i].append(new[i])
    return m


def echelon(m):
    lead = 0
    row_count = len(m)
    column_count = len(m[0])
    for row_elem_ in range(row_count):
        if column_count <= lead:
            return m
        i = row_elem_
        while m[i][lead] == 0:
            i += 1
            if row_count == i:
                i = row_elem_
                lead += 1
                if column_count == lead:
                    return m
        m[i], m[row_elem_] = m[row_elem_], m[i]
        lv = m[row_elem_][lead]
        m[row_elem_] = [elem / lv for elem in m[row_elem_]]
        for i in range(row_count):
            if i != row_elem_:
                lv = m[i][lead]
                m[i] = [elem - lv*elem2 for elem, elem2 in zip(m[i], m[row_elem_])]
        lead += 1
    return m


def solving_system_eqn(m):
    copy_ = m.copy()
    echelon_form = echelon(copy_)
    ans = []
    if len(copy_)+1 == len(copy_[0]):
        for i in range(len(copy_)):
            if all(x == 0 for x in echelon_form[i][:-1]):
                ans.append('Infinite solutions: Potentially inconsistent system')
            else:
                ans.append(echelon_form[i][len(copy_)])
        return ans
    elif len(copy_) == len(copy_[0]):
        pass


def mix_matrix(m):
    for j in range(len(m)):
        for i in range(len(m[0])-1):
            m[j][i], m[j][i+1] = m[j][i+1], m[j][i]
    return m


def swap1(m, j, i, j1, i1):
    if i < len(m[0]) and i1 < len(m[0]) and j < len(m) and j1 < len(m):
        m[j][i], m[j1][i1] = m[j1][i1], m[j][i]
    return m
