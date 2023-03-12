import {Box, IconButton, Stack, Typography} from '@mui/material'
import React, {useContext, useEffect, useState} from 'react'
import InfoIcon from '../../components/elements/icons/InfoIcon'
import AddTestIcon from '../../components/elements/icons/AddTestIcon'
import TestCard from '../../components/elements/cards/TestCard'
import {Link} from 'react-router-dom'
import API from '../../api'
import {MainContext} from '../../context'
import InfoModal from '../../components/elements/modals/InfoModal'

export default function HomePage() {
    const {setIsInfoModalOpen} = useContext(MainContext)
    const [tests, setTests] = useState([])

    useEffect(() => {
        // fetch data
        async function fetchData() {
            const result = await API.get(`/test`, {
                headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
            })
            setTests(result.data)
        }

        fetchData()
    }, [])

    const handleDeleteTest = async (id) => {
        await API.delete(`/test/${id}`, {
            headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`},
        })
        setTests(tests.filter((test) => test.id !== id))
    }

    return (
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
                    Tests
                </Typography>
                <IconButton onClick={() => setIsInfoModalOpen(true)}>
                    <InfoIcon/>
                </IconButton>
            </Stack>
            <Stack
                sx={{
                    gap: '10px',
                }}
            >
                {tests.map((test) => (
                    <TestCard key={test.id} test={test} deleteTest={() => handleDeleteTest(test.id)}/>
                ))}
            </Stack>
            <Stack
                direction='row'
                justifyContent='center'
                sx={{
                    padding: '8px',
                    position: 'fixed',
                    bottom: 0,
                    left: 0,
                    width: '100%',
                    background: 'var(--color-bg-1)',
                }}
            >
                <Link
                    to='/create'
                    style={{
                        WebkitTapHighlightColor: 'transparent',
                    }}
                >
                    <IconButton sx={{width: 'fit-content'}}>
                        <AddTestIcon/>
                    </IconButton>
                </Link>
            </Stack>
            <InfoModal/>
        </Box>
    )
}
