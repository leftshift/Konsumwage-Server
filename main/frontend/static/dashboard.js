$(document).ready(function () {
  var socket = io.connect(null, {port: 5000, rememberTransport: false});
  socket.on('new_values', function (msg) {
    $('.measurements tbody').append('<tr><td>'+msg.total+'</td><td>'+msg.last_minute+'</td><td>'+msg.last_delta.consumtion + '/' + msg.last_delta.time+'</td><td>'+msg.average+'</td></tr>');
  });
});
