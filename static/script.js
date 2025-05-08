
async function getRecords() {
  const year = document.getElementById("yearFilter")?.value;
  const month = document.getElementById("monthFilter")?.value;
  const state = document.getElementById("stateFilter")?.value;
  const indicator = document.getElementById("indicatorFilter")?.value;
  const limit = document.getElementById("limitFilter")?.value;

  const query = new URLSearchParams();
  if (year) query.append("year", year);
  if (month) query.append("month", month);
  if (state) query.append("state", state);
  if (indicator) query.append("indicator", indicator);
  if (limit) query.append("limit", limit);  

  const res = await fetch(`/api/records?${query.toString()}`);
  const data = await res.json();
  const tbody = document.querySelector("#dataTable tbody");
  if (!tbody) return;

  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No records found</td></tr>';
    return;
  }

  data.forEach(row => {
    tbody.innerHTML += `
      <tr>
        <td>${row.year}</td>
        <td>${row.month}</td>
        <td>${row.state}</td>
        <td>${row.indicator}</td>
        <td>${row.no_of_deaths}</td>
      </tr>`;
  });
}

async function populateFilters() {
  const res = await fetch('/api/filter-options');
  const options = await res.json();

  const setOptions = (id, values) => {
    const select = document.getElementById(id);
    if (!select) return;
    values.forEach(val => {
      const opt = document.createElement('option');
      opt.value = val;
      opt.textContent = val;
      select.appendChild(opt);
    });
  };

  setOptions("yearFilter", options.years);
  setOptions("monthFilter", options.months);
  setOptions("stateFilter", options.states);
  setOptions("indicatorFilter", options.indicators);
}

document.addEventListener("DOMContentLoaded", () => {
  populateFilters();  
  getRecords();       
});


