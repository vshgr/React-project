import {useState} from 'react'

export const useTextVariant = () => {
    const [textVariants, setTextVariants] = useState([{id: crypto.randomUUID(), text: '', isCorrect: true}])

    const handleTextVariant = (e) => {
        setTextVariants((prev) => prev.map((text) => ({...text, text: e.target.value})))
    }

    return {
        textVariants,
        setTextVariants,
        handleTextVariant,
    }
}
