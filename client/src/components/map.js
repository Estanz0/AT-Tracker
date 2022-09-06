import React, { useState, useEffect }  from 'react';
import { Map, Marker, Overlay } from "pigeon-maps";

const key = process.env.REACT_APP_AT_API_KEY;
const center = [-36.84558, 174.7541];
const imgSize= 20;
const busImgSize = 15;

const MyMap = () => {


    const [buses, setBuses] = useState([]);
    const [currentBuses, setCurrentBuses] = useState([]);

    const [stops, setStops] = useState([]);

    useEffect(() => { 
        fetch("http://127.0.0.1:8000/vehicle_positions/")
        .then(res => res.json())
        .then(
            (data) => {
                setBuses(data);
            },
            (error) => {
                console.log(error);
            }
    ) }, []);
    
    if(!buses)
        return <></>

    function updateBus(bus) {
        setCurrentBuses([bus]);
        
        fetch("http://127.0.0.1:8000/routes/" + bus.route_id)
        .then(res => res.json())
        .then(
            (data) => {
                setStops(data.stops);
            },
            (error) => {
                console.log(error);
            }
        )

        console.log(bus);
        console.log(stops);
    }

    function resetMap() {
        setCurrentBuses([]);
        setStops([]);
    }

    return (
        <Map height={1000} defaultCenter={center} defaultZoom={10} onClick={ () => resetMap() }>
            {currentBuses.length === 0 && buses.map((bus, index) => {
                var latlng = [+bus.vehicle_lat, +bus.vehicle_lon];
                return (
                    <Overlay anchor={latlng} offset={[busImgSize / 2,busImgSize]} key={index} >
                        <img src='bus_img.png' width={busImgSize} alt='' onClick={() => updateBus(bus)}/>
                    </Overlay>
                )
            })}
            {currentBuses.length && currentBuses.map((bus, index) => {
                var latlng = [+bus.vehicle_lat, +bus.vehicle_lon];
                return (
                    <Overlay anchor={latlng} offset={[busImgSize / 2,busImgSize]} key={index} >
                        <img src='bus_img.png' width={busImgSize} alt='' />
                    </Overlay>
                )
            })}
            {stops.length !== 0 && stops.map((stop, index) => {
                var latlng = [+stop.stop_lat, +stop.stop_lon];
                return (
                    <Overlay anchor={latlng} offset={[busImgSize / 2,busImgSize]} key={index} >
                        <img src='stop_img.png' width={busImgSize} alt='' />
                    </Overlay>
                )
            })}
        </Map>
    )
}

export default MyMap;