class Scatterplot {
  constructor(
    svg,
    data,
    width = 500,
    height = 500,
    margin = {
      top: 10,
      right: 50,
      bottom: 40,
      left: 40,
    }
  ) {
    this.svg = svg;
    this.data = data;
    this.width = width;
    this.height = height;
    this.margin = margin;

    this.selected = new Set();
    this.handlers = {};
  }

  initialize() {
    this.svg = d3.select(this.svg);
    this.container = this.svg.append("g");
    this.xAxis = this.svg.append("g");
    this.yAxis = this.svg.append("g");
    this.legend = this.svg.append("g");

    this.xScale = d3.scaleLinear();
    this.yScale = d3.scaleLinear();
    this.zScale = d3.scaleOrdinal().range(d3.schemeCategory10);

    this.svg
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom);

    this.container.attr(
      "transform",
      `translate(${this.margin.left}, ${this.margin.top})`
    );

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

  update(selectedIndex = this.selected) {
    this.container.call(this.brush);

    this.xScale
      .domain(d3.extent(this.data, (d) => d["0"]))
      .range([0, this.width]);
    this.yScale
      .domain(d3.extent(this.data, (d) => d["1"]))
      .range([this.height, 0]);

    this.circles = this.container
      .selectAll("circle")
      .data(this.data)
      .join("circle");

    this.circles
      .transition()
      .attr("cx", (d) => this.xScale(d["0"]))
      .attr("cy", (d) => this.yScale(d["1"]))
      .attr("fill", (d) =>
        selectedIndex.has(d[""]) ? "rgb(200,100,0)" : "rgb(0,100,200)"
      )
      .attr("opacity", 0.5)
      .attr("r", 2);

    console.log(selectedIndex);
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
  }

  isBrushed(d, selection) {
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
}
