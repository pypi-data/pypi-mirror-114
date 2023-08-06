# ToDos:
# Child class of Distribution class
# attributes: same as parent class
# methods: __init__, read_data_file, calculate_mean, calculate_stdev, plot_histogram, pdf, __add__, __repr__
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Gaussian(Distribution):
    def __init__(self, mu=0, sigma=1):
        Distribution.__init__(self, mu, sigma)


    def read_data_file(self, filename, sample=True):
        with open(filename) as file:
            lines = file.readlines()
            datalist = [float(n.strip('\n')) for n in lines]
        self.data = datalist.copy()
        file.close()
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev(sample)


    def calculate_mean(self):
        try:
            avg = 1.0 * sum(self.data) / len(self.data)
        except ZeroDivisionError as ze:
            return self.mean
        
        self.mean = avg
        return self.mean


    def calculate_stdev(self, sample=True):
        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        mean = self.calculate_mean()
        sigma = 0

        for x in self.data:
            sigma += (x - mean) ** 2
        sigma = math.sqrt(sigma / n)

        self.stdev = sigma
        return self.stdev
            

    def plot_histogram(self):
        plt.hist(self.data)
        plt.title('Histogram of Data Distribution')
        plt.xlabel('Data')
        plt.ylabel('Count')


    def pdf(self, k):
        return (1.0 / (self.stdev * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((k - self.mean) / self.stdev)**2)


    def __add__(self, other):
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt((self.stdev**2) + (other.stdev**2))
        
        return result


    def __repr__(self):
        return "mean: {}, standard deviation: {}".format(self.mean, self.stdev)