import React, {useEffect} from "react";
import {
    Dialog,
    DialogContent,
    DialogContentText,
    DialogTitle, IconButton,
    Paper, TableBody, TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";
import axios from "axios";
import config from "../config";
import {authenticationService} from "../services/Session";
import DeleteIcon from '@mui/icons-material/Delete';

export default function ListRouterUserDialog({router, openDialog, onClose}) {
    const [users, setUsers] = React.useState([])

    const getUsers = () => {
        axios.get(config.host + `network/router/${router._id.$oid}/user`, {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            setUsers(data)
        })
    }
    const deleteUser = (userId) => {
        return (event) => {
            axios.delete(config.host + `network/router/${router._id.$oid}/user/${userId}`, {
                headers: {
                    Authorization: 'Bearer ' + authenticationService.currentUserValue
                }
            }).then((res) => {
                let data = res.data
                console.log(data)
                getUsers()
                onClose()
            })
        }
    }
    useEffect(() => {
        getUsers()
    }, [])

    return <Dialog open={openDialog} onClose={onClose}>
        <DialogTitle>Users</DialogTitle>
        <DialogContent>
            <DialogContentText>
                Users for the router with IP {router.ip}
            </DialogContentText>
            <TableContainer component={Paper}>
                <TableHead>
                    <TableRow>
                        <TableCell>Username</TableCell>
                        <TableCell>Privilege</TableCell>
                        <TableCell>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {users.map((user) => {
                        return <TableRow>
                            <TableCell>{user.username}</TableCell>
                            <TableCell>{user.privilege}</TableCell>
                            <TableCell>
                                <IconButton color="secondary" aria-label="add an alarm" onClick={deleteUser(user.id)}>
                                    <DeleteIcon />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    })}
                </TableBody>
            </TableContainer>
        </DialogContent>
    </Dialog>
}