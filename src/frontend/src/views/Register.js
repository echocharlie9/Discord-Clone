import React from 'react'
import axios from 'axios'

import {Form, Input, Button, message} from 'antd'
import { UserOutlined, LockOutlined} from '@ant-design/icons';

function Register(props) {

    const onRegister = (values) => {
        axios.post('http://127.0.0.1:8000/auth/users/', {
            username: values.username,
            password: values.password,
          }).then(
            response => {
                console.log(response)
                message.success('Successfully registered!')
                props.history.push('/login')
            }).catch(error => console.log(error))
    }
    
    return (
        <div style = {{margin: '100px 40% 100px'}}>
            <h1> Registration </h1>
            <Form
            name="normal_register"
            className="register-form"
            initialValues={{
                remember: true,
            }}
            onFinish={onRegister}>
                <Form.Item
                    name="username"
                    rules={[
                    {
                        required: true,
                        message: 'A username is required',
                    },
                    ]}
                 >
                    <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Create Username" />
                </Form.Item>
                <Form.Item
                    name = "password"
                    hasFeedback
                    rules = {[
                    {
                        required: true,
                        message: 'A password is required'
                    },
                    ]}
                >
                    <Input prefix={<LockOutlined className="site-form-item-icon" />} placeholder="Password" type ='password'/>
                </Form.Item>
                <Form.Item
                    name = "confirmpassword"
                    dependencies = {['password']}
                    hasFeedback
                    rules = {[
                    {
                        required: true,
                        message: 'Re-enter your password'
                    },
                    ({getFieldValue}) => ({
                        validator(rule, value) {
                            if (!value || getFieldValue('password') === value) {
                                return Promise.resolve()
                            }
                            return Promise.reject('Error: Passwords do not match')
                        }
                    })
                    ]}
                >
                    <Input prefix={<LockOutlined className="site-form-item-icon" />} placeholder="Confirm Password" type ='password'/>
                </Form.Item>
                <Form.Item>
                <Button type="primary" htmlType="submit" className="register-form-button">
                Register
                </Button>
                </Form.Item>
                 Already have an account?<a href="login"> Login</a>
            </Form>
        </div>
    )
}

export default Register