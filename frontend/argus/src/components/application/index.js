// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import '../../App.css';

import React from 'react'
import Head from '../header'

const Application = () => {
  return (
    <div>
      <div style = {{
          backgroundColor: 'black',
          opacity: '0.8'
      }}>
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