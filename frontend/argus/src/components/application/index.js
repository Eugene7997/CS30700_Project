
// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap, LayersControl } from 'react-leaflet'
import '../../App.css';
import React, { useEffect, useState, Component } from 'react'
import Head from '../header'
import L, { latLng, latLngBounds, map } from "leaflet";
import img from "./bg.jpg"
import streetMapTileIcon from "./streetMapImg.jpg"
import satelliteMapTileIcon from "./satelliteMapImg.png"
import minimalistMapIcon from "./minimalistMapImg.png"
import { LatLng } from "leaflet"
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';


window.choice = "temperature";

//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const [lab, setLabel] = useState(null);
    const [ea, setEA] = useState(window.choice)
    const map = useMap()
    const { provider } = props

    

    useEffect(() => {
      Fetchdata();
    }, [x,y, ea])
    

    //retrieve the EA data when user searched location
    const Fetchdata = async() => {
     const response = await fetch('http://127.0.0.1:8000/arg/api/', {
      method: 'POST',
      body : JSON.stringify({'latitude': y, 'longitude': x, 'EA': window.choice}),
      headers: {
        'Accept': 'application/json, text/plain',
        'Content-Type': 'application/json; charset=utf-8'
      }
    })
    const res = await response.json();
    if( x != 0 && y != 0){
      console.log(Date().toLocaleString()+ "\n"  +"Coordinate: " +x + ", " + y + "\n" + JSON.stringify(res))
      var measurement = null;
      if(window.choice == "temperature"){
        measurement = "°C"
      }else if(window.choice == "humid"){
        measurement = "%"
      }else if(window.choice == "sea"){
        measurement = "inch"
      }else{
        measurement = " (tons)"
      }
      L.marker([y,x]).bindPopup(Date().toLocaleString().substring(0, 24)+ "<br>"  +"Coordinate: " +x + ", " + y + "<br>" + JSON.stringify(res).replaceAll("{","").replaceAll("\"", "").replaceAll("}","").replace(":", "(").replace(":", "): ") + measurement).addTo(map)
    }
   }
      
    //search the location by location_label
    useEffect(()  => {
        const searchControl = new GeoSearchControl({
            provider,
            autoComplete: true,
            showPopup: false,
            showMarker: false,
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

//  const response = fetch('http://127.0.0.1:8000/arg/api/', {
//         method: 'POST',
//         body: JSON.stringify({
//             LatLng
//         }),
//         headers: {
//           'Accept': 'application/json, text/plain',
//           'Content-Type': 'application/json; charset=utf-8'
//         }

//  }).then(response => response.json())
//     .then(data => console.log(data))
//     .catch(error => console.log("Error detected: " + error));
  
   


      
      

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
  const handleChange = (e) => {
    console.log(e.target.value)
  }
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
      <form>
                <div style={{
                  marginTop: 10,
                  marginBottom: 10,
                  width: '100%'
                }}>
                    <div>
                        <select onChange={(event) => window.choice = event.target.value}>
                            <option value="temperature">Temperature</option>
                            <option value="sea">Sea Level</option>
                            <option value="GHG">GHG</option>
                            <option value="humid">Humidity</option>
                        </select>
                        <div class="overSelect" />
                    </div>
                </div>
          </form>
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
