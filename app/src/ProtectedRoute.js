import React from "react";
import {Route, Redirect} from "react-router-dom";
import {authenticationService} from "./services/Session"

export const ProtectedRoute = ({component: Component, ...rest}) => (
    <Route {...rest} render={props => {
        const currentUser = authenticationService.currentUserValue;
        if (!currentUser) {
            return <Redirect to={{pathname: '/login', state: {from: props.location}}} />
        }
        return <Component {...props} />
    }} />
)