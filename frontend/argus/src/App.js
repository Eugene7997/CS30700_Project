import React, {Component, ScrollAnimation, useRef} from 'react';


import logo from './logo.svg';
import './App.css';



function App() { 
  const example1 = useRef(null);
  const example2 = useRef(null);
  const example3 = useRef(null);

  const scrollTosection = (elementRef) => {
    window.scrollTo({
      top: elementRef.current.offsetTop,
      behavior: 'smooth',
    })
  }

    return (
      <div className='App'>
        <div className='argus'>
          <ul>
            <li onClick={() => scrollTosection(example1)} className="link">Argus</li>
          </ul>
        </div>
        <div className='example1'>
          <li>Example1</li>
        </div><div className='example2'>
          <li>Example2</li>
        </div><div className='example3'>
          <li>Example3</li>
        </div>
      </div>
    )
  
}
 
export default App;
