from setuptools import setup

setup(
    name = 'AIRPrediction',
    version = '0.0.7',
    packages=['Time_Series_Models','data','docs',],
    scripts = ['sampleapp.py', 'AIRPrediction.py'],
    url = 'https://github.com/danielcasto/AIRPrediction',
    license = 'MIT',
    install_requires = ['PySide2', 'pystan==2.19.1.1', 'prophet', 'statsmodels'],
    #data_files = ['data/pollution_us_2000_2016.csv', 'data/predictable_areas.csv'],

    entry_points={
        'console_scripts': [
            'sampleapp = sampleapp:main'
        ]
    }
)
