import React, {useState} from 'react';
import './App.css';

import {Route, Switch} from 'react-router-dom'
import { withRouter } from 'react-router-dom';
import axios from 'axios'
import {Button} from 'antd';

import Navbar from './views/Navbar'
import Login from './views/Login'
import Register from './views/Register'
import ChatLobby from './views/ChatLobby'
import ChatRoom from './views/ChatRoom'
import Profile from './views/Profile'

//const serv = '127.0.0.1:8000/'
//const serv2 = 'localhost:8000/api'

function User(props) {
  const [token, setToken] = useState('')
  const [messages, setMessages] = useState([])

  // const handleClick = () => {
  //   axios.get('http://127.0.0.1:8000/api/').then(response => {
  //     console.log(response);
  //     setData(response.data.results[0].title)
  //   }).catch(error => console.log(error))
  // }

  // setToken(response.data.token)

  let config = {
    headers: {
      "Authorization": `JWT ${token}`,
      'Content-Type': 'application/json',
      "Accept": "application/json"
    }
  }

  const handleGetUser = () => {
    console.log(config.headers.Authorization)
    axios.get('http://127.0.0.1:8000/auth/users/me/', config).then(
      response => console.log(response)).catch(error => console.log(error))
  }

  const roomName = 'room1'

  const chatSocket = new WebSocket(
    'ws://'
    + 'localhost:8000'
    + '/ws/chat/'
    + roomName
    + '/'
);


chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  console.log(data);
  setMessages(messages.concat(data.message))
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

const sendMessage = () => {
chatSocket.send(JSON.stringify({
  'message': 'allah'
}));
}

  return (
    <div>
      <Button onClick={handleGetUser}>
        Get Jimmy
      </Button>
      <Button onClick={sendMessage}>
        Send Message
      </Button>
      {messages.map((value, index) => {
        return (
          <p>{value}</p>
        )
      })}
    </div>
  )
}

function App(props) {

  const [access, setAccess] = useState('')
  const changeAccess = (newval) => {
    setAccess(newval)
  }

  return (
    <div className="App">
      <header className="App-header">
        <Navbar/>
      </header>
      <Switch>
        <Route exact path = "/" component = {Login}/>
        <Route exact path = "/login" component = {Login} />
        <Route exact path = "/register" component = {Register} />
        <Route exact path = "/lobby" component = {ChatLobby} />
        <Route exact path = "/chatroom" component = {ChatRoom} />
        <Route exact path = "/profile" component = {Profile} />
      </Switch>
    </div>
  );
}

export default withRouter(App);
