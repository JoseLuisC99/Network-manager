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
import EditRouterDialog from "./EditRouterDialog";
import axios from "axios";
import config from "../config";
import { authenticationService } from "../services/Session";

export default function RouterCard({router}) {
    const [openNewUser, setOpenNewUser] = React.useState(false)
    const [openUsers, setOpenUsers] = React.useState(false)
    const [openEdit, setOpenEdit] = React.useState(false)

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
    const handleOpenEdit = (event) => {
        setOpenEdit(true)
    }
    const handleCloseEdit = (event) => {
        setOpenEdit(false)
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
                <Typography variant='subtitle2' display='block' component='div'>
                    <span style={{fontWeight: 'bold'}}>Contact</span>: {router.contact}
                </Typography>
                <Typography variant='subtitle2' display='block' component='div'>
                    <span style={{fontWeight: 'bold'}}>Location</span>: {router.location}
                </Typography>
                <Typography variant='caption' display='block' color='text.secondary'>
                    {router.description}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size='small' color='secondary' onClick={handleOpenUsers}>View users</Button>
                <Button size='small' color='secondary' onClick={handleOpenNew}>Add new user</Button>
                {/* <Button size='small' color='error' onClick={deleteRouter}>Delete</Button> */}
                <Button size='small' color='primary' onClick={handleOpenEdit}>Edit</Button>
            </CardActions>
        </Card>
        <NewUserDialog router={router} openDialog={openNewUser} onClose={handleCloseNew} />
        <ListRouterUserDialog router={router} openDialog={openUsers} onClose={handleCloseUsers} />
        <EditRouterDialog router={router} openDialog={openEdit} onClose={handleCloseEdit} />
    </>
}