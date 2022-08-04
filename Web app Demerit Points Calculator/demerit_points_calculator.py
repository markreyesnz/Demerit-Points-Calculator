#Assessment 3A Stage 2
#Mark Reyes mar0957@arastudent.ac.nz
#DTEC501
#10/11/2021


import os
from flask import Flask, render_template, request, flash

SUCCESS_MSG = 'success'
WARNING_MSG = 'warning'
KEY_SIZE = 24

# Create Flask instance and set the session key
app = Flask(__name__)
app.secret_key = os.urandom(KEY_SIZE)


def get_demerit_points(driving_speed, speed_limit, light_trailer=False, school_zone=False, holiday_period=False):
    """ works out the demerit points for a driving speed in a particular speed limited zone. """

#Find out the difference in driving speed and speed limit.
    acceleration_difference = driving_speed - speed_limit

    
#Validate if in speed limited zone, holiday period, or pulling a trailer with regards to speed differences and return a boolean value. 
    if school_zone or holiday_period:
        if acceleration_difference > 4:
            imposed_penalty = True
        else:
            imposed_penalty = False

    elif light_trailer:
        if acceleration_difference > 5:
            imposed_penalty = True
        else:
            imposed_penalty = False

    else:
        if acceleration_difference > 10:
            imposed_penalty = True
        else:
            imposed_penalty = False


#Validate the speed differences and equate it the correct amount of demerit points. 
    if acceleration_difference <= 0:
        demerit_points = 0

    elif acceleration_difference > 0 and acceleration_difference <= 10:
        demerit_points = 10

    elif acceleration_difference > 10 and acceleration_difference <= 20:
        demerit_points = 20

    elif acceleration_difference > 20 and acceleration_difference <= 30:
        demerit_points = 35

    elif acceleration_difference > 30 and acceleration_difference <= 35:
        demerit_points = 40

    else:
        demerit_points = 50

#Return mandatory penalty and penalty points
    return (imposed_penalty, demerit_points)
    

@app.route('/', methods = ['POST', 'GET'])
def home():
    """ Handles the home page of the website """

    print(f'DEBUG. Function received method type: {request.method}')
    
    if request.method == 'POST':
        #Process the data that has been sent via http post
        driver_full_name = request.form.get('full_name').lstrip().rstrip().title()
        car_speed = request.form.get('driving_speed')
        max_speed = request.form.get('speed_limit')
        trailer_towing = request.form.get('towing_box')
        within_school_zone = request.form.get('school_box')
        holiday_time = request.form.get('holiday_box')

        #Validate all of the input and return specifics based on different conditions.     
        if driver_full_name == '':
            flash('Please enter the driver name.', WARNING_MSG)
            return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)

        elif not driver_full_name.replace(' ','').replace('-','').isalpha():
            flash('Driver name needs to be alphabetic.', WARNING_MSG)
            return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)            

        elif not car_speed.replace('.','').isdigit():
            flash('Driving speed can be fractional. Speed limit must be a whole number.', WARNING_MSG)
            return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)

        
        elif not max_speed.isdigit():
            flash('Driving speed can be fractional. Speed limit must be a whole number.', WARNING_MSG)  
            return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)

        else:
            car_speed = eval(car_speed)
            max_speed = int(max_speed)
            demerit_points = get_demerit_points(car_speed, max_speed, trailer_towing, within_school_zone, holiday_time)
            gets_ticket = demerit_points[0]
            penalty_points = demerit_points[1]

            #Validate whether a ticket is or is not required. 
            if gets_ticket:

                flash(f"{driver_full_name}, the mandatory penalty for driving at \n{car_speed}km/h in a {max_speed}km/h zone is {penalty_points} points.", SUCCESS_MSG)
                return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)


            elif gets_ticket is False and penalty_points > 0:

                flash(f"{driver_full_name}, the discretional penalty for driving at \n{car_speed}km/h in a {max_speed}km/h zone is {penalty_points} points.", SUCCESS_MSG)
                return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)

            
            else:
    
                flash(f"{driver_full_name}, driving at {car_speed}km/h in a {max_speed}km/h zone is not speeding.", SUCCESS_MSG)
                return render_template('DemeritPoints.html', title='Home', full_name=driver_full_name, driving_speed=car_speed, speed_limit=max_speed, towing_box=trailer_towing, school_box=within_school_zone, holiday_box=holiday_time)     
        

    return render_template('DemeritPoints.html', title='Home')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def error(path):
    """ Handles different paths entered """
    
    return render_template('differentURLpath.html'), {"Refresh": "5; url=http://127.0.0.1:5000"}

if __name__ == '__main__':
    app.run()


