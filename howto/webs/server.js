#!/usr/bin/env node

/*
npm init -f -y
npm install ws
*/
const WebSocket = require('ws')

const wss = new WebSocket.Server({ port: 5678 })

wss.on('connection', ws => {
  ws.on('message', message => {
    console.log(`Received message => ${message}`)
  })
  ws.send('ho!')
})
