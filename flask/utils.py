import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from scipy import stats
from scipy.signal import find_peaks


SR_lifetime = 158288793.025
SR_avg_process_time = 1232.63

SL_lifetime = 31650 
SL_avg_process_time = 1222.44


# In[3]:


def blank_df():
    df_blank = pd.read_csv("Book1.csv",header = None, decimal = ',', skiprows = range(0,8), delimiter = ';', names = ["time", "DrehmomentX", "DrehmomentY", "DrehmomentZ","DrehmomentS1",
                                        "GeschwindigkeitX", "GeschwindigkeitY", "GeschwindigkeitZ", "GeschwindigkeitS1", 
                                        "LageistwertX", "LageistwertY", "LageistwertZ", 
                                        "Wirkleistung", "Trigger", "Trigger2", "Zählen", "BearbeitungsvorschubK1",
                                        "WerkzeugeinsatzK1", "Zählwert", "Nacharbeit", "Alarme Aus", "Lernen", "AchseK1",
                                        "Override-Wert", "Programmnummer", "Werkzeugnummer", "Werkzeug-Typ", "Bearbeitungsnummer",
                                        "Schneidennummer", "Quellkanal", "Programm", "Bearbeitung", "Werkzeug", "ID", "AchseK2",
                                        "AchseK3", "AchseK4", "AchseK5", "AchseK6", "AchseK7", "AchseK8", "AchseK9", "AchseK10",
                                        "AchseK11", "AchseK12", "Gef.DrehmomentS1", "Testwert0S1", "Gef.DrehmomentZ", "Testwert1Z"] ,encoding = "ISO-8859-1")

    df_blank = df_blank.iloc[:,[0,1,2,3,9,10,11]]
    return df_blank

def more_possible_processes(lifetime, runtime, avg_process_time):
    no_of_processes = np.floor((lifetime - runtime))
    return no_of_processes

