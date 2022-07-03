import React, { useState, useEffect }  from 'react';

const Home = () => {
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
        return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Loading...</div>;
    } else {
        return (
            <></>
        );
    }
}
export default Home;