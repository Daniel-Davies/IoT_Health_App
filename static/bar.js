function newChart(inVal){
  $.getJSON('/retrieve_steps/'+inVal,
    function(data) {
      drawBar(data);
    });
}

function drawBarBase(){
  clearInterval(myTimedVar);
  document.getElementById("selector1").className = "btn btn-lg btn-primary"
  document.getElementById("selector2").className = "btn btn-lg btn-secondary"
  document.getElementById("select_container").innerHTML = `<div class="form-group col-4 offset-4">
    <label for="exampleFormControlSelect1">Duration</label>
    <select class="form-control" id="exampleFormControlSelect1" onChange="newChart(this.options[this.selectedIndex].value)">
      <option value="0">Today</option>
      <option value="1">Week</option>
      <option value="2">Month</option>
    </select>
  </div>`
  newChart('0');
}

function drawBar(data){
  document.getElementById("chart_container").innerHTML = ""

  Highcharts.chart('chart_container', {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Step analysis'
    },
    xAxis: {
      categories:  data[0]
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Number of Steps'
      },
      stackLabels: {
        enabled: true,
        style: {
          fontWeight: 'bold',
          color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
        }
      }
    },
    legend: {
      align: 'right',
      x: -30,
      verticalAlign: 'top',
      y: 25,
      floating: true,
      backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
      borderColor: '#CCC',
      borderWidth: 1,
      shadow: false
    },
    tooltip: {
      headerFormat: '<b>{point.x}</b><br/>',
      pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
    },
    plotOptions: {
      column: {
        stacking: 'normal',
        dataLabels: {
          enabled: true,
          color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
        }
      }
    },
    series: [{
      name: 'Number of Steps',
      data: data[1]
    }]
  });

}
