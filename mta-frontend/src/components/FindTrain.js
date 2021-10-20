import React, { useEffect, useState } from 'react'

function FindTrain() {

  const [trains, setTrains] = useState([]);
  const [allStations, setAllStations] = useState({})
  const [stations, setStations] = useState({});
  const [showStations, setShowStations] = useState(false);
  useEffect(() => {
    let url = 'http://localhost:5000/stations'
    
    fetch(url)
      .then(res => res.json())
      .then((result) => {
        setTrains(Object.keys(result));
        setAllStations(result);
        return
      })
  },[])

  const onChangeTrain = (event) => {
    event.preventDefault();
    let selectedTrain = event.target.value;
    let stationOptions = allStations[selectedTrain];    
    setShowStations(true);
    setStations(stationOptions)

  }

  let stationList;
  if (showStations) {
    stationList = (
      <select id="lang"  >
        <option value="select"> Select Station! </option>
        {Object.keys(stations).map(id => {
          return <option value={id}> {stations[id]} </option>
        })}
       </select> 
    )
  }

  return (
    <div>
      <h1> Pick a subway line below:</h1>      
      <select id="lang" onChange={onChangeTrain} >
        <option value="select"> Select Train! </option>
        {trains.map(train => {
          return <option value={train}> {train} </option>
        })}
       </select> 
       <br />
      {stationList}

      
      <p>{}</p>
    </div>
  )
}

export default FindTrain;