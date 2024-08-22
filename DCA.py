import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import re
#Domain knowledge about your dataset is highly recommended before you use this algorithm
#Assumes that your csv file as a single row of defined header (starting point, titles/headers is first row)


print('Welcome To OCDC by @AyFait')
#Copy your csv filepath here
cleanedFilepath = '/home/a0x0bc1/Downloads/TitanictrainCleaned.csv'#where you want to export the output
#filepath = '/home/a0x0bc1/Downloads/CMC_24h_Gainers_Starting_07_10_24 mod.csv'
filepath = '/home/a0x0bc1/Downloads/Titanictrain.csv'#your input filepath here

#Initializing root Tkinter and hiding it
def selectFile():
    pass
    #loadFile = input('Press Enter to select and load your csv file...')
    #root = tk.Tk()
    #root.withdraw()
    ##Prompt to select file
    #filepath = filedialog.askopenfilename(
    #    title = 'Select your csv file',
    #    filetypes=[('CSV files', '*.csv'),
    #    ('Excel files', '*.xls; *.xlsx')]
    #)
    #return filepath

#To fill empty cells
def fillNullCells(workingCol):
    workingCol = pd.to_numeric(workingCol, errors='coerce')
    if pd.isna(workingCol.iloc[0]):#Probably first cell in col is empty
        colMedian = workingCol.median()
        workingCol.iloc[0] = colMedian#interpolate doesnt fill the first cell id its empty so need to fill manually
    workingCol.fillna(workingCol.interpolate(), inplace=True)#Using interpolate as it is best fit for time series data
    #print(workingCol)
    return workingCol

#To turn alphabets to lowercase
def turnAlphaLower(workingCol):
    for idx, elmt in enumerate(workingCol):#itrs over each elmt in a single col 
        if pd.isna(elmt): #skips an empty cell
            continue
        try: #To avoid float * isalpha * str * strip errors when there are empty cells in the col
            #elmt = re.sub('[^a-zA-Z0-9]+', '', str(elmt))#remove all whitespaces and special characters that negates alphabets or numbers from each elmt, no need for 'str'
            elmt = re.sub('[^a-zA-Z0-9]+', '', elmt)#remove all other chars apart from alphas and nums
            try: #To catch errors that will come from values other than numbers
                floatelmt = float(elmt)
            except: #Then value is str or unknown, i.e mix of chars
                if not elmt.isalpha() and  not elmt.isalnum():#If value tossed here is not an alphabet and not alphanumeric
                    csvFile.at[idx, col] = np.nan
                else:
                    csvFile.at[idx, col] = elmt.lower() #return the elmt in lowercase without spaces 
        except:
            continue #skip the empty cell
    return workingCol

#To map each nonnumerical elemt to a num for categorical col
def mapElmtToNum(workingCol):
    nonNum = []
    for idx, elmt in enumerate(workingCol):#itrs over each elmt in a single col 
        if pd.isna(elmt): #skips an empty cell
            continue
        try:
            elmt = re.sub('[^a-zA-Z0-9]+', '', elmt)#remove all other chars apart from alphas and nums
            try: #Try to get nums are included in the col
                floatelmt = float(elmt)
            except: #Then value is str or unknown, i.e mix of chars
                nonNum.append(elmt)
        except:
            continue
    nonNum = pd.unique(pd.Series(nonNum))
    #If nums are included in the col, we need the max 
    startNum = pd.to_numeric(workingCol, errors='coerce').max()+1#Trying to get max num in the col, turning all num to float and nonnum to nan
    if pd.isna(startNum):#All the values are probably alphabets
        startNum = 1
        mapped = {val: idx for idx, val in enumerate(nonNum, start=int(startNum))}
        workingCol = workingCol.map(lambda elmt: mapped.get(elmt, elmt))
    else: #Then there are nums
        mapped = {val: idx for idx, val in enumerate(nonNum, start=int(startNum))}
        workingCol = workingCol.map(lambda elmt: mapped.get(elmt, elmt))
    workingCol = pd.to_numeric(workingCol, errors='coerce')
    workingCol = fillNullCells(workingCol)
    return workingCol
    
