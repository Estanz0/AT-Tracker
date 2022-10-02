import React, { useState, useEffect }  from 'react';
import { Map, Marker, Overlay } from "pigeon-maps";
import { stamenToner } from 'pigeon-maps/providers'

import useWindowDimensions from './hooks/useWindowDimensions';

const key = process.env.REACT_APP_AT_API_KEY;
const MAP_DEFAULT_CENTER = [-36.84558, 174.7541];
const MAP_DEFAULT_ZOOM = 10

const TRACESTRACK_ACCESS_TOKEN = '74a26ad038c91b2a5cfb1db3afef30d2'

function tracestrack (x, y, z, dpr) {
  return `https://tile.tracestrack.com/base/${z}/${x}/${y}.png?key=${TRACESTRACK_ACCESS_TOKEN}`

}




const MyMap = () => {

    const [buses, setBuses] = useState([]);
    const [currentBuses, setCurrentBuses] = useState([]);
    const [stops, setStops] = useState([]);

    const [busImgSize, setBusImgSize] = useState(0)
    const [stopImgSize, setStopImgSize] = useState(0)

    const { height, width } = useWindowDimensions();


    useEffect(() => { 
        fetch("http://127.0.0.1:8000/vehicle_positions/")
        .then(res => res.json())
        .then((data) => {
            setBuses(data);
            setCurrentBuses(data); 
        })
        .catch((error) => { console.log(error); }) 
    }, []);

    function updateBus(bus) {
        setCurrentBuses([bus]);
        
        fetch("http://127.0.0.1:8000/stops/trip/" + bus.trip_id)
        .then(res => res.json())
        .then((data) => { 
            setStops(data); 
        })
        .catch((error) => { console.log(error); })
    }

    function resetBuses() {
        setCurrentBuses(buses);
        setStops([]);
    }

    function handleBoundsChanged({ center, zoom, bounds, initial }) {
        setBusImgSize(1.80 * zoom - 2.5);
        setStopImgSize(1.50 * zoom - 2.5);
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
        </Map>
    )
}

export default MyMap;