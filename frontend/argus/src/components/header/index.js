import React, {useState} from 'react'
import Arugslogo from './logo.png'
import { useNavigate } from "react-router-dom";
import ProgressButton from 'react-progress-button'
import styled from 'styled-components'


const Head = () => {
    let navigate = useNavigate();
    const [name, setName] = useState("Sign In")
    const toAbout = () => {
        navigate("/about")
    }
    const toMain = () => {
        navigate('/')
    }
    const toSignin  = () => {
        navigate("/signin")
    }
    const Button = styled.button`
        background-color: transparent;
        color: white;
        border-color: white;
        font-size: 17px;
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px 0px;
        cursor: pointer;
    `;
  return (
    <div style={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingBottom: 10,
        backgroundColor: 'navy'
        
    }}>
        <div style={{
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            marginTop: '10px',
            marginLeft: '20px'
        }}>
            <div style={{display: 'flex'}} onClick={() => toMain()}>
                <img src={Arugslogo} alt="Logo" height={60} width={60} />
                <h1 style={{marginLeft: '8px', color: 'white', marginTop: '10px'}}>Argus</h1>
            </div>
        </div>
        <div style={{marginTop: 10, display: 'flex', flexDirection: 'row', aliggItems: 'center', justifyContent: 'center'}}>
            <div  style={{marginRight: 20}}>
                <Button onClick={() => toSignin()}>{name}</Button>
            </div>
            <div style={{marginRight: 20}}>
                <Button onClick={() => toAbout()}>About us</Button>
            </div>
        </div>
        
    </div>
  )
}

export default Head


