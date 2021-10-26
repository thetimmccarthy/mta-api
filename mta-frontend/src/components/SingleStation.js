import React from 'react'

function SingleStation({ stationId, stationInfo }) {

    return (
        <div>
            <h4>
                {stationInfo['stop_name']}
            </h4>
            <div>
                <p> Trains coming at the following times:</p>
                <ul>
                    {stationInfo['trains'].map(train => {
                        return <li> {`${train[1]} train @ ${train[2]}`} </li>
                    })}
                </ul>
            </div>
        </div>
    )
}

export default SingleStation;