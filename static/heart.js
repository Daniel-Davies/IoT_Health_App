var myTimedVar = 23;
function heartChartBase(){
  myTimedVar = setInterval(retrieveLiveHeart, 1000);
  document.getElementById("selector1").className = "btn btn-lg btn-secondary"
  document.getElementById("selector2").className = "btn btn-lg btn-primary"
  $.getJSON('/chart_heart',
    function(data) {
      heartChart(data)
    });
}

function refreshChart(){
  $.getJSON('/chart_heart',
    function(data) {
      drawHighChart(data)
    });
}

function retrieveLiveHeart(){
  $.getJSON('/live_heart',
    function(data) {
      document.getElementById("heartBeatEntry").innerHTML = data[0]
      document.getElementById("heartTime").innerHTML = "Last heart rate reading:" + data[1]
    });
}

function drawHighChart(data) {
  Highcharts.chart('chart_container', {

   title: {
     text: 'Average Heart Rate per Hour'
   },

   yAxis: {
     title: {
       text: 'Average Beats per Minute'
     }
   },
   legend: {
     layout: 'vertical',
     align: 'right',
     verticalAlign: 'middle'
   },

   plotOptions: {
     series: {
       label: {
         connectorAllowed: false
       },
       categories: data[0]
     }
   },

   series: [{
     name: 'Beats per minute',
     data: data[1]
   }],

   responsive: {
     rules: [{
       condition: {
         maxWidth: 500
       },
       chartOptions: {
         legend: {
           layout: 'horizontal',
           align: 'center',
           verticalAlign: 'bottom'
         }
       }
     }]
   }

  });
}

function heartChart(data){
  document.getElementById("chart_container").innerHTML = ""
  document.getElementById("select_container").innerHTML = `
  <div class="col-6 offset-3 p-0 jumbotron d-flex justify-content-center">
    <img src="static/heart.png" class="rounded float-left mr-3" style="width:20%; height:20%;">
    <div class="ml-2">
      <p id="heartTime" class="col-12 mb-1 ml-2">Last heart rate reading:</p>
      <p id="heartBeatEntry" class="col-12 font-weight-bold large d-flex justify-content-center" style="font-size: 50px">0</p>
    </div>
  </div>
  <div class="d-flex justify-content-center">
    <button class="btn btn-success btn-lg mb-2" onclick="refreshChart()">Refersh Chart</button>
  </div>
  `

  drawHighChart(data);

}
