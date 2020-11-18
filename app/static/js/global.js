//initialisation
const width = document.getElementById("map-container").offsetWidth * 1.3,
height = document.getElementById("map-container").offsetHeight * 1.3,
legendCellSize = 30,
colors = ['#ff9999', '#ff4d4d', '#ff0000', '#e60000', '#b30000', '#660000'];

const svg = d3.select('#map').append("svg")
    .attr("id", "svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "svg");

//add legend
function addLegend(min, max) {
    var legend = svg.append('g')
        .attr('transform', 'translate(80, '+height/2+')');

    legend.selectAll()
        .data(d3.range(colors.length))
        .enter().append('svg:rect')
            .attr('height', legendCellSize + 'px')
            .attr('width', legendCellSize + 'px')
            .attr('x', 5)
            .attr('y', function(d) { return d * legendCellSize; })
            .style("fill", function(d) { return colors[d]; })
            .on("mouseover", function(d) {
                legend.select("#cursor")
                    .attr('transform', 'translate(' + (legendCellSize + 5) + ', ' + (d * legendCellSize) + ')')
                    .style("display", null);
                d3.selectAll("path[scorecolor='" + colors[d] + "']")
                    .style('fill', "#9966cc");
            })
            .on("mouseout", function(d) {
                legend.select("#cursor")
                    .style("display", "none");
                d3.selectAll("path[scorecolor='" + colors[d] + "']")
                    .style('fill', colors[d]);
            });
            
    var legendScale = d3.scaleLinear().domain([min, max])
        .range([0, colors.length * legendCellSize]);
    
    legendAxis = legend.append("g")
        .attr("class", "axis")
        .attr('stroke', 'black')
        .call(d3.axisLeft(legendScale));
    
    return legend;
}
     
//add toolTip
function addTooltip() {
    var tooltip = svg.append("g") // Group for the whole tooltip
        .attr("id", "tooltip")
        .style("display", "none");
    
    tooltip.append("polyline") // The rectangle containing the text, it is 210px width and 60 height
        .attr("points","0,0 210,0 210,170 0,170 0,0")
        .style("fill", "#bebebe")
        .style("stroke","black")
        .style("opacity","0.9")
        .style("stroke-width","0")
        .style("padding", "1em");
    
    tooltip.append("line") // A line inserted between country name and score
        .attr("x1", 40)
        .attr("y1", 60)
        .attr("x2", 150)
        .attr("y2", 60)
        .style("stroke","white")
        .style("stroke-width","0.5")
        .attr("transform", "translate(0, 5)");

    var text = tooltip.append("text") // Text that will contain all tspan (used for multilines)
        .style("font-size", "13px")
        .style("fill", "black")
        .attr("transform", "translate(0, 20)");

    text.append("tspan") // Country name udpated by its id
        .attr("x", 105) // ie, tooltip width / 2
        .attr("y", 30)
        .attr("id", "tooltip-country")
        .attr("text-anchor", "middle")
        .style("font-weight", "600")
        .style("font-size", "16px");
    
    text.append("tspan") // Fixed text
        .attr("x", 20) // ie, tooltip width / 2
        .attr("y", 70)
        .style("fill", "black")
        .text("Confirmed : ");
    
    text.append("tspan") // Score udpated by its id
        .attr("id", "tooltip-confirmed")
        .style("fill","red")
        .style("font-weight", "bold");

    text.append("tspan") // Fixed text
        .attr("x", 20) // ie, tooltip width / 2
        .attr("y", 90)
        .style("fill", "black")
        .text("Deaths : ");
    
    text.append("tspan") // Deaths udpated by its id
        .attr("id", "tooltip-deaths")
        .style("fill","red")
        .style("font-weight", "bold");

    text.append("tspan") // Fixed text
        .attr("x", 20) // ie, tooltip width / 2
        .attr("y", 110)
        .style("fill", "black")
        .text("Recovered : ");
    
    text.append("tspan") // Recovered udpated by its id
        .attr("id", "tooltip-recovered")
        .style("fill","green")
        .style("font-weight", "bold");

    text.append("tspan") // Fixed text
        .attr("x", 20) // ie, tooltip width / 2
        .attr("y", 130)
        .style("fill", "black")
        .text("Active : ");
    
    text.append("tspan") // Recovered udpated by its id
        .attr("id", "tooltip-active")
        .style("fill","orange")
        .style("font-weight", "bold");
    
    return tooltip;
}

//Title construction
function addTitle(date) {
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", height)
        .attr("text-anchor", "middle")
        .style("fill", "white")
        .style("font-weight", "300")
        .style("font-size", "14px")
        .text("Last updated : "+date);
}

//map
function getColorIndex(color) {
    for (var i = 0; i < colors.length; i++) {
        if (colors[i] === color) {
            return i;
        }
    }
    return -1;
}

// config references
var chartConfig = {
    target : 'loader'
};

// loader settings
var opts = {
  lines: 9, // The number of lines to draw
  length: 9, // The length of each line
  width: 10, // The line thickness
  radius: 14, // The radius of the inner circle
  color: '#EE3124', // #rgb or #rrggbb or array of colors
  speed: 1.5, // Rounds per second
  trail: 40, // Afterglow percentage
  className: 'spinner', // The CSS class to assign to the spinner
};

var target = document.getElementById(chartConfig.target);

/**
 * Create global map
 * 
 * @param string url 
 */
function createMap(url) {

    // trigger loader
    var spinner = new Spinner(opts).spin(target);

    const projection = d3.geoNaturalEarth1()
    .scale(1)
    .translate([0, 0]);
    
const path = d3.geoPath()
    .pointRadius(2)
    .projection(projection);
    
const cGroup = svg.append("g").attr('transform', 'translate(0, 0)');

var promises = [];
promises.push(d3.json("static/files/world-countries-no-antartica.json"));
promises.push(d3.json(url));

Promise.all(promises).then(function(values) {
    
    spinner.stop();
    
    const geojson = values[0];
    const scores = values[1];

    var b  = path.bounds(geojson),
        s = .90 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
        t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

        projection
            .scale(s)
            .translate(t);
        
        cGroup.selectAll("path")
            .data(geojson.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("id", function(d) {return "code" + d.id; })
            .attr("class", "country");
        

        const min = d3.min(scores['locations'], function(e) { return +e.total.confirmed; }),
        max = d3.max(scores['locations'], function(e) { return +e.total.confirmed; });

        var quantile = d3.scaleQuantile().domain([min, max])
            .range(colors);
        
        var legend = addLegend(min, max);
        var tooltip = addTooltip();

        addTitle(scores['last_updated']);
        
        scores['locations'].forEach(function(element, i) {
            var countryPath = d3.select("#code" + element.country_code);
            
            countryPath
                .attr("scorecolor", quantile(+element.total.confirmed))
                .style("fill", function(d) { return quantile(+element.total.confirmed); })
                .on("mouseover", function(d) {
                    countryPath.style("fill", "lightsteelblue");
                    tooltip.style("display", null);
                    tooltip.select('#tooltip-country')
                        .text(element.country);
                    tooltip.select('#tooltip-confirmed')
                        .text(element.total.confirmed);
                    tooltip.select('#tooltip-deaths')
                        .text(element.total.deaths);
                    tooltip.select('#tooltip-recovered')
                        .text(element.total.recovered);
                    tooltip.select('#tooltip-active')
                        .text(element.total.active);
                    legend.select("#cursor")
                        .attr('transform', 'translate(' + (legendCellSize + 5) + ', ' + (getColorIndex(quantile(+element.latest)) * legendCellSize) + ')')
                        .style("display", null);
                })
                .on("mouseout", function(d) {
                    countryPath.style("fill", function(d) { return quantile(+element.total.confirmed); });
                    tooltip.style("display", "none");
                    legend.select("#cursor").style("display", "none");
                })
                .on("mousemove", function(d) {
                    //var mouse = d3.mouse(this);
                    tooltip.attr('transform', 'translate("100", "100")');
                    //tooltip.attr("transform", "translate(" + mouse[0] + "," + (mouse[1] - 75) + ")");
                })
                .on("click", function(d) {
                    var url = "/"+element.country_code;
                    window.location = url;
                  });
        });
    });

    return d3;
}

//creation de la map
createMap('/v1/all/grouped');