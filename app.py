import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes - Main Route
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    start=[]
    end=[]
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurements<br/>"
        f"/api/v1.0/precipitations<br/>"

        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"

        f"/api/v1.0/&lt;startdate&gt;<br/>"
        f"/api/v1.0/&lt;startdate&gt;,&lt;enddate&gt;><br/><br/>"
        f"NOTE: for custom URL start and end date, date format is YYYY-mm-dd"
        # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates
        # between the start and end date inclusive.
    )

#################################################
# Flask Routes - Measurements
# All measurements
#################################################


@app.route("/api/v1.0/measurements")
def measures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all items names"""
    # Query all passengers
    resultsp = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    all_measurements = []
    for all in resultsp:
        meas_dict = {}
        meas_dict["id"] = all.id
        meas_dict["station"] = all.station
        meas_dict["date"] = all.date
        meas_dict["prcp"] = all.prcp
        meas_dict["tobs"] = all.tobs

        all_measurements.append(meas_dict)

    return jsonify(all_measurements)


#################################################
# Flask Routes - Precipitations
#✓ Returns the jsonified precipitation data for the last year in the database
#✓ Returns json with the date as the key and the value as the precipitation
# #################################################


@app.route("/api/v1.0/precipitations")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all items names"""
    # Query all passengers
    resultsp = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_info = []
    for row in resultsp:
        prcp_dict = {}
        prcp_dict["date"] = row.date
        prcp_dict["prcp"] = row.prcp
        prcp_info.append(prcp_dict)
    return jsonify(prcp_info)


#################################################
# Flask Routes - Tobs
#Returns jsonified data for the most active station (USC00519281) for the last year of data
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query year

    resultst = session.query(Station.name, Measurement.date, Measurement.prcp, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(
        Measurement.date > (dt.date(2017, 8, 23) - dt.timedelta(days=365))).order_by(desc(Measurement.date)).all()

    session.close()

    # Create a list with the date and tobs
    tobs_info = []
    for row in resultst:
        tob_dict = {}
        tob_dict["date"] = row.date
        tob_dict["tobs"] = row.tobs
        tobs_info.append(tob_dict)
    return jsonify(tobs_info)


#################################################
# Flask Routes - Stations
# Returns jsonified data of all of the stations in the database
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   #Return statin datta
    # Query all stations
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for all in results:
        station_dict = {}
        station_dict["id"] = all.id
        station_dict["station"] = all.station
        station_dict["name"] = all.name
        station_dict["latitude"] = all.latitude
        station_dict["longitude"] = all.longitude
        station_dict["elevation"] = all.elevation

        all_stations.append(station_dict)

    return jsonify(all_stations)


#################################################
# Flask Routes - Start Date
# # Return a JSON list of the minimum temperature, the average temperature, and the max
# temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and
# equal to the start date.
#################################################

@app.route('/api/v1.0/<start>')
def startdate(start):
    session = Session(engine)

   #Return statin datta
    # Query all stations
    
    # startresult=session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
     
    # startresult=session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= (dt.datetime.strptime(start, '%Y-%m-%d'))).all()

    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    resultsel = session.query(*sel).filter(Measurement.date >= start).group_by(Measurement.date).all()

    session.close()

    return jsonify(resultsel)

#################################################
# Flask Routes - Start Date
# # Return a JSON list of the minimum temperature, the average temperature, and the max
# temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and
# equal to the start date.
#################################################

@app.route('/api/v1.0/<start2>,<end>')
def startend(start2, end):
    session = Session(engine)

    sel2 = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    resultsel2 = session.query(*sel2).filter(Measurement.date.between(start2,end)).group_by(Measurement.date).all()

    session.close()

    return jsonify(resultsel2)

if __name__ == '__main__':
    app.run(debug=True)
