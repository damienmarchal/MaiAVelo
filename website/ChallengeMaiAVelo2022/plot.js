function asyncLoadChart(results)
{
  // Split timestamp and data into separate arrays
  var labels = [], data1=[], data2=[], data3=[];

  // Add a helper to format timestamp data
  Date.prototype.formatMMDDYYYY = function() {
    return  this.getDate() +
    "/" + (this.getMonth()+1) +
    "/" + this.getFullYear();
  }

  results["data"].forEach(function(entry)
  {
    labels.push(new Date(entry.date));
    data1.push(parseFloat(entry["progress-2022"]));
    data2.push(parseFloat(entry["progress-2021"]));
    data3.push(parseFloat(entry["progress-2020"]));
  });

  // Instantiate a new chart
  var tempData = {
    labels : labels,
    datasets : [
      {
        pointStyle            : "line",
        borderWidth           : 0.2,
        label                 : "CMV2020",
        backgroundColor       : "rgba(151,00,205,0.5)",
        fillColor             : "rgba(151,187,205,0.5)",
        strokeColor           : "rgba(151,187,205,1)",
        pointColor            : "rgba(151,187,205,1)",
        pointStrokeColor      : "#fff",
        pointHighlightFill    : "#fff",
        pointHighlightStroke  : "rgba(151,187,205,1)",
        data                  :  data3
    },
    {
      pointStyle            : "line",
      borderWidth           : 0.2,
      label                 : "CMV2021",
      backgroundColor       : "rgba(151,187,205,0.8)",
      fillColor             : "rgba(151,187,205,0.8)",
      strokeColor           : "rgba(151,187,205,1)",
      pointColor            : "rgba(151,187,205,1)",
      pointStrokeColor      : "#fff",
      pointHighlightFill    : "#fff",
      pointHighlightStroke  : "rgba(151,187,205,1)",
      data                  : data2
    },
    {
      pointStyle            : "line",
      borderWidth           : 0.2,
      label                 : "MAV2022",
      backgroundColor       : "rgba(255, 87, 51,0.5)",
      fillColor             : "rgba(255, 87, 51,0.2)",
      strokeColor           : "rgba(255, 87, 51,1)",
      pointColor            : "rgba(255, 87, 51,1)",
      pointStrokeColor      : "#fff",
      pointHighlightFill    : "#fff",
      pointHighlightStroke  : "rgba(151,187,205,1)",
      data                  :  data1
    }
    ]
  };

var ctx2 = document.getElementById('chart-cumulative-km')
var myLineChart = new Chart(ctx2, {
            type: "line",
            data: tempData,
            options: {
                     scales: {
                        yAxes: [{
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: 1000
                            }
                       }],
                       xAxes: [{
                            type: "time",
                            time: {
                              min: new Date("2022-05-01"), //, "YYYYMMDD"),
                              max: new Date("2022-05-31") //moment("20200630", "YYYYMMDD")
                          }
                            }]
                     },
                    title: {
                            display: true,
                            text: 'Nombre de km'
                    }
            }
 });

}


(function () {
  'use strict'

  feather.replace()

  var jsonData = $.ajax({
    url: './database/dashboard.json',
    dataType: 'json',
    cache: false
  }).done(asyncLoadChart);

}())
