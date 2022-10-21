
// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap, LayersControl } from 'react-leaflet'
import '../../App.css';
import React, { useEffect, useState, Component } from 'react'
import Head from '../header'
import L from "leaflet";
import img from "./bg.jpg"
import streetMapTileIcon from "./streetMapImg.jpg"
import satelliteMapTileIcon from "./satelliteMapImg.png"
import minimalistMapIcon from "./minimalistMapImg.png"

import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';



//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const [lab, setLabel] = useState(null);
    const map = useMap()
    const { provider } = props

    useEffect(() => {
      Fetchdata();
    }, [x,y])


    //retrieve the temperature and weather data when user searched location
    const Fetchdata = async() => {
      const APIKEY = "37cde85ed34605798aa360d4c26dc586"
      const apicall = await fetch(`//api.openweathermap.org/data/2.5/weather?lat=${y}&lon=${x}&appid=${APIKEY}&units=metric`)
      const dd = await apicall.json();
      console.log(
        "Label: " + lab + "\n"
      + "Temp: " + dd.main.temp + "\n"
      + "Temp (feels like): " + dd.main.feels_like + "\n"
      + "Temp (min): " + dd.main.temp_min + "\n"
      + "Temp (max): " + dd.main.temp_max + "\n"
      + "Pressure: " + dd.main.pressure +"\n"
      + "Temp: " + dd.main.temp +"\n"
      + "Temp: " + dd.main.temp + "\n"
      + "Weather: " + dd.weather[0].main+ "\n"
      + "Detailed weather: " + dd.weather[0].description);
      
      
    }

      
    //search the location by location_label
    useEffect(()  => {
        const searchControl = new GeoSearchControl({
            provider,
            autoComplete: true,
            showPopup: false,
            showMarker: true,
            popupFormat: ({query, result}) => {
              setX(result.x); 
              setY(result.y);
              setLabel(result.label);
              return result.label;
            }
            
        }).addTo(map)
        return () => map.removeControl(searchControl)
    }, [props])


    return  null // don't want anything to show up from this comp
}

 const response = fetch('http://127.0.0.1:8000/arg/api/', {
        method: 'POST',
        body: JSON.stringify({
            LatLng
        }),
        headers: {
          'Accept': 'application/json, text/plain',
          'Content-Type': 'application/json; charset=utf-8'
        }

 }).then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log("Error detected: " + error));
  
   


      
      

//function to retrieve user's current location
const CurrentLocation = () => {
    const [position, setPosition] = useState(null);
    const [bbox, setBbox] = useState([]);

    const map = useMap();

    useEffect(() => {
      map.locate().on("locationfound", function (e) {
        setPosition(e.latlng);
        // alert(e.latlng);
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

const {BaseLayer} = LayersControl

const Application = () => {

  return (
    <div style = {{
      backgroundImage: `url(${img})`,
      backgroundRepeat: `no-repeat`,
      height: '100vh',
      backgroundPosition: 'center',
    }}>

      <div>
        <Head />
      </div>
      
      <div id="map">    
        <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true}>
          <LayersControl>
            <BaseLayer checked name={`<img src=${streetMapTileIcon} alt="street" width=100/>`}> 
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
                subdomains={['mt1','mt2','mt3']}
              />
            </BaseLayer>
            <BaseLayer name={`<img src=${satelliteMapTileIcon} alt="satellite" width=100/>`}> 
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
                subdomains={['mt1','mt2','mt3']}
              />
            </BaseLayer>
            <BaseLayer name={`<img src=${minimalistMapIcon} alt="minimalist" width=100/>`}> 
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}"
                subdomains='abcd'
                ext= 'png'
              />
            </BaseLayer>
          </LayersControl>
          <Search provider={new OpenStreetMapProvider()} />
          <CurrentLocation />
        </MapContainer>
      </div>
    </div>
  )
}

export default Application;
