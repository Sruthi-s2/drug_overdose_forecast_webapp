function getSelectedValues(id) {
    const options = document.getElementById(id)?.selectedOptions || [];
    const values = Array.from(options).map(opt => opt.value);
    return values.includes("ALL") ? [] : values;
  }
  
  function fetchTrendData() {
    const states = getSelectedValues("stateFilter");
    const years = getSelectedValues("yearFilter");
    const months = getSelectedValues("monthFilter");
    const indicators = getSelectedValues("indicatorFilter");
  
    const params = new URLSearchParams();
    if (states.length) params.append("states", states.join(","));
    if (years.length) params.append("years", years.join(","));
    if (months.length) params.append("months", months.join(","));
    if (indicators.length) params.append("indicator", indicators[0]); 
  
    fetch(`/api/trend_charts?${params}`)
      .then(res => res.json())
      .then(data => {
        drawLineChart(data.totalByYear);
        drawBarChart(data.byStateOverTime);
        drawDonutChart(data.percentByDrug);
      });
  }
  
  
  function drawLineChart(data) {
    Plotly.newPlot('lineChart', [{
      x: data.years,
      y: data.values,
      type: 'scatter',
      mode: 'lines+markers',
      line: { shape: 'spline', color: '#17BECF' }
    }], {
      title: 'Overdose Deaths by Year',
      yaxis: { title: 'Deaths' },
      xaxis: { title: 'Year' }
    });
  }
  
  
  function drawBarChart(stateData) {
    const labels = stateData.map(d => d.state);
    const values = stateData.map(d => d.values[0]);  
  
    Plotly.newPlot('barChart', [{
      x: labels,
      y: values,
      type: 'bar',
      marker: { color: '#FF4136' }
    }], {
      title: 'Deaths per State (in 25,000s)',
      yaxis: { title: 'Deaths (×25,000)' },
      xaxis: { title: 'State' }
    });
  }
  
  
  function drawDonutChart(drugData) {
    Plotly.newPlot('donutChart', [{
      labels: drugData.labels,
      values: drugData.values,
      type: 'pie',
      hole: 0.4,
      marker: {
        colors: ['#0074D9', '#FF851B', '#2ECC40', '#B10DC9', '#FF4136',
                 '#FFDC00', '#39CCCC', '#01FF70', '#85144b', '#3D9970']
      }
    }], {
      title: '% Deaths by Drug',
      showlegend: true
    });
  }
  
  // Init
  window.addEventListener("DOMContentLoaded", () => {
    fetchTrendData();
    ["stateFilter", "yearFilter", "monthFilter", "indicatorFilter"].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener("change", fetchTrendData);
    });
  });
  