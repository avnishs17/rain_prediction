import joblib
from flask import Flask,render_template,request,jsonify
import numpy as np

app = Flask(__name__)

MODEL_PATH = "artifacts/models/model.pkl"
model = joblib.load(MODEL_PATH)


FEATURES = [
    'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
       'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
       'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
       'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
       'Temp3pm', 'RainToday', 'Year', 'Month', 'Day'
]

LABELS = {0 : "NO" , 1: "YES"}

# Field information for user guidance
FIELD_INFO = {
    'Location': {'type': 'select', 'description': 'Weather station location', 'example': 'Adelaide (0), Albany (1), Albury (2), etc.', 'range': '0-48'},
    'MinTemp': {'type': 'number', 'description': 'Minimum temperature', 'example': '13.4', 'range': '-8.5 to 33.9°C', 'unit': '°C'},
    'MaxTemp': {'type': 'number', 'description': 'Maximum temperature', 'example': '22.9', 'range': '7.4 to 48.1°C', 'unit': '°C'},
    'Rainfall': {'type': 'number', 'description': 'Amount of rainfall', 'example': '0.6', 'range': '0.0 to 371.0mm', 'unit': 'mm'},
    'Evaporation': {'type': 'number', 'description': 'Pan evaporation', 'example': '5.4', 'range': '0.0 to 145.0mm', 'unit': 'mm'},
    'Sunshine': {'type': 'number', 'description': 'Hours of sunshine', 'example': '10.9', 'range': '0.0 to 14.5 hours', 'unit': 'hours'},
    'WindGustDir': {'type': 'select', 'description': 'Wind gust direction', 'example': 'W (0), WNW (1), WSW (2), etc.', 'range': '0-15'},
    'WindGustSpeed': {'type': 'number', 'description': 'Wind gust speed', 'example': '44', 'range': '6 to 135 km/h', 'unit': 'km/h'},
    'WindDir9am': {'type': 'select', 'description': 'Wind direction at 9am', 'example': 'W (0), WNW (1), WSW (2), etc.', 'range': '0-15'},
    'WindDir3pm': {'type': 'select', 'description': 'Wind direction at 3pm', 'example': 'WNW (0), WSW (1), etc.', 'range': '0-15'},
    'WindSpeed9am': {'type': 'number', 'description': 'Wind speed at 9am', 'example': '20', 'range': '0 to 130 km/h', 'unit': 'km/h'},
    'WindSpeed3pm': {'type': 'number', 'description': 'Wind speed at 3pm', 'example': '24', 'range': '0 to 87 km/h', 'unit': 'km/h'},
    'Humidity9am': {'type': 'number', 'description': 'Humidity at 9am', 'example': '71', 'range': '0 to 100%', 'unit': '%'},
    'Humidity3pm': {'type': 'number', 'description': 'Humidity at 3pm', 'example': '22', 'range': '0 to 100%', 'unit': '%'},
    'Pressure9am': {'type': 'number', 'description': 'Atmospheric pressure at 9am', 'example': '1007.7', 'range': '980.5 to 1041.0 hPa', 'unit': 'hPa'},
    'Pressure3pm': {'type': 'number', 'description': 'Atmospheric pressure at 3pm', 'example': '1007.1', 'range': '977.1 to 1039.6 hPa', 'unit': 'hPa'},
    'Cloud9am': {'type': 'number', 'description': 'Cloud amount at 9am', 'example': '8', 'range': '0 to 8 oktas', 'unit': 'oktas'},
    'Cloud3pm': {'type': 'number', 'description': 'Cloud amount at 3pm', 'example': '0', 'range': '0 to 8 oktas', 'unit': 'oktas'},
    'Temp9am': {'type': 'number', 'description': 'Temperature at 9am', 'example': '16.9', 'range': '-7.2 to 39.4°C', 'unit': '°C'},
    'Temp3pm': {'type': 'number', 'description': 'Temperature at 3pm', 'example': '21.8', 'range': '2.1 to 46.7°C', 'unit': '°C'},
    'RainToday': {'type': 'select', 'description': 'Did it rain today?', 'example': 'No (0), Yes (1)', 'range': '0 or 1'},
    'Year': {'type': 'number', 'description': 'Year', 'example': '2017', 'range': '2008 to 2017', 'unit': ''},
    'Month': {'type': 'number', 'description': 'Month', 'example': '12', 'range': '1 to 12', 'unit': ''},
    'Day': {'type': 'number', 'description': 'Day of month', 'example': '1', 'range': '1 to 31', 'unit': ''}
}

@app.route("/" , methods=["GET" , "POST"])
def index():
    prediction = None
    error_message = None

    if request.method=="POST":
        try:
            input_data = [float(request.form[feature]) for feature in FEATURES]
            input_array = np.array(input_data).reshape(1,-1)

            pred = model.predict(input_array)[0]
            prediction = LABELS.get(pred, 'Unknown')
            print(prediction)

        except ValueError as e:
            error_message = "Please enter valid numeric values for all fields."
            print(f"ValueError: {e}")
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(str(e))
    
    return render_template("index.html", 
                         prediction=prediction, 
                         features=FEATURES, 
                         field_info=FIELD_INFO,
                         error_message=error_message)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = [float(request.form[feature]) for feature in FEATURES]
        input_array = np.array(input_data).reshape(1,-1)

        pred = model.predict(input_array)[0]
        prediction = LABELS.get(pred, 'Unknown')
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'message': f'Tomorrow it will {"rain" if prediction == "YES" else "not rain"}!'
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': "Please enter valid numeric values for all fields.",
            'details': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}",
            'details': str(e)
        })

if __name__=="__main__":
    app.run(debug=True , port=5000 , host="0.0.0.0")
