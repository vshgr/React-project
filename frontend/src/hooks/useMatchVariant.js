import {useState} from 'react'

export const useMatchVariant = () => {
    const [matchVariants, setMatchVariants] = useState([])

    const handleAddMatchVariant = () => {
        setMatchVariants([
            ...matchVariants,
            {id: crypto.randomUUID(), text: '', subText: '', isCorrect: true},
        ])
    }

    const handleDeleteMatchVariant = (id) => {
        setMatchVariants(matchVariants.filter((text) => text.id !== id))
    }

    const handleChangeMatchVariant = (id, e) => {
        setMatchVariants(
            matchVariants.map((text) => (text.id === id ? {...text, text: e.target.value} : text)),
        )
    }

    const handleChangeCorrectMatchVariant = (id, e) => {
        setMatchVariants(
            matchVariants.map((text) => (text.id === id ? {...text, subText: e.target.value} : text)),
        )
    }

    return {
        matchVariants,
        setMatchVariants,
        handleAddMatchVariant,
        handleDeleteMatchVariant,
        handleChangeMatchVariant,
        handleChangeCorrectMatchVariant,
    }
}
