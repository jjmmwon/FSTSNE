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

    this.redSelected = new Set();
    this.greenSelected = new Set();

    this.handlers = {};
    this.isRed = true;
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

    this.xScale.domain([-2, 2]).range([0, this.width]);
    this.yScale.domain([-2, 2]).range([this.height, 0]);

    this.circles = this.container
      .selectAll("circle")
      .data(this.data)
      .join("circle");

    this.circles
      .transition()
      .attr("cx", (d) => this.xScale(d["0"]))
      .attr("cy", (d) => this.yScale(d["1"]))
      .attr("fill", "rgb(0,100,200)")
      .attr("opacity", 0.6)
      .attr("r", 2);

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
    this.isRed = d3
      .select("input[type=radio][id=redBrush]")
      .property("checked");

    if (this.isRed) {
      selectedIndex.forEach((val) => {
        this.redSelected.add(val);
      });
    } else {
      selectedIndex.forEach((val) => {
        this.greenSelected.add(val);
      });
    }

    this.circles
      .transition()
      .attr("r", (d) => (selectedIndex.has(d[""]) ? 3 : 2));

    // this.isRed = d3
    //   .select("input[type=radio][id=redBrush]")
    //   .property("checked");

    if (this.isRed) {
      this.circles.classed("redBrush", (d) => this.redSelected.has(d[""]));
    } else {
      this.circles.classed("greenBrush", (d) => this.greenSelected.has(d[""]));
    }

    // .attr("fill", (d) =>
    //   selectedIndex.has(d[""]) ? "rgb(200,50,0)" : "rgb(0,100,200)"
    // );
  }

  brushReset() {
    this.isRed = d3
      .select("input[type=radio][id=redBrush]")
      .property("checked");

    if (this.isRed) {
      this.redSelected.clear();
      this.circles.classed("redBrush", false);
    } else {
      this.greenSelected.clear();
      this.circles.classed("greenBrush", false);
    }
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

    this.isRed = d3
      .select("input[type=radio][id=redBrush]")
      .property("checked");

    if (this.isRed) {
      this.circles.classed("redBrush", (d) => this.isBrushed(d, selection));
    } else {
      this.circles.classed("greenBrush", (d) => this.isBrushed(d, selection));
    }
    //this.circles.classed("brushed", (d) => this.isBrushed(d, selection));

    if (this.handlers.brush)
      this.handlers.brush(
        this.data.filter((d) => this.isBrushed(d, selection))
      );
  }

  on(eventType, handler) {
    this.handlers[eventType] = handler;
  }
}
