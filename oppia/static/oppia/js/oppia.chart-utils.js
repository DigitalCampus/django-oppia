
function downloadFile(content, fileName, mimeType) {
    //usage; downloadFile(csvContent, 'dowload.csv', 'text/csv');
  var a = document.createElement('a');
  mimeType = mimeType || 'application/octet-stream';

  if (navigator.msSaveBlob) { // IE10
    return navigator.msSaveBlob(new Blob([content], { type: mimeType }),     fileName);
  } else if ('download' in a) { //html5 A[download]
    a.href = 'data:' + mimeType + ',' + encodeURIComponent(content);
    a.setAttribute('download', fileName);
    document.body.appendChild(a);
    setTimeout(function() {
      a.click();
      document.body.removeChild(a);
    }, 66);
    return true;
  } else { //do iframe dataURL download (old ch+FF):
    var f = document.createElement('iframe');
    document.body.appendChild(f);
    f.src = 'data:' + mimeType + ',' + encodeURIComponent(content);

    setTimeout(function() {
      document.body.removeChild(f);
    }, 333);
    return true;
  }
}

function getDefaultAreaChartConfig(title){
    var defaultConfig = {
        width: '100%',
        height: 400,
        vAxis: {minValue:0},
        pointSize:3,
        chartArea: {left:80,width:"90%",height:"75%"},
        backgroundColor: 'transparent',
        legend: 'none',
        series: [{areaOpacity:0.2}]
    };
    defaultConfig.title = title;
    return defaultConfig;
}

function getCSVFromDatatable(datatable){
    var numColumns = datatable.getNumberOfColumns();
    var numRows = datatable.getNumberOfRows();
    var csvText = "";

    for (var j=0; j<numColumns; j++){
        csvText+=datatable.getColumnLabel(j);
        if (j<(numColumns-1)) csvText+=',';
    }
    csvText+='\n';
    for (var i=0; i<numRows; i++){
        for (var j=0; j<numColumns; j++){
            csvText+=datatable.getValue(i,j);
            if (j<(numColumns-1)) csvText+=',';
        }
        csvText+='\n';
    }

    return csvText;
}
