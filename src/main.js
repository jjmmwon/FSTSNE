import { Update, Reset } from "./components/Update.mjs";

function main() {
  d3.select("#update").on("click", Update);
  d3.select("#reset").on("click", Reset);

  Update();
}

main();
