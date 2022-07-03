import React, { useState, useEffect }  from 'react';
import { Map, Marker, Overlay } from "pigeon-maps";
import { Stops } from './stops';
import { Test } from './test';

const key = process.env.REACT_APP_AT_API_KEY;
const center = [-36.84558, 174.7541];
const imgSize= 20;
const busImgSize = 15;

const MyMap = () => {
    // const [stops, setStops] = useState([]);
    // useEffect(() => { 
    //     fetch("/Stops/")
    //     .then(res => res.json())
    //     .then(
    //         (data) => {
    //             setStops(data);
    //         },
    //         (error) => {
    //             console.log(error);
    //         }
    // ) }, []);
    // if(!stops)
    //     return <></>

    const [buses, setBuses] = useState([]);
    useEffect(() => { 
        apiCall('realtime', 'vehiclelocations', '')
        .then(
            (data) => {
                setBuses(data.entity);
            },
            (error) => {
                console.log(error);
            })
        const interval = setInterval(() => {
        apiCall('realtime', 'vehiclelocations', '')
        .then(
            (data) => {
                setBuses(data.entity);
            },
            (error) => {
                console.log(error);
            }) 
        }, 50000);
    }, []);

    return (
        <Map height={1000} defaultCenter={center} defaultZoom={10}>
            {buses.map((bus, index) => {
                var latlng = [+bus.vehicle.position.latitude, +bus.vehicle.position.longitude];
                return (
                    <Overlay anchor={latlng} offset={[busImgSize / 2,busImgSize]} key={index} >
                        <img src='bus_img.png' width={busImgSize} alt='' />
                    </Overlay>
                    
                )
            })}
            {/* <Test /> */}
            {/* {
                console.log(state)
            } */}
            
            {/* {stops.map((stop, index) => {
                var latlng = [+stop.latitude, +stop.longitude];
                // console.log(latlng);
                if(index % 100 !== 0)
                    return;
                return (
                    <Overlay anchor={latlng} offset={[imgSize / 2,imgSize]} key={index} >
                        <img src='stop_img.png' width={imgSize} alt='' />
                    </Overlay>
                )
            })} */}
        </Map>
    )
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

export default MyMap;