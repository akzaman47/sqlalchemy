# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def Home():
    return f'''
    <h1>Hawaii Climate API</h1>
    <h3>Routes:</h3>
    <ul>
    <li><a href="/api/v1.0/precipitation">Precipitation</a></li>
    <li><a href="/api/v1.0/station">Station</a></li>
    <li><a href="/api/v1.0/tobs">Temperature Observed</a></li>
    <li>/api/v1.0/<start></li>
    <li>/api/v1.0/start/end</li>
    </ul>
'''

@app.route('/api/v1.0/precipitation')
def precipitation():
    return { date:prcp for date, prcp in session.query(measurement.date,measurement.prcp).filter(measurement.date>'2016-08-23').all()}

@app.route('/api/v1.0/station')
def Station():
    return {id:name for id,name in session.query(station.station,station.name).all()}


@app.route('/api/v1.0/tobs')
def tobs():
    return  {date:temp for date,temp in session.query(measurement.date, measurement.tobs).filter_by(station = 'USC00519281').all()}

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dateRange(start, end= '8-23-2017'):
      result = session.query(func.min(measurement.tobs),
                                 func.max(measurement.tobs),
                                 func.avg(measurement.tobs)).\
                                     filter_by((measurement.station=='USC00519281') & 
                                         (measurement.date >= start)
                                         (measurement.date <= end)).all()

    result = session.query(func.min(measurement.tobs)).all()
    
    print(result)
