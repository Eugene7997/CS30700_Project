import React from 'react'
// import chloropleth_legends_styles from "./chloropleth_legends_styles.css"
import "./chloropleth_legends_style.css"

const Chloropleth_legends = () => {

    // const chloropleth_legends_style = {
    //     "position":"fixed",
    //     "zIndex":"999",
    //     "right":"5px",
    //     "bottom":"25px",
    //     "padding":"20px 10px",
    //     "boxShadow":"0 0 5px 0 rgba(184, 140, 140, 0.3)",
    //     "fontSize":"12px","letterSpacing":"2px",
    //     "background":"rgba(0,0,0,0.8)",
    //     "borderRadius":"5px",
    //     "width":"16%"
    // }
    
    return (
        // <div className="chloropleth_legends" style={chloropleth_legends_style}>
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