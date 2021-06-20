"""
The authorization method of the account object of the API
"""

from ...funcs import check_params, online_start
from ...models.user import User, process_login, process_lower, \
                           pre_process_phone, process_password
from ...models.token import Token
from ...errors import ErrorWrong, ErrorAccess


async def handle(this, **x):
    """ Sign in / Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне

    # Checking parameters

    check_params(x, (
        ('login', True, str), # login / mail / phone
        ('password', True, str),
    ))

    # Data preparation

    # TODO: None / not ''
    # if 'password' in x and not x['password']:
    #     del x['password']

    fields = {
        'login',
        'avatar',
        'name',
        'surname',
        'mail',
        'status',
    } # TODO: optimize

    # Login

    new = False

    try:
        login = process_login(x['login'])
        user = User.get(login=login, fields=fields)[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(x['mail'])
            user = User.get(mail=mail,fields=fields)[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(x['phone'])
            user = User.get(phone=phone, fields=fields)[0]
        except:
            pass
        else:
            new = False

    if not new:
        password = process_password(x['password'])

        try:
            User.get(id=user.id, password=password)
        except:
            raise ErrorWrong('password')

    # Register

    if new:
        user_data = User(
            password=x['password'],
            mail=x['login'], # TODO: login / phone
            mail_verified=False,
        )
        user_data.save()
        user_id = user_data.id

        user = User.get(id=user_id, fields=fields)[0]

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('token')

    token = Token(
        id=this.token,
        user=user.id,
    )

    token.save()

    # Update online users

    await online_start(this.sio, this.token)

    # Response

    res = user.json(fields={
        'id', 'login', 'avatar', 'name', 'surname', 'mail', 'status',
    })
    res['new'] = new

    return res # TODO: del None
