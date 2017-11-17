url_split = window.location.href.split("/");
current_server_name = url_split[url_split.length - 1];
$.ajax({
    url: '/api/get_server_data/' + current_server_name + '/72',
    success: function (result) {
        var pingChart = echarts.init(document.getElementById('pingchart'));

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