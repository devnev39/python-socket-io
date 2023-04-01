import socketio

sio  = socketio.AsyncServer(async_mode = 'asgi')
app = socketio.ASGIApp(sio)

operators = []
guards = []

def convert_to_key_val(query_string : str) -> dict:
    key_val_pairs = query_string.split('&')
    key_vals = dict()
    for pair in key_val_pairs:
        key_vals[pair.split('=')[0]] = pair.split('=')[1]
    return key_vals

@sio.event
async def connect(sid,environ):
    print('connected ',sid)
    key_vals = convert_to_key_val(environ['QUERY_STRING'])

    if key_vals.get('type') == 'operator':
        operators.append({'identity' : 'operator','socketId' : sid})
        await sio.emit('update-operator',operators)
    
    if key_vals.get('type') == 'guard':
        guards.append({'indentity' : 'guard','socketId' : sid})
        await sio.emit('update-operator',guards)
    
@sio.on('get-guard-list')
async def get_guard_list(sid):
    await sio.emit('get-guard-list',guards,sid)

@sio.on('get-operator-list')
async def get_operator_list(sid):
    await sio.emit('get-operator-list',operators,sid)

@sio.on('send-call-request')
async def send_call_request(sid,data):
    receiverSocketID = data.get('receiverSocketID')
    senderIdentity = data.get('senderIdentity')
    senderSocketID = data.get('senderSocketID')
    
    await sio.emit('receive-call-request',{
        'senderIdentity' : senderIdentity,
        'senderSocketID' : senderSocketID
    },receiverSocketID)

@sio.on('answer-call-request')
async def send_call_request(sid,data):
    await sio.emit('receive-call-request',{
        'accept' : data.get('accept'),
        'peerId' : data.get('peerId')
    },data.get('senderSocketID'))