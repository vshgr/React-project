import React, {useContext, useEffect, useState} from 'react'
import {MainContext} from '../../../../context/MainContextProvider'
import {Button, IconButton, Stack, SwipeableDrawer, TextField, Typography} from '@mui/material'
import TabButton from '../../buttons/TabButton'
import CheckIcon from '@mui/icons-material/Check'
import AddIcon from '@mui/icons-material/Add'
import DeleteIcon from '@mui/icons-material/Delete'
import {useChoiceVariant} from '../../../../hooks/useChoiceVariant'
import {useMatchVariant} from '../../../../hooks/useMatchVariant'
import {useTextVariant} from '../../../../hooks/useTextVariant'

const drawerBleeding = 56

export default function BottomDrawer({questions, setQuestions}) {
    const {isBottomDrawerOpen, setIsBottomDrawerOpen, selectedQuestion, setSelectedQuestion} =
        useContext(MainContext)
    const [activeTab, setActiveTab] = useState(0)
    const {
        choiceVariants,
        setChoiceVariants,
        handleAddChoiceVariant,
        handleDeleteChoiceVariant,
        handleChangeChoiceVariant,
        handleChangeCorrectChoiceVariant,
    } = useChoiceVariant()
    const {
        matchVariants,
        setMatchVariants,
        handleAddMatchVariant,
        handleDeleteMatchVariant,
        handleChangeMatchVariant,
        handleChangeCorrectMatchVariant,
    } = useMatchVariant()
    const {textVariants, setTextVariants, handleTextVariant} = useTextVariant()
    const [title, setTitle] = useState('')
    const [type, setType] = useState('text')
    const types = {
        0: 'text',
        1: 'choice',
        2: 'match',
    }
    const tabs = {
        'text': 0,
        'choice': 1,
        'match': 2,
    }

    useEffect(() => {
        if (selectedQuestion) {
            setTitle(selectedQuestion.title)
            setType(selectedQuestion.type)
            setActiveTab(tabs[selectedQuestion.type])
            selectedQuestion.type === 'text' && setTextVariants(selectedQuestion.answers)
            selectedQuestion.type === 'choice' && setChoiceVariants(selectedQuestion.answers)
            selectedQuestion.type === 'match' && setMatchVariants(selectedQuestion.answers)
        }
    }, [selectedQuestion])

    const handleToggleTabs = (index) => {
        setType(types[index])
        setActiveTab(index)
    }

    const handleClose = () => {
        setIsBottomDrawerOpen(false)
        setSelectedQuestion(null)
        setTitle('')
        setActiveTab(0)
        setChoiceVariants([])
        setMatchVariants([])
        setTextVariants([])
    }

    const handleSave = () => {
        if(selectedQuestion) {
            const newQuestions = questions.map((question) => {
                if (question.id === selectedQuestion.id) {
                    question.title = title
                    question.type = type
                    question.answers = type === 'text' ? textVariants : type === 'choice' ? choiceVariants : matchVariants
                }
                return question
            })
            setQuestions(newQuestions)
        }
        else {
            const newQuestion = {
                id: crypto.randomUUID(),
                title,
                type,
                answers: type === 'text' ? textVariants : type === 'choice' ? choiceVariants : matchVariants,
            }
            setQuestions([...questions, newQuestion])
        }
        handleClose()
    }

    const handleQuestionTitleChange = (e) => {
        //e.preventDefault()
        setTitle(e.target.value)
    }

    return (
        <SwipeableDrawer
            anchor='bottom'
            open={isBottomDrawerOpen}
            onClose={handleClose}
            onOpen={() => setIsBottomDrawerOpen(true)}
            swipeAreaWidth={drawerBleeding}
            disableSwipeToOpen={true}
            ModalProps={{
                keepMounted: true,
            }}
            sx={{
                '& .MuiPaper-root': {
                    padding: '36px',
                    background: 'var(--color-bg-1)',
                    borderTopLeftRadius: 'var(--border-radius-2)',
                    borderTopRightRadius: 'var(--border-radius-2)',
                },
            }}
        >
            <Stack sx={{gap: '43px'}}>
                <Stack sx={{gap: '12px'}}>
                    <Stack direction='row' justifyContent='space-between' alignItems='center'>
                        <Typography
                            sx={{
                                color: '#fff',
                                fontFamily: 'var(--primary-font)',
                                fontWeight: 500,
                                fontSize: '20px',
                                lineHeight: '23px',
                            }}
                        >
                            Question text
                        </Typography>
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
                    <TextField
                        placeholder='enter title'
                        onChange={handleQuestionTitleChange}
                        value={title}
                        multiline
                        rows={4}
                        sx={{
                            marginBottom: '26px',

                            '& textarea': {
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

                <Stack sx={{gap: '12px'}}>
                    <Typography
                        sx={{
                            color: '#fff',
                            fontFamily: 'var(--primary-font)',
                            fontWeight: 500,
                            fontSize: '20px',
                            lineHeight: '23px',
                        }}
                    >
                        Type of question
                    </Typography>
                    <Stack direction='row' sx={{gap: '12px'}}>
                        {['text', 'choice', 'match'].map((tab, index) => (
                            <TabButton
                                key={tab}
                                onClick={() => handleToggleTabs(index)}
                                active={activeTab === index}
                            >
                                {tab}
                            </TabButton>
                        ))}
                    </Stack>
                </Stack>
                {activeTab === 0 ? (
                    <Stack sx={{gap: '12px'}}>
                        <Typography
                            sx={{
                                color: '#fff',
                                fontFamily: 'var(--primary-font)',
                                fontWeight: 500,
                                fontSize: '20px',
                                lineHeight: '23px',
                            }}
                        >
                            Correct answer
                        </Typography>
                        <TextField
                            placeholder='enter answer'
                            multiline
                            value={textVariants.length > 0 ? textVariants[0].text : ''}
                            onChange={(e) => handleTextVariant(e)}
                            rows={4}
                            sx={{
                                marginBottom: '26px',

                                '& textarea': {
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
                ) : null}
                {activeTab === 1 ? (
                    <Stack sx={{gap: '12px'}}>
                        <Typography
                            sx={{
                                color: '#fff',
                                fontFamily: 'var(--primary-font)',
                                fontWeight: 500,
                                fontSize: '20px',
                                lineHeight: '23px',
                            }}
                        >
                            Variants
                        </Typography>
                        <Stack sx={{gap: '12px'}}>
                            {choiceVariants.map((variant) => (
                                <Stack
                                    key={variant.id}
                                    direction='row'
                                    justifyContent='space-between'
                                    alignItems='center'
                                    sx={{gap: '4px'}}
                                >
                                    <TextField
                                        placeholder='variant'
                                        value={variant.text}
                                        onChange={(e) => handleChangeChoiceVariant(variant.id, e)}
                                        sx={{
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
                                    <IconButton
                                        onClick={() => handleChangeCorrectChoiceVariant(variant.id)}
                                        sx={{
                                            width: 'fit-content',
                                            color: variant.isCorrect ? 'var(--color-success)' : 'var(--color-bg-2)',
                                            transition: 'color .3s',
                                        }}
                                    >
                                        <CheckIcon/>
                                    </IconButton>
                                    <IconButton
                                        onClick={() => handleDeleteChoiceVariant(variant.id)}
                                        sx={{width: 'fit-content', color: 'var(--color-error)'}}
                                    >
                                        <DeleteIcon/>
                                    </IconButton>
                                </Stack>
                            ))}
                            <IconButton
                                onClick={handleAddChoiceVariant}
                                sx={{
                                    margin: '0 auto',
                                    width: 'fit-content',
                                    background: 'var(--color-primary)',
                                    color: '#fff',
                                    transition: 'background .3s',

                                    '&:hover': {
                                        background: '#9dcbf5',
                                    },
                                }}
                            >
                                <AddIcon/>
                            </IconButton>
                        </Stack>
                    </Stack>
                ) : null}
                {activeTab === 2 ? (
                    <Stack sx={{gap: '12px'}}>
                        <Stack
                            sx={{
                                display: 'grid',
                                gridTemplateColumns: '1fr 1fr 40px',
                                gap: '4px',
                            }}
                        >
                            <Typography
                                sx={{
                                    color: '#fff',
                                    fontFamily: 'var(--primary-font)',
                                    fontWeight: 500,
                                    fontSize: '20px',
                                    lineHeight: '23px',
                                }}
                            >
                                Statement
                            </Typography>
                            <Typography
                                sx={{
                                    color: '#fff',
                                    fontFamily: 'var(--primary-font)',
                                    fontWeight: 500,
                                    fontSize: '20px',
                                    lineHeight: '23px',
                                }}
                            >
                                Correct match
                            </Typography>
                        </Stack>
                        {matchVariants.map((variant) => (
                            <Stack
                                key={variant.id}
                                sx={{
                                    display: 'grid',
                                    gridTemplateColumns: '1fr 1fr 40px',
                                    gap: '4px',
                                }}
                            >
                                <TextField
                                    placeholder='variant'
                                    value={variant.text}
                                    onChange={(e) => handleChangeMatchVariant(variant.id, e)}
                                    sx={{
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
                                <TextField
                                    placeholder='correct'
                                    value={variant.subText}
                                    onChange={(e) => handleChangeCorrectMatchVariant(variant.id, e)}
                                    sx={{
                                        '& input': {
                                            fontFamily: 'var(--primary-font)',
                                            color: 'var(--color-100)',
                                        },
                                        '& fieldset': {
                                            transition: 'border-color .2s',
                                            borderColor: 'var(--color-success)',
                                        },
                                        '& .MuiOutlinedInput-root': {
                                            borderRadius: 'var(--border-radius)',
                                            '&.Mui-focused fieldset': {
                                                borderColor: 'var(--color-primary)',
                                            },
                                        },
                                    }}
                                />
                                <IconButton
                                    onClick={() => handleDeleteMatchVariant(variant.id)}
                                    sx={{
                                        width: 'fit-content',
                                        height: 'fit-content',
                                        color: 'var(--color-error)',
                                    }}
                                >
                                    <DeleteIcon/>
                                </IconButton>
                            </Stack>
                        ))}
                        <IconButton
                            onClick={handleAddMatchVariant}
                            sx={{
                                margin: '0 auto',
                                width: 'fit-content',
                                background: 'var(--color-primary)',
                                color: '#fff',
                                transition: 'background .3s',

                                '&:hover': {
                                    background: '#9dcbf5',
                                },
                            }}
                        >
                            <AddIcon/>
                        </IconButton>
                    </Stack>
                ) : null}
            </Stack>
        </SwipeableDrawer>
    )
}
