import React from 'react'
import "./chloropleth_legends_style.css"

const Chloropleth_legends = () => {

    return (
        <div className="chloropleth_legends">
            <div style={{ "--color": '#a50f15' }}>Hot</div  >
            <div style={{ "--color": '#de2d26' }}>mildly hot</div>
            <div style={{ "--color": '#fb6a4a' }}>warm</div>
            <div style={{ "--color": '#fc9272' }}>normal</div>
            <div style={{ "--color": '#fcbba1'}}>cold</div>
            <div style={{ "--color": '#fee5d9' }}>very cold</div>
        </div>
    );
}

export default Chloropleth_legends