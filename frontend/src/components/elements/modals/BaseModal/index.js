import React from 'react'
import {Modal} from '@mui/material'
import {Box} from '@mui/system'

export default function BaseModal({children, open, onClose}) {
    return (
        <Modal
            open={open}
            onClose={onClose}
            sx={{
                p: 2,
            }}
        >
            <Box
                sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '100%',
                    maxWidth: '367px',
                    background: 'var(--color-bg-1)',
                    borderRadius: 'var(--border-radius)',
                    padding: '28px',
                }}
            >
                {children}
            </Box>
        </Modal>
    )
}
