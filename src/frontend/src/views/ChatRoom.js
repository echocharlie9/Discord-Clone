import React, {useState} from 'react'
import axios from 'axios'

import {SettingFilled} from '@ant-design/icons';

import {Input,Button, Descriptions, Row, Col, Modal} from 'antd'

const {Search} = Input;

function ChatRoom(props) {
    const [messages, setMessages] = useState([])

    const [settingsVisible, setSettingsVisible] = useState(false)
    const [roomTitle, setRoomName] = useState(props.location.state.data.title)
    const [roomDescription, setRoomDescription] = useState(props.location.state.data.description)

    const roomName = 'room1'

    // const chatSocket = new WebSocket(
    //     'ws://'
    //     + 'localhost:8000'
    //     + '/ws/chat/'
    //     + roomName
    //     + '/'
    // );

    // chatSocket.onmessage = function(e) {
    // const data = JSON.parse(e.data);
    // console.log(data);
    // setMessages(messages.concat(data.message))
    // };

    // chatSocket.onclose = function(e) {
    // console.error('Chat socket closed unexpectedly');
    // };

    // const sendMessage = () => {
    //     console.log('sending message')
    //     chatSocket.send(JSON.stringify({
    //     'message': 'allah'
    //     }));
    // }

    const getMessages = () => {
        console.log(props)
    }

    const handle = () => {
        console.log(props.location.state.title)
    }

    const handleSettingsClick = () => {
        setSettingsVisible(true)
    }

    const handleOk = () => {
        setSettingsVisible(false)
    }

    const handleCancel = () => {
        setSettingsVisible(false)
    }

    const handleEditTitle = (e) => {
        console.log(e.target.value)
        const config = {
            'roomName': roomTitle,
            'title' : 'newroom'
        
    }
        axios.post('http://127.0.0.1:8000/chat/changeRoomTitle',config).then(response => {
            console.log(response)
        })
    }

    const handleEditDescription = (e) => { 
        console.log(e.target.value)
        const config = {
            'roomName': roomTitle,
            'description' : 'new description'
        
    }
        axios.post('http://127.0.0.1:8000/chat/changeDescription',config).then(response => {
            console.log(response)
        })
    }
    return (
        <div>
            <Row justify = 'center'>
            {/* <Button onClick = {handle}>
                test prop passing
            </Button>
            <SettingFilled></SettingFilled> */}
            <Col>
            <div className = 'info' style = {{
                height: '250px',
                width: '200px',
                margin: '20px',
                border: '2px solid grey',
                borderRadius:'5px'
            }}>
                <SettingFilled onClick = {handleSettingsClick}/>
                <Descriptions title = 'Room Info' size = 'small' layout = 'vertical' column = {1} bordered = 'true'>
                    <Descriptions.Item label = 'Name'> {roomTitle} </Descriptions.Item>
                    <Descriptions.Item label = 'Description'> {roomDescription} </Descriptions.Item>
                </Descriptions>
            </div>
            </Col>
            <Col flex = 'auto'>
            <div className = 'messagebox' style = {{
                height: '300px',
                border: '2px solid grey',
                borderRadius:'5px'
            }}>
                {messages.map((value,index) => {
                    return (
                        <div>
                            {value}
                        </div>
                    )
                })}
            </div>
            </Col>
            <Col>
            <div className = 'memberslist' style = {{
                height: '250px',
                width: '200px',
                margin: '20px',
                border: '2px solid grey',
                borderRadius:'5px'
            }}>
            </div>
            </Col>
            </Row>
            <Input  style = {{
                margin: '10px 10% 50px',
                padding: '10px'
            }}>
            </Input>
            {/* add onclick function */}
            <Button>
                send message
            </Button>

            <Modal 
            title = 'Room Options' 
            visible = {settingsVisible}
            onOk = {handleOk}
            onCancel = {handleCancel}
            >
                <Input defaultValue = {roomTitle} onPressEnter = {handleEditTitle}></Input>
                <Input defaultValue = {roomDescription} onPressEnter = {handleEditDescription}></Input>
            </Modal>
        </div>
    )
}

export default ChatRoom