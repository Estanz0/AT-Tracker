import React, { useState, useEffect, render }  from 'react';
import { Map, Marker, Overlay, GeoJson } from "pigeon-maps";
import { stamenToner } from 'pigeon-maps/providers'
import Line from './line'

import useWindowDimensions from './hooks/useWindowDimensions';

const key = process.env.REACT_APP_AT_API_KEY;
const MAP_DEFAULT_CENTER = [-36.84558, 174.7541];
const MAP_DEFAULT_ZOOM = 10
const LOCAL_API_ROOT = 'http://127.0.0.1:8000/'

const TRACESTRACK_ACCESS_TOKEN = '74a26ad038c91b2a5cfb1db3afef30d2'

// The map display provider
function tracestrack (x, y, z, dpr) {
  return `https://tile.tracestrack.com/base/${z}/${x}/${y}.png?key=${TRACESTRACK_ACCESS_TOKEN}`
}

// let tripPath = {
//     type: 'FeatureCollection',
//     features: [
//         {
//             type: 'Feature',
//             geometry: {
//             type: 'LineString',
//             coordinates: [
//                 [174.0, -37.0],
//                 [174.0, -36.0],
//             ],
//             },
//             properties: {
//             prop0: 'value0',
//             prop1: 0.0,
//             },
//         },
//     ],
// }




const MyMap = () => {

    const [buses, setBuses] = useState([]);
    const [currentBuses, setCurrentBuses] = useState([]);
    const [stops, setStops] = useState([]);
    const [tripPath, setTripPath] = useState(
        {
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: {
                    type: 'LineString',
                    coordinates: [
                        [174.8, -37.0],
                        [174.8, -36.0],
                    ],
                    },
                    properties: {
                    prop0: 'value0',
                    prop1: 0.0,
                    },
                },
            ],
        }
    );
    const [tripPathKey, setTripPathKey] = useState(1); 


    const [busImgSize, setBusImgSize] = useState(0)
    const [stopImgSize, setStopImgSize] = useState(0)

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
            for(let i = 0; i < data.length; i++) {
                coords.push([data[i].shape_pt_lon, data[i].shape_pt_lat]);
            }

            coords =    [[174.5, -37.0],
                        [173.5, -37.0],
                        [174.0, -36.0],]

            return coords;
        })
        .then((coords) => {
            // coords =    [[174.5, -37.0],
            //             [174.0, -36.0],]
            // tripPath.features.coordinates = coords
            console.log('Coords');
            console.log(coords);
            setTripPathKey(1);
            setTripPath(
                {
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            geometry: {
                            type: 'LineString',
                            coordinates: coords,
                            },
                            properties: {
                            prop0: 'value0',
                            prop1: 0.0,
                            },
                        },
                    ],
                }
            );      
        })
        .then(() => {
            console.log('Update');
            console.log(tripPathKey);
            console.log(tripPath.features[0].geometry.coordinates);
        })
        .catch((error) => { console.log(error); }) 
    }

    function resetBuses() {
        setCurrentBuses(buses);
        setStops([]);

        setTripPathKey(0);

        // tripPath.features.geometry.coordinates = [[174.0, -37.0]];
        setTripPath(
            {
                type: 'FeatureCollection',
                features: [
                    {
                        type: 'Feature',
                        geometry: {
                            type: 'LineString',
                            coordinates: [
                                [174.8, -37.0],
                                [174.8, -36.0],
                            ],
                        },
                        properties: {
                            prop0: 'value0',
                            prop1: 0.0,
                        },
                    },
                ],
            }
        );
        console.log('Reset');
        console.log(tripPathKey);
        console.log(tripPath.features[0].geometry.coordinates);
    }

    function handleBoundsChanged({ center, zoom, bounds, initial }) {
        setBusImgSize(1.80 * zoom - 2.5);
        setStopImgSize(1.50 * zoom - 2.5);
    }

    if(!buses)
        return <></>

    // render() 
    //     {
    //         const geoJsonComponent = () => {
    //             if(tripPathKey == 1) {
    //                 return (
    //                     <GeoJson
    //                         key={tripPathKey}
    //                         data={tripPath}
    //                         styleCallback={(feature, hover) => {
    //                             return { strokeWidth: '2', stroke: 'black' }
    //                         }}
    //                     />
    //                 )
    //             }
    //         }
    //     }

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
            <GeoJson
                key={tripPathKey}
                data={tripPath}
                styleCallback={(feature, hover) => {
                    return { strokeWidth: '2', stroke: 'black' }
                }}
            />
        </Map>
    )
}

export default MyMap;