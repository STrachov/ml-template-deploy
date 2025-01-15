$(function () {

  // =====================================
  // Professional terminology usage
  // =====================================
  var options = {
    series: [
      {
        name: "Correctly",
        data: [1.5, 2.7, 2.2, 3.4, 3.5],
      },
      {
        name: "Incorrectly",
        data: [-3.1, -2.1, -2.5, -1.5, -1.2],
      },
    ],
    chart: {
      toolbar: {
        show: false,
      },
      type: "bar",
      fontFamily: "Plus Jakarta Sans,sans-serif",
      foreColor: "#adb0bb",
      height: 270,
      stacked: true,
      offsetX: -20
    },
    colors: ["var(--bs-primary)", "#777"],
    // "var(--bs-secondary)"
    plotOptions: {
      bar: {
        horizontal: false,
        barHeight: "70%",
        columnWidth: "20%",
        borderRadius: [5],
        borderRadiusApplication: 'end',
        borderRadiusWhenStacked: 'all'
      },
    },
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    grid: {
      show: false,
    },
    yaxis: {
      min: -4,
      max: 4,
      tickAmount: 4,
    },
    xaxis: {
      categories: [
        "Jan",
        "Fab",
        "Mar",
        "Apr",
        "May",
      ],
      show: false,
      axisTicks: {
        show: false,
      },
      axisBorder: {
        show: false,
      }
    },
    tooltip: {
      theme: "dark",
    },
  };

  var chart = new ApexCharts(document.querySelector("#terminology-usage"), options);
  chart.render();




  // =====================================
  // Errors structure
  // =====================================

  var options_basic = {
    series: [{
      name: "September",
      data: [67, 51, 78, 40, 63]
    }, ],
    chart: {
      fontFamily: '"Nunito Sans", sans-serif',
      height: 350,
      type: "radar",
      toolbar: {
        show: false,
      },
    },
    colors: ["#615dff"],
    xaxis: {
      categories: ["Sentence structure", "Tense", "Article", "Punctuation", "Other"],
    },
    tooltip: {
      theme: "dark",
    },
  };

  new ApexCharts(document.querySelector("#errors-structure-monthly"), options_basic).render();


  // =====================================
  // Response time
  // =====================================
  var options = {
    chart: {
      id: "response-time",
      type: "area",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
      toolbar: false,
    },
    series: [
      {
        name: "Response Time",
        color: "var(--bs-primary)",
        data: [{x:"Apr", y:52}, {x:"May", y:56}, {x:"June", y:47},{x:"July", y:45}, {x:"Aug", y:40}],
      },
    ],
    xaxis: {
      type: "category",
    },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 0,
        inverseColors: false,
        opacityFrom: 0.18,
        opacityTo: 0,
        stops: [20, 180],
      },
    },

    markers: {
      size: 0,
    },
    tooltip: {
      theme: "dark",
      fixed: {
        enabled: true,
        position: "right",
      },
      x: {
        show: false,
      },
    },
  };
  new ApexCharts(document.querySelector("#response-time"), options).render();


  // =====================================
  // Error rate
  // =====================================
  var options = {
    series: [
      {
        name: "Error rate",
        data: [33, 35, 30, 25, 15, 18],
      },
    ],

    chart: {
      toolbar: {
        show: false,
      },
      offsetX: -20,
      height: 250,
      type: "bar",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
    },
    colors: ["#777", "#777", "#777", "#777", "var(--bs-primary)", "#777"],
    plotOptions: {
      bar: {
        borderRadius: 5,
        columnWidth: "45%",
        distributed: true,
        endingShape: "rounded",
      },
    },

    dataLabels: {
      enabled: true,
    },
    legend: {
      show: false,
    },
    grid: {
      yaxis: {
        lines: {
          show: false,
        },
      },
      xaxis: {
        lines: {
          show: false,
        },
      },
    },
    xaxis: {
      categories: [["Apr"], ["May"], ["June"], ["July"], ["Aug"], ["Sept"]],
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      labels: {
        show: false,
      },
    },
    tooltip: {
      theme: "dark",
    },
  };

  var chart = new ApexCharts(document.querySelector("#errors-rate"), options);
  chart.render();


  // =====================================
  // Time used daily
  // =====================================
  var time_used_daily = {
    series: [20, 40],
    labels: ["Used", "Available"],
    chart: {
      height: 110,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#c6d1e9",
    },

    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },

    colors: ["var(--bs-primary)", "var(--bs-secondary)", "var(--bs-yellow)"],
    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },

    stroke: {
      show: false,
    },

    plotOptions: {
      pie: {
        donut: {
          size: "70%",
          background: "none",
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: "18px",
              color: undefined,
              offsetY: -10,
            },
            value: {
              show: false,
              color: "#98aab4",
            },
          },
        },
      },
    },
  };

  var time_used_daily_chart = new ApexCharts(document.querySelector("#time-used-daily"), time_used_daily);
  time_used_daily_chart.render();

  // =====================================
  // Time used monthly
  // =====================================
  var time_used_monthly = {
    series: [200, 1800],
    labels: ["Used", "Available"],
    chart: {
      height: 110,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#c6d1e9",
    },

    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },

    colors: ["var(--bs-primary)", "var(--bs-secondary)", "var(--bs-yellow)"],
    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },

    stroke: {
      show: false,
    },

    plotOptions: {
      pie: {
        donut: {
          size: "70%",
          background: "none",
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: "18px",
              color: undefined,
              offsetY: -10,
            },
            value: {
              show: false,
              color: "#98aab4",
            },
          },
        },
      },
    },
  };

  var time_used_monthly_chart = new ApexCharts(document.querySelector("#time-used-monthly"), time_used_monthly);
  time_used_monthly_chart.render();






});
