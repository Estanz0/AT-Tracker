import React, { useState, useEffect, render }  from 'react';
import { Map, Marker, Overlay, GeoJson, Point } from "pigeon-maps";
import { stamenToner } from 'pigeon-maps/providers'
import Line from './line'

import useWindowDimensions from './hooks/useWindowDimensions';

const key = process.env.REACT_APP_AT_API_KEY;
const MAP_DEFAULT_CENTER = [-36.84558, 174.7541];
const MAP_DEFAULT_ZOOM = 10
const LOCAL_API_ROOT = 'http://127.0.0.1:8000/'

const TRACESTRACK_ACCESS_TOKEN = '74a26ad038c91b2a5cfb1db3afef30d2'

const MIN_MARKER_SIZE = 3
const POINT_SIZE_MULTIPLIER = 0.15

// The map display provider
function tracestrack (x, y, z, dpr) {
  return `https://tile.tracestrack.com/base/${z}/${x}/${y}.png?key=${TRACESTRACK_ACCESS_TOKEN}`
}

const MyMap = () => {

    const [buses, setBuses] = useState([]);
    const [currentBuses, setCurrentBuses] = useState([]);
    const [stops, setStops] = useState([]);
    const [tripPath, setTripPath] = useState([]);

    const [busImgSize, setBusImgSize] = useState(0)
    const [stopImgSize, setStopImgSize] = useState(0)
    const [pointRadius, setPointRadius] = useState(0)

    const { height, width } = useWindowDimensions();


    useEffect(() => { 
        fetch(`${LOCAL_API_ROOT}vehicle_positions/`)
        .then(res => res.json())
        .then((data) => {
            setBuses(data);
            setCurrentBuses(data); 
        })
        .catch((error) => { console.log(error); }) 
    }, []);

    function updateBus(bus) {
        setCurrentBuses([bus]);
        
        fetch(`${LOCAL_API_ROOT}stops/trip/${bus.trip_id}`)
        .then(res => res.json())
        .then((data) => { 
            setStops(data); 
        })
        .catch((error) => { console.log(error); })

        fetch(`${LOCAL_API_ROOT}shapes/trip/${bus.trip_id}`)
        .then(res => res.json())
        .then((data) => { 
            let coords = []
            console.log('Data')
            console.log(data)
            console.log('bus')
            console.log(bus)
            for(let i = 0; i < data.length; i++) {
                coords.push([data[i].shape_pt_lon, data[i].shape_pt_lat]);
            }
            return coords;
        })
        .then((coords) => {
            console.log('Coords');
            console.log(coords);
            setTripPath(coords)
        })
        .catch((error) => { console.log(error); }) 
    }

    function resetBuses() {
        setCurrentBuses(buses);
        setStops([]);
        setTripPath([]);
    }

    function handleBoundsChanged({ center, zoom, bounds, initial }) {
        setBusImgSize(1.80 * zoom - 2.5);
        setStopImgSize(1.50 * zoom - 2.5);
        setPointRadius(Math.max(POINT_SIZE_MULTIPLIER * zoom, MIN_MARKER_SIZE));
    }

    if(!buses)
        return <></>

    return (
        <Map 
            height={height} 
            width={width} 
            defaultCenter={MAP_DEFAULT_CENTER} 
            defaultZoom={MAP_DEFAULT_ZOOM}
            minZoom={8} 
            provider={tracestrack}
            zoomSnap={true}
            onClick={ () => resetBuses() }
            onBoundsChanged={ (center, zoom, bounds, initial) => handleBoundsChanged(center, zoom, bounds, initial)}
        >
            {stops && stops.length !== 0 && stops.map((stop, index) => {
                var latlng = [+stop.stop_lat, +stop.stop_lon];
                return (
                    <Overlay anchor={latlng} offset={[stopImgSize / 2,stopImgSize]} key={index} >
                        <img src='stop_img.png' width={stopImgSize} alt='' />
                    </Overlay>
                )
            })}
            {currentBuses.length && currentBuses.map((bus, index) => {
                var latlng = [+bus.vehicle_lat, +bus.vehicle_lon];
                return (
                    <Overlay anchor={latlng} offset={[busImgSize / 2,busImgSize]} key={index} >
                        <img src='bus_img.png' width={busImgSize} alt='' onClick={() => updateBus(bus)}/>
                    </Overlay>
                )
            })}
            {tripPath.length && tripPath.map((point, index) => {
                var latlng = [+point[1], +point[0]];
                return (
                    <Overlay anchor={latlng} offset={[pointRadius, pointRadius / POINT_SIZE_MULTIPLIER]} key={index} >
                        <svg width={pointRadius * 2} height={pointRadius * 2}>
                            <circle cx={pointRadius} cy={pointRadius} r={pointRadius} fill="green" />
                        </svg>
                    </Overlay>
                )
            })}
        </Map>
    )
}

export default MyMap;