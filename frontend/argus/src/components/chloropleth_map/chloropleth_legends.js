import React from 'react'
import "./chloropleth_legends_style.css"

const Chloropleth_legends = (props) => {

    if (props.ea_type === "temperature") {
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
    else if (props.ea_type === "sea level") {
        return (
            <div className="chloropleth_legends">
                <div style={{ "--color": '#005D59' }}>High</div  >
                <div style={{ "--color": '#00746F' }}>mildly high</div>
                <div style={{ "--color": '#0CD1CA' }}>slightly high</div>
                <div style={{ "--color": '#1EE1DA' }}>normal</div>
                <div style={{ "--color": '#94F3EF'}}>low</div>
                <div style={{ "--color": '#CFFCFA' }}>very low</div>
            </div>
        );
    }
    else if (props.ea_type === "GHG") {
        return (
            <div className="chloropleth_legends">
                <div style={{ "--color": '#006834' }}>Dense</div  >
                <div style={{ "--color": '#009149' }}>mildly dense</div>
                <div style={{ "--color": '#00BE60' }}>slightly dense</div>
                <div style={{ "--color": '#00DA6F' }}>normal</div>
                <div style={{ "--color": '#A4ECC8'}}>sparse</div>
                <div style={{ "--color": '#C9EEDC' }}>very sparse</div>
            </div>
        )
    }
    else if (props.ea_type === "humidity") {
        return (
            <div className="chloropleth_legends">
                <div style={{ "--color": '#FF8300' }}>Highly Humid</div  >
                <div style={{ "--color": '#FE992D' }}>mildly Humid</div>
                <div style={{ "--color": '#FFA84B' }}>slightly Humid</div>
                <div style={{ "--color": '#FFBF7B' }}>normal</div>
                <div style={{ "--color": '#FFD7AC'}}>dry</div>
                <div style={{ "--color": '#FCE0C2' }}>very dry</div>
            </div>
        )
    }
    else {
        return null
    }

}

export default Chloropleth_legends