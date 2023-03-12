import React, {createContext, useState} from 'react'

export const MainContext = createContext(null)

export function MainContextProvider({children}) {
    const [isBottomDrawerOpen, setIsBottomDrawerOpen] = useState(false)
    const [selectedQuestion, setSelectedQuestion] = useState()
    const [isInfoModalOpen, setIsInfoModalOpen] = useState(false)

    return (
        <MainContext.Provider
            value={{
                isBottomDrawerOpen,
                setIsBottomDrawerOpen,
                selectedQuestion,
                setSelectedQuestion,
                isInfoModalOpen,
                setIsInfoModalOpen,
            }}
        >
            {children}
        </MainContext.Provider>
    )
}
