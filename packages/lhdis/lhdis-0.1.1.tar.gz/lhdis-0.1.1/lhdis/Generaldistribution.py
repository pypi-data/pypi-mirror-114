# ToDos
# Parent class Gaussian
# attributes: mean, standard_deviation, data
# methods: __init__, read_data_file

class Distribution:
    def __init__(self, mu=0, sigma=1):
        self.mean = mu
        self.stdev = sigma
        self.data = []


    """def read_data_file(self, filename):
        with open(filename) as file:
            datalist = []
            lines = file.readlines()
            for line in lines:
                datalist.append(int(line.strip('\n')))
        file.close()
        self.data = datalist.copy()"""