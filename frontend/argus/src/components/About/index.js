import React from 'react'

import Head from '../header'
import {Animation, FadeOut,ZoomOut,MoveIn, Move, StickyIn, FadeIn, ZoomIn,MoveOut, Animator, ScrollContainer, ScrollPage, Sticky, Zoom, Fade, batch} from 'react-scroll-motion'
import '../../App.css'



const ZoomInScrollOut = batch(StickyIn(), FadeIn(), ZoomIn());
const FadeUp = batch(Fade(), Sticky(70), Move())
const Spin = (cycle) =>
  ({
    in: {
      style: {
        // `p` is number (0~1)
        // When just before this page appear, `p` will be 0
        // When this page filled your screen, `p` will be 1
        transform: (p) => `rotate(${p * 360 * cycle}deg)`,
      },
    },
    out: {
      style: {
        // `p` is number (0~1)
        // When this page filled your screen, `p` will be 0
        // When just after this page disappear, `p` will be 1
        transform: (p) => `rotate(${p * 360 * cycle}deg)`,
      },
    },
  });

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
          <ScrollPage page={9}>
            <div className='pages'>
              <Animator animation={batch(Fade(), Sticky(), Move())}>
                <h1>Instructions on how to use our application</h1>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={10}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <h1>This is our home page</h1>
                <img src={require('./Instructions/1-1.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={11}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <h1>You can sign-in here</h1>
                <img src={require('./Instructions/1-2.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={12}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <h1>You can sign-up here</h1>
                <img src={require('./Instructions/1-3.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={13}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <h1>This is the initial screen when you run the application</h1>
                <img src={require('./Instructions/2.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={14}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-1.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={15}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-2.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={16}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-3.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={17}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-4.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={18}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-5.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={19}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/2-6.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={20}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/6.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          <ScrollPage page={21}>
            <div className='pages'>
              <Animator animation={batch(Sticky(), Fade())}>
                <img src={require('./Instructions/7.png')} width="1200" heigth="1600"/>
              </Animator>
            </div>
          </ScrollPage>
          
          <ScrollPage page={22}>
            <div className="pages">
              <Animator animation={batch(Sticky(50,15), Fade(), Spin(3))}>
                <div style={{fontSize: 54, textDecorationLine: 'underline'}}>Argus Team 19</div>
              </Animator>
              <Animator animation={batch(Fade(), MoveIn(1000,300),Sticky(50,30))}>
                <div style={{fontSize: 30, textAlign: 'center'}}>Adam Rutledge</div>
                <div style={{fontSize: 25, textAlign: 'center'}}>(rutledgea20@gmail.com)</div>
              </Animator>
              <Animator animation={batch(Fade(), MoveIn(-1000,300),Sticky(50,42))}>
                <div style={{fontSize: 30, textAlign: 'center'}}>Bhavik Sardar</div>
                <div style={{fontSize: 25, textAlign: 'center'}}>(bhaviksardar@gmail.com)</div>
              </Animator>
              <Animator animation={batch(Fade(), MoveIn(300, 1000),Sticky(50,54))}>
                <div style={{fontSize: 30, textAlign: 'center'}}>Eugene Poh</div>
                <div style={{fontSize: 25, textAlign: 'center'}}>(eugenepoh999@gmail.com)</div>
              </Animator>
              <Animator animation={batch(Fade(), MoveIn(300, -1000),Sticky(50,66))}>
                <div style={{fontSize: 30, textAlign: 'center'}}>Ji Woong Park</div>
                <div style={{fontSize: 25, textAlign: 'center'}}>(qkrwldnd97@gmail.com)</div>
              </Animator>
              <Animator animation={batch(Fade(), MoveIn(-300,-1000), Sticky(50,78))}>
                <div style={{fontSize: 30, textAlign: 'center'}}>Sahithi Tummala</div>
                <div style={{fontSize: 25, textAlign: 'center'}}>(sahithi.tummala1@gmail.com)</div>
              </Animator>
            </div>
          </ScrollPage>
      </ScrollContainer>
       </div>
      
  )
}

export default About