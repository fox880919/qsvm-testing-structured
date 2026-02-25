import os

import pandas as pd

from classes.parameters import MyParameters

class MyDataFrame:

    def formatData(self, scoreOfOriginal, scoreOfMutant, mutantNumber, typeOfMutant, tStatistic, pValue, nullHypothesisIsRejected, all_original_scores, all_mutant_scores, n_folds, featureMap, appliedMr, MrValue, startTime = '', endTime = ''):

        # myParameters = MyParameters()

        formattedData = {
                # 'Feature_Map': [MyParameters.featureMaps[usedParameters['featureMapType']]], 
                # 'Data_Type':[MyParameters.allDataTypes[usedParameters['dataType']]], 
                'Feature_Map': [MyParameters.featureMaps[MyParameters.featureMapType]],

                'Data_Type':[MyParameters.allDataTypes[MyParameters.dataType]],                 
                'Score_Of_Original': [scoreOfOriginal],
                'Score_Of_Mutant': [scoreOfMutant],

                'mutant_#': [mutantNumber],

                'type_of_mutant': [typeOfMutant],

                't_statistic': [tStatistic],
                'p_value': [pValue],

                'null_Hypothes_Is_Rejected': [nullHypothesisIsRejected],                  

                'All_Scores_Of_Original': [all_original_scores],
                'All_Scores_Of_Mutant': [all_mutant_scores],

                'n_fold': n_folds,
                'featureMap': [featureMap],
                'Applied_MR': [appliedMr],
                'Mr_Value': [MrValue],
    
                'start_time': [startTime],
                'end_time': [endTime],

                }
        
        return formattedData

    def formatMiniData(self, mutantNumber, MrNumber, value1, value2, inputNumber):

        # myParameters = MyParameters()

        formattedData = {
                

                'mutant_#': [mutantNumber],

                'mr_number': [MrNumber],
                'value_1': [value1],
                'value_2': [value2],
                'input_number': [inputNumber]
                }
        
        return formattedData

    def processToDataFrame(self, data):
        myDataFrame = pd.DataFrame(data)

        # don't use in testing
        MyDataFrame.saveDataFrame(myDataFrame)

    def processToMiniDataFrame(self, data):
        myDataFrame = pd.DataFrame(data)

        # don't use in testing
        MyDataFrame.saveMiniDataFrame(myDataFrame)


    def saveDataFrame(myDataFrame):

        # myDataFrame.index = myDataFrame.index + 1

        lastIndex = MyDataFrame.getDataIndex()

        filePath = MyDataFrame.getFilePath()

        # print('lastIndex: ', lastIndex)

        myDataFrame.index = range(lastIndex + 1, lastIndex + 1 + len(myDataFrame))

        # print('lastIndex: ', lastIndex)

        if lastIndex < 0: 
            myDataFrame.to_csv(filePath, mode='a', index=True, header = True)
        else:
            myDataFrame.to_csv(filePath, mode='a', index=True, header = False)
  
    def saveMiniDataFrame(myDataFrame):

        # myDataFrame.index = myDataFrame.index + 1

        lastIndex = MyDataFrame.getMiniDataIndex()

        filePath = MyDataFrame.getMiniFilePath()

        # print('lastIndex: ', lastIndex)

        myDataFrame.index = range(lastIndex + 1, lastIndex + 1 + len(myDataFrame))

        # print('lastIndex: ', lastIndex)

        if lastIndex < 0: 
            myDataFrame.to_csv(filePath, mode='a', index=True, header = True)
        else:
            myDataFrame.to_csv(filePath, mode='a', index=True, header = False)
  
    
    def getDataIndex():

            filePath = MyDataFrame.getFilePath()
            try:
                # Read the existing CSV file
                existingDataFrame = pd.read_csv(filePath)
                last_index = existingDataFrame.index[-1]  # Get the last index
            except FileNotFoundError:

                print
                # If the file doesn't exist, start from index 0
                last_index = -1  # Start from 0 for new data

            return last_index
            # return range(last_index + 1, last_index + 1 + len(new_df))

    def getMiniDataIndex():

            filePath = MyDataFrame.getMiniFilePath()
            try:
                # Read the existing CSV file
                existingDataFrame = pd.read_csv(filePath)
                last_index = existingDataFrame.index[-1]  # Get the last index
            except FileNotFoundError:

                print
                # If the file doesn't exist, start from index 0
                last_index = -1  # Start from 0 for new data

            return last_index
            # return range(last_index + 1, last_index + 1 + len(new_df))

    
    def getFilePath():

        current_directory = os.getcwd()  # Get the current working directory
        # print('current_directory: ', current_directory)

        # parent_directory = os.path.dirname(current_directory)  # Get the parent directory
        # print('parent_directory: ', parent_directory)

        # target_folder = os.path.join(parent_directory, 'saved_data') 
        
        target_folder = os.path.join(current_directory, 'saved_data')

         # Construct the target folder path
        # print('target_folder: ', target_folder)

        # savingFileName = MyParameters.getSavingFileName()
        
        # file_path = os.path.join(target_folder, MyParameters.savingFileName)
        file_path = os.path.join(target_folder, MyParameters.getSavingFileName())

        # print('file_path is:', file_path)

        return file_path
    
    def getMiniFilePath():

        current_directory = os.getcwd()  # Get the current working directory
        # print('current_directory: ', current_directory)

        # parent_directory = os.path.dirname(current_directory)  # Get the parent directory
        # print('parent_directory: ', parent_directory)

        # target_folder = os.path.join(parent_directory, 'saved_data') 
        
        target_folder = os.path.join(current_directory, 'saved_data')

         # Construct the target folder path
        # print('target_folder: ', target_folder)

        # savingFileName = MyParameters.getMiniSavingFileName()
        
        # file_path = os.path.join(target_folder, MyParameters.savingFileName)
        file_path = os.path.join(target_folder, MyParameters.getMiniSavingFileName())

        # print('file_path is:', file_path)

        return file_path
    
        
    #not used
    def getDataFrameByName(self, modelName):


        df = pd.read_csv('saved_data/my_dataframe.csv')

        filtered_row = df[df['Name'] == modelName]

        if not filtered_row.empty:
            
            return filtered_row
        
        else:

            print(f"No data found for the name: {modelName}")

    def getModelScoreValue(self, mr, value, kfoldIndex, nfold):

        extraDigit = ''

        if mr< 10:
            extraDigit = '0'

        dfFilteredRows = MyDataFrame.getDataFrameByParameters(mr, value, kfoldIndex, nfold)

        # modelName = 'saved_models/SVM' + extraDigit + str(mr) + '-' + str(value) + '-' + str(kfoldIndex) + '-of-' + str(nfold)

        # print('modelName: ', modelName)
        
        # print('len(dfFilteredRow): ', len(dfFilteredRows))

        # print('dfFilteredRow: ', dfFilteredRow)

        # print('Accuracy_Score: ', dfFilteredRows.iloc[0]['Accuracy_Score'])

        return dfFilteredRows.iloc[0]['Accuracy_Score']


    def getDataFrameByParameters(mr, value, kFoldIndex, nfold):

        mrColumnName = MyDataFrame.getColumnNameFromMr(mr)

        # print('mrColumnName: ', mrColumnName)

        # df = pd.read_csv('saved_data/my_dataframe.csv')
        df = pd.read_csv(f'saved_data/{MyParameters.savingFileName}')

        mr_condition = df[mrColumnName] == value

        nfold_condition = df['fold_index'] == kFoldIndex
        kfold_condition = df['n_fold'] == nfold

        combined_condition = mr_condition & kfold_condition & nfold_condition

        # combined_condition = mr_condition & kfold_condition & nfold_condition

        filtered_rows = df[combined_condition]
        
        # filtered_row = df[df['Name'] == modelName]

        if not filtered_rows.empty:
            
            return filtered_rows
        
        else:

            print(f"No data frame found for the parameters")


    
    def getColumnNameFromMr(mr):

        if mr == 0:
            return 'Used_Metamorphic'
        
        elif mr == 1:
            return 'Scalar_Value'    

        elif mr == 2:

            return 'Angle_Rotation'
        
        elif mr == 3:

            return 'Apply_Permutation'

        elif mr == 4:

            return 'Invert_Labels'

        elif mr == 5:

            return 'Perturb_Noise'

        


