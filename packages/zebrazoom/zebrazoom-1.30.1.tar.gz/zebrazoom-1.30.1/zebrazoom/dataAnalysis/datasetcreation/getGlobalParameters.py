from zebrazoom.dataAnalysis.datasetcreation.getDeltaHead import getDeltaHead
import numpy as np
from scipy.interpolate import UnivariateSpline
import math

def getGlobalParameters(curbout, fps, pixelSize, frameStepForDistanceCalculation, previousBoutEnd, listOfParametersToCalculate):
  
  listOfParametersCalculated = []
  
  for parameterToCalculate in listOfParametersToCalculate:
    
    
    
    if parameterToCalculate == 'BoutDuration':
      
      BoutDuration = (curbout["BoutEnd"] - curbout["BoutStart"] + 1) / fps
      listOfParametersCalculated.append(BoutDuration)
    
    
    
    elif parameterToCalculate == 'TotalDistance':
      
      TotalDistance = 0
      posX = curbout["HeadX"]
      posY = curbout["HeadY"]
      rangeUsedForDistanceCalculation   = [frameStepForDistanceCalculation*i for i in range(0, int(len(posX)/frameStepForDistanceCalculation))]
      if len(rangeUsedForDistanceCalculation) == 0:
        rangeUsedForDistanceCalculation = [0, len(posX) - 1]
      else:
        rangeUsedForDistanceCalculation = rangeUsedForDistanceCalculation + [len(posX) - 1]
      posX = [posX[i] for i in rangeUsedForDistanceCalculation]
      posY = [posY[i] for i in rangeUsedForDistanceCalculation]
      for j in range(0, len(posX)-1):
          TotalDistance = TotalDistance + math.sqrt((posX[j+1] - posX[j])**2 + (posY[j+1] - posY[j])**2)
      TotalDistance = TotalDistance * pixelSize
      listOfParametersCalculated.append(TotalDistance)
    
    
    
    elif parameterToCalculate == 'Speed':
      
      Speed = TotalDistance / BoutDuration # This is a bit of a "hack" (not very "clean"), it only works because the listOfParametersToCalculate provided contains BoutDuration and TotalDistance before Speed
      listOfParametersCalculated.append(Speed)
    
    
    
    elif parameterToCalculate == 'NumberOfOscillations':
      
      if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list:
        NumberOfOscillations = len(curbout["Bend_Timing"]) / 2
      else:
        NumberOfOscillations = float('NaN')
      listOfParametersCalculated.append(NumberOfOscillations)
    
    
    
    elif parameterToCalculate == 'meanTBF':
      
      meanTBF = NumberOfOscillations / BoutDuration # This is a bit of a "hack" (not very "clean"), it only works because the listOfParametersToCalculate provided contains NumberOfOscillations and BoutDuration before meanTBF
      listOfParametersCalculated.append(meanTBF)
    
    
    
    elif parameterToCalculate == 'maxOfInstantaneousTBF':
      
      if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list and len(curbout["Bend_Timing"]):
        maxOfInstantaneousTBF = np.max(fps / (2 * np.diff([0] + curbout['Bend_Timing'])))
      else:
        maxOfInstantaneousTBF = float('NaN')
      listOfParametersCalculated.append(maxOfInstantaneousTBF)
    
    
    
    elif parameterToCalculate == 'meanOfInstantaneousTBF':
      
      if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list and len(curbout["Bend_Timing"]):
        meanOfInstantaneousTBF = np.mean(fps / (2 * np.diff([0] + curbout['Bend_Timing'])))
      else:
        meanOfInstantaneousTBF = float('NaN')
      listOfParametersCalculated.append(meanOfInstantaneousTBF)
    
    
    
    elif parameterToCalculate == 'medianOfInstantaneousTBF':
      
      if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list and len(curbout["Bend_Timing"]):
        medianOfInstantaneousTBF = np.median(fps / (2 * np.diff([0] + curbout['Bend_Timing'])))
      else:
        medianOfInstantaneousTBF = float('NaN')
      listOfParametersCalculated.append(medianOfInstantaneousTBF)
    
    
    
    elif parameterToCalculate == 'maxBendAmplitude':
      
      if "Bend_Amplitude" in curbout and type(curbout["Bend_Amplitude"]) == list and len(curbout["Bend_Amplitude"]):
        maxBendAmplitude = max(list(map(abs, curbout["Bend_Amplitude"]))) * (180 / math.pi)
      else:
        maxBendAmplitude = float('NaN')
      listOfParametersCalculated.append(maxBendAmplitude)
    
    
    
    elif parameterToCalculate == 'medianBendAmplitude':
      
      if "Bend_Amplitude" in curbout and type(curbout["Bend_Amplitude"]) == list and len(curbout["Bend_Amplitude"]):
        medianBendAmplitude = np.median(list(map(abs, curbout["Bend_Amplitude"]))) * (180 / math.pi)
      else:
        medianBendAmplitude = float('NaN')
      listOfParametersCalculated.append(medianBendAmplitude)
    
    
    
    elif parameterToCalculate == 'meanBendAmplitude':
      
      if "Bend_Amplitude" in curbout and type(curbout["Bend_Amplitude"]) == list and len(curbout["Bend_Amplitude"]):
        meanBendAmplitude = np.mean(list(map(abs, curbout["Bend_Amplitude"]))) * (180 / math.pi)
      else:
        meanBendAmplitude = float('NaN')
      listOfParametersCalculated.append(meanBendAmplitude)
    
    
    
    elif parameterToCalculate == 'maxTailAngleAmplitude':
      
      if "TailAngle_smoothed" in curbout and len(curbout["TailAngle_smoothed"]):
        maxAmplitude = max([abs(ta) for ta in curbout["TailAngle_smoothed"]]) * (180 / math.pi)
      else:
        if "TailAngle_Raw" in curbout and len(curbout["TailAngle_Raw"]):
          maxAmplitude = max([abs(ta) for ta in curbout["TailAngle_Raw"]]) * (180 / math.pi) # Maybe this value should be "reduced" in some way to be consistent with the previous smoothed tail angle
        else:
          maxAmplitude = float('NaN')
      listOfParametersCalculated.append(maxAmplitude)



    elif parameterToCalculate == 'binaryClass25degMaxTailAngle': # Kind of a hack again as it relies on maxAmplitude having been calculated previously
      
      if maxAmplitude != float('NaN'):
        binaryClass25degMaxTailAngle = 0 if maxAmplitude <= 25 else 1
      else:
        binaryClass25degMaxTailAngle = float('NaN')
        
      listOfParametersCalculated.append(binaryClass25degMaxTailAngle)    
    
    
    
    elif parameterToCalculate == 'deltaHead':
      
      deltahead  = abs(getDeltaHead(curbout))
      listOfParametersCalculated.append(deltahead)
    
    
    
    elif parameterToCalculate == 'xstart':
      
      posX = curbout["HeadY"]
      if len(posX) >= 1:
        xstart = posX[0] * pixelSize
      else:
        xstart = 0
      listOfParametersCalculated.append(xstart)
    
    
    
    elif parameterToCalculate == 'xend':
      
      posX = curbout["HeadX"]
      if len(posX) >= 1:
        xend = posX[len(posX)-1] * pixelSize
      else:
        xend = 0
      listOfParametersCalculated.append(xend)
    
    
    
    elif parameterToCalculate == 'xmean':
      
      posX = curbout["HeadX"]
      if len(posX) >= 1:
        xmean = np.mean(posX) * pixelSize
      else:
        xmean = 0
      listOfParametersCalculated.append(xmean)



    elif parameterToCalculate == 'ymean':
      
      posY = curbout["HeadY"]
      if len(posY) >= 1:
        ymean = np.mean(posY) * pixelSize
      else:
        ymean = 0
      listOfParametersCalculated.append(ymean)      
    
    
    
    elif parameterToCalculate == 'firstBendTime':
    
      if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list and len(curbout["Bend_Timing"]):
        firstBendTime = curbout["Bend_Timing"][0] / fps
      else:
        firstBendTime = float('NaN')  
      listOfParametersCalculated.append(firstBendTime)
    
    
    
    elif parameterToCalculate == 'firstBendAmplitude':
      
      if "Bend_Amplitude" in curbout and type(curbout["Bend_Amplitude"]) == list and len(curbout["Bend_Amplitude"]):
        firstBendAmplitude = abs(curbout["Bend_Amplitude"][0]) * (180 / math.pi)
      else:
        firstBendAmplitude = float('NaN')
      listOfParametersCalculated.append(firstBendAmplitude)
    
    
    
    elif parameterToCalculate == 'IBI':
      
      IBI = (curbout["BoutStart"] - previousBoutEnd) / fps
      listOfParametersCalculated.append(IBI)
    
    

    elif parameterToCalculate == 'BoutFrameNumberStart':
      
      BoutFrameNumberStart = curbout["BoutStart"]
      listOfParametersCalculated.append(BoutFrameNumberStart)
    
    
    
    else:
      
      print("The parameter", parameterToCalculate, "is not specified")
      break;
      
    # elif parameterToCalculate == '':
      # listOfParametersCalculated.append()
  
  return listOfParametersCalculated