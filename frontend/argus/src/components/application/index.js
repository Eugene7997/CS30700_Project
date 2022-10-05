import React from 'react'
import Head from '../header'

const Application = () => {
  return (
    <div>
      <div style = {{
          backgroundColor: 'black',
          opacity: '0.8'
      }}>
        <Head />
      </div>
      
      <div>
        <h1>Application</h1>
      </div>
    </div>
  )
}

export default Application