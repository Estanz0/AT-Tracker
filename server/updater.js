require("dotenv").config();
const csv = require('csv-parser')
const fs = require('fs')

const Pool = require('pg').Pool;

const key = process.env.AT_API_KEY;

const pool = new Pool({
  user: 'byron',
  host: 'localhost',
  database: 'buses',
  password: 'Field2703',
  port: 5432
});

var update = async function () {
    updateStops();
    updateRoutes();
    updateShapes();
    updateTrips();
    updateStopTimes(); 
    // updateVehicleLocations();
}

function updateStops() {
    var fName = 'stops.txt';
    var stopsObj = [];
    var queryStr = "INSERT INTO Stops(stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, location_type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)";
    fs.createReadStream('data/gtfs/' + fName)
    .pipe(csv())
    .on('data', (data) => {
        pool.query(queryStr, [
            data.stop_id,
            data.stop_code,
            data.stop_name,
            data.stop_desc,
            parseFloat(data.stop_lat),
            parseFloat(data.stop_lon),
            data.zone_id,
            data.location_type
        ]).catch(err => {
            console.log(data)
            console.log(err);
        });
        stopsObj.push(data);
    })
    .on('end', function() { 
        // parent_station has FK constraint on stops so need to update it last
        queryStr = "UPDATE Stops SET parent_station = $1 WHERE stop_id = $2";
        for(let i = 0; i < stopsObj.length; i++) {
            pool.query(queryStr, [
                stopsObj[i].parent_station,
                stopsObj[i].stop_id
            ]).catch(err => {
                console.log(data)
                console.log(err);
            });
        }
        console.log("Stops Updated");
    });  
    
}

function updateRoutes() {
    var fName = 'routes.txt';
    var queryStr = "INSERT INTO Routes VALUES ($1, $2, $3, $4, $5, $6, $7)";
    fs.createReadStream('data/gtfs/' + fName)
    .pipe(csv())
    .on('data', (data) => {
        pool.query(queryStr, [
            data.route_id,  
            data.route_long_name,                     
            +data.route_type, 
            data.route_text_color,   
            data.agency_id,                       
            +data.route_color,    
            data.route_short_name
        ]).catch(err => {
            console.log(data)
            console.log(err);
        });
    })
    .on('end', function() { 
        console.log("Routes Updated");
    })
}

function updateShapes() {
    var fName = 'shapes_copy.txt';
    var queryStr = "INSERT INTO Shapes VALUES ($1, $2, $3, $4, $5)";
    fs.createReadStream('data/gtfs/' + fName)
    .pipe(csv())
    .on('data', (data) => {
        pool.query(queryStr, [
            data.shape_id,  
            parseFloat(data.shape_pt_lat),                     
            parseFloat(data.shape_pt_lon), 
            +data.shape_pt_sequence,   
            +data.shape_dist_traveled
        ]).catch(err => {
            console.log(data)
            console.log(err);
        });
    })
    .on('end', function() { 
        console.log("Shapes Updated");
    })
}

function updateTrips() {
    var fName = 'trips.txt';
    var queryStr = "INSERT INTO Trips VALUES ($1, $2, $3, $4, $5, $6, $7)";
    fs.createReadStream('data/gtfs/' + fName)
    .pipe(csv())
    .on('data', (data) => {
        pool.query(queryStr, [
            data.trip_id,  
            data.route_id,                     
            +data.block_id, 
            +data.direction_id,   
            +data.trip_headsign,
            data.shape_id,
            data.service_id
        ]).catch(err => {
            console.log(data)
            console.log(err);
        });
    })
    .on('end', function() { 
        console.log("Trips Updated")
    })
}

function updateStopTimes() {
    var fName = 'stop_times_copy.txt';
    var queryStr = "INSERT INTO Stop_times VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)";
    fs.createReadStream('data/gtfs/' + fName)
    .pipe(csv())
    .on('data', (data) => {
        pool.query(queryStr, [
            data.trip_id,  
            data.arrival_time,                     
            +data.departure_time, 
            +data.stop_id,   
            +data.stop_sequence,
            data.stop_headsign,
            +data.pickup_type,
            +data.drop_off_type,
            +data.shape_dist_traveled
        ]).catch(err => {
            console.log(data)
            console.log(err);
        });
    })
    .on('end', function() { 
        console.log("Stop Times Updated")
    })
}

async function apiCall(feed, urlExt, id) {
    let url = 'https://api.at.govt.nz/v2/';
    if(feed === 'general') {
        url += 'gtfs/';
    } else if(feed === 'realtime')  {
        url += 'public/realtime/';
    }

    url += urlExt

    if (id) {
        url += id;
    } else {
        url += '?';
    }

    return fetch(url, {
        method: "GET",
        headers: {"Ocp-Apim-Subscription-Key": key}
    })
    .then(response => response.json()) 
    .then(json => {
        return json.response;
    })
    .catch(err => {
        return err;
    });
}


update()