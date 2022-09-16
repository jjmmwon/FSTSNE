export { Scatterplot };
class Scatterplot {
  constructor(svg, data, width = 400, height = 400) {
    this.svg = svg;
    this.data = data;
    this.width = width;
    this.height = height;
    this.margin = {
      top: 50,
      right: 50,
      bottom: 50,
      left: 40,
    };

    this.selected = new Set();

    this.handlers = {};
    this.isClassed = false;
  }

  // initialize by making title, brush and groups of scatterplot
  initialize() {
    let svgtitle = this.svg.slice(12);

    this.svg = d3.select(this.svg);
    this.container = this.svg.append("g");
    this.title = this.svg.append("text");
    this.xAxis = this.svg.append("g");
    this.yAxis = this.svg.append("g");

    this.xScale = d3.scaleLinear();
    this.yScale = d3.scaleLinear();

    this.svg
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom);

    this.container.attr(
      "transform",
      `translate(${this.margin.left}, ${this.margin.top})`
    );

    this.title
      .text(svgtitle)
      .attr(
        "transform",
        `translate(${
          (this.width + this.margin.left + this.margin.right) / 2
        },${35})`
      )
      .attr("text-anchor", "middle")
      .attr("font-size", "1.5rem")
      .attr("font-weight", "bold");

    this.brush = d3
      .brush()
      .extent([
        [0, 0],
        [this.width, this.height],
      ])
      .on("end", (event) => {
        this.brushCircles(event);
      });
  }

  //update when select event happened
  selectionUpdate(data) {
    this.data = data ?? this.data; // First update => this.data, else => data

    this.isClassed = "2" in this.data ? true : false;

    this.xScale.domain([-2, 2]).range([0, this.width]);
    this.yScale.domain([-2, 2]).range([this.height, 0]);

    this.circles = this.container
      .selectAll("path")
      .data(this.data)
      .join("path");

    if (this.isClassed) {
      let symbolScale = d3
        .scaleOrdinal()
        .domain([...new Set(this.data.map((d) => d["2"]))])
        .range(d3.symbolsFill);

      // let domain = [...new Set(this.data.map((d) => d["2"]))];
      // let symbolsRange = [
      //   d3.symbolCircle,
      //   d3.symbolCross,
      //   d3.symbolDiamond,
      //   d3.symbolSquare,
      //   d3.symbolStar,
      //   d3.symbolTriangle,
      //   d3.symbolWye,
      // ];

      //symbolsRange[domain.indexOf(d)]
      this.circles
        .transition()
        .attr("transform", (d) => {
          return (
            "translate(" + this.xScale(d["0"]) + "," + this.yScale(d["1"]) + ")"
          );
        })
        .attr("d", d3.symbol().type((d)=>{return symbolScale(d["2"])}).size(40))
        .attr("fill", "Steelblue")
        .attr("opacity", 0.9);
    } else {
      this.circles
        .transition()
        .attr("transform", (d) => {
          return (
            "translate(" + this.xScale(d["0"]) + "," + this.yScale(d["1"]) + ")"
          );
        })
        .attr("d", d3.symbol().type(d3.symbolCircle).size(40))
        .attr("fill", "Steelblue")
        .attr("opacity", 0.9);

      // this.circles
      // .transition()
      // .attr("transform", (d) => this.xScale(d["0"]))
      // .attr("cy", (d) => this.yScale(d["1"]))
      // .attr("fill", "rgb(20,20,20)")
      // .attr("opacity", 0.5)
      // .attr("r", 2);
    }

    this.xAxis
      .attr(
        "transform",
        `translate(${this.margin.left}, ${this.margin.top + this.height})`
      )
      .transition()
      .call(d3.axisBottom(this.xScale));

    this.yAxis
      .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`)
      .transition()
      .call(d3.axisLeft(this.yScale));

    this.container.call(this.brush);
  }

  brushUpdate(selectedIndex) {
    selectedIndex.forEach((val) => {
      this.selected.add(val);
    });

    // this.circles
    //   .transition()
    //   .attr("r", (d) => (selectedIndex.has(d[""]) ? 3 : 2));

    this.circles.classed("brushed", (d) => this.selected.has(d[""]));
  }

  brushReset() {
    this.circles.classed("brushed", false);
  }

  isBrushed(d, selection) {
    if (!selection) return;
    let [[x0, y0], [x1, y1]] = selection;
    let x = this.xScale(d["0"]);
    let y = this.yScale(d["1"]);

    return x0 <= x && x <= x1 && y0 <= y && y <= y1;
  }

  brushCircles(event) {
    let selection = event.selection;

    this.circles.classed("brushed", (d) => this.isBrushed(d, selection));

    if (this.handlers.brush)
      this.handlers.brush(
        this.data.filter((d) => this.isBrushed(d, selection))
      );
  }

  on(eventType, handler) {
    this.handlers[eventType] = handler;
  }

  frequentSubgraphUpdate(fsList) {
    let colorScale = d3.scaleOrdinal().domain([0,1,2,3,4,5,6,7,8,9]).range(d3.schemeCategory10)
    let color;
    fsList.forEach((fs, idx) => {
      color = colorScale(idx%10)
      this.circles
        .filter((d) => fs.includes(Number(d[""])))
        .attr("fill", color)
        .attr("opacity", 0.9);
    });
  }
}
