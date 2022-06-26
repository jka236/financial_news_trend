import * as d3 from "d3";
import * as d3Collection from "d3-collection";
import React, { useRef, useLayoutEffect } from "react";

const TrendChart = ({ width, height, data, fromDate, toDate }) => {
  const ref = useRef();
  // const recWidth = 100;
  const x = (d, i) => d.key; // given d in data, returns the (ordinal) x-value
  const y = (d) => d.value; // given d in data, returns the (quantitative) y-value
  let title; // given d in data, returns the title text
  let marginTop = 20; // the top margin, in pixels
  let marginRight = 0; // the right margin, in pixels
  let marginBottom = 30; // the bottom margin, in pixels
  let marginLeft = 40; // the left margin, in pixels
  //   let width = 640 // the outer width of the chart, in pixels
  //   let height = 400 // the outer height of the chart, in pixels
  let xDomain; // an array of (ordinal) x-values
  let xRange = [marginLeft, width - marginRight]; // [left, right]
  let yType = d3.scaleLinear; // y-scale type
  let yDomain; // [ymin, ymax]
  let yRange = [height - marginBottom, marginTop]; // [bottom, top]
  let xPadding = 0.1; // amount of x-range to reserve to separate bars
  let yFormat; // a format specifier string for the y-axis
  let yLabel = "word count"; // a label for the y-axis
  let color = "steelblue"; // bar fill color

  useLayoutEffect(() => {
    if (data !== undefined) {
      draw();
    }
  });

  const draw = () => {
    // Compute values.
    // function getFilteredData(data, word) {
    //   return data.filter(function (point) {
    //     return point.word === word;
    //   });
    // }

    const dataFilter = (data, fromDate, toDate) =>
      data.filter((point) => point.date >= fromDate && point.date <= toDate);

    data = dataFilter(data, fromDate, toDate);
    data = d3Collection
      .nest()
      .key((d) => d.word)
      .rollup((d) => d3.sum(d, (g) => g.count))
      .entries(data);

    data = data.sort((a, b) => d3.descending(a.value, b.value)).slice(0, 10);

    const X = d3.map(data, x);
    const Y = d3.map(data, y);

    if (xDomain === undefined) xDomain = X;
    if (yDomain === undefined) yDomain = [0, d3.max(Y)];
    xDomain = new d3.InternSet(xDomain);
    const I = d3.range(X.length).filter((i) => xDomain.has(X[i]));
    const xScale = d3.scaleBand(xDomain, xRange).padding(xPadding);
    const yScale = yType(yDomain, yRange);
    const xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
    const yAxis = d3.axisLeft(yScale).ticks(height / 40, yFormat);

    if (title === undefined) {
      const formatValue = yScale.tickFormat(100, yFormat);
      title = (i) => `${X[i]}\n${formatValue(Y[i])}`;
    } else {
      const O = d3.map(data, (d) => d);
      const T = title;
      title = (i) => T(O[i], i, data);
    }

    const svg = d3.select(ref.current);

    svg
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    svg
      .append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(yAxis)
      .call((g) => g.select(".domain").remove())
      .call((g) =>
        g
          .selectAll(".tick line")
          .clone()
          .attr("x2", width - marginLeft - marginRight)
          .attr("stroke-opacity", 0.1)
      )
      .call((g) =>
        g
          .append("text")
          .attr("x", -marginLeft)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(yLabel)
      );

    //bar
    svg
      .append("g")
      .attr("fill", color)
      .selectAll("rect")
      .data(I)
      .join("rect")
      .attr("x", (i) => xScale(X[i]))
      .attr("y", (i) => yScale(Y[i]))
      .attr("height", (i) => yScale(0) - yScale(Y[i]))
      .attr("width", xScale.bandwidth());

    svg
      .append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(xAxis);
  };

  return (
    <div className="chart">
      <svg ref={ref}></svg>
    </div>
  );
};

export default TrendChart;
