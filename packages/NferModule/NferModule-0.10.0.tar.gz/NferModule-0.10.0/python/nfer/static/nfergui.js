/* Adapted from: (Bo Ericsson) realTimeChartMulti */
'use strict';

function intervalUI() {
  var version = "0.1",
      data,
      // defaults
      maxSeconds = 300, viewportSeconds = 30,
      svgWidth = 700, svgHeight = 300,
      intervalHeight = 5,
      // dimensions
      margin = { top: 20, bottom: 20, left: 100, right: 30, topNav: 10, bottomNav: 20 },
      dimension = { chartTitle: 20, xAxis: 20, yAxis: 20, xTitle: 20, yTitle: 20, navChart: 70 },
      maxY = 100, minY = 0,
      // charts
      chartTitle, yTitle, xTitle,
      drawXAxis = true, drawYAxis = true, drawNavChart = true,
      border,
      selection,
      barId = 0,
      yDomain = [],
      debug = false,
      barWidth = 5,
      x, y,
      xNav, yNav,
      width, height,
      widthNav, heightNav,
      xAxisG, yAxisG,
      xAxis, yAxis,
      xAxisNav, xAxisGNav,
      svg, viewport, viewportG,
      canvas, context,
      hiddenCanvas, hiddenContext,
      tooltip, tooltips = [],
      navCanvas, navContext,
      startTime, endTime,
      startTimeViewport, endTimeViewport,
      transition,
      counts = {}, modCount,
      colors = d3.scaleOrdinal(d3.schemeCategory10),
      updateUI = true;

  // create the chart
  var chart = function(s) {
    selection = s;
    if (selection == undefined) {
      console.error("selection is undefined");
      return;
    };

    transition = d3.transition().duration(500);

    // process titles
    chartTitle = chartTitle || "";
    xTitle = xTitle || "";
    yTitle = yTitle || "";

    // compute component dimensions
    var chartTitleDim = chartTitle == "" ? 0 : dimension.chartTitle,
        xTitleDim = xTitle == "" ? 0 : dimension.xTitle,
        yTitleDim = yTitle == "" ? 0 : dimension.yTitle,
        xAxisDim = !drawXAxis ? 0 : dimension.xAxis,
        yAxisDim = !drawYAxis ? 0 : dimension.yAxis,
        navChartDim = !drawNavChart ? 0 : dimension.navChart;

    // compute dimension of main and nav charts, and offsets
    var marginTop = margin.top + chartTitleDim;
    height = svgHeight - marginTop - margin.bottom - chartTitleDim - xTitleDim - xAxisDim - navChartDim + 30;
    heightNav = navChartDim - margin.topNav - margin.bottomNav;
    var marginTopNav = svgHeight - margin.bottom - heightNav - margin.topNav;
    width = svgWidth - margin.left - margin.right - yAxisDim;
    widthNav = width;
    modCount = Math.floor((height / yDomain.length) / intervalHeight) - 2;

	// hidden canvas for determining what tooltip to show
	hiddenCanvas = selection.append('canvas')
		.attr('width', width)
		.attr('height', height)
		.attr("class", "canvas-hidden")
		.style("position", "absolute")
        .style("left", (margin.left + yAxisDim) + "px")
        .style("top", marginTop + "px")
        .style("display", "none");

    hiddenContext = hiddenCanvas.node().getContext('2d');

    // append the canvas we will use to draw points (well, shapes)
    navCanvas = selection.append("canvas")
        .attr("width", width)
        .attr("height", heightNav)
        .attr("class", "canvas-nav")
        .style("position", "absolute")
        .style("left", (margin.left + yAxisDim) + "px")
        .style("top", marginTopNav + "px")
        .style("z-index", 1);

    // 2d context for drawing on the canvas
    navContext = navCanvas.node().getContext("2d");

    // append the svg
    svg = selection.append("svg")
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .style("position", "absolute")
        .style("z-index", 2)
        .style("border", function(d) {
           if (border) return "1px solid lightgray";
           else return null;
        });

    // append the canvas we will use to draw points (well, shapes)
    canvas = selection.append("canvas")
        .attr("width", width)
        .attr("height", height)
        .attr("class", "canvas-plot")
        .style("position", "absolute")
        .style("left", (margin.left + yAxisDim) + "px")
        .style("top", marginTop + "px")
        .style("z-index", 3);

    // 2d context for drawing on the canvas
    context = canvas.node().getContext("2d");

    // styled in the page CSS
    tooltip = selection.append("div").attr("id", "tooltip");

    // create main group and translate
    var main = svg.append("g")
        .attr("transform", "translate (" + margin.left + "," + marginTop + ")");

    // add group for x axis
    xAxisG = main.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate("+yAxisDim+"," + height + ")");

    // add group for y axis
    yAxisG = main.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate("+yAxisDim+",0)");

    // in x axis group, add x axis title
    main.append("text")
        .attr("class", "title")
        .attr("x", (width / 2) + yAxisDim)
        .attr("y", height + margin.top + 10)
        .attr("dy", ".71em")
        .text(function(d) {
          var text = xTitle == undefined ? "" : xTitle;
          return text;
        });

    // in y axis group, add y axis title
    main.append("text")
        .attr("class", "title")
        .attr("transform", "rotate(-90)")
        .attr("x", - height / 2)
        .attr("y", -margin.left + 15) //-35
        .attr("dy", ".71em")
        .text(function(d) {
          var text = yTitle == undefined ? "" : yTitle;
          return text;
        });

    // in main group, add chart title
    main.append("text")
        .attr("class", "chartTitle")
        .attr("x", (width / 2) + yAxisDim)
        .attr("y", -20)
        .attr("dy", ".71em")
        .text(function(d) {
          var text = chartTitle == undefined ? "" : chartTitle;
          return text;
        });

    // define main chart scales
    x = d3.scaleTime().range([0, width]);
    y = d3.scalePoint().domain(yDomain).rangeRound([height, 0]).padding([1])

    // define main chart axis
    xAxis = d3.axisBottom(x);
    yAxis = d3.axisLeft(y);

    // add nav chart
    var nav = svg.append("g")
        .attr("transform", "translate (" + (margin.left + yAxisDim) + "," + marginTopNav + ")");

    // add group to hold nav x axis
    // please note that a clip path has yet to be added here (tbd)
    xAxisGNav = nav.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + heightNav + ")");

    // define nav chart scales
    xNav = d3.scaleTime().range([0, widthNav]);
    yNav = d3.scalePoint().domain(yDomain).rangeRound([heightNav, 0]).padding([1])

    // define nav axis
    xAxisNav = d3.axisBottom(xNav);

    // compute initial time domains...
    var ts = new Date().getTime();

    // first, the full time domain
    endTime = new Date(ts);
    startTime = new Date(endTime.getTime() - maxSeconds * 1000);
    var interval = endTime.getTime() - startTime.getTime();

    // then the viewport time domain (what's visible in the main chart and the viewport in the nav chart)
    endTimeViewport = new Date(ts);
    startTimeViewport = new Date(endTime.getTime() - viewportSeconds * 1000);
    var intervalViewport = endTimeViewport.getTime() - startTimeViewport.getTime();
    var offsetViewport = startTimeViewport.getTime() - startTime.getTime();

    // set the scale domains for main and nav charts
    x.domain([startTimeViewport, endTimeViewport]);
    xNav.domain([startTime, endTime]);

    // update axis with modified scale
    xAxis.scale(x)(xAxisG);
    yAxis.scale(y)(yAxisG);
    xAxisNav.scale(xNav)(xAxisGNav);

    // create brush (moveable, changable rectangle that determines the time domain of main chart)
    viewport = d3.brushX()
        .extent([[0, 0], [widthNav, heightNav]])
        .on("brush", brushed);

    function brushed () {
      // get the current time extent of viewport
      var selection = d3.event.selection;
      startTimeViewport = xNav.invert(selection[0]);
      endTimeViewport = xNav.invert(selection[1]);

      // compute viewport extent in milliseconds
      intervalViewport = endTimeViewport.getTime() - startTimeViewport.getTime();
      offsetViewport = startTimeViewport.getTime() - startTime.getTime();

      // handle invisible viewport
      if (intervalViewport == 0) {
        intervalViewport = maxSeconds * 1000;
        offsetViewport = 0;
      }

      // update the x domain of the main chart
      x.domain([startTimeViewport, endTimeViewport]);

      // update the x axis of the main chart
      xAxis.scale(x)(xAxisG);

      // update display
      chart.refresh();
    }

    // create group and assign to brush
    viewportG = nav.append("g")
        .attr("class", "viewport")
        .call(viewport)
        .call(viewport.move, [xNav(startTimeViewport), xNav(endTimeViewport)]);

    // for tooltip
    canvas.on("mousemove", mousemove);

    function mousemove() {
	  chart.draw(true);

	  var mouseX = d3.event.layerX || d3.event.offsetX,
		  mouseY = d3.event.layerY || d3.event.offsety,
		  col = hiddenContext.getImageData(mouseX, mouseY, 1, 1).data,
          colKey = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')',
		  nodeData = colorToNode[colKey],
		  tipData = [], i = 0, key;

      //console.log("layerXY: [" + d3.event.layerX + "," + d3.event.layerY + "]"+
      //            "offsetXY: [" + d3.event.offsetX + "," + d3.event.offsetY + "] " + colKey);

	  if (nodeData) {
	    // add the begin/end times to the tooltip
	    tipData.push("begin: " + nodeData.start.getTime());
	    tipData.push("end: " + nodeData.end.getTime());

	    if (tooltips.length > 0) {
	      //console.log(nodeData);
          for (; i < tooltips.length; i++) {
            key = tooltips[i];
            if (key in nodeData.data) {
              tipData.push(key + ": " + nodeData.data[key]);
            }
          }
        }

		tooltip.style('opacity', 0.8)
	      .style('top', mouseY + marginTop + 5 + 'px')
          .style('left', mouseX + margin.left + yAxisDim + 5 + 'px')
          .html(tipData.join("<br />"));
	  } else {
	    tooltip.style('opacity', 0);
	  }
    }

    return chart;
  } // end chart function

  // map to track color the nodes.
  var colorToNode = {}, nextCol = 1;
  // function to create new colors for picking
  var genColor = function() {
	var ret = [], color;
	if (nextCol < 16777215){
	  ret.push(nextCol & 0xff);             // R
	  ret.push((nextCol & 0xff00) >> 8);    // G
	  ret.push((nextCol & 0xff0000) >> 16); // B
      // more separation to avoid anti-alias related mismatches
	  nextCol += 3;
    }
	color = "rgb(" + ret.join(',') + ")";
	return color;
  }

  chart.draw = function(isHidden) {
    var c = isHidden ? hiddenContext : context;

    c.clearRect(0, 0, width, height);

    if (!isHidden) {
      context.fillStyle = "#F5F5F5";
      context.fillRect(0, 0, width, height);
      navContext.clearRect(0, 0, widthNav, heightNav);
      navContext.fillStyle = "#F5F5F5";
      navContext.fillRect(0, 0, widthNav, heightNav);
    }

    // loop over the data and draw each interval to the canvas
    for (var i = 0; i < data.length; i++) {
      var d = data[i],
          dx = Math.round(x(d.start)),
          dy = Math.round(y(d.name) - (intervalHeight / 2) + ((d.count % modCount) * intervalHeight)),
          dw = Math.round(x(d.end) - x(d.start)),
          nx = xNav(d.start),
          ny = yNav(d.name) - 0.5,
          nw = xNav(d.end) - xNav(d.start),
          cx = Math.round(x(d.end)),
          cy = Math.round(y(d.name) + ((d.count % modCount) * intervalHeight)),
          ncx = xNav(d.end),
          ncy = yNav(d.name);

      if (isHidden) {
        hiddenContext.fillStyle = d.tracking;

      } else {
        // apply the color
        context.fillStyle = colors(d.data.color || 0);
        // for the nav, just use black
        navContext.fillStyle = "black";
      }

      if (d.start.getTime() != d.end.getTime()) {
        // draw a rectangle
        c.fillRect(dx, dy, dw, intervalHeight);
        if (!isHidden) {
          // draw in the nav
          navContext.fillRect(nx, ny, nw, 1);
        }

      } else {
         c.beginPath();
         c.arc(cx, cy, intervalHeight / 2, 0,  2 * Math.PI, true);
         c.fill();
         c.closePath();

         if (!isHidden) {
           navContext.beginPath();
           navContext.arc(ncx, ncy, 1, 0,  2 * Math.PI, true);
           navContext.fill();
           navContext.closePath();
         }
      }
    }
  }

  // function to refresh the viz upon changes of the time domain
  // which happens after arrival of new data
  chart.refresh = function (doTransition) {

    // remove intervals from data that are no longer able to be shown
    data = data.filter(function(d) {
      if (d.start.getTime() > startTime.getTime()) {
        return true;
      } else {
        delete colorToNode[d.tracking];
        return false;
      }
    })

    // determine number of interval names
    if (debug) {
      console.log("yDomain", yDomain);
      console.log("data", data);
    }

    chart.draw(false);
  }

  chart.update = function(newEndTime) {
    // get current viewport selection
    var interval = endTimeViewport.getTime() - startTimeViewport.getTime();
    var offset = startTimeViewport.getTime() - xNav.domain()[0].getTime();

    // compute new nav extents
    endTime = newEndTime || new Date();
    startTime = new Date(endTime.getTime() - maxSeconds * 1000);

    // compute new viewport extents
    startTimeViewport = new Date(startTime.getTime() + offset);
    endTimeViewport = new Date(startTimeViewport.getTime() + interval);

    // update scales
    x.domain([startTimeViewport, endTimeViewport]);
    xNav.domain([startTime, endTime]);

    // move the viewport
    //viewportG.transition(transition).call(viewport.move, [xNav(startTimeViewport), xNav(endTimeViewport)]);
    viewportG.call(viewport.move, [xNav(startTimeViewport), xNav(endTimeViewport)]);

    // update axis
    xAxis.scale(x);
    xAxisNav.scale(xNav);

    // transition
    //xAxisG.transition(transition).call(xAxis);
    //xAxisGNav.transition(transition).call(xAxisNav);
    xAxisG.call(xAxis);
    xAxisGNav.call(xAxisNav);

    // refresh svg
    chart.refresh(true);
  }

  // chart accessors and methods
  // TODO: change this because this is JS, not Python or Java and this isn't even really a class

  // new interval. This most recent interval will appear
  // on the far right side of the chart
  chart.add = function(toAdd) {
    // for vertical positioning
    toAdd.count = counts[toAdd.name];
    counts[toAdd.name]++;
    // for tooltip tracking
    toAdd.tracking = genColor();
    colorToNode[toAdd.tracking] = toAdd;

    //console.log(toAdd);

    data.push(toAdd);
    if (updateUI) {
      chart.update(toAdd.end);
    }
    return chart;
  }

  // new array of intervals
  chart.batch = function(toAdd) {
    if (toAdd.length == 0) {
      return chart;
    }

    // precompute values for the whole batch
    for (var i = 0; i < toAdd.length; i++) {
      // for vertical positioning
      toAdd[i].count = counts[toAdd[i].name] || 0;
      counts[toAdd[i].name] = toAdd[i].count + 1;
      // for tooltip tracking
      toAdd[i].tracking = genColor();
      colorToNode[toAdd[i].tracking] = toAdd[i];
    }

    data = data.concat(toAdd);
    if (updateUI) {
      chart.update(toAdd[toAdd.length - 1].end);
    }
    return chart;
  }

  // interval bar height
  chart.intervalHeight = function(_) {
    if (arguments.length == 0) return intervalHeight;
    intervalHeight = _;
    return chart;
  }

  // svg width
  chart.width = function(_) {
    if (arguments.length == 0) return svgWidth;
    svgWidth = _;
    return chart;
  }

  // svg height
  chart.height = function(_) {
    if (arguments.length == 0) return svgHeight;
    svgHeight = _;
    return chart;
  }

  // svg border
  chart.border = function(_) {
    if (arguments.length == 0) return border;
    border = _;
    return chart;
  }

  // chart title
  chart.title = function(_) {
    if (arguments.length == 0) return chartTitle;
    chartTitle = _;
    return chart;
  }

  // x axis title
  chart.xTitle = function(_) {
    if (arguments.length == 0) return xTitle;
    xTitle = _;
    return chart;
  }

  // y axis title
  chart.yTitle = function(_) {
    if (arguments.length == 0) return yTitle;
    yTitle = _;
    return chart;
  }

  // yItems (can be dynamically added after chart construction)
  chart.yDomain = function(_) {
    if (arguments.length == 0) return yDomain;
    yDomain = _;
    // update the hash of item counts
    for (var i = 0; i < _.length; i++) {
      if (!(_[i] in counts)) {
        counts[_[i]] = 0;
      }
    }
    if (svg) {
      // update the y ordinal scale
      y = d3.scalePoint().domain(yDomain).rangeRound([height, 0]).padding([1]);
      // update the y axis
      yAxis.scale(y)(yAxisG);
      // update the y ordinal scale for the nav chart
      yNav = d3.scalePoint().domain(yDomain).rangeRound([heightNav, 0]).padding([1]);
      // update the mod number for count offset
      modCount = Math.floor((height / _.length) / intervalHeight);
    }
    return chart;
  }

  // set the maximum number of seconds displayed in the chart
  chart.maxSeconds = function(_) {
    if (arguments.length == 0) return maxSeconds;
    maxSeconds = _;
    return chart;
  }

  // set the maximum number of seconds displayed in the viewport at one time
  chart.viewportSeconds = function(_) {
    if (arguments.length == 0) return viewportSeconds;
    viewportSeconds = _;
    return chart;
  }

  chart.tooltips = function(_) {
    if (arguments.length == 0) return tooltips;
    tooltips = _;
    return chart;
  }

  chart.pause = function() {
    updateUI = false;
  }

  chart.resume = function() {
    updateUI = true;
  }

  // debug
  chart.debug = function(_) {
    if (arguments.length == 0) return debug;
    debug = _;
    return chart;
  }

  chart.data = function(_) {
    if (arguments.length == 0) return data;
    data = _;
    return chart;
  }

  chart.counts = function(_) {
    if (arguments.length == 0) return counts;
    counts = _;
    return chart;
  }

  // version
  chart.version = version;

  // initial data
  data = [];

  return chart;
}