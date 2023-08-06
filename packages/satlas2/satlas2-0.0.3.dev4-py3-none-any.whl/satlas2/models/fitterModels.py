from satlas2.core import Model, Parameter

import numpy as np
from scipy.special import wofz
from sympy.physics.wigner import wigner_6j, wigner_3j

__all__ = ['Linear', 'Exponential', 'HFS']

sqrt2 = 2 ** 0.5
sqrt2log2t2 = 2 * np.sqrt(2 * np.log(2))
log2 = np.log(2)

class Linear(Model):
    def __init__(self, a, b, name=None, prefunc=None):
        super().__init__(name=name, prefunc=prefunc)
        self.params = {
                'a': Parameter(value=a, min=-np.inf, max=np.inf, vary=True),
                'b': Parameter(value=b, min=-np.inf, max=np.inf, vary=True),
                }

    def f(self, x):
        x = self.transform(x)
        a = self.params['a'].value
        b = self.params['b'].value
        return a*x+b

class Exponential(Model):
    def __init__(self, a, b, c, name=None, prefunc=None):
        super().__init__(name=name, prefunc=prefunc)
        self.params = {
            'amplitude': Parameter(value=a, min=-np.inf, max=np.inf, vary=True),
            'halflife': Parameter(value=b, min=-np.inf, max=np.inf, vary=True),
            'background': Parameter(value=c, min=-np.inf, max=np.inf, vary=True),
        }

    def f(self, x):
        x = self.transform(x)
        a = self.params['amplitude'].value
        b = self.params['halflife'].value
        c = self.params['background'].value
        return a*np.exp(log2*x/b)+c

