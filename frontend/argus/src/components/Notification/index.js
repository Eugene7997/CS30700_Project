import React, { Component, useState } from "react";
import { json } from "react-router-dom";
import { v4 as uuidv4 } from 'uuid';
import Head from '../header'

function Notifcation() {

    const [email, setEmail] = useState(null);
    const [tempgreater, setTempGreater] = useState("");
    const [tempgreaterregion, setTempGreaterRegion] = useState("");
    const [templess, setTempLess] = useState("");
    const [templessregion, setTempLessRegion] = useState("");

    const [slgreater, setSLGreater] = useState("");
    const [slgreaterregion, setSLGreaterRegion] = useState("");
    const [slless, setSLLess] = useState("");
    const [sllessregion, setSLLessRegion] = useState("");

    const [humiditygreater, sethumidityGreater] = useState("");
    const [humiditygreaterregion, sethumidityGreaterRegion] = useState("");
    const [humidityless, sethumidityLess] = useState("");
    const [humiditylessregion, sethumidityLessRegion] = useState("");

    const [co2greater, setco2Greater] = useState("");
    const [co2greaterregion, setco2GreaterRegion] = useState("");
    const [co2less, setco2Less] = useState("");
    const [co2lessregion, setco2LessRegion] = useState("");

    const [no2greater, setno2Greater] = useState("");
    const [no2greaterregion, setno2GreaterRegion] = useState("");
    const [no2less, setno2Less] = useState("");
    const [no2lessregion, setno2LessRegion] = useState("");

    const [removeea, setRemoveEA] = useState(null);
    const [removeeavalue, setRemoveEAValue] = useState(null);
    const [removeearegion, setRemoveEARegion] = useState(null);
    const [removeeamode, setRemoveEAMode] = useState(null);

    const [region, setRegion] = useState(null)
    const [ea, setEA] = useState(null)
    const [mode, setMode] = useState(null)
    const [val, setVal] = useState(null)

    var d = {}
    const [list2, setList2] = useState([])
    const [displaylist, setDisplayList] = useState([])

    function handleAdd() {
        var add = true

        for (var l in displaylist) {
            if (displaylist[l].ea == ea && displaylist[l].region == region && displaylist[l].val == val && displaylist[l].mode == mode) {
                add = false
            }
        }

        if (add) {
            const d = { ea, mode, val, region }
            if (ea && mode && val && region) {
                setDisplayList((ls) => [...ls, d])
                setEA("")
                setMode("")
                setVal("")
                setRegion("")
            }
        }
        else {
            alert("Notification already added")
        }
    }
    
    function handleAdd23() {
        console.log(region, ea, "lll")
    }
    const hClick = m => {
        handleAdd()
        //submitNotification()
    }

    function handleRemove() {
        var remove = true
        for (var l in displaylist) {
            if (displaylist[l].ea == removeea && displaylist[l].region == removeearegion && displaylist[l].val == removeeavalue && displaylist[l].mode == removeeamode) {
                remove = false
                displaylist.splice(l, 1)
            }
        }
        //deleteNotification()
    }

    async function submitNotification() {
        const response = await fetch('http://127.0.0.1:8000/arg/notifications/', {
            method: 'POST',
            body: JSON.stringify({ 'email': email, 'ea': ea, 'region': region, 'threshold': parseFloat(val), 'mode': mode }),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json; charset=utf-8'
            }
        })
        var res = await response.json();
        console.log(res)
    }

    async function deleteNotification() {
        const response = await fetch('http://127.0.0.1:8000/arg/delete_notification/ ', {
            method: 'POST',
            body: JSON.stringify({ 'email': email, 'ea': removeea, 'region': removeearegion, 'threshold': parseFloat(removeeavalue), 'mode': removeeamode }),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json; charset=utf-8'
            }
        })
        var res = await response;
        console.log(JSON.stringify(res))
        //if (res.error )
    }

    async function listNotifications() {
        const response = await fetch('http://127.0.0.1:8000/arg/list_notifications/ ', {
            method: 'POST',
            body: JSON.stringify({ 'email': email }),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json; charset=utf-8'
            }
        })

    }

    const headerstyle = {
        color: "black",
        backgroundColor: "white",
        padding: "20px",
        marginLeft: 120,
        fontFamily: "Geneva"
    };

    const eastyle = {
        color: "grey",
        backgroundColor: "white",
        padding: "5px",
        marginLeft: 160,
        fontFamily: "system-ui"
    };

    const liststyle = {
        marginTop: "20px",
        color: "darkblue",
        backgroundColor: "transparent",
        padding: "5px",
        marginLeft: 120,
        fontFamily: "Geneva"
    };

    const buttonstyle = {
        marginTop: "10px",
    };



    return (
        <div className="formCenter">
            <Head />
            <form className="formFields" >
                <header className="formFieldHeader" style={headerstyle} >
                    Email
                </header>
                <input type="text" id="email" className="formFieldInput" placeholder="Enter Email"
                    name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </form>

            <header className="formFieldHeader" style={headerstyle} >
                Notifications Created
            </header>
            {
                displaylist.map((a) => <div>
                    <li style={liststyle}> When {a.ea} is {a.mode} than {a.val} in {a.region}</li>
                </div>)
            }

            <form className="formFields">
                <div className="formField">
                    <header className="formFieldHeader" style={headerstyle} >
                        Add New Notification
                    </header>
                    <select id="region" name="region" className="formFieldInput" value={region} onChange={(e) => setRegion(e.target.value)}>
                        <option value="">Select Region</option>
                        <option value="North America">North America</option>
                        <option value="South America">South America</option>
                        <option value="Asia">Asia</option>
                        <option value="Europe">Europe</option>
                        <option value="Africa">Africa</option>
                        <option value="Australia">Australia</option>
                        <option value="Antarctica">Antarctica</option>
                    </select>
                    <select id="ea" name="ea" className="formFieldInput" value={ea} onChange={(e) => setEA(e.target.value)}>
                        <option value="">Select Environmental Activity</option>
                        <option value="Temperature">Temperature</option>
                        <option value="Sea Level">Sea Level</option>
                        <option value="Humidity">Humidity</option>
                        <option value="CO2">Carbon Dioxide (CO2)</option>
                        <option value="NO2">Nitrogen Dioxide (NO2)</option>
                    </select>
                    <input type="number" id="val" className="formFieldInput" placeholder="Enter Threshold"
                        name="val" value={val} onChange={(e) => setVal(e.target.value)} />
                    <select id="mode" name="mode" className="formFieldInput" value={mode} onChange={(e) => setMode(e.target.value)}>
                        <option value="">Select Mode</option>
                        <option value="Greater">Greater</option>
                        <option value="Less">Less</option>
                    </select>
                </div>

                <button type="button" onClick={hClick} className="formFieldButton">Create</button>
            </form>


            <form className="formFields" onSubmit={handleRemove}>
                <div className="formField">
                    <header className="formFieldHeader" style={headerstyle} >
                        Remove Notification
                    </header>

                    <select id="removedEARegion" name="removedEARegion" className="formFieldInput" value={removeearegion} onChange={(e) => setRemoveEARegion(e.target.value)}>
                        <option value="">Select Region</option>
                        <option value="North America">North America</option>
                        <option value="South America">South America</option>
                        <option value="Asia">Asia</option>
                        <option value="Europe">Europe</option>
                        <option value="Africa">Africa</option>
                        <option value="Australia">Australia</option>
                        <option value="Antarctica">Antarctica</option>
                    </select>

                    <select id="removedEA" name="removedEA" className="formFieldInput" value={removeea} onChange={(e) => setRemoveEA(e.target.value)}>
                        <option value="">Select Environmental Activity</option>
                        <option value="Temperature">Temperature</option>
                        <option value="Sea Level">Sea Level</option>
                        <option value="Humidity">Humidity</option>
                        <option value="CO2">Carbon Dioxide (CO2)</option>
                        <option value="NO2">Nitrogen Dioxide (NO2)</option>
                    </select>

                    <input type="number" id="removedEAValue" className="formFieldInput" placeholder="Enter Threshold"
                        name="removedEAValue" value={removeeavalue} onChange={(e) => setRemoveEAValue(e.target.value)} />

                    <select id="removedEAMode" name="removedEAMode" className="formFieldInput" value={removeeamode} onChange={(e) => setRemoveEAMode(e.target.value)}>
                        <option value="">Select Mode</option>
                        <option value="Greater">Greater</option>
                        <option value="Less">Less</option>
                    </select>

                    <button type="button" onClick={() => handleRemove()} className="formFieldButton" style={buttonstyle}>Remove</button>
                </div>
            </form>

        </div>
    )

}

export default Notifcation