import { Update } from "./components/Update.mjs";

function main() {
  d3.select("#update").on("click", Update);
  Update();
}

main();
