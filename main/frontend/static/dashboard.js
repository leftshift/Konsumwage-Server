$(document).ready(function () {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('new_values', function (msg) {
    console.log(new_values);
    $('.measurements tbody').append('<tr><td>'+msg.total+'</td><td>'+msg.last_minute+'</td><td>'+msg.last_delta.consumtion + '/' + msg.last_delta.time+'</td><td>'+msg.average+'</td></tr>');
  });
});
