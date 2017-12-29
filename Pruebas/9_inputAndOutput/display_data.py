from pandas import read_csv
from IPython.display import display

students = read_csv('../../sample_data/sample_student_data.csv',
	skiprows=[1], index_col=0)

#print(students.keys())
display(students)

headers = ["X", "Y"]
unlabelled = read_csv('../../sample_data/noHeader_noIndex_vert.csv',
	names=headers)

#display(unlabelled)


large_set = read_csv('../../sample_data/country_codes.csv')
#display(large_set)
#print(large_set.head(3))

#print(students.iloc[4,3], end='\n\n') 
'''
print(students.iloc[1, 2], end='\n\n')  
print(students.iloc[2, 3], end='\n\n')  
print(students.iloc[3, 4], end='\n\n')  
print(students.iloc[0],    end='\n\n')  
'''
#print(students.iloc[:, 3].head(), end='\n\n')  # all height data (first 5 entries)
print(students.loc['JW-1'], end='\n\n')