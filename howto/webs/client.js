#!/usr/bin/env node

/*
https://flaviocopes.com/node-websockets/

npm init
npm install ws
*/

const WebSocket = require('ws')
var connection  = new WebSocket("ws://localhost:5678/")

//connection.onmessage = function(e) {
//or, equivalently
//connection.onmessage = (e) => {

connection.onopen = function(e) {
  connection.send('hi')
  setTimeout(() => {
    connection.send('ho')
  }, 2000);
}
connection.onmessage = function(e) {
  console.log(e.data)
  connection.close(1000, "Work complete");
  /*
  setTimeout(() => {
    connection.close(1000, "Work complete");
  }, 2000);
  */
}
/*
Most common code values:

1000 - the default, normal closure (used if no code supplied),
1006 - no way to set such code manually, indicates that the connection was lost (no close frame).
There are other codes like:

1001 - the party is going away, e.g. server is shutting down, or a browser leaves the page,
1009 - the message is too big to process,
1011 - unexpected error on server,
…and so on.
The full list can be found in RFC6455, §7.4.1.
*/

connection.onclose = function() {
  // websocket is closed.
}



