import React, {useEffect} from "react";
import {Grid} from "@mui/material";
import RouterCard from "./RouterCard";
import axios from "axios";
import config from "../config";
import {authenticationService} from "../services/Session";

export default function RouterList() {
    const [routers, setRouters] = React.useState([])
    const getRouters = () => {
        axios.get(config.host + 'network/router', {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue,
            }
        }).then((res) => {
            let data = res.data
            if(data.status === 'error') {
                if(data.info === 'Invalid token')
                    authenticationService.logout()
            } else {
                setRouters(res.data)
            }
            console.log(data)
        })
    }
    useEffect(() => {
        getRouters()
    }, [])
    return <Grid container spacing={2}>
        {routers.map((router) => {
            return <Grid item sm={4}>
                <RouterCard router={router} />
            </Grid>
        })}
    </Grid>
}