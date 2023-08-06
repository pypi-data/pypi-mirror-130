import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from zebrazoom.dataAnalysis.dataanalysis.outputValidationVideo import outputValidationVideo
import cv2
import os
import shutil
import pickle

def generateValidationVideoForCluster(excelFileName, clusterNum, nbVideos, ZZoutputLocation=''):

  cur_dir_path = os.path.dirname(os.path.realpath(__file__))
  cur_dir_path = Path(cur_dir_path)
  cur_dir_path = cur_dir_path.parent
  
  if ZZoutputLocation == '':
    ZZoutputLocation = os.path.join(cur_dir_path.parent, 'ZZoutput')
  
  cur_dir_path = os.path.join(os.path.join(os.path.join(cur_dir_path, 'resultsClustering'), excelFileName), 'classifications.txt')
  
  classifications = pd.read_csv(cur_dir_path)
  
  clusterOfInterest = classifications[classifications['classification'] == clusterNum]
  
  clusterOfInterestWT  = classifications[classifications['Genotype'] == 'WT']
  clusterOfInterestMut = classifications[classifications['Genotype'] == 'Parkinson']
  
  
  length = 150

  out = cv2.VideoWriter(os.path.join(outputFolderResult, 'cluster' + str(clusterNum) + '.avi'), cv2.VideoWriter_fourcc('M','J','P','G'), 10, (length, length))
  indices = 
  nbTemp  = len(indices)
  if nbTemp < nbVideosToSave:
    nbVideosToSave = nbTemp
  
  pathToVideos = ''
  r = [i for i in range(0, nbVideosToSave)]
  for num in r:
    BoutStart = int(dfParam.loc[indices[num],'BoutStart'])
    BoutEnd   = int(dfParam.loc[indices[num],'BoutEnd'])
    Well_ID   = int(dfParam.loc[indices[num],'Well_ID'])
    Trial_ID  = dfParam.loc[indices[num],'Trial_ID']
    NumBout   = dfParam.loc[indices[num],'NumBout']
    out = outputValidationVideo(pathToVideos, Trial_ID, '.txt', Well_ID, NumBout, 1, BoutStart, BoutEnd, out, length, analyzeAllWellsAtTheSameTime, ZZoutputLocation)
  
  out.release()
  