import {Box, Button, IconButton, Stack, TextField, Typography} from '@mui/material'
import React, {useContext, useEffect, useState} from 'react'
import EditQuestionCard from '../../components/elements/cards/EditQuestionCard'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import {Link, useParams} from 'react-router-dom'
import BottomDrawer from '../../components/elements/drawers/BottomDrawer'
import {MainContext} from '../../context'
import {useNavigate} from 'react-router-dom'
import API from '../../api'

export default function EditTestPage() {
    let {testId} = useParams()
    const navigate = useNavigate()

    const {setIsBottomDrawerOpen} = useContext(MainContext)

    const [questions, setQuestions] = useState([])
    const [oldQuestions, setOldQuestions] = useState([])
    const [title, setTitle] = useState('')

    useEffect(() => {
        async function fetchData() {
            const result = await API.get(`/test/${testId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                },
            })
            setTitle(result.data.title)
            setQuestions(result.data.questions)
            setOldQuestions(result.data.questions)
        }
        fetchData()
    }, [])
    const handleTitleChange = (e) => {
        e.preventDefault()
        setTitle(e.target.value)
    }

    const handleSave = async (e) => {
        e.preventDefault()
        const titleRequestBody = {
            title: title,
        }
        const result = await API.put(`/test/${testId}`, titleRequestBody, {
            headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
        })
        if (oldQuestions.length > questions.length) {
            oldQuestions.forEach(async (question) => {
                if (!questions.find((q) => q.id === question.id)) {
                    await API.delete(`/question/${question.id}`, {
                        headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
                    })
                }
            })
        }
        questions.forEach(async (question) => {
            const questionRequestBody = {
                testGuid: testId,
                title: question.title,
                type: question.type,
            }
            const result = await API.put(`/question/${question.id}`, questionRequestBody, {
                headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
            })
            const questionId = result.data.id
            question.answers.forEach(async (answer) => {
                const answerRequestBody = {
                    questionGuid: questionId,
                    subText: answer.subText,
                    text: answer.text,
                    isCorrect: answer.isCorrect,
                }
                await API.put(`/answer/${answer.id}`, answerRequestBody, {
                    headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
                })
            })
        })
        navigate('/home')
    }

    return (
        <>
            <Box
                component='section'
                sx={{
                    padding: 'calc(89px + 26px) 34px calc(91px + 26px)',
                    // height: '100vh',
                }}
            >
                <Stack
                    direction='row'
                    justifyContent='space-between'
                    alignItems='center'
                    sx={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: 'var(--header-height)',
                        padding: '34px 34px 13px',
                        background: 'var(--color-bg-1)',
                        zIndex: 1,

                        '&::after': {
                            content: '""',
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            width: '100%',
                            height: '1px',
                            background: 'var(--color-100)',
                        },
                    }}
                >
                    <Stack direction='row' alignItems='center' sx={{gap: '12px'}}>
                        <Link
                            to='/home'
                            style={{
                                WebkitTapHighlightColor: 'transparent',
                            }}
                        >
                            <IconButton sx={{color: 'var(--color-100)'}}>
                                <ArrowBackIcon/>
                            </IconButton>
                        </Link>
                        <Typography
                            component='h1'
                            sx={{
                                fontWeight: 800,
                                fontSize: '25px',
                                lineHeight: '29px',
                                textTransform: 'uppercase',
                                fontFamily: 'var(--primary-font)',
                            }}
                        >
                            Edit
                        </Typography>
                    </Stack>
                    <Button
                        variant='text'
                        onClick={handleSave}
                        sx={{
                            fontWeight: 700,
                            fontSize: '15px',
                            lineHeight: '18px',
                            fontFamily: 'var(--primary-font)',
                            color: 'var(--color-primary)',
                        }}
                    >
                        Save
                    </Button>
                </Stack>
                <Stack
                    sx={{
                        marginBottom: '30px',
                    }}
                >
                    <Typography
                        sx={{
                            marginBottom: '14px',
                            fontWeight: 500,
                            fontSize: '20px',
                            lineHeight: '23px',
                            fontFamily: 'var(--primary-font)',
                        }}
                    >
                        Title
                    </Typography>
                    <TextField
                        placeholder='enter title'
                        value={title}
                        onChange={handleTitleChange}
                        sx={{
                            marginBottom: '26px',

                            '& input': {
                                fontFamily: 'var(--primary-font)',
                                color: 'var(--color-100)',
                            },
                            '& fieldset': {
                                transition: 'border-color .2s',
                                borderColor: 'var(--color-bg-2)',
                            },
                            '& .MuiOutlinedInput-root': {
                                borderRadius: 'var(--border-radius)',
                                '&.Mui-focused fieldset': {
                                    borderColor: 'var(--color-primary)',
                                },
                            },
                        }}
                    />
                </Stack>
                <Stack sx={{gap: '18px'}}>
                    {questions.map((question, index) => (
                        <EditQuestionCard
                            key={index}
                            question={question}
                            questions={questions}
                            setQuestions={setQuestions}
                            index={index}
                        />
                    ))}
                </Stack>
            </Box>
            <BottomDrawer questions={questions} setQuestions={setQuestions}/>
        </>
    )
}
