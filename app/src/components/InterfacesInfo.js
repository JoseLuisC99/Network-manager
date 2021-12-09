import React, { useState, useEffect } from "react"
import axios from "axios"
import { Grid, Pagination, Typography, Card, CardHeader, CardContent, Avatar, Tabs, Tab } from "@mui/material"
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

export default function InterfacesInfo() {
    const [interfacesInfo, setInterfacesInfo] = useState()
    const [page, setPage] = useState(1)
    const [router, setRouter] = useState()
    const [interfaceOf, setInterfaceOf] = useState()
    const [interfaceIdx, setInterfaceIdx] = useState()
    const [dataChart, setDataChart] = useState()
    const [optionsChart, setOptionsChart] = useState()    

    const getInterfacesInfo = () => {
        axios.get(config.host + 'info/interfaces', {
            headers: {
                Authorization: 'Bearer ' + authenticationService.currentUserValue
            }
        }).then((res) => {
            let data = res.data
            if(data.status === 'error') {
                if(data.info === 'Invalid token')
                    authenticationService.logout()
            } else {
                data.sort(function(r1, r2) {
                    let x = r1['_id'][0]['hostname']
                    let y = r2['_id'][0]['hostname']
                    if (x < y)
                        return -1;
                    if (x > y)
                        return 1;
                    return 0;
                });
                setInterfacesInfo(data)
                if(data.length > 0) {
                    setRouter(data[0]['_id'][0])
                    setInterfaceOf(data[0]['interfaces'])
                    setInterfaceIdx(1)
                    updateChart(data[0]['interfaces'][0])
                }
            }
        })
    }

    const updateChart = (interfaceSelected) => {
        let data = {
            labels: interfaceSelected['time'].map((date) => { return new Date(date['$date']).toTimeString().split(' ')[0] }),
            datasets: [
                {
                    label: 'Input packages',
                    data: interfaceSelected['inPkgs'],
                    borderColor: 'rgb(11, 132, 165)',
                    backgroundColor: 'rgba(11, 132, 165, 0.5)',
                },
                {
                    label: 'Input error packages',
                    data: interfaceSelected['inErrPkgs'],
                    borderColor: 'rgb(246, 200, 95)',
                    backgroundColor: 'rgba(246, 200, 95, 0.5)',
                },
                {
                    label: 'Output packages',
                    data: interfaceSelected['outPkgs'],
                    borderColor: 'rgb(157, 216, 102)',
                    backgroundColor: 'rgba(157, 216, 102, 0.5)',
                },
                {
                    label: 'Output error packages',
                    data: interfaceSelected['outErrPkgs'],
                    borderColor: 'rgb(202, 71, 47)',
                    backgroundColor: 'rgba(202, 71, 47, 0.5)',
                },
            ]
        }
        let options = {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: `Package flow ${interfaceSelected['description']}`,
                }
            }
        } 
        setDataChart(data)
        setOptionsChart(options)
    }
    
    const handlePaginationChange = (event, value) => {
        setPage(value)
        setRouter(interfacesInfo[value - 1]['_id'][0])
        setInterfaceOf(interfacesInfo[value - 1]['interfaces'])
        setInterfaceIdx(1)
        updateChart(interfaceOf[0])
    }

    const handleInterfaceChange = (event, value) => {
        setInterfaceIdx(value)
        updateChart(interfaceOf[value - 1])
        console.log(interfaceOf[value - 1])
    }

    useEffect(() => {
        getInterfacesInfo()
    }, [])

    return <Grid container>
        <Grid item sm={12}>
            {router && <Card>
                <CardHeader
                    avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">R</Avatar>}
                    title={`Router ${router['hostname']}`}
                    subheader={router['ip']}
                />
                {interfaceOf && interfaceIdx && <CardContent>
                    <Tabs value={interfaceIdx}
                        onChange={handleInterfaceChange}
                        variant="scrollable"
                        scrollButtons="auto"
                    >
                        {interfaceOf.map((interfaceData, i) => {
                            if(interfaceData['status'])
                                return <Tab label={interfaceData['description']} value={i + 1} key={`InterfaceTab_${i}`} />
                        })}
                    </Tabs>
                </CardContent>}
            </Card>}
        </Grid>
        <Grid item sm={12}>
            {dataChart && optionsChart && <Line options={optionsChart} data={dataChart} />}
        </Grid>
        <Grid item sm={12}>
            {interfacesInfo && <Grid container direction="column" alignItems="center" justifyContent="center">
                <Pagination count={interfacesInfo.length} defaultPage={1} page={page} onChange={handlePaginationChange} />
            </Grid>}
        </Grid>
    </Grid>
}