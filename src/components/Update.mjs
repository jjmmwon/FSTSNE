import { Scatterplot } from "./Scatterplot.js";
import { url } from "./url.mjs";
import { ResultTable } from "./Table.mjs";
import { Procrustes } from "./Procrustes.mjs";

let title, perp, iter, lr, resultTable;
let init = true;

const selectionTitle = document.getElementById("dataTitle");
const selectionPerp = document.getElementById("Perplexity");
const selectionIter = document.getElementById("Iterations");
const selectionLR = document.getElementById("LearningRate");

resultTable = new ResultTable("#result-table");

let data, procrustes;

async function Update() {
  /*
    Take title and hyperparameters
    -> update url and data
    -> apply Procrustes analysis to data
    -> init ? drawScatterplot : select update
    -> table update    
  */
  title = selectionTitle.options[selectionTitle.selectedIndex].text;
  perp = selectionPerp.options[selectionPerp.selectedIndex].text;
  iter = selectionIter.options[selectionIter.selectedIndex].text;
  lr = selectionLR.options[selectionLR.selectedIndex].text;
  url.update(title, perp, iter, lr);

  await urltoData(url);

  console.log(data);

  procrustes = new Procrustes(data);
  procrustes.run();

  console.log(data);

  if (init) {
    drawScatterplot(url);
    init = false;
  } else {
    selectionOccured();
  }

  await resultTable.update(title, perp, iter, lr);
}

let scatterplot, brushedIndex;

function drawScatterplot(url) {
  scatterplot = [];
  let size = 300;
  for (let i = 0; i < 11; i++) {
    scatterplot[i] = new Scatterplot(
      `#scatterplot${url.indexList[i]}`,
      data[i],
      size,
      size
    );
    scatterplot[i].initialize();
    scatterplot[i].on("brush", (brushedItems) => {
      brushedIndex = new Set(brushedItems.map((d) => d[""]));
      brushOccured(brushedIndex);
    });
  }
  initScatterplot(scatterplot);
}

function initScatterplot(scatterplot) {
  scatterplot.forEach((d) => d.selectionUpdate());
}

function selectionOccured() {
  scatterplot.forEach((d, idx) => d.selectionUpdate(data[idx]));
}

function brushOccured(brushedIndex) {
  scatterplot.forEach((d) => d.brushUpdate(brushedIndex));
}

async function urltoData(url) {
  data = [];
  for (let i = 0; i < url.indexList.length; i++) {
    data[i] = await d3.csv(url.urlList[i]);
    data[i].forEach((d) => {
      d["0"] = +d["0"];
      d["1"] = +d["1"];
    });
  }
}

export { Update };
