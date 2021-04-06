var default_values = [
  {food: "Chilli Crab", value: 0.0833},
  {food: "Curry Puff", value: 0.0833},
  {food: "Dim Sum", value: 0.0833},
  {food: "Ice Kacang", value: 0.0833},
  {food: "Kaya Toast", value: 0.0833},
  {food: "Nasi Ayam", value: 0.0833},
  {food: "Popiah", value: 0.0833},
  {food: "Roti Prata", value: 0.0833},
  {food: "Sambal Stingray", value: 0.0833},
  {food: "Satay", value: 0.0833},
  {food: "Tau Huay", value: 0.0833},
  {food: "Wanton Noodle", value: 0.0833},
];

var width = 520,
  height = 420,
  margin = 30;

var radius = Math.min(width, height) / 2 - margin;

var color = d3.scaleOrdinal().range([
  "#001f3f",
  "#0074D9",
  "#7FDBFF",
  "#3D9970",
  "#2ECC40",
  "#01FF70",
  "#FFDC00",
  "#FF851B",
  "#FF4136",
  "#85144b",
  "#F012BE",
  "#B10DC9"]);


// Piechart details
var pie = d3.pie()
  .value(function (d) {
    return d.value;
  })(default_values);

var arc = d3.arc()
  .outerRadius(radius - 10)
  .innerRadius(0);

var svg = d3.select("div#food_chart")
  .append("svg")
  //.attr("width", width)
  //.attr("height", height)
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", `0 0 ${width} ${height}`)
  .classed("svg-content", true)
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var div = d3.select("body").append("div")
  .attr("class", "tooltip-pie")
  .style("opacity", 0);


// Mouseover opacity changes
var g = svg.selectAll("arc")
  .data(pie)
  .enter().append("g")
  .attr("class", "arc")
  .on('mouseover', function (d, i) {
    d3.select(this).transition()
      .duration('50')
      .attr('opacity', '.95');
  })
  .on('mouseout', function (d, i) {
    d3.select(this).transition()
      .duration('50')
      .attr('opacity', '1');
  })
  .attr('transform', 'translate(0, -40)');


// Mouseover popups
g.append("path")
  .attr("d", arc)
  .style("fill", function (d) {
    return color(d.data.food);
  })
  .on('mouseover', function (d, i) {
    d3.select(this).transition()
      .duration('50')
      .attr('opacity', '.5');
    div.transition()
      .duration(50)
      .style("opacity", 1);
    div.html((d.value * 100).toFixed(1) + " % " + d.data.food)
      .style("left", (d3.event.pageX + 10) + "px")
      .style("top", (d3.event.pageY - 15) + "px");
  })
  .on('mouseout', function (d, i) {
    d3.select(this).transition()
      .duration('50')
      .attr('opacity', '1');
    div.transition()
      .duration('50')
      .style("opacity", 0);
  });


// Legend
var legendRectSize = 9.5;
var legendSpacing = 7;

var legend = svg.selectAll('.legend')
  .data(color.domain())
  .enter()
  .append('g')
  .attr('class', 'circle-legend')
  .attr('transform', function (d, i) {
    x = 20 + width / 4 * (Math.floor(i / 3) - 2)
    y = (i % 3) * 20 + 155
    return 'translate(' + x + ',' + y + ')';
  });

legend.append('circle')
  .style('fill', color)
  .style('stroke', color)
  .attr('cx', 0)
  .attr('cy', 0)
  .attr('r', '.5rem');

legend.append('text')
  .attr('x', legendRectSize + legendSpacing)
  .attr('y', legendRectSize - legendSpacing)
  .style("font-size", "13px")
  .text(function (d) {
    return d;
  });


// Update function
function updateChart(data) {
  var pie = d3.pie()
    .value(function (d) {
      return d.value;
    })(data);

  path = d3.select("#food_chart")
    .selectAll("path")
    .data(pie); // Compute the new angles
  path.transition().duration(500).attr("d", arc); // redrawing the path with a smooth transition
}
