# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Welcome Route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/11252016</br>"
        f"/api/v1.0/temp/09152016/07152017"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Define date from 12 months ago
    other_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= other_date).all()
    # Create a dictionary and append to Rain Data list
    rain_data = []
    for date, precipitation in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = precipitation
        rain_data.append(rain_dict)
    # Jsonify list
    return jsonify(rain_data)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
    # Query stations
    results = session.query(Station.station).all()
    # Convert tuple into list
    station_list = list(np.ravel(results))
    # Jsonify data
    return jsonify(station_list)

# Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    # Define other date
    other_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query temperatures
    temperatures = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= other_date).all()
    # Convert tuple into list
    tobs_list = list(np.ravel(temperatures))
    # Jsonify data
    return jsonify(tobs_list)

@app.route("/api/v1.0/temp/<start>")
def starting(start=None, end=None):
    # Define start date
    start_date = dt.date(2016, 11, 25)
    start = start_date.strftime('%m%d%Y')
    # Start query
    start_averages = session.query(func.min(Measurement.tobs),
                                   func.avg(Measurement.tobs),
                                   func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    # Convert tuple into list
    start_list = list(np.ravel(start_averages))
    # Jsonify data
    return jsonify(start_list)

@app.route("/api/v1.0/temp/<start>/<end>")
def ending(start=None, end=None):
    # Define start date and end date
    start_date = dt.date(2016, 9, 15)
    start = start_date.strftime('%m%d%Y')
    end_date = dt.date(2017, 7, 15)
    end = end_date.strftime('%m%d%Y')
    # Start/End query
    end_averages = session.query(func.min(Measurement.tobs),
                                 func.avg(Measurement.tobs),
                                 func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    # Convert tuple into list
    end_list = list(np.ravel(end_averages))
    # Jsonify data
    return jsonify(end_list)

# Close session
session.close()

# Run code
if __name__ == '__main__':
    app.run(debug=True)