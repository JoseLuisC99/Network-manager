import { Backdrop, Button, CircularProgress, FormControl, Grid, InputLabel, OutlinedInput, ToggleButton, ToggleButtonGroup, Typography } from "@mui/material";
import axios from "axios";
import React from "react";
import config from "../config";
import { authenticationService } from "../services/Session";
import AddRouterDialog from "./AddRouterDialog";

export default function NetworkConfig() {
    const [protocol, setProtocol] = React.useState('RIP')
    const [backdrop, setBackdrop] = React.useState(false)
    const [userInfo, setUserInfo] = React.useState({
        username: '',
        privilege: 15,
        password: ''
    })
    const [openAddRouter, setOpenAddRouter] = React.useState(false)

    const changeProtocol = (event) => {
        setBackdrop(true)
        console.log(protocol.toLowerCase())
        axios.post(config.host + 'network/configure', {
            method: protocol.toLowerCase()
        }, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            console.log(data)
            setBackdrop(false)
        })
    }
    const handleChangeProtocol = (event, newProtocol) => {
        setProtocol(newProtocol)
    }

    const handleChange = (prop) => (event) => {
        setUserInfo({...userInfo, [prop]: event.target.value})
    }

    const sendSSH = (event) => {
        setBackdrop(true)
        axios.post(config.host + 'network/configure/users', {
            username: userInfo.username,
            privilege: userInfo.privilege,
            password: userInfo.password
        }, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            console.log(data)
            setBackdrop(false)
        })
    }

    const handleOpenRouter = (event) => {
        setOpenAddRouter(true)
    }
    const handleCloseRouter = (event) => {
        setOpenAddRouter(false)
    }

    return <>
        <Grid container justifyContent='center' spacing={4}>
            <Grid item sm={8}>
                <Grid container spacing={4}>
                    <Grid item sm={12}>
                        <Typography variant='h5' component='div'>Routing protocol: {protocol}</Typography>
                    </Grid>
                    <Grid item sm={12}>
                        <ToggleButtonGroup
                            value={protocol}
                            exclusive
                            onChange={handleChangeProtocol}
                        >
                            <ToggleButton value='RIP'>RIP</ToggleButton>
                            <ToggleButton value='OSPF'>OSPF</ToggleButton>
                            <ToggleButton value='EIGRP'>EIGRP</ToggleButton>
                        </ToggleButtonGroup>
                        <Button variant='outlined' style={{marginLeft: 50}} onClick={changeProtocol}>Change protocol</Button>
                    </Grid>

                    <Grid item sm={12}>
                        <Typography variant='h5' component='div'>Global SSH users</Typography>
                    </Grid>
                    <Grid item sm={12}>
                        <FormControl fullWidth>
                            <InputLabel htmlFor='username'>Username</InputLabel>
                            <OutlinedInput
                                id='username'
                                value={userInfo.username}
                                label='Username'
                                onChange={handleChange('username')}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item sm={12}>
                        <FormControl fullWidth>
                            <InputLabel htmlFor='privilege'>Privilege</InputLabel>
                            <OutlinedInput
                                id='privilege'
                                type='number'
                                value={userInfo.privilege}
                                label='Privilege'
                                onChange={handleChange('privilege')}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item sm={12}>
                        <FormControl fullWidth>
                            <InputLabel htmlFor='password'>Password</InputLabel>
                            <OutlinedInput
                                id='password'
                                type='password'
                                value={userInfo.password}
                                label='Password'
                                onChange={handleChange('password')}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item sm={12}>
                        <Button variant='outlined' fullWidth onClick={sendSSH}>
                            Submit
                        </Button>
                    </Grid>

                    <Grid item sm={12}>
                        <Typography variant='h5' component='div'>Routers</Typography>
                    </Grid>
                    <Grid item sm={12}>
                        <Button variant='contained' color='success' fullWidth onClick={handleOpenRouter}>
                            Add router
                        </Button>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
        <Backdrop
            sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
            open={backdrop}
        >
            <CircularProgress color='inherit' />
        </Backdrop>
        <AddRouterDialog openDialog={openAddRouter} onClose={handleCloseRouter} />
    </>
}