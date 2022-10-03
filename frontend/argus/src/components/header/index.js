import React from 'react'
import Arugslogo from './logo.png'

const Head = () => {
    const handleClick = () => {
        alert("hello");
        console.log('div clicked');
    }
  return (
    <div style={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        
    }}>
        <div style={{
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            marginTop: '10px',
            marginLeft: '20px'
        }}>
            <img src={Arugslogo} alt="Logo" height={60} width={60} />
            <h1 style={{marginLeft: '10px', color: 'white'}}>Argus</h1>
        </div>
        <div onClick={() => handleClick()} style={{color:'white', marginRight: '20px'}}>
            About Us
        </div>
    </div>
  )
}

export default Head


