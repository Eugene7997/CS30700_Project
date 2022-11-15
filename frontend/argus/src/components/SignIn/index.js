import React, { Component } from "react";
import { Link,useNavigate, Navigate } from "react-router-dom";
import Head from '../header'


class SignInForm extends Component {
  constructor() {
    super();

    this.state = {
      Username: "",
      password: "",
      token: null,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    let target = event.target;
    let value = target.type === "checkbox" ? target.checked : target.value;
    let name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log("The form was submitted with the following data:");
    console.log(this.state);
    this.setState({submitted: true})
    this.props.navigation.navigate('/')
    
  }
  async authentication() {
    //POST request to the backend
    // const response = await fetch('http://127.0.0.1:8000/arg/auth/', {
    //   method: 'POST',
    //   body : JSON.stringify({'authentication': 'true', 'email':this.state.email, 'password':this.state.password}),
    //   headers: {
    //     'Accept': 'application/json, text/plain',
    //     'Content-Type': 'application/json; charset=utf-8'
    //   }
    // })
    // var res = await response.json();
    // res = JSON.stringify(res) 
    // this.setState({token : res})
    // if(!res){
    //   alert("Wrong email address or password. Please try again.")
    // }
    //globally reset whether user sign in

    
    const user_data = this.state.Username + " " + "res"
    localStorage.setItem("user", user_data)
    const saved = localStorage.getItem("user")
    console.log(JSON.stringify(saved))
    this.setState({token : "res"})
  }

  render() {
    return (
      <div className="formCenter">
        <Head />
        <form className="formFields" onSubmit={this.handleSubmit}>
          <div className="formField">
            <label className="formFieldLabel" htmlFor="email">
              Username
            </label>
            <input
              type="text"
              id="email"
              className="formFieldInput"
              placeholder="Enter your Username"
              name="email"
              defaultvalue={this.state.Username}
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
              onChange={this.handleChange}
            />
          </div>

          <div className="formField">
            <Link onClick={() => this.authentication()} className="formFieldButton">Sign In</Link>
            {this.state.token != null && (
              <Navigate to='/' replace={true} />
            )}
            <Link style={{marginLeft: 20}} to="/signup" className="formFieldLink">
              Create an account
            </Link>
          </div>

        </form>
      </div> 
    );
  }
}

export default SignInForm;

