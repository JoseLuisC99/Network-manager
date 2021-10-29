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
                <Button size='small' color='secondary'>Active RSA</Button>
                <Button size='small' color='secondary' onClick={handleOpenNew}>Add new user</Button>
            </CardActions>
        </Card>
        <NewUserDialog router={router} openDialog={openNewUser} onClose={handleCloseNew} />
        <ListRouterUserDialog router={router} openDialog={openUsers} onClose={handleCloseUsers} />
    </>
}