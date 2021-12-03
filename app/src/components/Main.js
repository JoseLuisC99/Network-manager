import React from "react";
import {Box, Tab} from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import {TabList, TabPanel} from "@mui/lab";
import RouterList from "./RouterList";
import NetworkConfig from "./NetworkConfig";
import Topology from "./Topology";

export default function Main() {
    const [tabValue, setTabValue] = React.useState('1')
    const handleTabChange = (event, newValue) => {
        setTabValue(newValue)
    }

    return <Box sx={{ width: '100%', typography: 'body1', padding: 0 }}>
        <TabContext value={tabValue}>
            <Box sx={{width: '100%', typography: 'body1', borderColor: 'divider'}}>
                <TabList onChange={handleTabChange}>
                    <Tab label='Network' value='1' />
                    <Tab label='Routers' value='2' />
                    <Tab label='Users' value='3' />
                    <Tab label='Topology' value='4' />
                </TabList>
            </Box>
            <TabPanel value='1'>
                <NetworkConfig />
            </TabPanel>
            <TabPanel value='2'>
                <RouterList />
            </TabPanel>
            <TabPanel value='3'>
                Hola, mundo!
            </TabPanel>
            <TabPanel value='4'>
                <Topology />
            </TabPanel>
        </TabContext>
    </Box>
}