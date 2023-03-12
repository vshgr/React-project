import React, {createContext, useState, useContext} from 'react'
import API from '../api'

const authContext = createContext(null)

function useAuth() {
    const [isAuth, setIsAuth] = useState(false)

    return {
        isAuth,
        async login(response) {
            const result = await API.get('/auth?token=' + response.credential)
            if (result.status === 200) {
                return new Promise((res) => {
                    localStorage.setItem('access_token', result.data.accessToken)
                    setIsAuth(true)
                    res()
                })
            }
        },
        logout() {
            return new Promise((res) => {
                localStorage.removeItem('access_token')
                setIsAuth(false)
                res()
            })
        },
    }
}

export function AuthProvider({children}) {
    const isAuth = useAuth()
    return <authContext.Provider value={isAuth}>{children}</authContext.Provider>
}

export default function AuthConsumer() {
    return useContext(authContext)
}
