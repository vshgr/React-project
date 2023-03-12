import React from 'react'
import ReactDOM from 'react-dom/client'
import './styles/index.scss'
import App from './App'
import {BrowserRouter} from 'react-router-dom'
import {GoogleOAuthProvider} from '@react-oauth/google'
import {AuthProvider} from './hooks/useAuth'

const root = ReactDOM.createRoot(document.getElementById('root'))
const clientId = process.env.REACT_APP_GOOGLE_CLIENT_ID

root.render(
    <React.StrictMode>
        <AuthProvider>
            <GoogleOAuthProvider clientId={clientId}>
                <BrowserRouter>
                    <App/>
                </BrowserRouter>
            </GoogleOAuthProvider>
        </AuthProvider>
    </React.StrictMode>,
)
