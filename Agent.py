# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image

class Agent:
    def __init__(self):
        self.all_images = {}
        self.horizontal = {}
        self.vertical = {}
        self.diagonal = {}
        self.problem = {}
        pass
    
    def Solve(self,problem):
        
        self.problem = problem
        # if problem.name == "Basic Problem C-01":
        for key in problem.figures.keys():
            figure = problem.figures[key]
            self.all_images[key] = Image.open(figure.visualFilename)

        self.get_all_pixel_counts()
        self.get_horizontal()
        self.get_vertical()

        hor_ans = self.generate_horizontal_answer()
        return int(ans)
        return -1

    def generate_horizontal_answer(self):

        A = self.problem.figures['A'].pixel_counts
        B = self.problem.figures['B'].pixel_counts
        C = self.problem.figures['C'].pixel_counts
        
        D = self.problem.figures['D'].pixel_counts
        E = self.problem.figures['E'].pixel_counts
        F = self.problem.figures['F'].pixel_counts

        G = self.problem.figures['G'].pixel_counts
        H = self.problem.figures['H'].pixel_counts

        if A[0] == 0.0:
            ABblack = (B[0]-A[0])/B[0]
        else:
            ABblack = (B[0]-A[0])/A[0]
        if B[0] == 0.0:
            BCblack = (C[0]-B[0])/C[0]
        else:
            BCblack = (C[0]-B[0])/B[0]

        print ABblack, BCblack
        DEblack = (E[0]-D[0])/D[0]
        EFblack = (F[0]-E[0])/E[0]
        print DEblack, EFblack

        avg_black_change = (BCblack + EFblack)/2
        print avg_black_change
        BCsame = self.horizontal['BC']/(B[0]+C[0])
        EFsame = self.horizontal['EF']/(E[0]+F[0])

        avg_black_same = (BCsame + EFsame)/2

        change_ratios = []
        same_ratios = []


        for ans in ['1','2','3','4','5','6','7','8']:

            same = self.same_black('H',ans)/(H[0]+self.problem.figures[ans].pixel_counts[0])
            change = (self.problem.figures[ans].pixel_counts[0] - H[0])/H[0]
            print abs(change - avg_black_change)
            change_ratios.append(abs(change - avg_black_change)) #/avg_black_change)
            same_ratios.append(abs(same - avg_black_same)) #/avg_black_same)
        
        print change_ratios
        print same_ratios

        all_ratios = [change + same for change,same in zip(change_ratios,same_ratios)]

        return all_ratios

    def get_horizontal(self):
        rows = [['A','B','C'],['D','E','F'],['G','H']]
        for row in rows:
            for i in range(len(row)-1):
                self.horizontal[row[i]+row[i+1]] = self.same_black(row[i], row[i+1])

    def get_vertical(self):
        cols = [['A','D','G'],['B','E','H'],['C','F']]
        for col in cols:
            for i in range(len(col)-1):
                self.vertical[col[i] + col[i+1]] = self.same_black(col[i], col[i+1])

        self.diagonal = self.same_black('A','E')
    
    
    def get_all_pixel_counts(self):

        for key in self.problem.figures.keys():
            figure = self.problem.figures[key]
            figure.pixel_counts = self.num_pixels(figure.name)


    def num_pixels(self, name):
        # print figureA.size, figureB.size
        figure = self.all_images[name]
        figure_loaded = figure.load()
        white = 0.0
        black = 0.0
        for i in range(0, figure.size[0]):
            for j in range(0, figure.size[1]):
                pixel = figure_loaded[i,j]
                if pixel == (255,255,255,255):
                    white += 1
                else:
                    black += 1
        return black, white

    def same_black(self, name1, name2):
        figure1 = self.all_images[name1]
        figure1_loaded = figure1.load()

        figure2 = self.all_images[name2]
        figure2_loaded = figure2.load()
        same_black = 0.0
        for i in range(0, figure1.size[0]):
            for j in range(0, figure1.size[1]):
                pixel1 = figure1_loaded[i,j]
                pixel2 = figure2_loaded[i,j]
                if pixel1 != (255,255,255,255) and pixel2 != (255,255,255,255):
                    same_black += 1
        return same_black

