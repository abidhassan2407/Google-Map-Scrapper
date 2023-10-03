import pandas as pd
import glob

# df = pd.read_csv('./output_files/Bandarban_Lama_Lama Paurashava.csv')

files = glob.glob('./output_files/*.csv')


for f in files:
    print(f)
    df = pd.read_csv(f)

    df.drop_duplicates(subset=None,keep='first',inplace=True)

    df.to_csv(f,index=False)