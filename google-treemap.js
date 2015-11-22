google.load("visualization", "1.1", {packages:["treemap"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'ID');
    data.addColumn('string', 'Parent');
    data.addColumn('number', 'Number Of Lines');
    data.addRows(
            

    );

    var tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

    var options = {
        highlightOnMouseOver: true,
        maxDepth: 1,
        maxPostDepth: 2,
        minHighlightColor: '#8c6bb1',
        midHighlightColor: '#9ebcda',
        maxHighlightColor: '#edf8fb',
        minColor: '#009688',
        midColor: '#f7f7f7',
        maxColor: '#ee8100',
        headerHeight: 15,
        showScale: true,
        height: 500,
        useWeightedAverageForAggregation: true
    };

    tree.draw(data, options);
}
