import React, {useContext} from 'react'
import BaseModal from '../BaseModal'
import {IconButton, Stack, Typography} from '@mui/material'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import {MainContext} from '../../../../context'
import CancelIcon from '@mui/icons-material/Cancel'

export default function InfoModal() {
    const {isInfoModalOpen, setIsInfoModalOpen} = useContext(MainContext)

    return (
        <BaseModal open={isInfoModalOpen} onClose={() => setIsInfoModalOpen(false)}>
            <Stack direction='row' justifyContent='flex-end' sx={{marginBottom: '40px'}}>
                <IconButton
                    onClick={() => setIsInfoModalOpen(false)}
                    sx={{width: 'fit-content', color: 'var(--color-100)'}}
                >
                    <CancelIcon/>
                </IconButton>
            </Stack>
            <Typography
                sx={{
                    marginBottom: '23px',
                    fontWeight: 400,
                    fontSize: '15px',
                    lineHeight: '30px',
                    textAlign: 'center',
                }}
            >
                Чтобы скопировать тест, нажмите на <ContentCopyIcon/> на плашке теста. Теперь вы можете
                вставить скопированный тест куда угодно
            </Typography>
            <Stack
                direction='row'
                justifyContent='space-between'
                alignItems='center'
                sx={{
                    padding: '14px 20px',
                    border: '1px solid var(--color-bg-2)',
                    borderRadius: 'var(--border-radius-2)',
                }}
            >
                <Stack sx={{gap: '30px'}}>
                    <Stack sx={{gap: '3px'}}>
                        <Typography
                            sx={{
                                fontWeight: 400,
                                fontSize: '15px',
                                lineHeight: '18px',
                                color: 'var(--color-bg-2)',
                            }}
                        >
                            Тест по анализу данных
                        </Typography>
                        <Typography
                            sx={{
                                fontWeight: 400,
                                fontSize: '15px',
                                lineHeight: '18px',
                                color: 'var(--color-bg-2)',
                            }}
                        >
                            17 вопросов
                        </Typography>
                    </Stack>
                    <Typography
                        sx={{
                            fontWeight: 400,
                            fontSize: '8px',
                            lineHeight: '10px',
                            color: 'var(--color-bg-2)',
                        }}
                    >
                        отредактировано: 12.10.2022
                    </Typography>
                </Stack>
                <Stack
                    sx={{
                        width: '50px',
                        height: '50px',
                        display: 'grid',
                        placeContent: 'center',
                        borderRadius: '50%',
                        border: '1px solid var(--color-success)',
                    }}
                >
                    <ContentCopyIcon/>
                </Stack>
            </Stack>
        </BaseModal>
    )
}
