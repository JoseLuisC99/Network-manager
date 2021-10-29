import { Button, Dialog, DialogContent, DialogTitle, FormControl, Grid, InputLabel, OutlinedInput } from "@mui/material";
import axios from "axios";
import React from "react";
import config from "../config";
import { authenticationService } from "../services/Session";

export default function AddRouterDialog({openDialog, onClose}) {
    const [router, setRouter] = React.useState({
        hostname: '',
        ip: ''
    })
    const handleChange = (prop) => (event) => {
        setRouter({...router, [prop]: event.target.value})
    }
    const addRouter = (event) => {
        console.log(config.host + 'network/router')
        axios.post(config.host + 'network/router', {
            hostname: router.hostname,
            ip: router.ip
        }, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            console.log(data)
            setRouter({
                hostname: '',
                ip: ''
            })
            onClose()
        })
    }

    return <Dialog open={openDialog} onClose={onClose}>
        <DialogTitle>New router</DialogTitle>
        <DialogContent>
            <Grid container spacing={4} style={{paddingTop: 15}}>
                <Grid item sm={12}>
                    <FormControl fullWidth>
                        <InputLabel htmlFor='hostname'>Hostname</InputLabel>
                        <OutlinedInput
                            id='hostname'
                            value={router.hostname}
                            label='Hostname'
                            onChange={handleChange('hostname')}
                        />
                    </FormControl>
                </Grid>
                <Grid item sm={12}>
                    <FormControl fullWidth>
                        <InputLabel htmlFor='ip'>IP</InputLabel>
                        <OutlinedInput
                            id='ip'
                            value={router.ip}
                            label='IP'
                            onChange={handleChange('ip')}
                        />
                    </FormControl>
                </Grid>
                <Grid item sm={12}>
                <Button color='success' variant='outlined' fullWidth onClick={addRouter}>Submit</Button>
                </Grid>
            </Grid>
        </DialogContent>
    </Dialog>
}