import React, {useContext} from 'react';
import axios from 'axios'

import {Button} from 'antd'

import UserContext from '../context'

function Profile() {
    const accessToken = localStorage.getItem('accessToken')

    const {access} = useContext(UserContext)

    const config = {
        headers: {
        'Authorization': `JWT ${access}`
        }
    }
    const changePassword = () => {
        axios.get('http://127.0.0.1:8000/auth/users/me/', config).then(response => {
            console.log(response)
        }).catch(error => console.log(error))
    }

    const seeAccess = () => {
        console.log(access)
    }

    return (
        <div>
            <Button onClick = {changePassword}> change password </Button>
            <Button onClick = {seeAccess}> see Access </Button>
        </div>
    )
}

export default Profile