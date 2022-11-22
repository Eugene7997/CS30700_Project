import React, { Component } from "react";
import Head from '../header'

class Notifcation extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <div className="formCenter">
                <Head />
                <form className="formFields">
                    <div className="formField">

                        <header className="formFieldHeader">
                            Temperature
                        </header>
                        <label className="formFieldLabel" htmlFor="tempgreaterthan">
                            Notification for Temperature Greater Than:
                        </label>
                        <input type="number" id="tempgreaterthan" className="formFieldInput" placeholder="Enter Temperature (F)"
                            name="tempgreaterthan" />
                        <label className="formFieldLabel" htmlFor="tempgreaterthan">
                            in
                        </label>
                        <select id="tempgreaterthanRegion" name="tempgreaterthanRegion" className="formFieldInput">
                            <option value="North America">North America</option>
                            <option value="South America">South America</option>
                            <option value="Asia">Asia</option>
                            <option value="Europe">Europe</option>
                            <option value="Africa">Africa</option>
                            <option value="Australia">Australia</option>
                            <option value="Antarctica">Antarctica</option>
                        </select>
                        <input type="submit"></input>

                    </div>
                </form>
            </div>
        )
    }
}

export default Notifcation