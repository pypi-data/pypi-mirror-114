import csv
import pandas as pd
from os import listdir
from os.path import isfile, join

class Result_Parser:
  def __init__(self, result_path):
    self.result_path = result_path
  
  def get_result(self, roll_no):
    file = self.result_path + roll_no + ".csv"
    result = {}

    with open(file, "r") as infile:
      r = csv.reader(infile)
      D = list(r)
      row_count = len(D)
      result["Roll No"] = D[1][1]
  
      for i in range(2,7):
        result[D[i][0]] = D[i][1]
      
      result[D[15][0]] = D[15][1] 
      
      sum = 0
      for i in range(10,15):
        result[D[i][0]+'.theory'] = D[i][1]
        result[D[i][0]+'.practical'] = D[i][2]
        result[D[i][0]+'.total'] = D[i][3]
        result[D[i][0]+'.grade'] = D[i][4]
        if 'F' in D[i][3]:
          sum += int(D[i][3][:3])
        elif 'AAA' in D[i][3]:
          continue
        else:
          sum += int(D[i][3])
      
      result["Percentage"] = sum/6
    
    return result