import React, { useState, useEffect }  from 'react';
import { Overlay } from "pigeon-maps"

export const Stops = (props) => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [stops, setStops] = useState([]);
    useEffect(() => {
        fetch("/Stops/")
            .then(res => res.json())
            .then(
                (data) => {
                    setIsLoaded(true);
                    setStops(data);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])
    if (error) {
        return <></>;
    } else if (!isLoaded) {
        return <></>;
    } else {
        return (
            <>
                {props.left}
                {stops.map((stop, index) => {
                    var latlng = [+stop.latitude, +stop.longitude];
                    var imgSize = 20;
                    // console.log(latlng);
                    return (
                        <Overlay anchor={latlng} 
                                offset={[imgSize / 2,imgSize]} 
                                key={index} 
                                left={props.left}
                                top={props.top}
                            >
                            <img src='stop_img.png' width={imgSize} alt='' />
                        </Overlay>
                    )
                })}
            </>
        );
    }
}
export default Stops;