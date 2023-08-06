name = "software"
hwid = ["software"]


class instrument:
    def __init__(self, port):
        pass

    def Shutter(self, val=0):
        if val == 1:
            print("Shutter not Opened")
        else:
            print("Shutter not Closed")

    def Get_Wavelength(self):
        return 0

    def Set_Wavelength(self, position):
        print(f"Not setting {position}")

    def On(self):
        print("Not on")

    def Off(self):
        print("Not off")

    def CheckStatus(self):
        print("You're not operating a real MaiTai")
        return 420

    def CheckWarm(self):
        print("Not real")
        return "Not real"
