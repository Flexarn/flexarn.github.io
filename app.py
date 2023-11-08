from flask import Flask, request, jsonify
from flask_cors import CORS  # Notera att det är flask_cors, inte flask


def format_number(num):
    if num.is_integer():
        return int(num)
    return num

def format_time(total_minutes):
    # Calculate hours, remaining minutes, and remaining seconds
    hours = int(total_minutes // 60)
    remaining_minutes = int(total_minutes % 60)
    remaining_seconds = round((total_minutes * 60) % 60)

    # Create the formatted time string
    if hours == 0:
        return f"{remaining_minutes} min {remaining_seconds} s"
    else:
        return f"{hours} h {remaining_minutes} min {remaining_seconds} s"


def calculate_pace(time_hours, time_minutes, time_seconds, total_distance_km):
    time_hours = int(time_hours)
    time_minutes = int(time_minutes)
    time_seconds = int(time_seconds)
    distance_dict = {
        'Marathon': 42.195,
        'Half Marathon': 21.0975,
        '100 miles': 160.9344,
        '50 miles': 80.4672,
        '1 mile': 1.609344,
        '2 miles': 3.218688,
    }

    original_distance_name = total_distance_km

    if total_distance_km in distance_dict:
        total_distance_km = distance_dict[total_distance_km]
    else:
        total_distance_km = float(total_distance_km)

    total_time_minutes = float(time_hours*60+time_minutes+time_seconds/60)

    if total_distance_km <= 0 or total_time_minutes <= 0:
        return {'error': 'Invalid input values'}

    pace_per_km = total_time_minutes / total_distance_km
    minutes = int(pace_per_km)
    seconds = round((pace_per_km - minutes) * 60)
    formatted_pace = f"{minutes}:{seconds:02d}"

    if original_distance_name in distance_dict:
        distance_name = original_distance_name
    else:
        distance_name = f"{total_distance_km}k"

    formatted_time = format_time(total_time_minutes)
    total_distance_km = format_number(total_distance_km)

    return {
        'distance_name': distance_name,
        'formatted_time': formatted_time,
        'formatted_pace': formatted_pace
    }

def equivalent_time_list(t1, d1):
    def eq_time(t1, d1, d2):
        t2 = t1 * (d2 / d1)**1.06
        return t2

    distance_dict = {
        '100 miles': 160.9344,
        '50 miles': 80.4672,
        '50 km': 50,
        'Marathon': 42.195,
        'Half Marathon': 21.0975,
        '10 km': 10,  # Fixed incorrect value
        '5 km': 5,    # Fixed incorrect value
        '3 km': 3,
        '2 miles': 3.218688,
        '1 mile': 1.609344,
    }

    eq_times = []
    for distance_name, distance_value in distance_dict.items():
        
        eq_t = eq_time(t1, d1, distance_value)
        eq_times.append((distance_name, format_time(eq_t)))

    return eq_times


#print(f'eq time is {equivalent_time_list(20, 5)}')

#print(calculate_pace(,'2','2',10))


app = Flask(__name__)

CORS(app)
@app.route('/calculate_pace', methods=['POST'])
def calculate_pace_api():
    try:
        data = request.json
        
        time_hours = data.get('time_hours')
        time_minutes = data.get('time_minutes')
        #print('test innan')
        time_seconds = data.get('time_seconds')
        #print('test efter')
        total_distance_km = data.get('total_distance_km')
        #print(time_seconds)


        #print(time_seconds)



        result = calculate_pace(time_hours, time_minutes, time_seconds, total_distance_km)
        return jsonify(result)

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/equivalent_times', methods=['POST'])
def equivalent_times_api():
    try:
        data = request.json
        t1 = data.get('time_minutes')
        d1 = data.get('distance_km')
        
        if t1 is None or d1 is None:
            return jsonify({'error': 'Missing required parameters'}), 400

        eq_times = equivalent_time_list(float(t1), float(d1))
        return jsonify(eq_times)

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)