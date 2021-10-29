import './App.css';
import {BrowserRouter, Redirect, Route, Switch} from "react-router-dom";

import MyNavbar from './components/MyNavbar'
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import {Container} from "@mui/material";
import {ProtectedRoute} from "./ProtectedRoute";
import {PublicRoute} from "./PublicRoute";
import Main from "./components/Main";

function App() {
  return (
    <BrowserRouter>
        <MyNavbar></MyNavbar>
        <Container style={{paddingTop: 30}}>
            <Switch>
                <PublicRoute exact path='/login' component={LoginForm} />
                <PublicRoute exact path='/register' component={RegisterForm} />
                <ProtectedRoute exact path='/' component={Main} />
            </Switch>
        </Container>
    </BrowserRouter>
  );
}

export default App;
