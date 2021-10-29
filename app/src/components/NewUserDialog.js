import React from "react";
import {
    Button,
    Dialog,
    DialogContent,
    DialogContentText,
    DialogTitle,
    FormControl,
    Grid, InputLabel,
    OutlinedInput,
    TextField
} from "@mui/material";
import axios from "axios";
import config from "../config";
import {authenticationService} from "../services/Session";

export default function NewUserDialog({router, openDialog, onClose}) {
    const [userInfo, setUserInfo] = React.useState({
        username: '',
        privilege: 15,
        password: ''
    })
    const handleChange = (prop) => (event) => {
        setUserInfo({...userInfo, [prop]: event.target.value})
    }
    const createUser = (event) => {
        event.preventDefault()
        axios.post(config.host + `network/router/${router._id.$oid}/user`, {
            username: userInfo.username,
            privilege: userInfo.privilege,
            password: userInfo.password
        }, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            onClose()
        })
    }

    return <Dialog open={openDialog} onClose={onClose}>
        <DialogTitle>New user</DialogTitle>
        <DialogContent>
            <DialogContentText>
                Add new user to the router with IP {router.ip}
            </DialogContentText>
            <Grid container spacing={4} style={{paddingTop: 15}}>
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
                    <Button color='success' variant='outlined' fullWidth onClick={createUser}>Create new user</Button>
                </Grid>
            </Grid>
        </DialogContent>
    </Dialog>
}