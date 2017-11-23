url_split = window.location.href.split("/");
current_server_name = url_split[url_split.length - 1];

$(document).ready(function(){
    render_server_graph(24);
});

$('#timerange_select').change(function(){
    render_server_graph($('#timerange_select').val());
})

function render_server_graph(time_range){
    $.ajax({
        url: '/api/get_server_data/' + current_server_name + '/' + time_range,
        success: function (result) {
            var pingChart = echarts.init(document.getElementById('pingchart'),'shine');
    
            var server_series = [];
            for (var i in result) {
                data = [];
                for (var j = 0; j < result[i].data.length; j++) {
                    data.push([result[i].date[j], result[i].data[j]]);
                }
                server_series.push({
                    name: i,
                    type: 'line',
                    smooth: true,
                    data: data
                })
            }
    
            // 指定图表的配置项和数据
            var server_option = {
                title: {
                    text: current_server_name
                },
                tooltip: {},
                legend: {
                    //data:['销量']
                },
                xAxis: {
                    type: 'time'
                },
                yAxis: {},
                series: server_series
            };
    
            // 使用刚指定的配置项和数据显示图表。
            pingChart.setOption(server_option);
        }
    });
}