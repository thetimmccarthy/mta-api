import React, { useEffect, useState } from 'react'
import SingleStation from "./SingleStation";

function FavoriteStations({ stationIds }) {

    const [upcomingTrainsAtFavs, setUpcomingTrainsAtFavs] = useState({})
    const [stations, setStations] = useState(stationIds)
    useEffect(() => {
        console.log("IDs:", stationIds)
        let url = 'http://localhost:5000/trains/' + stations.join(',');        
        
        if(stations.length > 0 ) {
            fetch(url)
                .then(res => res.json())
                .then((data) => {
                    setUpcomingTrainsAtFavs(data)
                    return
                })
            }
    }, [stations])
    
    let favoriteStations;
    if (stations.length > 0 ) {
        console.log('STATIONS: ', stationIds)
        favoriteStations = (
        <div>
            {stations.map(id => {
                return <SingleStation stationId={id} stationInfo={upcomingTrainsAtFavs[id]} />
                })}
        </div>
        )
    } else {
        favoriteStations = (
        <div>
            <h4>
                No favorites yet!
            </h4>
        </div>
        )
    }

    return (
        <div>
            {favoriteStations}
       </div>
    )
    
}

export default FavoriteStations;