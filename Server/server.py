
import base64
import io
import time
from io import BytesIO

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from flask import Flask, request, Response
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model
from Server.runGraphs import mkGraphs
from Supports.Support_Functions import nanoMeter_to_Meter, microMeter_to_Meters, toMHz

matplotlib.use('Agg')
app = Flask(__name__)


@app.route('/api/plot', methods=['POST'])
def get_query_from_react():

    Error_msg = ""
    successful = True

    try:

        data = request.get_json()['data']


        StartFreq = toMHz(float(data['StartFreq']))
        EndFreq = toMHz(float(data['EndFreq']))
        resolution = int(data['resolution'])


        Er = float(data['Er'])
        H = nanoMeter_to_Meter(float(data['H']))
        Jc = float(data['Jc'])
        Pn = float(data['Pn'])
        Tc = float(data['Tc'])
        Temp = float(data['Temp'])
        Tg = nanoMeter_to_Meter(float(data['Tg']))
        Ts = nanoMeter_to_Meter(float(data['Ts']))
        tand = float(data['tand'])

        # Wl = microMeter_to_Meters(float(data['Wl']))
        # Wu = microMeter_to_Meters(float(data['Wu']))
        # D = microMeter_to_Meters(float(data['D'])))
        # D0 = microMeter_to_Meters(float(data['D0']))
        # D1 = microMeter_to_Meters(float(data['D1']))
        # D2 = microMeter_to_Meters(float(data['D2']))
        # D3 = microMeter_to_Meters(float(data['D3']))
        # threeLoads = data['threeLoads']
        #
        # Aii = float(data['Aii'])
        # Api = float(data['Api'])
        # Asi = float(data['Asi'])
        # pumpF = float(data['pumpF'])




    except:

        inputFailure = ["todo"]
        Error_msg = f"failure to read input(s): {inputFailure}"
        successful = False



    # ---------------------------- unit cell inputs from paper
    unit_Cell_Len = microMeter_to_Meters(2300)
    l1 = microMeter_to_Meters(50)
    width_unloaded = microMeter_to_Meters(1.49)
    a = 1.2
    b = 2

    # ---------------------------- SC inputs

    if successful:
        try:
            mkGraphs(unit_Cell_Len, l1, width_unloaded, a, b, Er, H, Ts, Tg,
                 Tc, Pn, tand, Temp,StartFreq, EndFreq, resolution)
        except:
            successful = False

    return {
            "successful":successful,
            "Error_msg":Error_msg
            }


if __name__ == "__main__":
    app.run(debug=True)
