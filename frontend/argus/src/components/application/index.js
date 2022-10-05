// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import '../../App.css';

import React from 'react'
import Head from '../header'

import img from "./bg.jpg"

const Application = () => {
  return (
    <div style = {{
      backgroundImage: `url(${img})`,
      backgroundSize: 'cover',
      backgroundRepeat: `no-repeat`,
      height: '100vh',
      backgroundPosition: 'center',
    }}>

      <div>
        <Head />
      </div>
      
      <div id="map">    
        <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[51.505, -0.09]}>
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker>
        </MapContainer>
      </div>

    </div>
  )
}

export default Application