import numpy as np
from keras.models import load_model

from .classifiers import *
from .crops import *

model = load_model("models/soil_prediction.h5")
# model = load_model("models/soil_moisture_model.h5")

class SoilFertilityTester():
    inputarr = []
    stdinputarr = []

    avg = [296, 17, 506, 8, 1, 1, 7, 1, 4, 1, 9, 1]
    stdavg = [200, 40, 100, 7, 3.4, 0.63, 10, 0.6, 4.5, 0.2, 2.0, 0.5]
    norm = [0, 0, 0, 0, -1, 0, 1, 1, 1, 1, 1, 1]
    mul = [5500, 5500, 5500, 15000, 5500, 3000, 1000, 1000, 1000, 1000, 1000, 1000]
    classifiers = [lmhClassifier, lmhClassifier, lmhClassifier, 
                phClassifier, salineClassifier, lmhClassifier, 
                microClassifier, microClassifier, microClassifier, 
                microClassifier, microClassifier, microClassifier]

    normal = ['150-300', '23-57', '70-207', '7', '0-5', '0.51-0.75', '>10', '>0.6', '>4.5', '>0.2', '>2.0', '>0.5']
    params = ['N', 'P', 'K', 'pH', 'EC', 'OC', 'S', 'Zn', 'Fe', 'Cu', 'Mn', 'B']

    dev = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # (stdinp - stdavg)/stdavg
    colorarr = []
    verdict = []

    def __init__(self, inp: dict) -> None:
        inparr = []
        for k in self.params:
            inparr.append(inp[k])
        self.stdinputarr = inparr

    def convertInput(self):
        self.inputarr = []
        for i, inp_nutrient in enumerate(self.stdinputarr):
            sp = inp_nutrient/self.stdavg[i]
            if self.norm[i]<0:
                if sp<=1:
                    sp = 1
                else:
                    sp = sp*abs(self.norm[i])
            elif self.norm[i]>0:
                if sp>=1:
                    sp = 1
                else:
                    sp = sp*abs(self.norm[i])
            self.inputarr.append(sp*self.avg[i])

    def predictFertility(self):
        self.convertInput()
        print(self.inputarr)
        sample_input = np.array([self.inputarr])
        predicted_quality = model.predict(sample_input)
        quality = predicted_quality[0][0]
        if quality<=0:
            quality = 0
        elif quality>=1:
            quality = 1
        return quality
    
    def analyseSample(self):
        self.verdict = []
        self.colorarr = []
        sum = 0
        summ = 0
        for i, inp_nutrient in enumerate(self.stdinputarr):
            self.dev[i] = (inp_nutrient - self.stdavg[i])/self.stdavg[i]
            if self.norm[i]<0:
                if self.dev[i]<=0:
                    self.dev[i] = 0
            elif self.norm[i]>0:
                if self.dev[i]>=0:
                    self.dev[i] = 0
            sum += abs(self.dev[i]) * self.mul[i]
            summ += self.mul[i]
            self.verdict.append(self.classifiers[i](inp_nutrient, self.normal[i], self.colorarr))
        ampavgdev = sum / summ
        # ampwavgdev = wsum / summ
        devscore = 1 - ampavgdev
        if devscore<0:
            devscore = 0
        elif devscore>1:
            devscore = 1
        sgcrops = suggestCrops(self.stdinputarr)
        print(sgcrops)
        return {
            'dev': self.dev,
            'verdict': self.verdict,
            'devscore': devscore,
            'colorarr': self.colorarr,
            'crops': sgcrops
        }

# Driver code, for testing only
if __name__ == '__main__':
    stdinputarr = [480, 9.63, 201, 7.3, 0.11, 0.9, 42, 5.32, 46.68, 2.21, 36.98, 11]
    st = SoilFertilityTester(stdinputarr)

    print(f"Predicted Quality: {(int)(st.predictFertility()*100)}%")
    print(f"The deviation in parameters from optimal value: \n")

    analy = st.analyseSample()
    dev = analy['dev']
    verdict = analy['verdict']

    for i, nutrientdev in enumerate(dev):
        dpercent = round(nutrientdev*100)
        print(f'{st.params[i]}: {dpercent}%')
        print(f'Verdict: {verdict[i]}\n')

