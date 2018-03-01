class Board:
    def __init__(self):
        self.adjacency_list = {
            1: [2, 5, 6],
            2: [1, 3, 8],
            3: [2, 4, 10],
            4: [3, 5, 12],
            5: [1, 4, 14],
            6: [1, 7, 15],
            7: [6, 8, 16],
            8: [2, 7, 9],
            9: [8, 10, 17],
            10: [3, 9, 11],
            11: [10, 12, 18],
            12: [4, 11, 13],
            13: [12, 14, 19],
            14: [5, 13, 15],
            15: [6, 14, 20],
            16: [7, 17, 20],
            17: [9, 16, 18],
            18: [11, 17, 19],
            19: [13, 18, 20],
            20: [15, 16, 19]
        }

    def get_adjacent(self, v):
        return self.adjacency_list[int(v)]

    def is_adjacent(self, v1, v2):
        return int(v1) in self.adjacency_list[int(v2)]
