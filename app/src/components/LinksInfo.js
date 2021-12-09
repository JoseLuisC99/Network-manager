import React, { useState, useEffect } from "react"
import axios from "axios"
import { Grid, Pagination, Card, CardHeader, CardContent, Avatar, Tabs, Tab } from "@mui/material"
import { red } from "@mui/material/colors"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

import { authenticationService } from "../services/Session"
import config from "../config"

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function LinksInfo() {
    const [linksInfo, setLinksInfo] = useState()
    const [link, setLink] = useState()
    const [page, setPage] = useState(1)
    const [dataChart, setDataChart] = useState()
    const [optionsChart, setOptionsChart] = useState()    

    const getLinksInfo = () => {
        axios.get(config.host + 'info/link', {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            if(data.status === 'error') {
                if(data.info === 'Invalid token')
                    authenticationService.logout()
            } else {
                let links = []
                for(const [ip, data] of Object.entries(res.data)) {
                    links.push({
                        ip: ip,
                        router_1: data['interface_1']['router']['hostname'],
                        router_2: data['interface_2']['router']['hostname'],
                        interface_1: data['interface_1']['description'],
                        interface_2: data['interface_2']['description'],
                        loss_12: data['loss_12'],
                        loss_21: data['loss_21'],
                        time: data['interface_1']['time']
                    })
                }
                console.log(links)
                setLinksInfo(links)
                setLink(links[0])
                updateChart(links[0])
            }
        })
    }

    const updateChart = (linkSelected) => {
        let data = {
            labels: linkSelected['time'].map((date) => { return new Date(date).toTimeString().split(' ')[0] }),
            datasets: [
                {
                    label: `Loss packages from ${linkSelected['router_1']} to ${linkSelected['router_2']}`,
                    data: linkSelected['loss_12'],
                    borderColor: 'rgb(11, 132, 165)',
                    backgroundColor: 'rgba(11, 132, 165, 0.5)',
                },
                {
                    label: `Loss packages from ${linkSelected['router_2']} to ${linkSelected['router_1']}`,
                    data: linkSelected['loss_21'],
                    borderColor: 'rgb(202, 71, 47)',
                    backgroundColor: 'rgba(202, 71, 47, 0.5)',
                }
            ]
        }
        let options = {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: `Package flow subnetwork ${linkSelected['ip']}`,
                }
            }
        } 
        setDataChart(data)
        setOptionsChart(options)
    }
    
    const handlePaginationChange = (event, value) => {
        setPage(value)
        setLink(linksInfo[value - 1])
        updateChart(linksInfo[value - 1])
    }

    useEffect(() => {
        getLinksInfo()
    }, [])

    return <Grid container>
        <Grid item sm={12}>
            {link && <Card>
                <CardHeader
                    avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">L</Avatar>}
                    title={`Subnetwork ${link['ip']}`}
                    subheader={`Connection between ${link['router_1']} (${link['interface_1']}) and ${link['router_2']} (${link['interface_2']})`}
                />
            </Card>}
        </Grid>
        <Grid item sm={12}>
            {dataChart && optionsChart && <Line options={optionsChart} data={dataChart} />}
        </Grid>
        <Grid item sm={12}>
            {linksInfo && <Grid container direction="column" alignItems="center" justifyContent="center">
                <Pagination count={linksInfo.length} defaultPage={1} page={page} onChange={handlePaginationChange} />
            </Grid>}
        </Grid>
    </Grid>
}