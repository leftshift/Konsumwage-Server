var data = [];
var lineChart = null;

var total = 0;
var last_measurement;

function datapoint_from_measurement(m, total) {
  label = new Date(m.timestamp * 1000);
  datasets = [total, m.consumption_delta / m.time_delta];
  return [label, datasets];
}

function graphdata_from_history(history) {
  new_data = [];
  total = 0;
  for (var m in history) {
    if (history[m].consumption_delta > 0) {
      total = total + history[m].consumption_delta;
      console.log(total);
    }
    new_data.push(datapoint_from_measurement(history[m], total));
  }
  return new_data;
}

function update_dashboard(delta_consumption, delta_time, average, total) {
  $("#current_consumption").text((delta_consumption / delta_time).toFixed(1));
  if (average) {
    $("#average_consumption").text(average.toFixed(1));
  }
  $("#total_consumption").text(total.toFixed(1));
}


function major_update(msg) {
  last_measurement = msg;
  lineChart.data.datasets[0].data.push(msg.total);
  lineChart.data.labels.push(new Date());
  lineChart.update();

  update_dashboard(msg.last_delta.consumption, msg.last_delta.time, msg.average, msg.total);
}

function minor_update(msg) {
  update_dashboard(msg.delta_consumption, msg.delta_time, null, msg.total);
}

$(document).ready(function () {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  past_data = $.ajax({
    url: location.protocol + '//' + document.domain + ':' + location.port + '/api/get/history'
  }).done(function (d) {
    data = d;

    generate_graph(graphdata_from_history(data));
    socket.on('major_update', major_update);
    socket.on('minor_update', minor_update);
  });
});

var ctx = document.getElementById("canvas");

function generate_graph(dataset){
  l = dataset.map(function (x) {
    return x[0];
  });
  d1 = dataset.map(function (x) {
    return x[1][0];
  });
  graph_data = {
    labels: l,
    datasets: [
        {
            label: "Total consumption",
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
            cubicInterpolationMode: 'linear'
        }
    ]
  };
  lineChart = new Chart.Line(ctx, {
    data: graph_data,
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }],
            xAxes: [{
                type: 'time',
            }]
        }
    }
  });
}
