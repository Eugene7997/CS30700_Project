
// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap, LayersControl, GeoJSON, LayerGroup, Circle } from 'react-leaflet'
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
import geoDatas from '../chloropleth_map/annualTemperatureOfCountyUSA.json'
import Chloropleth_legends from '../chloropleth_map/chloropleth_legends';

window.choice = "temperature";

//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const [lab, setLabel] = useState(null);
    const [ea, setEA] = useState(window.choice)
    const map = useMap()
    const { provider } = props
    
    const [co2Value, setCo2Value] = useState(0)
    const [no2Value, setNo2Value] = useState(0)
    const [ozoneValue, setOzoneValue] = useState(0)    

    useEffect(() => {
      Fetchdata();
      Fetchdata2();
    }, [x,y,ea])

   const Fetchdata2 = async() => {
    // Eric's key
    const response = await fetch(`https://api.co2signal.com/v1/latest?lon=${x}&lat=${y}&auth-token=S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55`)
    const response2 = await fetch(`https://api.ambeedata.com/latest/by-lat-lng?lat=${y}&lng=${x}&x-api-key=b1637cd664e7dce01cbd651b44e311e27b269c4717eb903fe290388116354b69`)

    // https://api.co2signal.com/v1/latest?countryCode=DK-DK1&lon=-0.05153279397682829&lat=51.325478033406156&auth-token=GKntl9oAJF4H0asImg3MpjSXiIdmLAcU
    // https://api.ambeedata.com/latest/by-lat-lng?lat=51.325478033406156&lng=-0.05153279397682829&x-api-key=97b6df2236ea4855729d070695e4dfa664a62b0e8f0e432ca94f78de78e7ee7d

    // const response = await fetch(`https://api.co2signal.com/v1/latest?countryCode=DK-DK1&lon=${x}&lat=${y}&auth-token=GKntl9oAJF4H0asImg3MpjSXiIdmLAcU`)
    // const response2 = await fetch(`https://api.ambeedata.com/latest/by-lat-lng?lat=${y}&lng=${x}&x-api-key=97b6df2236ea4855729d070695e4dfa664a62b0e8f0e432ca94f78de78e7ee7d`)
    const res = await response.json();
    const res2 = await response2.json();
    
    const temp1 = res['data'].carbonIntensity
    const temp2 = res2['stations'][0].OZONE
    const temp3 = res2['stations'][0].NO2

    console.log("carbon intensity: ", temp1)
    console.log("Ozone: ", temp2)
    console.log("NO2: ", temp3)
    
    setCo2Value(temp1)
    setOzoneValue(temp2)
    setNo2Value(temp3)
  }

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
      } else if (window.choice == "humid"){
        measurement = "%"
      } else if (window.choice == "sea"){
        measurement = "inch"
      } else {
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

  return (
    <LayersControl>
      <LayersControl.Overlay name="CO2">
        <LayerGroup>
          {(x!=0 && y!=0) &&
            <Marker position = {[y,x]}>
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
            <Marker position = {[y,x]}>
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
            <Marker position = {[y,x]}>
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

//function to retrieve user's current location
const CurrentLocation = () => {
  const [position, setPosition] = useState(null)
  const [bbox, setBbox] = useState([])
  const map = useMap()

  useEffect(() => {
    map.locate().on("locationfound", function (e) {
      setPosition(e.latlng)
      // alert(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
      const radius = e.accuracy
      const circle = L.circle(e.latlng, radius)
      circle.addTo(map)
      setBbox(e.bounds.toBBoxString().split(","))
    });
  }, [map])

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
  )
}

const ChoroplethMap = () => {

  const [legendToggle, setLegendToggle] = useState(false)
  
  const highlightChloropleth = (e => {
    var layer = e.target
    layer.setStyle({
      weight: 1,
      color: "black",
      fillOpacity: 1
    })
  })

  const resetHighlight= (e =>{
    e.target.setStyle(chloropleth_style(e.target.feature));
  })

  const onEachFeature= (feature, layer)=> {
    console.log(feature)
    const name = feature.properties.NAME
    const temp_celsius = feature.properties.tempchg_c
    layer.bindPopup(`<strong>name: ${name} <br/> temp change in celsius: ${temp_celsius} </strong>`)
    layer.on({
      mouseover: highlightChloropleth,
      mouseout: resetHighlight,
    })
  }

  const mapPolygonColorToDensity=(value => {
    return value > 1
      ? '#a50f15'
      : value > 0.75
      ? '#de2d26'
      : value > 0.50
      ? '#fb6a4a'
      : value > 0.25
      ? '#fc9272'
      : value > 0
      ? '#fcbba1'
      : '#fee5d9';
  })

  const chloropleth_style = (feature => {
    return ({
      fillColor: mapPolygonColorToDensity(feature.properties.tempchg),
      weight: 1,
      opacity: 1,
      color: 'white',
      dashArray: '2',
      fillOpacity: 0.5
    })
  })
  
  return (
    <LayersControl>
      <LayersControl.Overlay name = "Choropleth map - Temperature">
        <LayerGroup
          eventHandlers = {
            {
              add:() => {
                setLegendToggle(true)
              },
              remove:() => {
                setLegendToggle(false)
              }
            }
          }
        >
          {geoDatas && (<GeoJSON data = {geoDatas} onEachFeature={onEachFeature} style = {chloropleth_style}/>)}
        </LayerGroup>
      </LayersControl.Overlay>
      {legendToggle ? <Chloropleth_legends/> : null}
    </LayersControl>
  )
}

const {BaseLayer} = LayersControl

const Application = () => {
  
  const mapStyle = {
    margin: '0 auto',
  }

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
        <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true} style={mapStyle}>
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
          <ChoroplethMap/>
          <Search provider={new OpenStreetMapProvider()} />
          <CurrentLocation />
        </MapContainer>
      </div>
    </div>
  )
}

export default Application;
