import pandas as pd
from os import listdir, remove
from os.path import isfile, join
from result_downloader import Result_Downloader
import pandas
from result_parser import Result_Parser

results_directory = "/home/tnzl/work/UP_Board_Result_Maker_2021/up_results/results/"
roll_no_file = "/home/tnzl/Downloads/roll number list.xlsx"
driver_path = '/home/tnzl/Downloads/geckodriver'

df = pandas.read_excel(roll_no_file)
df[df.columns[0]] = df[df.columns[0]].astype(int)
df = df.set_index(df.columns[0])
roll_nos = df.index[:3]

rd = Result_Downloader(results_directory, driver_path)
rp = Result_Parser(results_directory)

df_result = pd.DataFrame()

for roll_no in roll_nos:
    roll_no = str(roll_no)
    print("Downloading for " + roll_no+ "....", end="")
    try:
        rd.downloadResult(roll_no)
        result = rp.get_result(roll_no)
        df_result = df_result.append(result, ignore_index = True)
        remove(results_directory + roll_no + ".csv")
        
        df['Status'][int(roll_no)] = "Done"
        print("successful!")
    
    except Exception as e: 
        print("failed!!!")
        print("Exception" + e)
        df['Status'][int(roll_no)] = "Error"
        
df.to_excel(join(results_directory, "Download results.xlsx"))
print("Download results saved.") 
df_result.to_excel(join(results_directory, "Result.xlsx"))
print("Final Result saved.")

rd.close()
