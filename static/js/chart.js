google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var container = document.getElementById('timeline');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();
  var d = new Date();
  dataTable.addColumn({ type: 'string', id: 'user' });
  dataTable.addColumn({ type: 'string', id: 'shift'});
  dataTable.addColumn({ type: 'date', id: 'enter_time' });
  dataTable.addColumn({ type: 'date', id: 'exit_time' });
  dataTable.addRow([ date,' ㅤ', new Date(0,0,0,0,0), new Date(0,0,0,0,0) ]);
  dataTable.addRow([ date,'ㅤ ', new Date(0,0,0,24,0), new Date(0,0,0,24,0) ]);
  dataTable.addRow([ date,'Current Time', new Date(0,0,0,d.getHours(),d.getMinutes()), new Date(0,0,0,d.getHours(),d.getMinutes()) ]);
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
      [ usr,'', new Date(0,0,0,enter_hr,enter_min), new Date(0,0,0,exit_hr,exit_min) ]);
   }}
   chart.draw(dataTable);
   add_shifts('timeline');
  
  google.visualization.events.addListener(chart, 'onmouseover', function(obj){
    if(obj.row == 0){
      $('.google-visualization-tooltip').css('display', 'none');
    }
    add_shifts('timeline');
  })
  
  google.visualization.events.addListener(chart, 'onmouseout', function(obj){
    add_shifts('timeline');
  })
 }
 function add_shifts(div){

//get the height of the timeline div
  var height;
  $('#' + div + ' rect').each(function(index){
    var x = parseFloat($(this).attr('x'));
    var y = parseFloat($(this).attr('y'));
    
    if(x == 0 && y == 0) {height = parseFloat($(this).attr('height'))}
  })

  $('#' + div + ' text:contains("Current Time")').prev().first().attr('height', height + 'px').attr('width', '1px').attr('y', '0');
  $('#' + div + ' text:contains("ㅤ ")').prev().first().attr('height', height + 'px').attr('width', '1px').attr('y', '0');
  $('#' + div + ' text:contains(" ㅤ")').prev().first().attr('height', height + 'px').attr('width', '1px').attr('y', '0');
}