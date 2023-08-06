from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import datetime
import time
from AIRPrediction import *


"""
..  module:: sampleapp
    :synopsis: The sample app that demonstrates the functionality of the AIRPrediction framework. Creates a UI that 
    accepts user input and calls the functions in the AIRPrediction to utilize the Time Series Models to produce
    predictions.
..  moduleauthors:: Colin Naehr <cnaehr@ufl.edu>, Daniel Casto <danielcasto@ufl.edu>, Derek Pena <derek.pena@ufl.edu>,
    Haotian Wang <haotianwang@ufl.edu>
"""


class MainWindow(QWidget):
    """ Class that holds all of the UI elements of the sample app and their functionality.
        Parent class: QWidget
    """
    def __init__(self):
        """ Initializes the UI elements of the sample app.
        """
        super().__init__()
        self.setGeometry(0, 0, 1000, 700)
        self.setWindowTitle("Pollutant Forecaster")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.pollutant_label = QLabel('Enter Pollutant (NO2, O3, SO2, or CO):')
        self.pollutant_edit = QLineEdit()

        self.city_label = QLabel('Enter City: ')
        self.city_edit = QLineEdit()

        self.county_label = QLabel('Enter County: ')
        self.county_edit = QLineEdit()

        self.state_label = QLabel('Enter State: ')
        self.state_edit = QLineEdit()

        self.end_date_label = QLabel('Enter Future Date (MM/DD/YYYY): ')
        self.end_date_edit = QLineEdit()

        selector = QLabel('Select a forecasting method below:')
        self.radiobtn1 = QRadioButton('Prophet Model')
        self.radiobtn1.setMinimumHeight(40)
        self.radiobtn2 = QRadioButton('Arima')
        self.radiobtn2.setMinimumHeight(40)
        self.radiobtn3 = QRadioButton('Compare Both Models')
        self.radiobtn3.setMinimumHeight(40)

        self.msg_text = QLabel()

        self.button_one = QPushButton("Get Results")

        self.grid.addWidget(self.pollutant_label, 0, 0)
        self.grid.addWidget(self.pollutant_edit, 0, 1)

        self.grid.addWidget(self.state_label, 1, 0)
        self.grid.addWidget(self.state_edit, 1, 1)

        self.grid.addWidget(self.county_label, 2, 0)
        self.grid.addWidget(self.county_edit, 2, 1)

        self.grid.addWidget(self.city_label, 3, 0)
        self.grid.addWidget(self.city_edit, 3, 1)

        self.grid.addWidget(self.end_date_label, 4, 0)
        self.grid.addWidget(self.end_date_edit, 4, 1)

        self.grid.addWidget(selector, 5, 0)
        self.grid.addWidget(self.radiobtn1, 6, 0)
        self.grid.addWidget(self.radiobtn2, 6, 1)
        self.grid.addWidget(self.radiobtn3, 7, 0)

        self.msg_text.setMaximumSize(1000, 50)
        self.grid.addWidget(self.msg_text, 5, 1)

        self.button_one.clicked.connect(self.__submit_input)
        self.grid.addWidget(self.button_one, 8, 1)

        self.show()

    def __submit_input(self):
        """ Reads input and outputs state updates informing the user of errors, progress, and results. Functions from
            AIRPrediction are called to validate input and call on the prediction models.
            Called when submit button is pressed.
            :return: None
        """
        self.msg_text.setText('')
        QApplication.processEvents()
        pl = self.pollutant_edit.text()
        state = self.state_edit.text()
        county = self.county_edit.text()
        city = self.city_edit.text()
        date_feature_available = True
        if date_feature_available:
            ed = self.end_date_edit.text()
        try:
            self.msg_text.setText('Validating Input... (Fields cannot be edited at this time)')
            QApplication.processEvents()
            validate, return_message, date_string = validate_input(pl, state, county, city, ed)
            if self.radiobtn1.isChecked():
                if validate:
                    self.msg_text.setText('Input Validation Success! Running Prophet Model... (Fields cannot be edited at this time)')
                    QApplication.processEvents()
                    prophet_result, pollutant_unit = prophet_prediction(pl, state, county, city, date_string)
                    self.msg_text.setText(f'The forecast for {pl} in {city}, {county}, {state} is {prophet_result} {pollutant_unit}')
                else:
                    self.msg_text.setText(return_message)
            elif self.radiobtn2.isChecked():
                if validate:
                    self.msg_text.setText('Input Validation Success! Running ARIMA Model... (Fields cannot be edited at this time)')
                    QApplication.processEvents()
                    arima_result, pollutant_unit = arima_prediction(pl, state, county, city, date_string)
                    self.msg_text.setText(f'The forecast for {pl} in {city}, {county}, {state} is {arima_result} {pollutant_unit}')
                else:
                    self.msg_text.setText(return_message)
            elif self.radiobtn3.isChecked():
                if validate:
                    self.msg_text.setText('Input Validation Success! Running Model Comparison... (Fields cannot be edited at this time)')
                    QApplication.processEvents()
                    results = compare_models(pl, state, county, city, date_string)
                    self.msg_text.setText(f'Prophet Prediction: {results[0]} {results[1]}   Time: {results[2]} seconds'
                                            f'\nARIMA Prediction: {results[3]} {results[4]}    Time: {results[5]} seconds.')
                else:
                    self.msg_text.setText(return_message)
            else:
                self.msg_text.setText(f'Please select a prediction method.')

        except:
            self.msg_text.setText('Error: something went wrong in prediction')
            print('Error: something went wrong in prediction')


def main():

    """ The sample app that demonstrates the functionality of the AIRPrediction framework. Creates a UI that
    accepts user input and calls the functions in the AIRPrediction to utilize the Time Series Models to produce
    predictions. main () generates the window the application is hosted on.

    Module Authors: Colin Naehr <cnaehr@ufl.edu>, Daniel Casto <danielcasto@ufl.edu>, Derek Pena <derek.pena@ufl.edu>,
    Haotian Wang <haotianwang@ufl.edu>

    :return: None
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
