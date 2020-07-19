import React from 'react'

import {Menu} from 'antd'

function Landing() {

    return (
        <Menu mode = 'horizontal'>
            <Menu.Item key = 'homepage'> 
                Home
            </Menu.Item>
                <a href = './login'>Login</a>
                <a href = './register'>    Register</a>
        </Menu>
    )
}

export default Landing