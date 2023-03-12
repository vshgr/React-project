import {useState} from 'react'

export const useChoiceVariant = () => {
    const [choiceVariants, setChoiceVariants] = useState([])

    const handleAddChoiceVariant = () => {
        setChoiceVariants([...choiceVariants, {id: crypto.randomUUID(), text: '', isCorrect: false}])
    }

    const handleDeleteChoiceVariant = (id) => {
        setChoiceVariants(choiceVariants.filter((text) => text.id !== id))
    }

    const handleChangeChoiceVariant = (id, e) => {
        setChoiceVariants(
            choiceVariants.map((text) => (text.id === id ? {...text, text: e.target.value} : text)),
        )
    }

    const handleChangeCorrectChoiceVariant = (id) => {
        setChoiceVariants(
            choiceVariants.map((text) =>
                text.id === id ? {...text, isCorrect: !text.isCorrect} : text,
            ),
        )
    }

    return {
        choiceVariants,
        setChoiceVariants,
        handleAddChoiceVariant,
        handleDeleteChoiceVariant,
        handleChangeChoiceVariant,
        handleChangeCorrectChoiceVariant,
    }
}
