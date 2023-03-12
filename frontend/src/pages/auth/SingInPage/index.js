import React, {useEffect, useState} from 'react'
import Box from '@mui/material/Box'
import {useNavigate} from 'react-router-dom'
import useAuth from '../../../hooks/useAuth'
import {GoogleLogin} from '@react-oauth/google'
import Logo from '../../../components/elements/icons/Logo'

export default function SignInPage() {
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()
    const {login} = useAuth()

    useEffect(() => {
        let timer = setTimeout(() => setLoading(false), 3000)
        return () => {
            clearTimeout(timer)
        }
    }, [])

    const handleAuth = (response) => {
        login(response).then(() => {
            navigate('/home')
        })
    }

    return (
        <Box
            component='main'
            sx={{
                padding: '16px',
                width: '100%',
                minHeight: '100vh',
                display: 'grid',
                placeContent: 'center',
            }}
        >
            {loading ? (
                <Logo/>
            ) : (
                <GoogleLogin
                    onSuccess={handleAuth}
                    text='continue_with'
                    shape='circle'
                    onError={() => {
                        console.log('Login Failed')
                    }}
                />
            )}
        </Box>
    )
}
