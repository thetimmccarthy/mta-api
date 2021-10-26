import React, { useEffect, useState } from 'react'
import SingleStation from "./SingleStation";

function FavoriteStations({ stationIds, upcomingTrainsAtFavs }) {
    
    // const [upcomingTrainsAtFavs, setUpcomingTrainsAtFavs] = useState({})
    // const [stations, setStations] = useState(stationIds)
    // useEffect(() => {
        
    //     let url = 'http://localhost:5000/trains/' + stationIds.join(',');        
        
    //     if(stationIds.length > 0 ) {
    //         fetch(url)
    //             .then(res => res.json())
    //             .then((data) => {
    //                 setUpcomingTrainsAtFavs(data)
    //                 return
    //             })
    //         }
    // }, [])
    
    let favoriteStations;
    if (stationIds.length > 0) {
        
        favoriteStations = (
        <div>
            {stationIds.map(id => {
                if (id in upcomingTrainsAtFavs) {
                   return <SingleStation stationId={id} stationInfo={upcomingTrainsAtFavs[id]} />
                } else {
                    return <div>
                    <h4>
                        No favorites yet!
                    </h4>
                </div>
                }
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