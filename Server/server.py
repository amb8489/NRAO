from flask import Flask, request
from Server.runGraphs import mkGraphs
from Utills.Functions import nanoMeters_to_Meters, microMeters_to_Meters, toGHz, microMeters_to_Meters, \
    nanoMeters_to_Meters

app = Flask(__name__)


@app.route('/api/plot', methods=['POST'])
def get_query_from_react():
    Error_msg = "None"
    successful = True

    try:

        data = request.get_json()['data']

        StartFreq = toGHz(float(data['StartFreq']))
        EndFreq = toGHz(float(data['EndFreq']))
        resolution = int(data['resolution'])

        Er = float(data['Er'])
        H = nanoMeters_to_Meters(float(data['H']))
        Jc = float(data['Jc'])
        Pn = float(data['Pn'])
        Tc = float(data['Tc'])
        Temp = float(data['Temp'])
        Tg = nanoMeters_to_Meters(float(data['Tg']))
        Ts = nanoMeters_to_Meters(float(data['Ts']))
        tand = float(data['tand'])

        # Wl = microMeter_to_Meters(float(data['Wl']))
        # Wu = microMeter_to_Meters(float(data['Wu']))
        # threeLoads = data['threeLoads']

        # D = microMeter_to_Meters(float(data['D'])))
        # D0 = microMeter_to_Meters(float(data['D0']))
        # D1 = microMeter_to_Meters(float(data['D1']))
        # D2 = microMeter_to_Meters(float(data['D2']))
        # if threeLoads == "TRUE":
        #     D3 = microMeter_to_Meters(float(data['D3']))
        #
        # Aii = float(data['Aii'])
        # Api = float(data['Api'])
        # Asi = float(data['Asi'])
        # pumpF = float(data['pumpF'])




    except:
        print("failure on inputs")
        inputFailure = ["todo"]
        Error_msg = f"failure to read input(s): {inputFailure}"
        successful = False

    graphData = {}

    # ------ START remove later in replacement of user input
    unit_Cell_Len = microMeters_to_Meters(2300)
    width_unloaded = microMeters_to_Meters(1.49)
    width_loaded = width_unloaded * 1.2

    D0 = .0007666666666666666666
    D1 = 5e-5
    D2 = 5e-5
    D3 = .0001
    loads_Widths = [D1, D2, D3]

    # ---------------------------- SC inputs
    er = 10
    Height = nanoMeters_to_Meters(250)
    line_thickness = nanoMeters_to_Meters(60)
    Tc = 14.28
    T = 0
    pn = 1.008e-6
    tanD = 0
    Jc = 1
    # ------ END remove later in replacement of user input

    if successful:
        try:
            graphData = mkGraphs(StartFreq, EndFreq, resolution, unit_Cell_Len, D0, loads_Widths, width_unloaded,
                                 width_loaded, er,
                                 Height, line_thickness, Tc, pn, tanD, T, Jc)
        except:
            Error_msg = "failed on run to do error message"
            successful = False

    # opt compact data with groupby() kinda
    # opt adaptive sampling algo to speend up and mk graphs better
    return {
        "successful": successful,
        "Error_msg": Error_msg,
        "GraphData": graphData
    }


if __name__ == "__main__":
    app.run(debug=True)
