import React from "react";
import {authenticationService} from "../services/Session"
import {
    Alert,
    Box,
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
import CloseIcon from "@mui/icons-material/Close";

export default function LoginForm() {
    const [userInfo, setUserInfo] = React.useState({
        username: '',
        password: ''
    })
    const [showAlert, setShowAlert] = React.useState(false)
    const [alertInfo, setAlertInfo] = React.useState('')

    const handleChange = (prop) => (event) => {
        setUserInfo({...userInfo, [prop]: event.target.value})
    }
    const sendLogin = async (event) => {
        event.preventDefault()
        let data = await authenticationService.login(userInfo.username, userInfo.password)
        if(data.token) {
            window.location.reload(true)
        } else {
            setAlertInfo(data.info)
            setShowAlert(true)
        }
    }

    return <Grid container justifyContent='center' spacing={2} >
        <Grid item xs={6}>
            <Card>
                <CardContent>
                    <Typography variant='h4' component='div' className='text-centered'>
                        Login
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
                                <InputLabel htmlFor='password'>Password</InputLabel>
                                <OutlinedInput
                                    id='password'
                                    type='password'
                                    value={userInfo.password}
                                    label='Password'
                                    onChange={handleChange('password')}
                                />
                                <FormHelperText>Do not share your password with anyone</FormHelperText>
                            </FormControl>
                        </Grid>
                    </Grid>
                </CardContent>
                <CardActions>
                    <Button variant='outlined' fullWidth onClick={sendLogin}>
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
}