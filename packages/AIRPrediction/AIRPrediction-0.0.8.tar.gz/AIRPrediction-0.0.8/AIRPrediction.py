import datetime
import sys
import csv
import time
from Time_Series_Models.prophet_model import prophet_prediction
from Time_Series_Models.ARIMA_model import arima_prediction
"""
..  module:: AIRPrediction
    :synopsis: The driver file that is to be imported to utilize the AIRPrediction Framework.
    Includes a function for input validation, prophet predictions, ARIMA predictions, and comparison of the two models.
..  moduleauthors:: Derek Pena <derek.pena@ufl.edu>, Colin Naehr <cnaehr@ufl.edu>, Daniel Casto <danielcasto@ufl.edu>, 
    Haotian Wang <haotianwang@ufl.edu>
"""


def validate_input(pollutant, state, county, city, date):
    """ Validates the input provided by a user. To be used before any predictions are made.
        :param pollutant: The specified pollutant to predict (NO2, O3, SO2, CO).
        :param state: The location parameter indicating the state in the United States of America to predict for.
        :param county: The location parameter indicating the county in the state to predict for.
        :param city: The location parameter indicating the city in the county to predict for.
        :param date: The calendar date to prediction for.
        :return: A boolean that determines where validation was successful, a string that contains any error messages
        and a string that rewrites the data parameter in YYYY/MM/DD format.
    """
    validate = True
    return_message = ""
    valid_pollutants = ['NO2', 'O3', 'SO2', 'CO']
    entered_datetime = ""
    if pollutant == "" or state == "" or county == "" or city == "" or date == "":
        return False, "Error: One or more fields left blank. Please fill out all fields.", entered_datetime

    if pollutant not in valid_pollutants:
        validate = False
        return_message = "Error: Invalid Pollutant."
    else:
        if len(date) == 10:
            if date[2] != '/' or date[5] != '/':
                validate = False
                return_message = "Error: Invalid Date Format."

            month = date[:2]
            day = date[3:5]
            year = date[6:]

            entered_datetime = datetime.datetime(int(year), int(month), int(day))

            current_date = datetime.date.today().strftime('%m/%d/%Y')
            current_month = current_date[:2]
            current_day = current_date[3:5]
            current_year = current_date[6:]
            current_datetime = datetime.datetime(int(current_year), int(current_month), int(current_day))

            if entered_datetime > current_datetime:
                validate = True
                month_string = str(entered_datetime.month)
                day_string = str(entered_datetime.day)
                if len(month_string) == 1:
                    month_string = '0' + month_string
                if len(day_string) == 1:
                    day_string = '0' + day_string
                entered_datetime = str(entered_datetime.year) + '-' + month_string + '-' + day_string

                with open("data/predictable_areas.csv") as file:
                    location_validator = csv.reader(file)
                    location_validation = False
                    state_validation = False
                    county_validation = False
                    city_validation = False
                    for row in location_validator:
                        if row[0] == state:
                            state_validation = True
                            if row[1] == county and row[2] == city:
                                location_validation = True
                        if row[1] == county:
                            county_validation = True
                        if row[2] == city:
                            city_validation = True
                    if not location_validation:
                        validate = False
                        if state_validation and county_validation and city_validation:
                            return_message = "Error: State, county, and city found. However, the combination of those parameters was not found in the dataset."
                        else:
                            return_message = "Error: Following location parameters not found in the dataset:"
                            if not state_validation:
                                return_message += " State,"
                            if not county_validation:
                                return_message += " County,"
                            if not city_validation:
                                return_message += " City."
                            if return_message[len(return_message) - 1] == ",":
                                return_message = return_message[0:(len(return_message) - 1)]
                                return_message += "."
            else:
                validate = False
                return_message = "Error: Invalid Date. Entered date must occur after current date."
        else:
            validate = False
            return_message = "Error: Invalid Date Format."
    return validate, return_message, entered_datetime


def prophet(pollutant, state, county, city, date):
    """ A function that uses the prophet_prediction from prophet_model.py to avoid using multiple import statements.
        :param pollutant: The specified pollutant to predict (NO2, O3, SO2, CO).
        :param state: The location parameter indicating the state in the United States of America to predict for.
        :param county: The location parameter indicating the county in the state to predict for.
        :param city: The location parameter indicating the city in the county to predict for.
        :param date: The calendar date to prediction for.
        :return: The prediction made by the prophet model given the above parameters and the units that prediction is in.
    """
    return prophet_prediction(pollutant, state, county, city, date)


def arima(pollutant, state, county, city, date):
    """ A function that uses the arima_prediction from ARIMA_model.py to avoid using multiple import statements.
        :param pollutant: The specified pollutant to predict (NO2, O3, SO2, CO).
        :param state: The location parameter indicating the state in the United States of America to predict for.
        :param county: The location parameter indicating the county in the state to predict for.
        :param city: The location parameter indicating the city in the county to predict for.
        :param date: The calendar date to prediction for.
        :return: The prediction made by the ARIMA model given the above parameters and the units that prediction is in.
    """
    return arima_prediction(pollutant, state, county, city, date)


def compare_models(pollutant, state, county, city, date):
    """The driver file that is to be imported to utilize the AIRPrediction Framework.
    Includes a function for input validation, prophet predictions, ARIMA predictions, and comparison of the two models.
    Module Authors: Derek Pena <derek.pena@ufl.edu>, Colin Naehr <cnaehr@ufl.edu>, Daniel Casto <danielcasto@ufl.edu>,
    Haotian Wang <haotianwang@ufl.edu>

    compare_models is a function that times both prediction models in order to compare their speed and their output.

    :param pollutant: The specified pollutant to predict (NO2, O3, SO2, CO).
    :param state: The location parameter indicating the state in the United States of America to predict for.
    :param county: The location parameter indicating the county in the state to predict for.
    :param city: The location parameter indicating the city in the county to predict for.
    :param date: The calendar date to prediction for.
    :return: A list that contains the outputs for each prediction model as well as the time taken to run them.
    """
    output_list = []
    start_one = time.time()
    prediction, units = prophet_prediction(pollutant, state, county, city, date)
    end_one = time.time()
    output_list.append(prediction)
    output_list.append(units)
    output_list.append(end_one - start_one)
    start_two = time.time()
    prediction, units = arima_prediction(pollutant, state, county, city, date)
    end_two = time.time()
    output_list.append(prediction)
    output_list.append(units)
    output_list.append(end_two - start_two)
    return output_list
