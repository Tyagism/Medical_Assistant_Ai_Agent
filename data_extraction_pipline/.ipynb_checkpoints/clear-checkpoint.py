import json, os
os.chdir(r"C:\Users\Harshit\Desktop\data_extraction_pipline")
a=json.load(open("structured_allergy_data.csv","r",encoding="utf-8"))
print("Total records:", len(a))
import pprint
pprint.pprint(a[:3])