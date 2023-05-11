import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = base.classes.measurement
Station = base.classes.station

# Create an app
app = Flask(__name__)


@app.route("/")
def homepage():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/2017-07-13 <br/>"
        f"/api/v1.0/2016-05-09/2017-07-13 <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all the dates and precipitation data"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all the dates and precipiation 
    results_prcp = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to the all_prcp list
    all_prcp = []
    for date, prcp in results_prcp:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    
    # Query all the distinct/unique stations 
    results_station = session.query(func.distinct(Measurement.station)).all()
    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results_station))
 
    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the date and precipitation data of station USC00519281 from the past 12 months"""
    
    # Query the date and observed temperature of the most active station USC00519281 from the past 12 months
    results_active_tobs = session.query(Measurement.date, Measurement.tobs).\
                            filter(Measurement.station == "USC00519281").\
                            filter(Measurement.date <= dt.date(2017,8,23)).\
                            filter(Measurement.date >= dt.date(2016,8,23)).all()
    
    session.close()

    # Convert list of tuples into normal list
    active_tobs = list(np.ravel(results_active_tobs))
 
    return jsonify(active_tobs)


@app.route("/api/v1.0/<start>")
def tobs_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the Temperature analysis from the given start date"""
    
    # Query the minimum, maximum, and average temperature from the given start date
    temps = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_temps = session.query(*temps).filter(Measurement.date >= start).all()
    
    session.close()

    # Convert list of tuples into normal list
    start_tobs = list(np.ravel(start_temps))
    tobs = {
        "TMIN": start_tobs[0],
        "TMAX": start_tobs[1],
        "TAVG": start_tobs[2]
        }
 
    return jsonify(tobs)

# COMMENT
@app.route("/api/v1.0/<start>/<end>")
def tobs_range(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the Temperature analysis from the given date range"""
    
    # Query the minimum, maximum, and average temperature from the given range of dates
    temps = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    range_temps = session.query(*temps).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Convert list of tuples into normal list
    range_tobs = list(np.ravel(range_temps))
    tobs = {
        "TMIN": range_tobs[0],
        "TMAX": range_tobs[1],
        "TAVG": range_tobs[2]
        }
 
    return jsonify(tobs)

if __name__ == "__main__":
    app.run(debug=True)
