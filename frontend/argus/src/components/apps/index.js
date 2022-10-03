
import React from 'react'
import { Button } from 'react-scroll'



const apps = () => {
    const handleClick = () => {
        alert("hello");
        console.log('div clicked');
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
       <button type='button' onClick={handleClick} style={{
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

export default apps