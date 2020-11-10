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
    position: 'relative'
};  

/**
 * Get the previous date of a known date
 * 
 * @param {string} date 
 */
function getPreviousDate(d) {
    let date = new Date(d);

    date.setDate(date.getDate() - 1);
    previousDate = (((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1)) + '/' + ((date.getDate() < 10 ? '0' : '') + date.getDate()) + '/'+ (date.getFullYear());

    return previousDate;
}

/**
 * Create histogramme
 * 
 * @param {string} url 
 * @param {string} divName
 */
function createHistogramme(url, divId, divName, histColorClass) {
    // trigger loader
    var target = document.getElementById(divId);
    var spinner = new Spinner(opts).spin(target);

    const margin = {top: 20, right: 20, bottom: 90, left: 120},
    width = document.getElementById(divId).offsetWidth * 0.95 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    const x = d3.scaleBand()
    .range([0, width])
    .padding(0.1);

    const y = d3.scaleLinear()
    .range([height, 0]);

    const svg = d3.select("#"+divName).append("svg")
    .attr("id", "svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const div = d3.select("body").append("div")
    .attr("class", "tooltip")         
    .style("opacity", 0);
    
    d3.json(url).then(function(data) {
        // Conversion des caractères en nombres
        last_updated = data['last_updated'];
        data = data['data'];
        spinner.stop();

        // Construct my data object
        dataArray = [];
        var i = 0;

        for(key in data) {
            //first iteration
            if (i == 0) {
                date = key
                population = data[key]; 
            } else {
                date = key
                population = data[key] - data[getPreviousDate(date)];
            }
            
            dataArray[i++] = {date, population}
        }
    
        // Mise en relation du scale avec les données de notre fichier
        // Pour l'axe X, c'est la liste des pays
        // Pour l'axe Y, c'est le max des populations
        x.domain(dataArray.map(function(d) { return d.date; }));
        y.domain([0, d3.max(dataArray, function(d) { return d.population; })]);
        
        // Ajout de l'axe X au SVG
        // Déplacement de l'axe horizontal et du futur texte (via la fonction translate) au bas du SVG
        // Selection des noeuds text, positionnement puis rotation
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSize(0))
            .selectAll("text")	
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)");
        
        // Ajout de l'axe Y au SVG avec 6 éléments de légende en utilisant la fonction ticks (sinon D3JS en place autant qu'il peut).
        svg.append("g")
            .call(d3.axisLeft(y).ticks(6));
    
        // Ajout des bars en utilisant les données de notre fichier data.tsv
        // La largeur de la barre est déterminée par la fonction x
        // La hauteur par la fonction y en tenant compte de la population
        // La gestion des events de la souris pour le popup
        svg.selectAll(".bar")
            .data(dataArray)
        .enter().append("rect")
            .attr("class", "bar")
            .attr("class", histColorClass)
            .attr("x", function(d) { return x(d.date); })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d.population); })
            .attr("height", function(d) { return height - y(d.population); })					
            .on("mouseover", function(d) {
                div.transition()        
                    .duration(200)      
                    .style("opacity", .9);
                div.html("Population : " + d.population + "<br/>" + "Date : " + d.date)
                    .style("left", (d3.event.pageX + 10) + "px")     
                    .style("top", (d3.event.pageY - 50) + "px");
            })
            .on("mouseout", function(d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    });

    return d3;
}


createHistogramme('/v0/confirmed/'+countryCode+'/'+provinceName, 'country_histo_confirmed', 'histo_confirmed', 'redBar');
createHistogramme('/v0/deaths/'+countryCode+'/'+provinceName, 'country_histo_deaths', 'histo_deaths', 'redBar');
createHistogramme('/v0/recovered/'+countryCode+'/'+provinceName, 'country_histo_recovered', 'histo_recovered', 'greenBar');