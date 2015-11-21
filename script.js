var tree = {
    name: "tree",
    children: [
	{ name: "Word-wrapping comes for free in HTML", size: 16000 },
	{ name: "animate makes things fun", size: 8000 },
	{ name: "data data everywhere...", size: 5220 },
	{ name: "display something beautiful", size: 3623 },
	{ name: "flex your muscles", size: 984 },
	{ name: "physics is religion", size: 6410 },
	{ name: "query and you get the answer", size: 2124 }
    ]
};

function render() {
    var margin = {top: 40, right: 10, bottom: 10, left: 10},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var color = d3.scale.category10()
    var treemap = d3.layout.treemap()
        .size([width, height])
        .sticky(true)
        .value(function value(d){
	    return d.mentions;
	});

    treemap.children(function children(d, depth){
	if (depth == 0)
	    return d.topics;
    });

    var div = d3.select("#treeDiv").append("div");

    d3.json("input.json", function(error, root) {
        // Data join
        var node = div.datum(root).selectAll(".node")
            .data(treemap.nodes);

        // Create new elements as needed
        node.enter().append("div")
            .attr("class", "node")
            .call(position)
            .style("background-color", function(d) { return color(d.name);})
            .text(function(d) { return d.name; });

    });

    function position() {
        this.style("left", function(d) { return d.x + "px"; })
            .style("top", function(d) { return d.y + "px"; })
            .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
            .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
    }
};

render();

