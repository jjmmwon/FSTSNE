import { Update, Reset } from "./components/Update.mjs";

function main() {
  let resetBtn = d3.select("#reset");

  d3.select("#update").on("click", Update);
  d3.select("#reset").on("click", Reset);
  d3.select("#redBrush").on("click", () => {
    resetBtn.classed("btn-success", false);
    resetBtn.classed("btn-danger", true);
  });
  d3.select("#greenBrush").on("click", () => {
    resetBtn.classed("btn-danger", false);
    resetBtn.classed("btn-success", true);
  });
  Update();
}

main();
