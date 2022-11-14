import React from 'react'
import "./etlegendstyle.css"

const etlegend = () => {

    return (
        <div className="etlegend">
            <div style={{ "--color": '#f5363d' }}>Earthquake</div  >
            <div style={{ "--color": '#025fc9' }}>Tsunami Flag</div>
        </div>
    );
}

export default etlegend