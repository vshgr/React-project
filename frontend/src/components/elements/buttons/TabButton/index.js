import {Button, Typography} from '@mui/material'
import React from 'react'

export default function TabButton({children, onClick, active, ...props}) {
    return (
        <Button
            variant='outlined'
            onClick={onClick}
            sx={{
                position: 'relative',
                padding: '0',
                textTransform: 'none',
                background: active ? 'transparent' : 'var(--color-bg-1)',
                border: 'none',
                borderRadius: 'var(--border-radius-2)',

                '&::after': {
                    content: '""',
                    position: 'absolute',
                    top: '-1px',
                    bottom: '-1px',
                    left: '-1px',
                    right: '-1px',
                    background: 'var(--color-primary-2)',
                    borderRadius: 'var(--border-radius-2)',
                    zIndex: -1,
                },

                '&:hover': {
                    border: 'none',
                    // background: active
                    //   ? 'var(--color-primary-acc2)'
                    //   : 'var(--color-primary-acc1)',
                },
            }}
            {...props}
        >
            <Typography
                sx={{
                    padding: '10px 20px',
                    fontWeight: 400,
                    fontSize: '15px',
                    lineHeight: '18px',
                    background: active ? '#fff' : 'var(--color-primary-3)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',

                    '&:hover': {
                        background: '#fff',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                    },
                }}
            >
                {children}
            </Typography>
        </Button>
    )
}
