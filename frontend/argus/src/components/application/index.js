
// react-learn JS libraries
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import '../../App.css';

import React, { useEffect, useState, Component } from 'react'
import Head from '../header'
import L from "leaflet";
import img from "./bg.jpg"
import { LatLng } from "leaflet"
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';



// class Application extends Component {
//   state = {
//     lat: undefined,
//     lon: undefined,  
//     city: undefined,
//     temperatureC: undefined,
//     temperatureF: undefined,
//     icon: undefined,
//     sunrise: undefined,
//     sunset: undefined,
//     errorMessage: undefined,
//     APIKEY: "37cde85ed34605798aa360d4c26dc586"
//   }
//   getPosition = () => {
//     return new Promise(function (resolve, reject) {
//       navigator.geolocation.getCurrentPosition(resolve, reject);
//     });    
//   }

//   getWeather = async (latitude, longitude) => {
//     const apicall = await fetch(`//api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=37cde85ed34605798aa360d4c26dc586&units=metric`)
//     const data = await apicall.json();
//     this.setState({
//       lat: latitude,
//       lon: longitude,
//       city: data.name,
//       // temperatureC: Math.round(data.main.temp),
//       // temperatureF: Math.round(data.main.temp * 1.8 + 32),
//       // icon: data.weather[0].icon,
//     })
//   }

//   componentDidMount() {
//     this.getPosition()
//     .then((position) => {      
//       this.getWeather(position.coords.latitude, position.coords.longitude)
//       alert(position.coords.latitude);
//     })
    
//     .catch((err) => {
//       this.setState({ errorMessage: err.message });
//     });

//     this.timerID = setInterval(        
//       () => 
//       this.getWeather(this.state.lat, this.state.lon),
//       60000
//     );
//   }

//   componentWillUnmount() {
//     clearInterval(this.timerID);
//   }

//   render() {
//     return (
//       <div style = {{
//         backgroundImage: `url(${img})`,
//         // backgroundSize: 'cover',
//         backgroundRepeat: `no-repeat`,
//         height: '100vh',
//         backgroundPosition: 'center',
//         // alignContent: 'center',
//         // justifyContent: 'center'
//       }}>
  
//         <div>
//           <Head />
//         </div>
        
//         <div id="map">    
//           <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true}>
//             <TileLayer
//               attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//               url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//             />
//             {/* <Marker position={[51.505, -0.09]}> */}
//               {/* <Popup>
//                 You are here <br />
//                 Temp: 0
//               </Popup> */}
//               <Search provider={new OpenStreetMapProvider()} /> */}
//               <CurrentLocation />
//               {/* <Fetchdata /> */}
//             {/* </Marker> */}
//           </MapContainer>
//         </div>
  
//       </div>
//     )
//   }
// }

// export default Application;

//function to search location by name
const Search = (props)  => {
    const [x, setX] = useState(0);
    const [y, setY] = useState(0);
    // const [dt, setData] = useState();
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const map = useMap()
    const { provider } = props
    
    

    useEffect(() => {
      Fetchdata();
    }, [x,y])

    const Fetchdata = async() => {
      const APIKEY = "37cde85ed34605798aa360d4c26dc586"

      const apicall = await fetch(`//api.openweathermap.org/data/2.5/weather?lat=${y}&lon=${x}&appid=${APIKEY}&units=metric`)
      const dd = await apicall.json();
      console.log(dd);
      
      return (<Marker>
      <Popup>
        You are here. <br />
      </Popup>
    </Marker>)
      
    }

    //retrieve the temperature data from API
    const Temp = (result) => {
      setX(result.x);
      setY(result.y);
      // handleShow();
      // return result.label
    }

    //search the location by location_label
    useEffect(()  => {
        const searchControl = new GeoSearchControl({
            provider,
            autoComplete: true,
            showPopup: false,
            showMarker: false,
            popupFormat: ({query, result}) => Temp(result)
            // marker: {
            //   // optional: L.Marker    - default L.Icon.Default
            //   icon: new L.Icon.Default(),
            //   draggable: false,
            // },
        }).addTo(map)
        
        return () => map.removeControl(searchControl)
    }, [props])

    // useEffect(() => {
    //   Fetchdata();
    //   // const {isLoading, error, data } = useFetch(`https://api.open-meteo.com/v1/forecast?latitude=${y}&longitude=${x}&current_weather=true`)
    //   // Fetchdata()
    // }, [])

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
            {/* <Fetchdata /> */}
          {/* </Marker> */}
        </MapContainer>
      </div>

    </div>
  )
}

export default Application;
