import React, {Component, ScrollAnimation, useRef} from 'react';


import './App.css';

import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import Home from './components/Home'
// import header from './components/header'
import About from './components/About'
import Application from './components/application'
import SignIn from './components/SignIn'
import SignUp from './components/SignUp'



function App() { 
    return (
      <div className='App'>
        <Routes>
          <Route path='/signin' element={<SignIn />} />
          <Route path='/signup' element={<SignUp />} />
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="application" element={<Application />} />
        </Routes>
      </div>
    )
  
}
 
export default App;
