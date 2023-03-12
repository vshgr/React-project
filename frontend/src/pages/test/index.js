import {Box, IconButton, Stack, Typography} from '@mui/material'
import React, {useEffect, useState} from 'react'
import {Link, useParams} from 'react-router-dom'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import BorderColorIcon from '@mui/icons-material/BorderColor'
import API from '../../api'

export default function TestPage() {
    let {testId} = useParams()
    const [test, setTest] = useState(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        // fetch data
        async function fetchData() {
            const result = await API.get(`/test/${testId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                },
            })
            setTest(result.data)
            setLoading(false)
        }

        fetchData()
    }, [])

    return (
        !loading && (
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
                                width: 'clamp(100px, 50vw, 600px)',
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                            }}
                        >
                            {test?.title}
                        </Typography>
                    </Stack>
                    <Link
                        to={`/edit/${testId}`}
                        style={{
                            WebkitTapHighlightColor: 'transparent',
                        }}
                    >
                        <IconButton sx={{color: 'var(--color-100)'}}>
                            <BorderColorIcon/>
                        </IconButton>
                    </Link>
                </Stack>
                <Stack
                    sx={{
                        gap: '38px',
                    }}
                >
                  {test?.questions.map((question, index) => {
                      switch (question.type) {
                          case 'text':
                              return (
                                  <Stack
                                      alignItems='center'
                                      sx={{
                                          display: 'grid',
                                          gridTemplateColumns: '21px 1fr',
                                          gap: '14px',
                                      }}
                                  >
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '18px',
                                              lineHeight: '21px',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {index + 1}
                                      </Typography>
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '15px',
                                              lineHeight: '18px',
                                              maxWidth: 'clamp(100px, 50vw, 1000px)',
                                              wordBreak: 'break-word',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {question.title}
                                      </Typography>
                                      <Typography
                                          sx={{
                                              gridColumn: '2 / 3',
                                              fontWeight: 400,
                                              fontSize: '15px',
                                              lineHeight: '18px',
                                              maxWidth: 'clamp(100px, 50vw, 1000px)',
                                              wordBreak: 'break-word',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {question.answers[0].text}
                                      </Typography>
                                  </Stack>
                              )
                          case 'match':
                              return (
                                  <Stack
                                      alignItems='center'
                                      sx={{
                                          display: 'grid',
                                          gridTemplateColumns: '21px 1fr',
                                          gap: '14px',
                                      }}
                                  >
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '18px',
                                              lineHeight: '21px',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {index + 1}
                                      </Typography>
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '15px',
                                              lineHeight: '18px',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {question.title}
                                      </Typography>
                                      <Stack
                                          sx={{
                                              gridColumn: '2 / 3',
                                              gap: '21px',
                                          }}
                                      >
                                          {question.answers.map((answer, index) => (
                                              <Stack
                                                  sx={{
                                                      position: 'relative',
                                                      display: 'grid',
                                                      gridTemplateColumns: '1fr 1fr',

                                                      '&:not(:last-child)::after': {
                                                          content: '""',
                                                          position: 'absolute',
                                                          bottom: '-12px',
                                                          left: 0,
                                                          width: '100%',
                                                          height: '1px',
                                                          background: 'var(--color-bg-2)',
                                                      },
                                                  }}
                                              >
                                                  <Typography
                                                      sx={{
                                                          fontWeight: 400,
                                                          fontSize: '15px',
                                                          lineHeight: '18px',
                                                          maxWidth: 'clamp(100px, 50vw, 1000px)',
                                                          wordBreak: 'break-word',
                                                          fontFamily: 'var(--primary-font)',
                                                      }}
                                                  >
                                                      {answer.text}
                                                  </Typography>
                                                  <Typography
                                                      sx={{
                                                          fontWeight: 400,
                                                          fontSize: '15px',
                                                          lineHeight: '18px',
                                                          maxWidth: 'clamp(100px, 50vw, 1000px)',
                                                          wordBreak: 'break-word',
                                                          fontFamily: 'var(--primary-font)',
                                                      }}
                                                  >
                                                      {answer.subText}
                                                  </Typography>
                                              </Stack>
                                          ))}
                                      </Stack>
                                  </Stack>
                              )
                          case 'choice':
                              return (
                                  <Stack
                                      alignItems='center'
                                      sx={{
                                          display: 'grid',
                                          gridTemplateColumns: '21px 1fr',
                                          gap: '14px',
                                      }}
                                  >
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '18px',
                                              lineHeight: '21px',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {index + 1}
                                      </Typography>
                                      <Typography
                                          sx={{
                                              fontWeight: 700,
                                              fontSize: '15px',
                                              lineHeight: '18px',
                                              fontFamily: 'var(--primary-font)',
                                          }}
                                      >
                                          {question.title}
                                      </Typography>
                                      <Stack
                                          sx={{
                                              gridColumn: '2 / 3',
                                              gap: '10px',
                                          }}
                                      >
                                          {question.answers.map((answer, index) => (
                                              <Typography
                                                  key={index}
                                                  sx={{
                                                      fontWeight: 400,
                                                      fontSize: '15px',
                                                      lineHeight: '18px',
                                                      fontFamily: 'var(--primary-font)',
                                                      color: answer.isCorrect ? 'var(--color-success)' : null,
                                                  }}
                                              >
                                                  {answer.text}
                                              </Typography>
                                          ))}
                                      </Stack>
                                  </Stack>
                              )
                              default:
                                return null
                        }
                    })}
                </Stack>
            </Box>
        )
    )
}
