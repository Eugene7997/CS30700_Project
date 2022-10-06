// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import '../../App.css';

import React, { useEffect, useState } from 'react'
import Head from '../header'
import L from "leaflet";
import img from "./bg.jpg"
import { LatLng } from "leaflet"
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';
import useFetch from "react-fetch-hook"
import axios from 'axios'




//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const {isLoading, error, data } = useFetch(`https://api.open-meteo.com/v1/forecast?latitude=${y}&longitude=${x}&current_weather=true`)
    const map = useMap()
    const { provider } = props
    

    //retrieve the temperature data from API
    const Temp = (x,y) => {
      setX(x);
      setY(y);
      return (JSON.parse(JSON.stringify(data)).current_weather.temperature);
    }

    //search the location by location_label
    useEffect(()  => {
        const searchControl = new GeoSearchControl({
            provider,
            autoComplete: true,
            showPopup: true,
            popupFormat: ({query, result}) => "Temperature: " + Temp(result.x, result.y).toString()
            // marker: {
            //   // optional: L.Marker    - default L.Icon.Default
            //   icon: new L.Icon.Default(),
            //   draggable: false,
            // },
        }).addTo(map)
        
        return () => map.removeControl(searchControl)
    }, [props])

    return null // don't want anything to show up from this comp
}

//function to retrieve user's current location
const CurrentLocation = () => {
    const [position, setPosition] = useState(null);
    const [bbox, setBbox] = useState([]);

    const map = useMap();

    useEffect(() => {
      map.locate().on("locationfound", function (e) {
        setPosition(e.latlng);
        map.flyTo(e.latlng, map.getZoom());
        const radius = e.accuracy;
        const circle = L.circle(e.latlng, radius);
        circle.addTo(map);
        setBbox(e.bounds.toBBoxString().split(","));
      });
    }, [map]);

    return position === null ? null : (
        <Marker position={position}>
          <Popup>
            You are here. <br />
            <b>SW lng</b>: {bbox[0]} <br />
            <b>SW lat</b>: {bbox[1]} <br />
            <b>NE lng</b>: {bbox[2]} <br />
            <b>NE lat</b>: {bbox[3]}
            
          </Popup>
        </Marker>
      );
}


const Application = () => {

  return (
    <div style = {{
      backgroundImage: `url(${img})`,
      // backgroundSize: 'cover',
      backgroundRepeat: `no-repeat`,
      height: '100vh',
      backgroundPosition: 'center',
      // alignContent: 'center',
      // justifyContent: 'center'
    }}>

      <div>
        <Head />
      </div>
      
      <div id="map">    
        <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {/* <Marker position={[51.505, -0.09]}> */}
            {/* <Popup>
              You are here <br />
              Temp: 0
            </Popup> */}
            <Search provider={new OpenStreetMapProvider()} />
            <CurrentLocation />
            
          {/* </Marker> */}
        </MapContainer>
      </div>

    </div>
  )
}

export default Application