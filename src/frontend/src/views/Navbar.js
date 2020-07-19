import React from 'react'
import { withRouter } from 'react-router-dom';
import {Menu,Button} from 'antd'

function Navbar(props) {
    const accessToken = localStorage.getItem('accessToken')

    //for debug purposes
    const getToken = () => {
        console.log(accessToken)
    }

   const isLoggedIn = () => {
        //console.log(accessToken)
        if (accessToken === '') return false
        return true
    }

    const logout = () => {
        localStorage.setItem('accessToken', '')
        props.history.push('/')
    }

    const ConditionalLoggedIn = (props) => {
        const isLoggedIn = props.isLoggedIn
        if (isLoggedIn) {
            return (
                <div style = {{
                position: 'absolute', 
                right: '25px',
                top: '3px'
                }}>
                <Button onClick = {logout} >Logout</Button>
            </div>
            )
        }
        else 
        return (
            <div style = {{
                position: 'fixed', 
                right: '25px',
                top: '3px'
                }}>
                <a href = './login'>Login</a>
                <a href = './register'> Register</a>
            </div>
        )
    }
    
    // const handleLobbySelect = (isLoggedIn) => {
    //     // console.log('inside: ' + isLoggedIn)
    //     if (isLoggedIn) {
    //         props.history.push('/lobby')
    //     }
    //     else {
    //         message.error('You must be logged in to view that page!')
    //         props.history.push('/login')
    //     }
    // }

    const handleLobbySelect = () => {
        props.history.push('/lobby')
    }

    return (
        <div>
            <Menu mode = 'horizontal'>
                <Menu.Item key = 'homepage'> 
                    Home
                </Menu.Item>
                <Menu.Item key = 'lobbies' onClick = {handleLobbySelect}>
                    View Lobbies
                </Menu.Item>
                <ConditionalLoggedIn isLoggedIn = {isLoggedIn()}> </ConditionalLoggedIn>
            </Menu>
         </div>
    )
}

export default withRouter(Navbar)