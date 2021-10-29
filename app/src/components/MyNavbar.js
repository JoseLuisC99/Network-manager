import React from "react";
import {AppBar, Button, IconButton, Menu, MenuItem, Toolbar, Typography} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import AccountCircle from "@mui/icons-material/AccountCircle"
import {authenticationService} from "../services/Session"

export default function NavBar() {
    const [anchorEl, setAnchorEl] = React.useState(null)
    const [user, setUser] = React.useState(undefined)

    const closeSession = (event) => {
        authenticationService.logout()
        window.location.reload(true)
    }

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget)
    }

    const handleClose = () => {
        setAnchorEl(null)
    }

    return <>
        <AppBar position='static'>
            <Toolbar>
                <IconButton size='large' edge='start' color='inherit' aria-label='menu' sx={{mr: 2}}>
                    <MenuIcon />
                </IconButton>
                <Typography variant='h6' component='div' sx={{flexGrow: 1}}>
                    Network Manager
                </Typography>
                {!authenticationService.currentUserValue? (
                    <div>
                        <Button color='inherit' href='/login'>Login</Button>
                        <Button color='inherit' href='/register'>Register</Button>
                    </div>
                ) : (
                    <div>
                        <IconButton
                            size='large'
                            aria-label='account of current user'
                            aria-controls='menu-appbar'
                            aria-haspopup='true'
                            color='inherit'
                            onClick={handleMenu}
                        >
                            <AccountCircle />
                        </IconButton>
                        <Menu
                            id='menu-appbar'
                            anchorEl={anchorEl}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right'
                            }}
                            open={Boolean(anchorEl)}
                            onClose={handleClose}
                        >
                            <MenuItem onClick={closeSession}>Logout</MenuItem>
                        </Menu>
                    </div>
                )}
            </Toolbar>
        </AppBar>
    </>
}