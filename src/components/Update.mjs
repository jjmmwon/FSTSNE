import { Scatterplot } from "./Scatterplot.js";
import { url } from "./url.mjs";
import { ResultTable } from "./Table.mjs";
import { Procrustes } from "./Procrustes.mjs";

let title, perp, iter, lr, minSup, resultTable;
let init = true;

const selectionTitle = document.getElementById("dataTitle");
const selectionPerp = document.getElementById("Perplexity");
const selectionIter = document.getElementById("Iterations");
const selectionLR = document.getElementById("LearningRate");
const selectionMinSup = document.getElementById("MinSupport");

resultTable = new ResultTable("#result-table");

let data, procrustes, frqSubG;

async function Update() {
  /*
    Take title and hyperparameters
    -> update url and data
    -> apply Procrustes analysis to data
    -> init ? drawScatterplot : select update
    -> table update
  */
  title = selectionTitle.options[selectionTitle.selectedIndex].value;
  perp = selectionPerp.options[selectionPerp.selectedIndex].text;
  iter = selectionIter.options[selectionIter.selectedIndex].text;
  lr = selectionLR.options[selectionLR.selectedIndex].text;
  minSup = selectionMinSup.options[selectionMinSup.selectedIndex].text;
  url.update(title, perp, iter, lr);

  await urltoData(url);
  console.log(url.urlList.at(-1));
  console.log(data);

  procrustes = new Procrustes(data);
  procrustes.run();

  if (init) {
    drawScatterplot(url);
    init = false;
  } else {
    selectionOccured();
  }
  await frequentSubgraph(url.urlList.at(-1), minSup);
  await resultTable.update(title, perp, iter, lr);
}

let scatterplot, brushedIndex;

function drawScatterplot(url) {
  scatterplot = [];
  let size = 480;
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

async function frequentSubgraph(url, minSup) {
  d3.json(url).then((jsonData) => {
    jsonData.forEach((d) => {
      if (d["Min_support"] == minSup) {
        frqSubG = d["FSM"];
      }
    });
    scatterplot.forEach((d) => {
      d.frequentSubgraphUpdate(frqSubG);
    });
  });
}

function Reset() {
  scatterplot.forEach((d) => d.brushReset());
}

export { Update, Reset };
