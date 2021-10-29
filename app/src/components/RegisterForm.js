import React from "react";
import {
    Alert, Box,
    Button,
    Card, CardActions,
    CardContent, Collapse,
    FormControl,
    FormHelperText,
    Grid, IconButton,
    InputLabel,
    OutlinedInput,
    Typography
} from "@mui/material";
import axios from "axios";
import config from "../config"
import CloseIcon from "@mui/icons-material/Close";
import {Redirect} from "react-router-dom";
import {authenticationService} from "../services/Session";

export default function RegisterForm() {
    const [userInfo, setUserInfo] = React.useState({
        username: '',
        email: '',
        password: '',
        repeatPassword: ''
    })
    const [showAlert, setShowAlert] = React.useState(false)
    const [alertInfo, setAlertInfo] = React.useState('')
    const [redirect, setRedirect] = React.useState(false)

    const handleChange = (prop) => (event) => {
        setUserInfo({...userInfo, [prop]: event.target.value})
    }
    const sendRegister = async (event) => {
        event.preventDefault()
        if(userInfo.password !== userInfo.repeatPassword) {
            setAlertInfo('Passwords do not match')
            setShowAlert(true)
            return
        }
        axios.post(config.host + 'auth/register', {
            username: userInfo.username,
            password: userInfo.password
        }).then((res) => {
            let data = res.data
            if(data.status === 'error') {
                setAlertInfo(data.info)
                setShowAlert(true)
            } else {
                setRedirect(true)
            }
        })
    }

    return <>
        <Grid container justifyContent='center' spacing={2} >
            <Grid item xs={6}>
                <Card>
                    <CardContent>
                        <Typography variant='h4' component='div' className='text-centered'>
                            Register
                        </Typography>
                        <Grid container spacing={4}>
                            <Grid item xs={12}>
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
                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel htmlFor='email'>Email</InputLabel>
                                    <OutlinedInput
                                        id='email'
                                        type='email'
                                        value={userInfo.email}
                                        label='Email'
                                        onChange={handleChange('email')}
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item xs={12}>
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
                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel htmlFor='repeat_password'>Repeat password</InputLabel>
                                    <OutlinedInput
                                        id='repeat_password'
                                        type='password'
                                        value={userInfo.repeatPassword}
                                        label='Repeat password'
                                        onChange={handleChange('repeatPassword')}
                                    />
                                </FormControl>
                            </Grid>
                        </Grid>
                    </CardContent>
                    <CardActions>
                        <Button variant='outlined' fullWidth onClick={sendRegister}>
                            Submit
                        </Button>
                    </CardActions>
                </Card>
                <Box sx={{width: '100%'}} style={{marginTop: 20}}>
                    <Collapse in={showAlert}>
                        <Alert
                            severity='error'
                            action={
                                <IconButton
                                    aria-label='close'
                                    color='inherit'
                                    size='small'
                                    onClick={() => {
                                        setShowAlert(false)
                                    }}
                                >
                                    <CloseIcon fontSize="inherit" />
                                </IconButton>
                            }
                        >
                            {alertInfo}
                        </Alert>
                    </Collapse>
                </Box>
            </Grid>
        </Grid>
        {redirect && (
            <Redirect to='/login' />
        )}
    </>
}