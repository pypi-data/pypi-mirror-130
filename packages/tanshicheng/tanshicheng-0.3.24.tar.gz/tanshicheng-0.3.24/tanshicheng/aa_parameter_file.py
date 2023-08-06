class ParameterFile:
    def __init__(self, *parameterFileAddress):
        self.parameterDict = {}  # {parameter:[value,usedTimes]}
        self.conflictParameterDict = {}  # {parameter:[conflictValue1,..]}
        self.conflictTimes = 0

        self.readParameterFile(*parameterFileAddress)

    def readParameterFile(self, *parameterFileAddress):
        if len(parameterFileAddress) == 0:
            return 0
        for oneAddress in parameterFileAddress:
            with open(oneAddress, 'r', encoding='utf-8') as r:
                for line in r:
                    try:
                        parameter, value = line.split('#', 1)[0].strip().split('\t')
                        parameter, value = parameter.strip(), value.strip()
                    except:
                        continue
                    if parameter in self.parameterDict and self.parameterDict[parameter][0] != value:
                        if parameter in self.conflictParameterDict:
                            self.conflictParameterDict[parameter].append(value)
                        else:
                            self.conflictParameterDict[parameter] = [value]
                        self.conflictTimes += 1
                        continue
                    self.parameterDict[parameter] = [value, 0]
        return len(parameterFileAddress)

    def getConflictTimes(self):
        return self.conflictTimes

    def getConflictParameterAndTimes(self):
        conflictParameterTimes = []
        for parameter, values in self.conflictParameterDict.items():
            conflictParameterTimes.append((parameter, len(values)))
        return conflictParameterTimes

    def getParameter(self, parameter, count=True):
        if parameter not in self.parameterDict:
            return None
        if count:
            self.parameterDict[parameter][1] += 1
        return self.parameterDict[parameter][0]

    def getUsedParameters(self):
        usedParameterDict = {}
        for parameter, v in self.parameterDict.items():
            if v[1] > 0:
                usedParameterDict[parameter] = v
        return usedParameterDict

    def outUsedParameters(self, outAddress):
        usedParameterDict = self.getUsedParameters()
        with open(outAddress, 'w', encoding='utf-8') as w:
            for parameter, v in usedParameterDict.items():
                value = v[0]
                times = v[1]
                w.write(parameter + '\t' + value + '\t' + str(times) + '\r\n')

    def allParameters(self, outAddress):
        with open(outAddress, 'w', encoding='utf-8') as w:
            for parameter, v in self.parameterDict.items():
                value = v[0]
                times = v[1]
                w.write(parameter + '\t' + value + '\t' + str(times) + '\r\n')


if __name__ == '__main__':
    pf = ParameterFile('test1.txt', 'test2.txt')
    print('------getConflictTimes')
    print(pf.getConflictTimes())
    print('------getConflictParameterAndTimes')
    print(pf.getConflictParameterAndTimes())
    print('------getParameter')
    print(pf.getParameter('我'))
    print('------getUsedParameters')
    print(pf.getUsedParameters())
    print('------outUsedParameters')
    print(pf.outUsedParameters('test4.txt'))
    print('------allParameters')
    print(pf.allParameters('test3.txt'))
