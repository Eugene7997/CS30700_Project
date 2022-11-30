import React from 'react'

import Head from '../header'
import {FadeOut,ZoomOut,MoveIn, Move, StickyIn, FadeIn, ZoomIn,MoveOut, Animator, ScrollContainer, ScrollPage, Sticky, Zoom, Fade, batch} from 'react-scroll-motion'
import '../../App.css'



const ZoomInScrollOut = batch(StickyIn(), FadeIn(), ZoomIn());
const FadeUp = batch(Fade(), Sticky(70), Move())

const About = () => {
  return (
        
          <div>
            {/* <Head/> */}
        <ScrollContainer>
          <ScrollPage style={{backgroundColor: 'black'}}>
            <Head/>
          </ScrollPage>        
          <ScrollPage page={0}>
            <div className='pages'>
              <div style={{fontSize: 30, textAlign: 'center'}}>
                <Animator animation={batch(MoveOut(-1000,0),Sticky(50,33))}>It has become increasingly important to raise awareness regarding environmental issues.</Animator>
              </div>
              <div style={{fontSize: 30, textAlign:'center'}}>
                <Animator animation={batch(MoveOut(1000,0), Sticky(50,45))}>We have decided to create an all-in-one environmental monitoring app which is designed to be</Animator>
              </div>
              <div style={{fontSize: 50, fontWeight: 'bold', fontStyle: 'italic', textDecorationLine: 'underline'}}>
                <Animator animation={batch(MoveOut(300,-1000), Sticky(50,58))}>Minimal, Intuitive, and Fast</Animator>
              </div>
            </div>
          </ScrollPage>
          <ScrollPage style={{backgroundColor: 'black'}}>
          </ScrollPage> 
          <ScrollPage page={1}>
            <div className='pages'>
              <Animator animation={ZoomInScrollOut}>
                <div style={{fontSize: 160}}>Now</div>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage style={{backgroundColor: 'black'}}>
          </ScrollPage> 
          <ScrollPage page={2}>
            <div className='pages'>
              <Animator animation={ZoomInScrollOut}>
                <div style={{fontSize: 100}}>Introducing</div>
              </Animator>
            </div>
            
          </ScrollPage>
          <ScrollPage>
            <div className='page4' />
          </ScrollPage> 
          <ScrollPage page={3}>
            <div className='page4'>
              <Animator animation={batch(Sticky(28), Fade(), Zoom())}>
                <img src={require('../header/logo.png')} width="500" heigth="500"/>
              </Animator>
              <Animator animation={batch(StickyIn(70), FadeIn(), MoveOut(0,-200))}>
                <div style={{fontSize: 200}}>Argus</div>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage>
            <div className='page4' />
          </ScrollPage> 
          <ScrollPage page={4}>
            <div className='pages'>
              <Animator animation={ZoomInScrollOut}>
                <div style={{fontSize: 55}}>With Argus, users will be informed of the climate activity and other environmental activities in a single application</div>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={5}>
          <ScrollPage style={{backgroundColor: 'black'}}>
          </ScrollPage> 
            <div className='pages'>
              <Animator animation={FadeUp}>
                <h1>We allow users to monitor past, present, and future temepratures at any location.</h1>
              </Animator>
              <Animator animation={batch(Sticky(30), Fade(), Zoom(5,1))}>
                <img src={require('../../images/temp.jpg')} width="500" heigth="600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={6}>
            <div className="page1">
              <Animator animation={batch(Fade(), Sticky(), Move(0, -100))}>
                <h1>We enabled users to monitor rising sea level at anywhere</h1>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={7}> 
            <div className="page2">
              <Animator animation={batch(Fade(), Sticky(), Move(0, 80))}>
                <h1>We also support Greenhouse gas emission</h1>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={8}>
            <div className="page3">
              <Animator animation={batch(Fade(), Sticky(), Move(0, 60))}>
                <h1>Finally, Argus supports humidity monitoring</h1>
              </Animator>
            </div>
          </ScrollPage>
      </ScrollContainer>
       </div>
      
  )
}

export default About