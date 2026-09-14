import pandas as pd
import requests


class CitiesExtractor:
    
    def __init__(self,file):
        self.file = file
        
        
    def extract(self):
       df =  pd.read_csv(self.file)
       return df 
    
    
exct = CitiesExtractor("ma.csv")

df = exct.extract()
print(df)