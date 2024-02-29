import os
import pandas as pd
import sys

root="/nfs5/BPP/Liston_Lab/workspace/kurowski/fritillaria/REoutput/"
goodfolders = ['JW_FRAF/','JW_FRGE/','JW_FRRE/','MG_FRAF/','MG_FRRE/','MG_FRGE','PR_FRRE/','PR_FRGE/','PR_FRAF/','NRR_FRAF/','NRR_FRGE/','NRR_FRRE/']
results= {}

with open('output.txt', 'w') as file:
	sys.stdout = file
	for folder in goodfolders:
		folderpath = os.path.join(root, folder)
		if os.path.isdir(folderpath):
			csvfilepath = os.path.join(folderpath,"CLUSTER_TABLE.csv")
			totalreadsdf = pd.read_csv(csvfilepath, sep="\t", header=None, nrows=5)
			totalreadsvalue = totalreadsdf.iloc[4,1]	
			df = pd.read_csv(csvfilepath, sep="\t", skiprows=6, header=0)
			result = df.groupby("Automatic_annotation")['Size'].sum().reset_index()
			result['Proportion'] = (result['Size'] / totalreadsvalue) * 100	
			results[folder] = result	
	



	for folder, result in results.items():
		print(folder)
		print(result)	
	sys.stdout = sys.__stdout__	
