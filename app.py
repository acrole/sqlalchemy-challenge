import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

session.close()

#create app
app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Welcome to Hawaii Climate Page<br/> "
        f"Available Routes:<br/>"
        f"<br/>"  
        f"The list of precipitation data with dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"The list of stations and names:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"The list of temprture observations from a year from the last data point:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max. and Avg. temperatures for given start date: (please use 'yyyy-mm-dd' format):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"<br/>"
        f"Min. Max. and Avg. tempratures for given start and end date: (please use 'yyyy-mm-dd'/'yyyy-mm-dd' format for start and end values):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
        f"<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2012-01-01/2016-12-31' target='_blank'>/api/v1.0/min_max_avg/2012-01-01/2016-12-31</a>"
    )

#precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
  
    session = Session(engine)

    """Return the dictionary for date and precipitation info"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()

#directory

      precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
        precipitation.append(r)

    return jsonify(precipitation )

#station

@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset."""

    results = session.query(Station.station, Station.name).all()
    
    session.close()

#directories 

station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    
    return jsonify(station_list)


#temperatures


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
   
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= query_date).all()

    session.close()

  
    tobs_list = []
    for result in results:
        r = {}
        r["date"] = result[1]
        r["temprature"] = result[0]
        tobs_list.append(r)

    
    return jsonify(tobs_list)

#start route


@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
   
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).all()

    session.close()

    
    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

  
    return jsonify(t_list)


@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
   
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end dates."""

  
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")

    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt)

    session.close()

   
    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["EndDate"] = end_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

   
    return jsonify(t_list)


#run app
if __name__ == "__main__":
    app.run(debug=True)






