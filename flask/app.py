from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from utils import *
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET','POST'])
def predict():

    process = request.form['a']
    k = int(request.form['b'])
    i = int(request.form['c'])

    if process == 'SR':
        lifetime = SR_lifetime
    elif process == 'SL':
        lifetime = SL_lifetime    

    # print(type(k))
    df_blank = blank_df()

    final = df_blank.copy()    
    # process = 'SR'
    #data1 = np.array((type(l),type(k),type(i)))
    for j in range(1,i+1): #loop for number of usages
        df = pd.read_csv("data/{}_{}_{}.csv".format(j,str(k).zfill(3),process),header = None, decimal = ',', skiprows = range(0,8), delimiter = ';', names = ["time", "DrehmomentX", "DrehmomentY", "DrehmomentZ","DrehmomentS1",
                                    "GeschwindigkeitX", "GeschwindigkeitY", "GeschwindigkeitZ", "GeschwindigkeitS1", 
                                    "LageistwertX", "LageistwertY", "LageistwertZ", 
                                    "Wirkleistung", "Trigger", "Trigger2", "Zählen", "BearbeitungsvorschubK1",
                                    "WerkzeugeinsatzK1", "Zählwert", "Nacharbeit", "Alarme Aus", "Lernen", "AchseK1",
                                    "Override-Wert", "Programmnummer", "Werkzeugnummer", "Werkzeug-Typ", "Bearbeitungsnummer",
                                    "Schneidennummer", "Quellkanal", "Programm", "Bearbeitung", "Werkzeug", "ID", "AchseK2",
                                    "AchseK3", "AchseK4", "AchseK5", "AchseK6", "AchseK7", "AchseK8", "AchseK9", "AchseK10",
                                    "AchseK11", "AchseK12", "Gef.DrehmomentS1", "Testwert0S1", "Gef.DrehmomentZ", "Testwert1Z"] ,encoding = "ISO-8859-1")
        df = df.iloc[:,[0,1,2,3,5,6,7,9,10,11]]
        final = pd.concat([final, df], ignore_index = True)
    runtime = len(final) * 0.01

    p = more_possible_processes(lifetime, runtime, SR_avg_process_time)

    data1 = np.array((k,process,p,p/60))

    if p > 0:
        status = "OK"
    else: status = "NOT OK"

    value = {
        "prediction":{
        "healthInMinutes": p/60,
        "healthInSeconds": p,
        "healthCheck": status
         }
    }
    #return render_template('result.html', data = data1)
    return json.dumps(value)

@app.route('/modify')
def modify(process_name, times_used_before, times_used_after):
    with open( 'utils.py') as f :
        lines = f.readlines()
    
    if process_name == "SR":
        new_lifetime = (times_used_before + times_used_after) * SR_avg_process_time
        avg_lifetime = (new_lifetime + SR_lifetime)/2
        lines[9] = 'SR_lifetime = '+ str(avg_lifetime) + '\n'
    elif process_name == "SL":
        new_lifetime = (times_used_before + times_used_after) * SL_avg_process_time
        avg_lifetime = (new_lifetime + SL_lifetime)/2
        lines[12] = 'SL_lifetime = '+ str(avg_lifetime) + '\n'
        
    lines = "".join(lines)
    with open( 'utils.py','w') as f :
        f.write(lines)
        f.close()

    

if __name__ == "__main__":
    app.run(port = 7776, debug= True)
