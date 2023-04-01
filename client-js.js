const { io } = require('socket.io-client');
const socket = io('http://127.0.0.1:8000',{query : {indentity : 'xlx',type : "operator"}});

socket.on('connect',async () => {
    console.log('connected !');
})

socket.on('disconnect',async () => {
    console.log('disconnected !');
})