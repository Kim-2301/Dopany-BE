// var companyInfo = {
//   companyName: "{{ company_info.company_name|escapejs }}",
// };

var CompanyApp = CompanyApp || {}; // Namespace

CompanyApp.companyDetails = null;
CompanyApp.stockChart = null;

$(document).ready(function () {
  setTabs();
  requestCompanyDetails();
  resizeWordCloud();
  displayWordCloud();
  displayCompanyNews();
  displayRecruits();
});

function activateTab(event, tabId) {
  var i, tabcontent, tablinks;

  // Hide all tab content
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Reset all tabs to default style
  tablinks = document.getElementsByClassName("tab");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "white"; // 기본 비활성 색상
    tablinks[i].style.color = "black"; // 기본 텍스트 색상
  }

  // Display the current tab and change its style
  document.getElementById(tabId).style.display = "block";
  event.currentTarget.style.backgroundColor = "#f39189";
  event.currentTarget.style.color = "white";
}

function setTabs() {
  // Attach click event handler to the 'info-btn'
  $("#info-btn").on("click", function (event) {
    activateTab(event, "tab1");
  });

  // Attach click event handler to the 'recruit-btn'
  $("#recruit-btn").on("click", function (event) {
    activateTab(event, "tab2");
  });

  // Initialize by simulating a click on the first tab
  document.getElementsByClassName("tab")[0].click();
}

requestCompanyDetails = () => {
  console.log(companyInfo.companyName);
  $.ajax({
    url: "/etf",
    type: "GET",
    dataType: "json",
    data: {
      "company-name": companyInfo.companyName,
    },
    success: function (response) {
      console.log(response);
      CompanyApp.companyDetails = response.company_info;
      displayStockChart(response.company_info);
    },
    error: function (xhr, status, error) {
      displayEmptyChart();
      console.error(
        "Error fetching data: " + xhr.status + " " + xhr.responseText
      );
    },
  });
};

displayEmptyChart = () => {
  const canvas = $("#stock-chart")[0]; // DOM 요소로 접근
  const ctx = canvas.getContext("2d"); // 2D 컨텍스트 가져오기

  // 데이터가 없으므로 빈 데이터셋으로 차트 생성
  const chart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day", // 데이터가 없어도 일 단위로 설정, 필요에 따라 변경 가능
          },
          display: true,
          title: {
            display: true,
            text: "Date",
          },
        },
        y: {
          display: true,
          title: {
            display: true,
            text: "Price",
          },
        },
      },
      plugins: {
        legend: {
          display: false, // 레전드가 필요 없으므로 숨김
        },
      },
      maintainAspectRatio: false, // 그래프 비율을 유지
      responsive: true, // 반응형 디자인을 활성화
    },
  });
};

displayStockChart = (data) => {
  const canvas = $("#stock-chart").get(0); // DOM 요소로 접근
  const ctx = canvas.getContext("2d"); // 2D 컨텍스트 가져오기

  if (CompanyApp.stockChart) {
    CompanyApp.stockChart.destroy();
  }

  const stockDatasets = data.stock_info.map((stock, index) => {
    data = stock.closing_price.map((price, index) => ({
      x: stock.transaction_date[index],
      y: price,
    }));

    return {
      data: data,
      fill: false,
      // borderColor: getRandomColor(etf.etf_name), // 각 선의 색상을 랜덤으로 생성
      borderColor: purple,
      tension: 0.1,
    };
  });

  CompanyApp.stockChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: stockDatasets,
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day",
          },
        },
      },
      maintainAspectRatio: false, // 그래프 비율을 유지
      responsive: true, // 반응형 디자인을 활성화
    },
  });
};

resizeWordCloud = () => {
  const targetWidth = $("#keyword-cloud").width();
  const targetHeight = $("#keyword-cloud").height();
  displayWordCloud(targetWidth, targetHeight);
};

// const keywords = [
//   { text: "JavaScript", size: 50, pc: "pros" },
//   { text: "HTML", size: 40, pc: "pros" },
//   { text: "CSS", size: 35, pc: "pros" },
//   { text: "D3.js", size: 30, pc: "cons" },
//   { text: "Canvas", size: 25, pc: "cons" },
// ];

// Function to create/update the word cloud
displayWordCloud = (width, height) => {
  $("#keyword-cloud svg").remove();

  const keywords = [];

  // Loop through each key-value pair in the original data object
  for (const [text, [isPros, size]] of Object.entries(
    CompanyApp.companyDetails
  )) {
    keywords.push({ text, size, isPros });
  }

  // Initialize the SVG element
  const svg = d3
    .select("#keyword-cloud")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  // Set up d3 cloud layout
  const layout = d3.layout
    .cloud()
    .size([width, height])
    .words(keywords)
    .padding(5)
    .rotate(() => ~~360)
    .fontSize((d) => d.size)
    .on("end", (words) => {
      svg
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", (d) => d.size + "px")
        .style("fill", (d) => (d.isPros ? "blue" : "red"))
        .attr("text-anchor", "middle")
        .attr("transform", (d) => `translate(${d.x},${d.y})rotate(${d.rotate})`)
        .text((d) => d.text);
    });

  layout.start();
};

displayCompanyNews = () => {
  CompanyApp.companyDetails.company_news.forEach(function (item) {
    for (let news_id in item) {
      const news = item[news_id];

      const $anchor = $("<a></a>", {
        class: "card",
        href: news.news_url,
        target: "_blank",
        style: "text-decoration: none",
      });

      $("<h1></h1>", {
        text: news.news_title,
      }).appendTo($anchor);

      $("<p></p>", {
        text: news.posted_at,
      }).appendTo($anchor);

      $("<p></p>", {
        text: news.news_text,
      }).appendTo($anchor);

      $("#news-list").append($anchor);
    }
  });
};

displayRecruits = () => {
  // Simulating the recruitment data object
  const recruitmentData = {
    recruitment1: {
      title: "title1",
      url: "jobkorea_url1",
    },
    recruitment2: {
      title: "title2",
      url: "jobkorea_url2",
    },
    recruitment3: {
      title: "title3",
      url: "jobkorea_url3",
    },
  };
  // const recruitmentData = CompanyApp.companyDetails.company_recruitments

  for (let key in recruitmentData) {
    if (recruitmentData.hasOwnProperty(key)) {
      const recruitment = recruitmentData[key];

      // Create the anchor element
      const $anchor = $("<a></a>", {
        class: "card",
        href: recruitment.url,
        target: "_blank",
        style: "text-decoration: none",
      });

      // Create and append the h1 element for the title
      $("<h1></h1>", {
        text: recruitment.title,
      }).appendTo($anchor);

      // Replace these placeholder texts with the actual data if available
      $("<p></p>", {
        text:
          recruitment.career +
          "  " +
          recruitment.education +
          "  " +
          recruitment.due_date,
      }).appendTo($anchor);

      $("<p></p>", {
        text: recruitment.job_name,
      }).appendTo($anchor);

      $("<p></p>", {
        text: recruitment.skill_name,
      }).appendTo($anchor);

      // Append the completed anchor element to the main div container
      $("#recruit-section").append($anchor);
    }
  }
};

$(window).resize(resizeWordCloud);