class HFS(Model):
    def __init__(self, I, J, A=[0, 0], B=[0, 0], C=[0, 0], df=0, fwhm=50, bkg=1, name=None, N=None, offset=0, poisson=0, scale=1.0, racah=True, prefunc=None):
        super().__init__(name=name, prefunc=prefunc)
        J1, J2 = J
        lower_F = np.arange(abs(I - J1), I+J1+1, 1)
        upper_F = np.arange(abs(I - J2), I+J2+1, 1)

        self.lines = []
        self.intensities = {}
        self.scaling_Al = {}
        self.scaling_Bl = {}
        self.scaling_Cl = {}
        self.scaling_Au = {}
        self.scaling_Bu = {}
        self.scaling_Cu = {}

        for i, F1 in enumerate(lower_F):
            for j, F2 in enumerate(upper_F):
                if abs(F2 - F1) <= 1 and not F2 == F1 == 0.0:
                    if F1 % 1 == 0:
                        F1_str = '{:.0f}'.format(F1)
                    else:
                        F1_str = '{:.0f}_2'.format(2*F1)

                    if F2 % 1 == 0:
                        F2_str = '{:.0f}'.format(F2)
                    else:
                        F2_str = '{:.0f}_2'.format(2*F2)

                    line = '{}to{}'.format(F1_str, F2_str)
                    self.lines.append(line)

                    C1, D1, E1 = self.calcShift(I, J1, F1)
                    C2, D2, E2 = self.calcShift(I, J2, F2)

                    self.scaling_Al[line] = C1
                    self.scaling_Bl[line] = D1
                    self.scaling_Cl[line] = E1
                    self.scaling_Au[line] = C2
                    self.scaling_Bu[line] = D2
                    self.scaling_Cu[line] = E2

                    intens = float((2 * F1 + 1) * (2 * F2 + 1) * \
                         wigner_6j(J2, F2, I, F1, J1, 1.0) ** 2) # DO NOT REMOVE CAST TO FLOAT!!!
                    self.intensities['Amp'+line] = Parameter(value=intens, min=0, vary=not racah)

        norm = max([p.value for p in self.intensities.values()])
        for n, v in self.intensities.items():
            v.value /= norm

        pars = {'centroid': Parameter(value=df),
                'Al': Parameter(value=A[0]),
                'Au': Parameter(value=A[1]),
                'Bl': Parameter(value=B[0]),
                'Bu': Parameter(value=B[1]),
                'Cl': Parameter(value=C[0], vary=False),
                'Cu': Parameter(value=C[1], vary=False),
                'bkg': Parameter(value=bkg),
                'FWHMG': Parameter(value=fwhm, min=0.01),
                'FWHML': Parameter(value=fwhm, min=0.01),
                'scale': Parameter(value=scale, min=0, vary=racah)}
        if N is not None:
            pars['N'] = Parameter(value=N, vary=False)
            pars['Offset'] = Parameter(value=offset)
            pars['Poisson'] = Parameter(value=poisson, min=0, max=1)
            self.f = self.fShifted
        else:
            self.f = self.fUnshifted
        pars = {**pars, **self.intensities}

        self.params = pars

        if I < 2 or J1 < 2:
            self.params['Cl'].vary = False
        if I < 2 or J2 < 2:
            self.params['Cu'].vary = False
        if I < 1 or J1 < 1:
            self.params['Bl'].vary = False
        if I < 1 or J2 < 1:
            self.params['Bu'].vary = False
        if I == 0 or J1 == 0: 
            self.params['Al'].vary = False
        if I == 0 or J2 == 0:
            self.params['Au'].vary = False
        self.xtransformed = None
        self.xhashed = None

    def fUnshifted(self, x):
        centroid = self.params['centroid'].value
        Al = self.params['Al'].value
        Au = self.params['Au'].value
        Bl = self.params['Bl'].value
        Bu = self.params['Bu'].value
        Cl = self.params['Cl'].value
        Cu = self.params['Cu'].value
        FWHMG = self.params['FWHMG'].value
        FWHML = self.params['FWHML'].value
        scale = self.params['scale'].value
        bkg = self.params['bkg'].value

        result = np.zeros(len(x))
        x = self.transform(x)
        for line in self.lines:
            pos = centroid + Au * self.scaling_Au[line] + Bu * self.scaling_Bu[line] + Cu * self.scaling_Cu[line] - Al * self.scaling_Al[line] - Bl * self.scaling_Bl[line] - Cl * self.scaling_Cl[line]
            result += self.params['Amp' + line].value * self.peak(x - pos, FWHMG, FWHML)

        return scale * result + bkg

    def fShifted(self, x):
        centroid = self.params['centroid'].value
        Al = self.params['Al'].value
        Au = self.params['Au'].value
        Bl = self.params['Bl'].value
        Bu = self.params['Bu'].value
        FWHMG = self.params['FWHMG'].value
        FWHML = self.params['FWHML'].value
        scale = self.params['scale'].value
        N = self.params['N'].value
        offset = self.params['Offset'].value
        poisson = self.params['Poisson'].value
        bkg = self.params['bkg'].value

        result = np.zeros(len(x)) 
        for line in self.lines:
            pos = centroid + Au * self.scaling_Au[line] + Bu * self.scaling_Bu[line] + Cu * self.scaling_Cu[line] - Al * self.scaling_Al[line] - Bl * self.scaling_Bl[line] - Cl * self.scaling_Cl[line]
            for i in range(N + 1):
                if self.prefunc:
                    result += self.params['Amp' + line].value * self.peak(self.prefunc(x - i * offset) - pos, FWHMG, FWHML) * (poisson**i)/np.math.factorial(i)
                else:
                    result += self.params['Amp' + line].value * self.peak(x - pos - i * offset, FWHMG, FWHML) * (poisson**i)/np.math.factorial(i)

        return scale * result + bkg

    def peak(self, x, FWHMG, FWHML):
        z = self.preparePeak(x, FWHMG, FWHML)
        n = self.norm(FWHML, FWHMG)
        ret = wofz(z).real
        return ret/n

    def norm(self, FWHML, FWHMG):
        return wofz(1j * FWHML / (FWHMG * sqrt2)).real

    def preparePeak(self, x, FWHMG, FWHML):
        sigma, gamma = FWHMG / sqrt2log2t2, FWHML / 2
        z = (x + 1j * gamma) / (sigma * sqrt2)
        return z

    def calcShift(self, I, J, F):
        phase = (-1)**(I+J+F)
        contrib = []
        for k in range(1, 4):
            n = float(wigner_6j(I, J, F, J, I, k))
            d = float(wigner_3j(I, k, I, -I, 0, I) * wigner_3j(J, k, J, -J, 0, J))
            shift = phase * n / d
            if not np.isfinite(shift):
                contrib.append(0)
            else:
                if k == 1:
                    shift = shift * (I*J)
                elif k == 2:
                    shift = shift / 4
                contrib.append(shift)
        return contrib

    def pos(self):
        centroid = self.params['centroid'].value
        Al = self.params['Al'].value
        Au = self.params['Au'].value
        Bl = self.params['Bl'].value
        Bu = self.params['Bu'].value
        Cl = self.params['Cl'].value
        Cu = self.params['Cu'].value
        pos = []
        for line in self.lines:
            pos.append(centroid + Au * self.scaling_Au[line] + Bu * self.scaling_Bu[line] + Cu * self.scaling_Cu[line] - Al * self.scaling_Al[line] - Bl * self.scaling_Bl[line] - Cl * self.scaling_Cl[line])
        return pos
