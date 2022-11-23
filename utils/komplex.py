class Komplex():
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def add(self, zahl):
        return Komplex(self.real+zahl.real, self.imag+zahl.imag)

    def sub(self, zahl):
        return Komplex(self.real-zahl.real, self.imag-zahl.imag)

    def mul(self, zahl):
        r = self.real*zahl.real-self.imag*zahl.imag
        i = self.real*zahl.imag+self.imag*zahl.real
        return Komplex(r, i)

    def div(self, zahl):
        r = (self.real*zahl.real+self.imag*zahl.imag)/(zahl.real**2+zahl.imag**2)
        i = (self.imag*zahl.real-self.real*zahl.imag)/(zahl.real**2+zahl.imag**2)
        return Komplex(r, i)

    def norm(self):
        return self.real*self.real+self.imag*self.imag
