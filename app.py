################################################################
# Dependencies 
################################################################


# importing all dependency
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################################
# Database Setup
################################################################


# creating an engine to access sqlite DB
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

# reflecting, mirroring, tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# session line from python to sqlite
session = Session(engine)

# new flask instance (singular version)
# using double underscores as magic methods

################################################################
# Flask Setup
################################################################


app = Flask(__name__)

# creating routes(pathways)

@app.route('/')

# putting code that runs in this specific route under it 

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

    if __name__ == '__main__':
        app.run()


@app.route("/api/v1.0/precipitation")

def precipitation():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
    precip = {date: prcp for date, prcp in precipitation}
    
    return jsonify(precip)


@app.route("/api/v1.0/stations")

def stations():
    
    results = session.query(Station.station).all()
    
    stations = list(np.ravel(results)) 
#   unraveling the stations into 1d array
    
    return jsonify(stations=stations)
#   s=s to return list as JSON


@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
	
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))

    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
 