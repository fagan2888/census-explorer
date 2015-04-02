var filtered_data;
var data; 

var filterData = function(source, func) {
    if (!data && source) {
        d3.json(source, function(error, json) {
            data = json;
            filtered_data = data.filter(func);
            drawViz(filtered_data);
        });
    } else {
        filtered_data = data.filter(func);
        drawViz(filtered_data);
    }
}