#To determine for categorical col
def isCategorical(workingCol):
    numValues = sum(workingCol.isna() == False)#Total num of vals in the col
    numUniks = workingCol.nunique()#Total num of unique vals
    numTwiceUniques = sum(workingCol.value_counts() >= 2)#Total num of vals that reapeat atb least twice
    #print(workingCol.value_counts()) # To get a view of the freq of each val

    #Using at least one value must repeat atleast twice
    if numTwiceUniques >= 1:
        return True

    #Using max 60% should be unique threshold
    #isCat = (numUniks / numValues) #The ratio of unique vals to total vals
    #print(isCat)
    #if isCat <= 0.6:
        #return True

    #Using 60% of unique should repeat at least twice threshold
    #isCat2 = (0.6 * numUniks)#preferred ratio
    #print(isCat2)
    #if isCat2 <= numTwiceUniques:
        #return True

    #OR
    #if (numTwiceUniques / numUniks) >= 0.4:
    #    return True
    
    else:
        return None #This col is not cleaned

#To map Categorical vals to num
def mapCategorical(workingCol):
    if isCategorical(workingCol) is True:
        #Turn to categorical
        workingCol = turnAlphaLower(workingCol)
        workingCol = mapElmtToNum(workingCol)
        return workingCol

    else:
        return None #This col is not cleaned

#To clean a num col mixed with other chars
def cleanObjNumericalCol(workingCol):
    numUniks = workingCol.nunique()
    numValues = sum(workingCol.isna() == False)
    if isCategorical(workingCol):
        return True
    elif numUniks >= 0.6 * numValues:#To check if the col is not categorical i.e. not repeated values
        for idx, elmt in enumerate(workingCol):#itrs over each elmt in a single col 
            if pd.isna(elmt): #skips an empty cell
                continue
            elmt = re.sub('[^a-zA-Z0-9]+', '', elmt)#remove all other chars apart from alphas and nums
            try:
                floatelmt = float(elmt)
            except:
                csvFile.at[idx, col] = np.nan
        #workingCol = pd.to_numeric(workingCol, errors='coerce')
        workingCol = fillNullCells(workingCol)
        return workingCol
    else:
        return None

#To count each elmt in each col
def countObjsCol(workingCol):
    strCount = 0
    alphanumericCount = 0
    numCount = 0
    emptyCount = 0
    unknownCount = 0
    #for elmt in csvFile[col]:#itrs over each elmt in a single col
    
    for idx, elmt in enumerate(workingCol):#itrs over each elmt in a single col 
        if pd.isna(elmt): #skips an empty cell
            emptyCount += 1
            continue
        try: #To avoid float * isalpha * str * strip errors when there are empty cells in the col
            elmt = re.sub('[^a-zA-Z0-9]+', '', elmt)#remove all other chars apart from alphas and nums ONLY from each elmt
            if elmt.isalpha():#Checks if each elmt is an alphabet
                strCount += 1
                #print(elmt)#prints the alphabetical elmt
            
            else:
                try: #To catch errors that will come from values other than numbers
                    floatnum = float(elmt)
                    numCount += 1
                except:
                    if elmt.isalnum():#For alphanum chars
                        alphanumericCount += 1 
                    else:
                        unknownCount += 1 #Then value is unknown, i.e mix of chars 
                    continue #skip the value
                
        except:
            continue #skip the empty cel
    return strCount, alphanumericCount, numCount, emptyCount, unknownCount



#filepath = selectFile()
#Affirm selection
if filepath:
    print('Selected File: ', filepath)

else:
    print('No file has been selected!')

