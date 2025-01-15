$(function () {

    // =================================
    // Tooltip
    // =================================
    var tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // scroll

    $(".scroll-link").on("click", function (t) {
        var o = $(this);
        $("html, body").stop().animate({
           scrollTop: $(o.attr("href")).offset().top - 160
        }, 1e3), t.preventDefault()
     })

    // fixed header

    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $('header').addClass('fixed-header');
        } else {
            $('header').removeClass('fixed-header');
        }
    });

    // Aos

    AOS.init({
		once: true,
	});

    // Production Slider

    $('.production-slider .owl-carousel').owlCarousel({
        nav: false,
        dots: true,
        loop: true,
        items: 1,
        dots: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true
    })


    // Review Slider

    $('.review-slider .owl-carousel').owlCarousel({
        loop: true,
        margin: 0,
        dots: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    })
    // Review Slider

    $('.tutor-slider .owl-carousel').owlCarousel({
        loop: true,
        margin: 0,
        dots: false,
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            1024: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })

    var card1 = {
      series: [
        {
          name: "Task Success Rate",
          data: [0, 3, 1, 2, 8, 1, 5, 1],
        },
      ],
      chart: {
        height: 75,
        type: "area",
        fontFamily: '"Nunito Sans",sans-serif',
        zoom: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
        sparkline: {
          enabled: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#3699ff"],
      stroke: {
        curve: "smooth",
        width: 2,
      },
      fill: {
        type: "solid",
        opacity: 0.2,
      },
      grid: {
        show: false,
      },
      xaxis: {
        show: false,
      },
      yaxis: {
        show: false,
      },
      tooltip: {
        theme: "dark",
      },
    };

    var chart1 = new ApexCharts(document.querySelector(".speaking-skills"), card1);
    chart1.render();

    // 2
    var card2 = {
      series: [
        {
          name: "Word Recognition",
          data: [8, 6, 5, 6, 3, 6, 2, 4],
        },
      ],
      chart: {
        height: 75,
        type: "area",
        fontFamily: '"Nunito Sans",sans-serif',
        zoom: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
        sparkline: {
          enabled: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#ee9d01"],
      stroke: {
        curve: "smooth",
        width: 2,
      },
      fill: {
        type: "solid",
        opacity: 0.2,
      },
      grid: {
        show: false,
      },
      xaxis: {
        show: false,
      },
      yaxis: {
        show: false,
      },
      tooltip: {
        theme: "dark",
      },
    };

    var chart2 = new ApexCharts(
      document.querySelector(".listening-skills"),
      card2
    );
    chart2.render();

    // 3
    var card3 = {
      series: [
        {
          name: "Fluency Rate",
          data: [0, 1, 3, 2, 5, 4, 6, 8],
        },
      ],
      chart: {
        height: 75,
        type: "area",
        fontFamily: '"Nunito Sans",sans-serif',
        zoom: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
        sparkline: {
          enabled: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#f64e60"],
      stroke: {
        curve: "smooth",
        width: 2,
      },
      fill: {
        type: "solid",
        opacity: 0.2,
      },
      grid: {
        show: false,
      },
      xaxis: {
        show: false,
      },
      yaxis: {
        show: false,
      },
      tooltip: {
        theme: "dark",
      },
    };

    var chart3 = new ApexCharts(
      document.querySelector(".writing-skills"),
      card3
    );
    chart3.render();
  });
