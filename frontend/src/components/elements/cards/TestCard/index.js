import React, {useState} from 'react'
import {IconButton, Stack, Typography} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import {Link, useNavigate} from 'react-router-dom'

export default function TestCard({test, deleteTest}) {
    const [isCopied, setIsCopied] = useState(false)
    const navigate = useNavigate()

    const created = new Date(test.created).toISOString().split('T')[0]
    const updated = new Date(test.updated).toISOString().split('T')[0]

    const handleCopy = (e) => {
        e.stopPropagation()
        let text =
            'Название теста: ' +
            test.title +
            '\n' +
            'Количество вопросов: ' +
            test.questions.length +
            '\n' +
            'Вопросы:\n' +
            test.questions
                .map((question, index) => {
                    switch (question.type) {
                        case 'text':
                            return index + 1 + '. ' + question.title + '\n\n'
                        case 'choice':
                            return (
                                index +
                                1 +
                                '. ' +
                                question.title +
                                '\n\nВарианты ответов:\n' +
                                question.answers.sort(() => 0.5 - Math.random())
                                    .map((answer, index) => {
                                        return answer.text + '\n'
                                    })
                                    .join('') +
                                '\n\n'
                            )
                        case 'match':
                            return (
                                index +
                                1 +
                                '. ' +
                                question.title +
                                '\n\n' +
                                question.answers.sort(() => 0.5 - Math.random())
                                    .map((answer, index) => {
                                        return answer.text + '\n'
                                    })
                                    .join('') +
                                '\nСопоставьте каждое с одним из:\n' +
                                question.answers.sort(() => 0.5 - Math.random())
                                    .map((answer, index) => {
                                        return answer.subText + '\n'
                                    })
                                    .join('') +
                                '\n\n'
                            )
                        default:
                            return 'error'
                    }
                })
                .join('')
        navigator.clipboard.writeText(text.replace(',', ''))
        setIsCopied(true)
        setTimeout(() => {
            setIsCopied(false)
        }, 2000)
    }

    const handleCardClick = () => {
        navigate(`/test/${test.id}`)
    }

    return (
        <Stack direction='row' alignItems='center' sx={{gap: '24px'}}>
            <div
                style={{
                    flex: 1,
                    WebkitTapHighlightColor: 'transparent',
                }}
            >
                <Stack
                    onClick={handleCardClick}
                    direction='row'
                    justifyContent='space-between'
                    alignItems='center'
                    sx={{
                        border: '1px solid var(--color-bg-2)',
                        borderRadius: 'var(--border-radius-2)',
                        padding: '14px 19px',
                        transition: 'background .3s',

                        '&:hover': {
                            background: 'rgba(255, 255, 255, .1)',
                        },
                    }}
                >
                    <Stack sx={{gap: '11px'}}>
                        <Stack sx={{gap: '3px'}}>
                            <Typography
                                sx={{
                                    fontWeight: 400,
                                    fontSize: '15px',
                                    lineHeight: '18px',
                                    maxWidth: 'clamp(100px, 50vw, 1000px)',
                                    wordBreak: 'break-word',
                                }}
                            >
                                {test.title}
                            </Typography>
                            <Typography sx={{fontWeight: 400, fontSize: '15px', lineHeight: '18px'}}>
                                {test.questions.length} вопросов
                            </Typography>
                        </Stack>
                        <Stack>
                            {isCopied ? (
                                <Typography
                                    sx={{
                                        fontWeight: 400,
                                        fontSize: '11px',
                                        lineHeight: '13px',
                                        color: 'var(--color-success)',
                                    }}
                                >
                                    скопировано
                                </Typography>
                            ) : null}
                            <Typography sx={{fontWeight: 400, fontSize: '11px', lineHeight: '13px'}}>
                                создан: {created}
                            </Typography>
                            <Typography sx={{fontWeight: 400, fontSize: '11px', lineHeight: '13px'}}>
                                отредактирован: {updated}
                            </Typography>
                        </Stack>
                    </Stack>
                    <IconButton sx={{height: 'fit-content'}} onClick={handleCopy}>
                        <ContentCopyIcon sx={{color: 'var(--color-100)'}}/>
                    </IconButton>
                </Stack>
            </div>
            <IconButton sx={{height: 'fit-content'}} onClick={deleteTest}>
                <DeleteIcon sx={{color: 'var(--color-100)'}}/>
            </IconButton>
        </Stack>
    )
}
