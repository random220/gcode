/*
npm init
npm install ws
*/
const WebSocket = require('ws')
var connection  = new WebSocket("ws://localhost:5678/")

//connection.onmessage = function(e) {
//or, equivalently
//connection.onmessage = (e) => {

connection.onmessage = function(e) {
  console.log(e.data)
}
