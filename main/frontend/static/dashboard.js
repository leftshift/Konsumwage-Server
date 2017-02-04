$(document).ready(function () {
  var socket = io.connect(null, {port: 5000, rememberTransport: false});
  socket.on('new_values', function (msg) {
    console.log("recieved " + msg);
  });
});
