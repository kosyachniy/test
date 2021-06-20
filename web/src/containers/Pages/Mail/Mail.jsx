import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'
import Popup from '../../../components/Popup'


const checkPassword = password => {
    return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)
}

const Auth = (props) => {
    const { profileIn, handlerPopUp } = props
    const { t } = useTranslation()
    const [mail, setMail] = useState('')
    const [password, setPassword] = useState('')

    const signIn = (event) => {
        const handlerSuccess = res => {
            profileIn(res)
            handlerPopUp(false)
        }

        const handlerError = res => {
            console.log(res)
        }

        const data = {login: mail, password: password}
        api('account.auth', data, handlerSuccess, handlerError)

        event.preventDefault();
    }

    return (
        <div id="mail">
            <Popup handlerPopUp={handlerPopUp} >
                <form onSubmit={signIn}>
                    <div className="form-group">
                        <input
                            className="form-control"
                            type="text"
                            placeholder={t('profile.mail')}
                            value={mail}
                            onChange={(event) => { setMail(event.target.value) }}
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            className="form-control"
                            // className={(responce !== null && responce.result === 'password') ? 'error' : ''}
                            type="password"
                            placeholder={t('profile.password')}
                            value={password}
                            onChange={(event) => { setPassword(event.target.value) }}
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className="pass_info">
                        <span style={password.length >= 6 ? {} : { color: '#e74c3c' }}>
                            <i className="fas fa-genderless" />
                            { t('profile.passwordTip1') }
                        </span>
                        <span style={checkPassword(password) ? {} : { color: '#e74c3c' }}>
                            <i className="fas fa-genderless" />
                            { t('profile.passwordTip2') }
                        </span>
                    </div>
                    <input
                        type="submit"
                        className="btn btn-success"
                        value={t('system.sign_in')}
                    />
                </form>
            </Popup>
        </div>
    );
};

export default Auth;
