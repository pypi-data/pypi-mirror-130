from GSKhopt.CSVDataFrame import CSVDataFrame
class Logger():
    def __init__(self,filepath="log.csv",automatic_versioning=False):
        self.filepath = filepath
        self.resframe = CSVDataFrame()
        self.setheader()
        self.frame = []
        self._continue_logging = False
        print("Logging will be on file " + self.filepath)
        if automatic_versioning:
            pass
    def set_automatic_version(self):
        #create a folder using last version file (a file stored in config)
        pass


    def setheader(self,header=None):
        if header:
            self.resframe.setheader(header)
        else:
            self.resframe.setheader(['Step','best parameters','objective value','nfes'])
    def continue_log(self):
        print("Logging will continue on file " + self.filepath)
        self._continue_logging = True
    def log(self,data):
        self.frame.append(data)
    def end(self):
        self.resframe.PassDataFrame(self.frame)
        self.resframe.save(self.filepath)
        self.frame=[]
    def clear(self):
        self.frame = []
        self.resframe = CSVDataFrame()
        self.setheader()
