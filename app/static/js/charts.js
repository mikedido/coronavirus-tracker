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
 * New function to draw chart
 * 
 * @param {*} url 
 * @param {*} divName 
 * @param {*} chartName 
 */
function createChart(url, divName, chartName, chartColor) {
    // trigger loader
    var target = document.getElementById(divName);
    var spinner = new Spinner(opts).spin(target);

    const margin = {top: 20, right: 30, bottom: 30, left: 60},
    width = document.getElementById(divName).offsetWidth * 0.95 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

    const parseTime = d3.timeParse("%m/%d/%Y");
    const dateFormat = d3.timeFormat("%m/%d/%Y");

    const x = d3.scaleTime()
        .range([0, width]);

    const y = d3.scaleLinear()
        .range([height, 0]);


    const line = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.close); });

    const svg = d3.select("#"+chartName).append("svg")
        .attr("id", "svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // On demande à D3JS de charger notre fichier
    // On déclare également une map qui servira un peu plus bas pour l'affichage du tooltip
    var map = {};
    d3.json(url).then(function(data) {
        last_updated = data['last_updated'];
        data = data['data'];
        spinner.stop();
        //construct my data object
        dataArray = [];
        var i = 0;

        for(key in data) {
            date = parseTime(key);
            volume = +data[key];
            close = +data[key];
            map[date] = {date, volume}; 
            dataArray[i++] = {date, close, volume};
        }

        // Contrairement au tutoriel Bar Chart, plutôt que de prendre un range entre 0 et le max on demande 
        // directement à D3JS de nous donner le min et le max avec la fonction 'd3.extent', pour la date comme 
        // pour le cours de fermeture (close).
        x.domain(d3.extent(dataArray, function(d) { return d.date; }));
        y.domain(d3.extent(dataArray, function(d) { return d.volume; }));

        // Ajout de l'axe X
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        
        // Ajout de l'axe Y et du texte associé pour la légende
        svg.append("g")
            .call(d3.axisLeft(y))
            .append("text")
                .attr("fill", "#000")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", "0.71em")
                .style("text-anchor", "end");
        
        // Ajout de la grille horizontale (pour l'axe Y donc). Pour chaque tiret (ticks), on ajoute une ligne qui va 
        // de la gauche à la droite du graphique et qui se situe à la bonne hauteur.
        svg.selectAll("y axis").data(y.ticks(10)).enter()
            .append("line")
            .attr("class", "horizontalGrid")
            .attr("x1", 0)
            .attr("x2", width)
            .attr("y1", function(d){ return y(d);})
            .attr("y2", function(d){ return y(d);});
        
        // Ajout d'un path calculé par la fonction line à partir des données de notre fichier.
        svg.append("path")
            .datum(dataArray)
            .attr("class", "line "+chartColor)
            .attr("d", line);

         //Title construction
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", -10)
            .attr("text-anchor", "middle")
            .style("fill", "white")
            .style("font-weight", "300")
            .style("font-size", "14px")
            .text("Last updated : "+last_updated);
    });

    var div = d3.select("body").append("div")   
        .attr("class", "tooltip")
        .attr("x", width - 300)
        .attr("y", 0)
        .style("opacity", 0);

    var verticalLine = svg.append("line")
        .attr("class", "verticalLine")
        .attr("x1",0)
        .attr("y1",0)
        .attr("x2",0)
        .attr("y2",height)
        .style("opacity", 0);

    d3.select("#"+chartName).on("mousemove", function() {
        // Récupération de la position X & Y de la souris.
        var mouse_x = d3.mouse(this)[0];
        var mouse_y = d3.mouse(this)[1];
        
        // Si la position de la souris est en dehors de la zone du graphique, on arrête le traitement
        if (mouse_x < margin.left || mouse_x > (width + margin.left) || mouse_y < margin.top || mouse_y > (400 - margin.bottom)) {
            return ;
        }
        
        // Grâce à la fonction 'invert' nous récupérons la date correspondant à notre position
        // A noter, il faut soustraire la marge à gauche pour que la valeur soit correct.
        var selectedDate = x.invert(mouse_x - margin.left);
        
        // Positionnement de la barre verticale toujours en tenant compte de la marge
        verticalLine.attr("x1", mouse_x - margin.left);
        verticalLine.attr("x2", mouse_x - margin.left);
        verticalLine.style("opacity", 1);
        
        // Le revert est précis à la milliseconde, ce qui n'est pas le cas de nos données
        selectedDate.setHours(0,0,0,0);
        var entry = map[selectedDate];
        if (typeof entry === "undefined") {
            return ;
        }
        // Si une entrée existe pour la date sélectionnée nous pouvons afficher les données.
        
        // Le comportement est équivalent aux précédents exemples pour le tooltip.
        div.style("opacity", .9);
        div.style("left", (d3.event.pageX + 30) + "px")     
            .style("top", (d3.event.pageY - 60) + "px")
            .html("<b>Date : </b>" + dateFormat(entry.date) + "<br>"
            + "<b>Volume : </b>" + entry.volume + "<br>");
        }).on("mouseout", function() {

            var mouse_x = d3.mouse(this)[0];
            var mouse_y = d3.mouse(this)[1];

            // Si la position de la souris est en dehors de la zone du graphique, on masque la ligne et le tooltip
            if (mouse_x < margin.left || mouse_x > (width + margin.left) || mouse_y < margin.top || mouse_y > (300 - margin.bottom)) {
                div.style("opacity", 0);
                verticalLine.style("opacity", 0);
        }
    });

    return d3;
}


createChart('/api/confirmed/'+countryCode+'/'+provinceName, 'country_confirmed', 'chart_confirmed', "redLine");
createChart('/api/deaths/'+countryCode+'/'+provinceName, 'country_deaths', 'chart_deaths', 'redLine');
createChart('/api/recovered/'+countryCode+'/'+provinceName, 'country_recovered', 'chart_recovered', 'greenLine');