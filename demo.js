<script>    
    var plot_element = document.getElementById('a240582c-1f2d-4ccb-b290-15029a54dadd');
    console.log('callback js has been added to page. did we get plot_element?');
    console.log(plot_element);
    
    plot_element.on('plotly_click', function(data){
        console.log('Im inside the plotly_click!!');
        var point = data.points[0];
        if (point) {
            console.log(point);
            window.open(point.customdata);
        }
    })
</script>