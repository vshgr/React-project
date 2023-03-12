import React, {useContext} from 'react'
import {IconButton, Stack, Typography} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import BorderColorIcon from '@mui/icons-material/BorderColor'
import {MainContext} from '../../../../context'

export default function EditQuestionCard({question, questions, setQuestions, index}) {
    const {setIsBottomDrawerOpen, setSelectedQuestion} = useContext(MainContext)

    const handleEdit = () => {
        setSelectedQuestion(question)
        setIsBottomDrawerOpen(true)
    }

    const handleDelete = () => {
        setQuestions(questions.filter((q) => q.id !== question.id))
    }

    return (
        <Stack direction='row' alignItems='center' justifyContent='space-between'>
            <Typography
                sx={{
                    marginRight: '14px',
                    fontWeight: 700,
                    fontSize: '15px',
                    lineHeight: '18px',
                    fontFamily: 'var(--primary-font)',
                }}
            >
                {index + 1}
            </Typography>
            <Typography
                sx={{
                    fontWeight: 500,
                    fontSize: '13px',
                    lineHeight: '15px',
                    maxWidth: 'calc(100% - 100px)',
                    fontFamily: 'var(--primary-font)',
                }}
            >
                {question.title}
            </Typography>
            <Stack direction='row'>
                <IconButton sx={{width: 'fit-content', color: 'var(--color-100)'}} onClick={handleEdit}>
                    <BorderColorIcon/>
                </IconButton>
                <IconButton
                    sx={{width: 'fit-content', color: 'var(--color-error)'}}
                    onClick={handleDelete}
                >
                    <DeleteIcon/>
                </IconButton>
            </Stack>
        </Stack>
    )
}
