import React from 'react'
import img from "./bg.jpg"
import Head from '../header'
import Apps from '../apps'


const Iphone = () => {
  return (
    <div style = {{
        backgroundImage: `url(${img})`,
        backgroundSize: 'cover',
        backgroundRepeat: `no-repeat`,
        height: '100vh',
        backgroundPosition: 'center',
        // alignItems: 'center',
        // justifyContent: 'center',
    }}>
        <Head />
        <Apps />
    </div>
  )
}

export default Iphone
