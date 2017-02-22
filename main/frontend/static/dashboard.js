data = []

$(document).ready(function () {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  // generate_graph()
  past_data = $.ajax({
    url: location.protocol + '//' + document.domain + ':' + location.port + '/api/get/history'
  }).done(function (d) {
    data = d;
    socket.on('new_values', function (msg) {
      console.log("new_values: " + msg);
      $('.measurements tbody').append('<tr><td>'+msg.total+'</td><td>'+msg.last_minute+'</td><td>'+msg.last_delta.consumtion + '/' + msg.last_delta.time+'</td><td>'+msg.average+'</td></tr>');

      // In liters/second
      $("#current_consumtion").text((msg.last_delta.consumtion / msg.last_delta.time).toFixed(1));
      $("#average_consumtion").text(msg.average.toFixed(1));
      $("#total_consumtion").text(msg.total);
    });
  })
});


var margin = {top: 30, right: 30, bottom: 40, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scaleTime()
var y = d3.scaleLinear()

var xAxis = d3.axisBottom(x);

var yAxis = d3.axisLeft(y);

d3.select("#graph").append("svg:svg")
    .attr("width", "100%")
    .attr("height", "100%")
  .append("g")
    .call(yAxis)
