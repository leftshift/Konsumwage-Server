data = []

function graphdata_from_measurement(m) {
  label = new Date(m.timestamp);
  datasets = [m.consumtion, m.consumtion_delta / m.time_delta]
  return [label, datasets]
}

function graphdata_from_history(history) {
  new_data = [];
  for (var m in history) {
    new_data.push(graphdata_from_measurement(history[m]));
  }
  return new_data;
}

$(document).ready(function () {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  past_data = $.ajax({
    url: location.protocol + '//' + document.domain + ':' + location.port + '/api/get/history'
  }).done(function (d) {
    data = d;

    generate_graph(graphdata_from_history(data))
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

var ctx = document.getElementById("canvas")

function generate_graph(dataset){
  l = dataset.map(function (x) {
    return x[0]
  })
  d1 = dataset.map(function (x) {
    return x[1][0]
  })
  graph_data = {
    labels: l,
    datasets: [
        {
            label: "Total Consumtion",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: d1,
            spanGaps: false,
        }
    ]
  }
  var lineChart = new Chart.Line(ctx, {
    data: graph_data,
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
  })
}
