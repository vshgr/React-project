import {Route, Routes} from 'react-router-dom'
import {MainContextProvider} from './context'
import SignInPage from './pages/auth/SingInPage'
import HomePage from './pages/home'
import CreateTestPage from './pages/create'
import TestPage from './pages/test'
import EditTestPage from "./pages/edit";

function App() {
    return (
        <MainContextProvider>
            <Routes>
                <Route exact path='/' element={<SignInPage/>}/>
                <Route exact path='/home' element={<HomePage/>}/>
                <Route exact path='/create' element={<CreateTestPage/>}/>
                <Route exact path='/test/:testId' element={<TestPage/>}/>
                <Route exact path='/edit/:testId' element={<EditTestPage/>}/>
            </Routes>
        </MainContextProvider>
    )
}

export default App
