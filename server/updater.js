require("dotenv").config();

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
    // updateVehicleLocations();
}

var updateStops = async function () {
    var queryStr = "INSERT INTO stop(id, name, latitude, longitude) VALUES ($1, $2, $3, $4)";

    const stops = await apiCall('general', 'stops', '');

    for(let i = 0; i < stops.length; i++)
        pool.query(queryStr, [
            stops[i].stop_id, 
            stops[i].stop_name, 
            stops[i].stop_lat, 
            stops[i].stop_lon
        ]).catch(err => console.log(stops[i]));
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