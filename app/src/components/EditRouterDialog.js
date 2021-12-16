import React from "react"
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

export default function EditRouterDialog({router, openDialog, onClose}) {
    const [routerInfo, setRouterInfo] = React.useState(router)
    
    const handleChange = (prop) => (event) => {
        setRouterInfo({...routerInfo, [prop]: event.target.value})
    }
    const editRouter = (event) => {
        event.preventDefault()
        axios.put(config.host + `network/router/${router._id.$oid}`, {
            hostname: routerInfo.hostname,
            contact: routerInfo.contact,
            location: routerInfo.location
        }, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            console.log(data)
            onClose()
        })
    }

    return <Dialog open={openDialog} onClose={onClose}>
        <DialogTitle>Edit router {routerInfo.hostname}</DialogTitle>
        <DialogContent>
            <Grid container spacing={4} style={{paddingTop: 15}}>
                <Grid item sm={12}>
                    <FormControl fullWidth>
                        <InputLabel htmlFor='hostname'>Hostname</InputLabel>
                        <OutlinedInput
                            id='hostname'
                            value={routerInfo.hostname}
                            label='Hostname'
                            onChange={handleChange('hostname')}
                        />
                    </FormControl>
                </Grid>
                <Grid item sm={12}>
                    <FormControl fullWidth>
                        <InputLabel htmlFor='contact'>Contact</InputLabel>
                        <OutlinedInput
                            id='contact'
                            value={routerInfo.contact}
                            label='Contact'
                            onChange={handleChange('contact')}
                        />
                    </FormControl>
                </Grid>
                <Grid item sm={12}>
                    <FormControl fullWidth>
                        <InputLabel htmlFor='location'>Location</InputLabel>
                        <OutlinedInput
                            id='location'
                            value={routerInfo.location}
                            label='Location'
                            onChange={handleChange('location')}
                        />
                    </FormControl>
                </Grid>
                <Grid item sm={12}>
                    <Button color='success' variant='outlined' fullWidth onClick={editRouter}>Save changes</Button>
                </Grid>
            </Grid>
        </DialogContent>
    </Dialog>
}