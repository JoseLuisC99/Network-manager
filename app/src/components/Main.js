import React from "react";
import {Box, Tab} from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import {TabList, TabPanel} from "@mui/lab";
import RouterList from "./RouterList";

export default function Main() {
    const [tabValue, setTabValue] = React.useState('1')
    const handleTabChange = (event, newValue) => {
        setTabValue(newValue)
    }

    return <Box sx={{ width: '100%', typography: 'body1', padding: 0 }}>
        <TabContext value={tabValue}>
            <Box sx={{width: '100%', typography: 'body1', borderColor: 'divider'}}>
                <TabList onChange={handleTabChange}>
                    <Tab label='Routers' value='1' />
                    <Tab label='Users' value='2' />
                </TabList>
            </Box>
            <TabPanel value='1'>
                <RouterList />
            </TabPanel>
            <TabPanel value='2'>
                Hola, mundo!
            </TabPanel>
        </TabContext>
    </Box>
}