csvFile = pd.read_csv(filepath)
print(csvFile.dtypes)#prints datatypes for each col
print(type(csvFile))#prints <class 'pandas.core.frame.DataFrame'>
noInputCols = len(csvFile.columns)
print(f'Total of {noInputCols} input cols')
#print(csvFile.head(5))
while True:
    try:
        choice = int(input(f"Select: \n 1: For Quick Clean \n 2: To Edit Your Parameters \n"))
        if choice == 1:
            #Main Prog
            #Main Operation
            newCols = []
            deletedCols = []
            for col in csvFile.columns:#itrs over all cols at once, but a single col with index def
                #pass
                #print(csvFile[col]) #Prints the current col
                workingCol = csvFile[col]
    
                if csvFile[col].dtype == int: #Its perfect
                    newCols.append(col)
                    continue
                
                elif csvFile[col].dtype == float: #Might need fixing
                    strCount, alphanumericCount, numCount, emptyCount, unknownCount = countObjsCol(workingCol)
                    if emptyCount >= 0.4 * len(workingCol): #Probably almost all cells are empty
                        deletedCols.append(col)
                        csvFile.drop(col, axis=1, inplace=True)
                        #print(col)
                    else:
                        newCols.append(col)
                        csvFile[col] = fillNullCells(csvFile[col])
                        #print(csvFile[col])
    
    
                elif workingCol.dtype == object: #Checks for each cols first
                    strCount, alphanumericCount, numCount, emptyCount,  unknownCount = countObjsCol(workingCol)
                    values = strCount + alphanumericCount + numCount
    
                    #print(col)
                    #print('String: ', strCount)
                    #print('Alphanumeric: ', alphanumericCount)
                    #print('Nums: ', numCount)
                    #print('EmptyCells: ', emptyCount)
    
                    if numCount >= (0.8 * values):#Incase a numerical col is mixed with few other chars
                        #print(workingCol)
                        if cleanObjNumericalCol(csvFile[col]) is True:#means it's categorica. Can use if isCategorical(csvFile[col]) directly 
                            #print(col)
                            newCols.append(col)
                            csvFile[col] = mapCategorical(csvFile[col])
    
                        elif cleanObjNumericalCol(csvFile[col]) is None:
                            deletedCols.append(col)
                            csvFile.drop(col, axis=1, inplace=True)
                        else:
                            newCols.append(col)
                            csvFile[col] = cleanObjNumericalCol(csvFile[col])#Num col with some empty cells
                            #print(csvFile[col])
    
                    #This works well for cols with more alpha chars than the others
                    elif (strCount + alphanumericCount + numCount) >= (0.6 * len(workingCol)): #This ratio means cols is likely mixed up with invalid data
                        #To determine for Categorical col and then map
                        if isCategorical(csvFile[col]) is None:
                            deletedCols.append(col)
                            csvFile.drop(col, axis=1, inplace=True)#Means its not categorical so delete col
                        else:
                            newCols.append(col)
                            csvFile[col] = mapCategorical(csvFile[col])
                            #print(csvFile[col])
                            #print(col)#col name
    
                    else:
                        deletedCols.append(col)
                        #print(workingCol)
                        csvFile.drop(col, axis=1, inplace=True)#Means its not categorical so delete col
    
                else:
                    deletedCols.append(col)
                    csvFile.drop(col, axis=1, inplace=True)#Del any other col
    
            print(csvFile.dtypes)
            print()
            csvFile.to_csv(cleanedFilepath, index=False)
            noOutputCols = len(csvFile.columns)
            removedCols = noInputCols - noOutputCols
            print(f'Total of {noOutputCols} output cols: {newCols}')
            print()
            print(f'Total of {removedCols} cols removed: {deletedCols}')
            print()
            print(f'Cleaned Data Exported Successfully To {cleanedFilepath}')
            break

        else:
            print('Only option - 1 available for now')

    except ValueError:
        print('Wrong input, only input 1 or 2 as your selection!')

        

    