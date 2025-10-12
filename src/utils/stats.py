class Stats:
    def __init__(self):
        self.toopendms = 0
        self.toopenchannels = 0
        self.totalsent = 0
        self.totaltosend = 0
        self.progress = lambda: round((self.totalsent / self.totaltosend) * 100, 2) if self.totaltosend else 0
stats = Stats()