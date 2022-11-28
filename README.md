# Enterprise_project

To uncpmpress pickle data: df = pd.read_pickle(path, compression='zip')
 
preprocessing --> preprocess.py   #includes all functions required for cleaning the data

Final version --> see the folder named "Flask".

The directory is organized as follows.

1. data: It contains data files that will be used when user enters tool number, numberof times used and process name (SL/SR).
2. templates: It contains html templates used for 3 purposes. 
              1. home: The starting webpage to enter input data.
              2. modifyconstants: This is used when user wants to update the maximum runtime constants.
              3. result: This template is used to show output result.
3. Book1.csv: This is necessary file as it is used to append multiple data files of one tool. Do not change or update this file.
4. app.py: This is the most important file which conatains all APIs which will be called at various endpoints. You can find all code with logic in each APIs.
5. utils.py: This file contains all predetermined constants which will be used in prediction. Eg. If user updates the maximum runtime, then it gets updated in this file.
