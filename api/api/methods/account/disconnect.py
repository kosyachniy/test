"""
The disconnect socket of the account object of the API
"""

from ...funcs import online_stop


# pylint: disable=unused-argument
async def handle(this, request, data):
    """ Disconnect """

    print('OUT', request.socket)

    await online_stop(this.sio, request.socket)
