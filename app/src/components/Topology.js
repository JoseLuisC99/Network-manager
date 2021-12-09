import React, {useEffect, useState} from "react";
import axios from "axios";
import { authenticationService } from "../services/Session";
import { Grid } from "@mui/material";
import useNext, { TopologyConfig, TopologyData } from "react-next-ui";
import config from "../config";
import "react-next-ui/build/css/next.min.css";

export default function Topology() {
    const [topology, setTopology] = useState({})

    const getTopology = (force = false) => {
        axios.get(config.host + 'info/topology', {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            if(data.status === 'error') {
                if(data.info === 'Invalid token')
                    authenticationService.logout()
            } else {
                if(force || data.topology != topology)
                    console.log('Cambio')
                setTopology(data)
            }
        }).catch((err) => {
            console.log('Retrying...')
        })
    }
    useEffect(() => {
        getTopology(true)
    }, [])
    useEffect(() => {
        let interval = setInterval(() => {
            getTopology()
        }, 60000)
    }, [])

    let nextConfig = {
        autoLayout: true,
        adaptive: true,
        identityKey: 'id',
        nodeConfig: {
            label: 'model.name',
            iconType: 'router'
        },
        linkConfig: {
            linkType: 'curve'
        },
        showIcon: true,
        dataProcessor: 'force'
    }
    const { NextUI } = useNext({
        topologyData: topology,
        topologyConfig: nextConfig,
        style: { height: "700px", width: "100%" }
    })

    return <>
        <Grid container justifyContent='center' spacing={4}>
            <Grid item sm={10}>
                {NextUI}
            </Grid>
        </Grid>
    </>
}