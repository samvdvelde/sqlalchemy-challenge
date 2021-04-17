import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from statistics import mean
import datetime as dt

from flask import Flask, jsonify


#Database setup

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


#Routes



@app.route("/")
def welcome():
    test= (f"Welcome to the Climate app API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")
    return (test)


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    #Query dates and precipitation from Measurement table

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation = []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    #Query stations from measurement table

    results = session.query(Station.name).all()

    session.close()


    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    #Query temps for last year in station USC00519281


    results = session.query(Measurement.tobs).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    session.close()

    last_year_temps = list(np.ravel(results))

    return jsonify(last_year_temps)


#Prints date and min, max, avg temps for all the dates, not the min, max, avg of all the dates combined.

@app.route("/api/v1.0/<start>")

def start_date(start):

    session = Session(engine)




    result = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).\
        group_by(Measurement.date).\
        all()
        
    session.close()

    temp_list = list(np.ravel(result))


    return jsonify(temp_list)


#Prints date and min, max, avg temps for all the dates, not the min, max, avg of all the dates combined.

@app.route("/api/v1.0/<start>/<end>")

def startend_date(start, end):

    session = Session(engine)


    result = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= end).\
        group_by(Measurement.date).\
        all()
        
    session.close()



    temp_list = list(np.ravel(result))



    return jsonify(temp_list)




if __name__ == '__main__':
    app.run(debug=True)
