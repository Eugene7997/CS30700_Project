import React from 'react'
import "./etlegendstyle.css"

const ETlegendtest = () => {

    return (
        <div className="etlegendstyle">
            <div style={{ "--color": '#f5363d' }}>Earthquake</div  >
            <div style={{ "--color": '#025fc9' }}>Tsunami Flag</div>
        </div>
    );
}

export default ETlegendtest