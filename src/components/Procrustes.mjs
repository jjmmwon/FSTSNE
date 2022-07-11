export { Procrustes };

class Procrustes {
  constructor(data) {
    this.data = data;
  }

  #translation(datum) {
    let [x, y] = [0, 0];
    datum.forEach((d) => {
      x += d["0"];
      y += d["1"];
    });
    x /= datum.length;
    y /= datum.length;

    datum.forEach((d) => {
      d["0"] -= x;
      d["1"] -= y;
    });

    return datum;
  }
  #uniformScaling(datum) {
    let s = 0;
    datum.forEach((d) => {
      s += d["0"] * d["0"];
      s += d["1"] * d["1"];
    });
    s /= datum.length;
    s = Math.sqrt(s);

    datum.forEach((d) => {
      d["0"] /= s;
      d["1"] /= s;
    });

    return datum;
  }

  #findTheta(base, datum) {
    let [numerator, denominator] = [0, 0];
    let x, y, z, w, theta;

    for (let i = 0; i < datum.length; i++) {
      [x, y, z, w] = [base[i]["0"], base[i]["1"], datum[i]["0"], datum[i]["1"]];
      numerator += w * y - z * x;
      denominator += w * x + z * y;
    }
    theta = Math.atan(numerator / denominator);

    return theta;
  }

  #rotation(datum, theta) {
    let cos, sin, u, v;
    cos = Math.cos(theta);
    sin = Math.sin(theta);

    datum.forEach((d) => {
      u = cos * d["0"] - sin * d["1"];
      v = sin * d["0"] + cos * d["1"];
      d["0"] = u;
      d["1"] = v;
    });

    return datum;
  }

  run() {
    let base;

    this.data.forEach((d) => {
      this.#uniformScaling(this.#translation(d));
    });

    base = this.data[1];

    // for (let i = 1; i < this.data.length; i++) {
    //   this.#rotation(this.data[i], this.#findTheta(base, this.data[i]));
    // }
  }
}
