# ToDOs:
# child class of Generaldistribution class
# attributes: mean, stdev, n, p
# methods: __init__, calculate_mean, calculate_stdev, replace_stats_with_data(calcuate n, p from read data), plot_bar, pdf, 
# methods: plot_bar_pdf, __add__, __repr__
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    def __init__(self, prob=.5, n=10):
        Distribution.__init__(self, mu=0, sigma=1)
        self.p = prob
        self.n = n
    

    def read_data_file(self, filename):
        with open(filename) as file:
            lines = file.readlines()
            datalist = [int(n.strip('\n')) for n in lines]
        self.data = datalist.copy()
        file.close()
        self.p, self.n = self.replace_stats_with_data()


    def calculate_mean(self):
        self.mean = self.p * self.n
        return self.mean

    
    def calculate_stdev(self):
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev
    

    def replace_stats_with_data(self):
        self.n = len(self.data)
        # I think this method of finding p is wrong.
        self.p = 1.0 * sum(self.data) / len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n


    def plot_bar(self):
        pass


    def pdf(self, k):
        nCk = math.factorial(self.n) / (math.factorial(self.n - k) * math.factorial(k))
        return nCk * (self.p**k) * ((1 - self.p)**(self.n-k))


    def plot_pdf_bar(self):
        pass


    def __add__(self, other):
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as Ase:
            raise

        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.mean = result.calculate_mean()
        result.stdev = result.calculate_stdev()

        return result


    def __repr__(self):
        return "mean: {}, standard deviation: {}, p: {}, n: {}".format(self.mean, self.stdev, self.p, self.n)
    