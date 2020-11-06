// set the dimensions and margins of the graph
var donuts_width = 250,
    donuts_height = 250,
    donuts_margin = 60;

// The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
var radius = Math.min(donuts_width, donuts_height) / 2 - donuts_margin

// append the svg object to the div called 'my_dataviz'
var donuts_svg = d3.select("#donuts_world")
  .append("svg")
    .attr("width", donuts_width)
    .attr("height", donuts_height)
  .append("g")
    .attr("transform", "translate(" + donuts_width / 2 + "," + donuts_height / 2 + ")");

// Create dummy data
var data = {a: total_recovered, b:total_deaths, c:total_confirmed}

// set the color scale
var color = d3.scaleOrdinal()
  .domain(data)
  .range(["#70a800", "#ba55d3", "#FF8C00"])

// Compute the position of each group on the pie:
var pie = d3.pie()
  .value(function(d) {return d.value; })
var data_ready = pie(d3.entries(data))

// Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
donuts_svg
  .selectAll('whatever')
  .data(data_ready)
  .enter()
  .append('path')
  .attr('d', d3.arc()
    .innerRadius(100)         // This is the size of the donut hole
    .outerRadius(radius)
  )
  .attr('fill', function(d){ return(color(d.data.key)) })
  .attr("stroke", "black")
  .style("stroke-width", "2px")
  .style("opacity", 0.7)

console.log(total_confirmed);