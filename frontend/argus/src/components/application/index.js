
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
import earthquakedatas from './earthquake_plot/Past7days.json'
import Chloropleth_legends from '../chloropleth_map/chloropleth_legends';
import moment from 'moment'

window.choice = "temperature";
window.date = moment().format('YYYY-MM-DD')

//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    const [lab, setLabel] = useState(null);
    const [ea, setEA] = useState(window.choice)
    const map = useMap()
    const { provider } = props
    
    const [co2Value, setCo2Value] = useState("")
    const [no2Value, setNo2Value] = useState("")
    const [ozoneValue, setOzoneValue] = useState("")    

    useEffect(() => {
      Fetchdata();
    }, [x,y,ea])

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
      var measurement = null
      if(window.choice == "temperature"){
        measurement = "°C"
      } else if (window.choice == "humid"){
        measurement = "%"
      } else if (window.choice == "sea"){
        measurement = "inch"
      } else {
        measurement = " (tons)"
        var temp = JSON.stringify(res[Object.keys(res)[0]])
        var co2 = temp.match(/(?<=CO2: )\d+.\d+/)
        if (co2 != null) {
          setCo2Value(co2[0]+measurement)
        }
        var o3 = temp.match(/(?<=Ozone\(O3\): )\d+.\d+/)
        if (o3 != null) {
          setOzoneValue(o3[0]+measurement)
        }
        var no2 = temp.match(/(?<=NO2: )\d+.\d+/)
        if (no2 != null) {
          setNo2Value(no2[0]+measurement)
        }
        return
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
      <LayersControl.Overlay name="CO2" checked>
        <LayerGroup>
          {(x!=0 && y!=0) &&
            <Marker position = {[y,x]}>
              <Popup>
                {Date().toLocaleString().substring(0, 24)} <br/>
                Coordinate: {x} , {y} <br/> 
                CO2 value : <b>{co2Value}</b>
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
                {Date().toLocaleString().substring(0, 24)} <br/>
                Coordinate: {x} , {y} <br/> 
                Ozone value: <b>{ozoneValue}</b>
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
                {Date().toLocaleString().substring(0, 24)} <br/>
                Coordinate: {x} , {y} <br/> 
                NO2 value : <b>{no2Value}</b>
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

const Earthquake = () => {

  const onEachFeature= (feature, layer)=> {
    console.log(feature)
    const tsunamicheck = feature.properties.tsunami
    const mag = feature.properties.mag
    const place = feature.properties.place
    if (tsunamicheck == 0) {
      layer.bindPopup(`<strong>Earthquake <br/> Magntitude: ${mag} <br/> Location: ${place} </strong>`)
    }
    else {
      layer.bindPopup(`<strong>Tsunami Flag <br/> Magntitude: ${mag} <br/> Location: ${place} </strong>`)
    }
  }
  
  return (
    <LayersControl>
      <LayersControl.Overlay name = "Earthquake Layer">
        {earthquakedatas && (<GeoJSON data = {earthquakedatas} onEachFeature={onEachFeature}/>)}
      </LayersControl.Overlay>
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
            width: '100%',

          }}>
              <div>
                  <select style={{width: 100}} onChange={(event) => window.choice = event.target.value}>
                    <option value="temperature">Temperature</option>
                    <option value="sea">Sea Level</option>
                    <option value="GHG">GHG</option>
                    <option value="humid">Humidity</option>
                  </select>
                  <input type="date" onChange={e => window.date = e.target.value} max={moment().add(3, 'month').format("YYYY-MM-DD")} min={moment().subtract(3, 'month').format("YYYY-MM-DD")}/>
              </div>
            <div/>       
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
          <Earthquake/>
          <Search provider={new OpenStreetMapProvider()} />
          <CurrentLocation />
        </MapContainer>
      </div>
    </div>
  )
}

export default Application;
