import React, { Component } from "react";
import { Link, Navigate, useHistory } from "react-router-dom";
import Head from "../header"

class SignUpForm extends Component {
  constructor() {
    super();

    this.state = {
      email: "",
      password: "",
      name: "",
      hasAgreed: false,
      check: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleChange2 = this.handleChange2.bind(this);
    this.handleChange3 = this.handleChange3.bind(this);
    // this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    let target = event.target;
    let value = target.type === "checkbox" ? target.checked : target.value;
    let name = target.name;
    
    this.setState({
      name: value
    });
  }
  handleChange2(event){
    let target = event.target;
    let value = target.type === "checkbox" ? target.checked : target.value;
    let name = target.name;

    this.setState({
      password: value
    });
  }
  handleChange3(event){
    let target = event.target;
    let value = target.type === "checkbox" ? target.checked : target.value;
    let name = target.name;

    this.setState({
      email: value
    });
  }

  // handleSubmit(e) {
  //   e.preventDefault();

  //   console.log("The form was submitted with the following data:");
  //   console.log(this.state);
  // }

  async authentication() {
    console.log(this.state)
    if(!this.state.hasAgreed){
      alert("Please agree the notifications via email")
    }else{
      const response = await fetch('http://127.0.0.1:8000/arg/create/', {
        method: 'POST',
        body : JSON.stringify({'email':this.state.email, 'password':this.state.password, 'username' : this.state.name}),
        headers: {
          'Accept': 'application/json, text/plain',
          'Content-Type': 'application/json; charset=utf-8'
        }
      })
      var res = await response.json();
      //res = JSON.stringify(res) 
      if("error" in res){
        alert(res["error"])
      }else if ("success" in res){
        //globally reset whether user sign in
        //const user_data = this.state.Username + " " + res
        sessionStorage.setItem("email", this.state.email)
        localStorage.setItem("user", this.state.email)
        alert(res["success"])
        this.setState({check: true})
      } else {
        alert("failed to connect to backend")
      }
      this.setState({token : res})
    }
  }

  render() {
    return (
      <div className="formCenter">
        <Head />
        <form className="formFields">
          <div className="formField">
            <label className="formFieldLabel" htmlFor="name">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              className="formFieldInput"
              placeholder="Enter your Username"
              name="name"
              value={this.state.name}
              onChange={this.handleChange}
            />
          </div>
          <div className="formField">
            <label className="formFieldLabel" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="formFieldInput"
              placeholder="Enter your password"
              name="password"
              value={this.state.password}
              onChange={this.handleChange2}
            />
          </div>
          <div className="formField">
            <label className="formFieldLabel" htmlFor="email">
              E-Mail Address
            </label>
            <input
              type="email"
              id="email"
              className="formFieldInput"
              placeholder="Enter your email"
              name="email"
              value={this.state.email}
              onChange={this.handleChange3}
            />
          </div>

          <div className="formField">
            <label className="formFieldCheckboxLabel">
              <input
                className="formFieldCheckbox"
                type="checkbox"
                name="hasAgreed"
                value={this.state.hasAgreed}
                onChange={() => this.setState({hasAgreed: !this.state.hasAgreed})}
              />{" "}
              I agree to get notifications via email
            </label>
          </div>

          <div className="formField">
            <Link onClick={() => this.authentication()} className="formFieldButton">Sign Up</Link>
            {
                this.state.check ? <Navigate to={'/'} replace={true} /> : null
            }
            <Link style={{marginLeft: 20}} to="/signin" className="formFieldLink">
              I'm already member
            </Link>
          </div>
        </form>
      </div>
    );
  }
}
export default SignUpForm;
