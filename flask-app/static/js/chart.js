google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var container = document.getElementById('timeline');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();

  dataTable.addColumn({ type: 'string', id: 'user' });
  dataTable.addColumn({ type: 'date', id: 'enter_time' });
  dataTable.addColumn({ type: 'date', id: 'exit_time' });
  dataTable.addRow([ "header", new Date(0,0,0,0,0), new Date(0,0,0,24,0) ]);
  var usr = "";
  var enter_hr;
  var enter_min;
  var exit_min;
  var exit_hr;
  var file_data=JSON.parse(file_data1);
  for(i=0;i<4 ;i++){
    usr = "user_"+i;
    for(j=0;j<file_data[usr].length;j++){
     enter_hr = parseInt(file_data[usr][j].enter_time.hr);
     enter_min = parseInt(file_data[usr][j].enter_time.min);
     exit_hr = parseInt(file_data[usr][j].exit_time.hr);
     exit_min = parseInt(file_data[usr][j].exit_time.min);
     dataTable.addRow(
      [ usr, new Date(0,0,0,enter_hr,enter_min), new Date(0,0,0,exit_hr,exit_min) ]);
   }}
   chart.draw(dataTable);
 }