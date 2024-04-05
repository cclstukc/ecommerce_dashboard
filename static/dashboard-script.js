//JavaScript logic for data fetching and chart rendering is separated from html structure
//This makes the code more organised and scalable
//External scripts keep the .html clean and focused on structure and content
//Browsers cache external scripts, so if multiple pages use the same script the file is loaded once and cached
//The same external script can be used across multiple pages creating consistency and reducing code duplication

//Loading data asychronously can help webpages remain responsive when retrieving data
//Asychronous functions fetch data from api endpoints
//Async function extracts the repetitive task of fetching data and rendering charts.
//Use this function with different parameters to fetch data from different api endpoints and render multiple charts
//This also makes it easier to add new charts
async function fetchDataAndRenderChart(
  apiEndpoint,
  chartElementId,
  chartConfig
) {
  try {
    let response = await fetch(apiEndpoint);
    let data = await response.json();
    const ctx = document.getElementById(chartElementId).getContext("2d");
    new Chart(ctx, chartConfig(data));
  } catch (error) {
    console.error("Error fetching or rendering chart:", error);
  }
}


//Fetch data and render chart scripts from the dashboard.html
//The repetitive .then, const and new chart lines are removed to the new fetchDataAndRenderChart function above
//Use function to pull data from specified api endpoint (e.g. 'orders_over_time') and... 
//...uses this data to generate and display a chart on a predefined canvas element in the .html...
//...specified by its id (e.g. 'ordersChart'), <canvas id="ordersChart">.
fetchDataAndRenderChart("/api/orders_over_time", "ordersChart", (data) => ({
  type: "line",
  data: {
    labels: data.dates,
    datasets: [
      {
        label: "Number of Orders",
        data: data.counts,
        // ... other configPython
      },
    ],
  },
  // ... other options
}));

fetchDataAndRenderChart("/api/low_stock_levels", "stockChart", (data) => ({
  type: "bar",
  data: {
    labels: data.products,
    datasets: [
      {
        label: "Low Stock",
        data: data.quantities,
        // ... other config
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
      x: {
        display: false, // This will hide the x-axis labels
      },
    },
  },
}));

fetchDataAndRenderChart(
  "/api/most_popular_products",
  "popularProductsChart",
  (data) => ({
    type: "bar",
    data: {
      labels: data.map((item) => item.product_name),
      datasets: [
        {
          label: "Quantity Sold",
          data: data.map((item) => item.total_quantity),
          // ... other config
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
        x: {
          display: false, // This will hide the x-axis labels
        },
      },
    },
  })
);

// Revenue Generation Chart
fetchDataAndRenderChart("/api/revenue_generation", "revenueChart", (data) => ({
  type: "line",
  data: {
    labels: data.dates,
    datasets: [
      {
        label: "Total Revenue",
        data: data.revenues,
        // ... other config
      },
    ],
  },
  // ... other options
}));

// Product Category Popularity Chart
fetchDataAndRenderChart(
  "/api/product_category_popularity",
  "categoryPopularityChart",
  (data) => ({
    type: "pie",
    data: {
      labels: data.categories,
      datasets: [
        {
          label: "Total Sales",
          data: data.sales,
          // ... other config
        },
      ],
    },
  })
);

// Payment Method Popularity Chart
fetchDataAndRenderChart(
  "/api/payment_method_popularity",
  "paymentMethodChart",
  (data) => ({
    type: "pie",
    data: {
      labels: data.methods,
      datasets: [
        {
          label: "Transaction Count",
          data: data.counts,
          // ... other config
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          display: false, // This will hide the x-axis labels
        },
      },
    },
  })
);

// Temperature Over Time Chart
fetchDataAndRenderChart(
  "/api/temperature_over_time",
  "temperatureChart",
  (data) => ({
    type: "line",
    data: {
      labels: data.daily.time,
      datasets: [
        {
          label: "Temperature (°C)",
          data: data.daily.temperature_2m_max,
          borderColor: "rgba(255, 0, 0, 1)",
          backgroundColor: "rgba(200, 0, 192, 0.2)",
          fill: false,
        },
      ],
    },
    // ... other options can be added as needed
  })
);
