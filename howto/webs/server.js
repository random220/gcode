#!/usr/bin/env node

/*
npm init -f -y
npm install ws
*/
const WebSocket = require('ws')
const wss = new WebSocket.Server({ port: 5678 })

/*
wss.on('connection', ws => {
  ws.on('message', message => {
    console.log(`Received message => ${message}`)
  })
  ws.send(`ho!`)
})
*/

/*
wss.on('connection', function(ws) {
  ws.on('message', function(message) {
    console.log(`Received message => ${message}`)
  })
  ws.send(`ho!`)
})
*/



wss.on('connection', onconn)

function onconn(ws) {
  ws.on('message', onmsg)
  ws.send(`ho!`)
}

function onmsg(messge) {
  console.log(`Received message => ${message}`)
}
