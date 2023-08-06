import random
import time
import numpy as np
import random

name = "software"
hwid = ["software"]


class instrument:
    def __init__(self, port):
        pass

    def Power(self):
        return random.randint(0, 100)

    def PowAvg(self):
        P = []
        for i in range(0, 5, 1):
            p = self.Power()
            P.append(p)
            time.sleep(0)
        PowerAvg = np.mean(P)
        PowerStd = np.std(P)
        return PowerAvg, PowerStd
