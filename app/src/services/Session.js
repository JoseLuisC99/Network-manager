import Cookies from "js-cookie";
import {BehaviorSubject} from "rxjs";
import axios from "axios";
import config from "../config";

const currentUserSubject = new BehaviorSubject(Cookies.get('__token'))

async function login(username, password) {
    let res = await axios.post(config.host + 'auth/login', {
        username: username,
        password: password
    })
    let data = res.data
    console.log(data)
    if(data.token)
        Cookies.set('__token', data.token)
    return data
}

function logout() {
    Cookies.remove('__token')
}

export const authenticationService = {
    login,
    logout,
    currentUser: currentUserSubject.asObservable(),
    get currentUserValue() { return currentUserSubject.value }
}