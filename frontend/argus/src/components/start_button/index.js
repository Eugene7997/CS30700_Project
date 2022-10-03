
import React from 'react'
import { Button } from 'react-scroll'
import { useNavigate } from "react-router-dom";


const Start = () => {
    let Navi = useNavigate();
    const Navito = () => {
        Navi("application")
    }

    return (
    <div style={{
        color: 'white',
        fontSize: '100px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: '30%'
    }}>
       <button type='button' onClick={Navito} style={{
        fontSize: '60px',
        backgroundColor: 'transparent',
        borderBlockColor: 'transparent',
        borderBlockEndColor: 'transparent',
        color:'white',
        border: 'none'
       }}>
            Click to start
       </button>
    </div>
  )
}

export default Start