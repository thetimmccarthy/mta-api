import React, { useEffect, useState } from 'react'

function FindTrain() {

  const [stops, setStops] = useState([]);

  useEffect(() => {
    let url = 'http://localhost:5000/stations'
    
    fetch(url)
      .then(res => res.json())
      .then((result) => {
        let results = []
        for (const key in result) {
          results.push(result[key])
        }
        return setStops(results);
      })
  },[])

  return (
    <div>
      <h1> Pick a subway stop below:</h1>      
      <ul>
        {stops.map((stop) => {
          return <li>{stop}</li>
        })}
    
      </ul>
      <p>{}</p>
    </div>
  )
}

export default FindTrain;