import pandas as pd
import os
import requests


class CitiesExtractor:
    
    def __init__(self,file):
        self.file = file 
        
    def extactor(self):
        df = pd.read_csv(self.file)
        return df
    
    def save_to_bronze(self,data):

        out_path = "data/bronze/cities.csv"
        os.makedirs("data/bronze",exist_ok=True)

        data.to_csv(out_path,index=False)
        
        
exct = CitiesExtractor("ma.csv")
    
df = exct.extactor()
#print(df)

exct.save_to_bronze(df)

