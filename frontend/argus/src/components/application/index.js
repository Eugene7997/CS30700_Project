
// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap, LayersControl, LayerGroup, Circle } from 'react-leaflet'
import '../../App.css';
import React, { useEffect, useState, Component } from 'react'
import Head from '../header'
import L, { latLng, latLngBounds } from "leaflet";
import img from "./bg.jpg"
import streetMapTileIcon from "./streetMapImg.jpg"
import satelliteMapTileIcon from "./satelliteMapImg.png"
import minimalistMapIcon from "./minimalistMapImg.png"
import { LatLng } from "leaflet"
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';



//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const [lab, setLabel] = useState(null);
    const map = useMap()
    const { provider } = props
    
    const [co2Value, setCo2Value] = useState(0)
    const [no2Value, setNo2Value] = useState(0)
    const [ozoneValue, setOzoneValue] = useState(0)

    useEffect(() => {
      //Fetchdata();
      Fetchdata2();
    }, [x,y])


    //retrieve the temperature and weather data when user searched location
    //const Fetchdata = async() => {
     // const APIKEY = "37cde85ed34605798aa360d4c26dc586"
     // const apicall = await fetch(`//api.openweathermap.org/data/2.5/weather?lat=${y}&lon=${x}&appid=${APIKEY}&units=metric`)
      //const dd = await apicall.json();
     // console.log(
      //  "Label: " + lab + "\n"
     // + "Temp: " + dd.main.temp + "\n"
     // + "Temp (feels like): " + dd.main.feels_like + "\n"
     // + "Temp (min): " + dd.main.temp_min + "\n"
     // + "Temp (max): " + dd.main.temp_max + "\n"
     // + "Pressure: " + dd.main.pressure +"\n"
     // + "Temp: " + dd.main.temp +"\n"
     // + "Temp: " + dd.main.temp + "\n"
     // + "Weather: " + dd.weather[0].main+ "\n"
     // + "Detailed weather: " + dd.weather[0].description);
    // }

   const Fetchdata2 = async() => {
    // Eric's key
    const response = await fetch(`https://api.co2signal.com/v1/latest?lon=${x}&lat=${y}&auth-token=S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55`)
    const response2 = await fetch(`https://api.ambeedata.com/latest/by-lat-lng?lat=${y}&lng=${x}&x-api-key=b1637cd664e7dce01cbd651b44e311e27b269c4717eb903fe290388116354b69`)

    // const response = await fetch(`https://api.co2signal.com/v1/latest?lon=${x}&lat=${y}&auth-token=GKntl9oAJF4H0asImg3MpjSXiIdmLAcU`)
    // const response2 = await fetch(`https://api.ambeedata.com/latest/by-lat-lng?lat=${y}&lng=${x}&x-api-key=97b6df2236ea4855729d070695e4dfa664a62b0e8f0e432ca94f78de78e7ee7d`)
    const res = await response.json();
    const res2 = await response2.json();
    
    const temp1 = res['data'].carbonIntensity
    const temp2 = res2['stations'][0].OZONE
    const temp3 = ['stations'][0].NO2

    console.log("carbon intensity: ", temp1)
    console.log("Ozone: ", temp2)
    console.log("NO2: ", temp3)
    
    setCo2Value(temp1)
    setNo2Value(temp2)
    setOzoneValue(temp3)

  }

   let data = {
    'latitude': y,
    'longitude': x
   }

  //creating react post request and fetching data from django
  const response = fetch('http://127.0.0.1:8000/arg/api/', {
    method: 'POST',
    body : JSON.stringify(data),
    headers: {
      'Accept': 'application/json, text/plain',
      'Content-Type': 'application/json; charset=utf-8'
    }


  }).then(response => response.json())
  .then(data => console.log(JSON.stringify(data)))
  .catch(error => console.log("Error detected: " + error));


    useEffect(()  => {
        
        const searchControl = new GeoSearchControl({
            provider,
            autoComplete: true,
            showPopup: false,
            showMarker: true,
            popupFormat: ({query, result}) => {
              setX(result.y); 
              setY(result.x);
              setLabel(result.label);
              return result.label;
            }
            
        }).addTo(map)
        return () => map.removeControl(searchControl)
    }, [props])

    // return  null // don't want anything to show up from this comp
    return (
      <LayersControl>
        <LayersControl.Overlay name="CO2">
            <LayerGroup>
              {(x!=0 && y!=0) &&
                <Marker position = {[x,y]}>
                  <Popup>
                    CO2 value : {co2Value} {console.log("CO2 value : ",co2Value)}
                  </Popup>
                </Marker>
              }
            </LayerGroup>
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Ozone">
          <LayerGroup >
            {(x!=0 && y!=0) &&
              <Marker position = {[x,y]}>
                <Popup>
                  Ozone value: {ozoneValue} {console.log("Ozone value : ",ozoneValue)}
                </Popup>
              </Marker>
            }
          </LayerGroup>
        </LayersControl.Overlay>
        <LayersControl.Overlay name="NO2">
          <LayerGroup>
            {(x!=0 && y!=0) &&
              <Marker position = {[x,y]}>
                <Popup>
                  NO2 value : {no2Value} {console.log("NO2 value : ",no2Value)}
                </Popup>
              </Marker>
            }
          </LayerGroup>
        </LayersControl.Overlay>
      </LayersControl>
    )
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
            <b>NE lat</b>: {bbox[3]} <br />
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
