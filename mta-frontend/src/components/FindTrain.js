import React, { useEffect, useState } from 'react'

function FindTrain() {

  // list of subway train lines
  const [allTrains, setAllTrains] = useState([]);
  // key, value store of train line : stations 
  const [allStations, setAllStations] = useState({})
  // key, value store of station id: direction labels
  const [allDirectionLabels, setAllDirectionLabels] = useState({});

  // currently selected train
  const [selectedTrain, setSelectedTrain] = useState()
  // stations of currently selected train line
  const [stations, setStations] = useState({});
  // id of selected station
  const [selectedStation, setSelectedStation] = useState();
  // list of upcoming trains for train line and station
  const [upcomingTrains, setUpcomingTrains] = useState([]);
  const [favoriteStations, setFavoriteStations] = useState([]);

  // bool to determine if should show upcoming trains
  const [showUpcomingTrains, setShowUpcomingTrains] = useState(false);
  // bool to determine if should show 'stations' dropdown
  const [showStations, setShowStations] = useState(false);
  // bool to deteremine if should should 'direction' drop down
  const [showDirections, setShowDirections] = useState(false);
  

  let url = 'http://localhost:5000/'
  useEffect(() => {
    
    url = url + 'stations'
    fetch(url)
      .then(res => res.json())
      .then((result) => {
        setAllTrains(Object.keys(result['train_stops']));
        setAllStations(result['train_stops']);
        setAllDirectionLabels(result['direction'])
        return
      })
  },[])

  const onChangeTrain = (event) => {
    event.preventDefault();
    let selectedTrain = event.target.value;
    let stationOptions = allStations[selectedTrain];    
    setShowStations(true);
    setSelectedTrain(selectedTrain);
    setStations(stationOptions);

  }

  const onChangeStation = (event) => {
    event.preventDefault();
    let stationId = event.target.value;
    setSelectedStation(stationId);
    setShowDirections(true);
  }

  const onChangeDirection = (event) => {
    event.preventDefault()

    let direction = event.target.value
    url = url + `trains/${selectedTrain}/${selectedStation}/${direction}`

    fetch(url)
      .then(res => res.json())
      .then((result) => {
        let r = []
        Object.keys(result).map(x => {
          return r.push(result[x])
        })
        setUpcomingTrains(r);
        setShowUpcomingTrains(true);
      })
  }

  const addStationToFavorites = (event) => {
    event.preventDefault();
    setFavoriteStations([...favoriteStations, selectedStation]);
  }

  let stationList;
  if (showStations) {
    stationList = (
      <select id="lang"  onChange={onChangeStation}>
        <option value="select"> Select Station! </option>
        {Object.keys(stations).map(id => {
          return <option value={id}> {stations[id]} </option>
        })}
       </select> 
    )
  }


  let directionList;
  if (showDirections) {
    directionList = (
      <div>
        <select id="lang" onChange={onChangeDirection} >
          <option value="Select"> Select Direction! </option>
        {allDirectionLabels[selectedStation.toString()].map((dir, index) => {
          if (dir !== 0) {
            return <option value={index === 0 ? 'N' : 'S'}> {dir} </option>
          } else {
            return;
          }
        })}
        </select>        
      </div>
    )
  }
  
  let trainList;
  if (showUpcomingTrains) {
    trainList = (
    <div>
      <ul>
        {upcomingTrains.map((t) => {
          return <li value={t}> {`${t} mins`} </li>
        })}
      </ul>
    </div>
    )
  }

  return (
    <div>
      <h1> Pick a subway line below:</h1>      
      <select id="lang" onChange={onChangeTrain} >
        <option value="select"> Select Train! </option>
        {allTrains.map(train => {
          return <option value={train}> {train} </option>
        })}
       </select> 
       <br />
      {stationList}
      {directionList}
      {trainList}
      <h4>Add station to favorites!</h4>
      <button onClick={addStationToFavorites} >Add</button>
    </div>
  )
}

export default FindTrain;