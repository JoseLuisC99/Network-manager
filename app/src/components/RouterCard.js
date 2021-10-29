import React from "react";
import {
    Button,
    Card,
    CardActions,
    CardContent,
    Typography
} from "@mui/material";
import NewUserDialog from "./NewUserDialog";
import ListRouterUserDialog from "./ListRouterUserDialog";
import axios from "axios";
import config from "../config";
import { authenticationService } from "../services/Session";

export default function RouterCard({router}) {
    const [openNewUser, setOpenNewUser] = React.useState(false)
    const [openUsers, setOpenUsers] = React.useState(false)

    const handleOpenNew = () => {
        setOpenNewUser(true)
    }
    const handleCloseNew= () => {
        setOpenNewUser(false)
    }
    const handleOpenUsers = () => {
        setOpenUsers(true)
    }
    const handleCloseUsers = () => {
        setOpenUsers(false)
    }
    const deleteRouter = (event) => {
        axios.delete(config.host + `network/router/${router._id.$oid}`, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            console.log(data)
            window.location.reload(true)
        })
    }

    return <>
        <Card sx={{minWidth: 275}}>
            <CardContent>
                <Typography sx={{fontSize: 14}} color='text.secondary' gutterBottom>
                    {router.ip}
                </Typography>
                <Typography variant='h5' component='div'>
                    {router.hostname}
                </Typography>
                <Typography sx={{mb: 1.5}} color='text.secondary'>
                    cisco-ios
                </Typography>
            </CardContent>
            <CardActions>
                <Button size='small' color='secondary' onClick={handleOpenUsers}>View users</Button>
                <Button size='small' color='secondary' onClick={handleOpenNew}>Add new user</Button>
                <Button size='small' color='error' onClick={deleteRouter}>Delete</Button>
            </CardActions>
        </Card>
        <NewUserDialog router={router} openDialog={openNewUser} onClose={handleCloseNew} />
        <ListRouterUserDialog router={router} openDialog={openUsers} onClose={handleCloseUsers} />
    </>
}