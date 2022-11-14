import React, { Component } from "react";
import { Link } from "react-router-dom";
import { useNavigate, Navigate } from "react-router-dom";

// function Submit(event){
//   event.preventDefault();
//   console.log("The form was submitted with the following data:");
//   console.log(this.state);
//   this.setState({submitted: true})
//   let navigate = useNavigate()
//   navigate.navigate('/')
// }
// const Submit = (event) => {
//   event.preventDefault();
//   console.log("The form was submitted with the following data:");
//   console.log(this.state);
//   this.setState({submitted: true})
//   let navigate = useNavigate()
//   navigate.navigate('/')
// }

class SignInForm extends Component {
  constructor() {
    super();

    this.state = {
      email: "",
      password: "",
      submitted: false,
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

  render() {
    // {this.state.submitted ? <Navigate to={'/'}/> : 
    return (
      <div className="formCenter">
        <form className="formFields" onSubmit={this.handleSubmit}>
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
            <Link to='/' className="formFieldButton">Sign In</Link>
            <Link to="/signup" className="formFieldLink">
              Create an account
            </Link>
          </div>

        </form>
      </div> 
    );
  }
}

export default SignInForm;
