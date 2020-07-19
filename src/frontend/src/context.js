import React from 'react'

const UserContext = React.createContext({
    access: '',
    setAccess: () => {}
})

export const UserProvider = UserContext.Provider
export const UserConsumer = UserContext.Consumer

export default UserContext