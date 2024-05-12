// var companyInfo = {
//   companyName: "{{ company_info.company_name|escapejs }}",
// };

var CompanyApp = CompanyApp || {}; // Namespace

CompanyApp.companyDetails = {};
CompanyApp.stockChart = null;

$(document).ready(function () {
  setTabs();
  requestCompanyDetails();
  requestCompanyRecruitments();
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
    url: "/company",
    type: "GET",
    dataType: "json",
    data: {
      "company-name": companyInfo.companyName,
    },
    success: function (response) {
      console.log(response);
      CompanyApp.companyDetails = response.data;
      displayStockChart(response.data);
      displayCompanyNews(response.data);
      resizeWordCloud();
    },
    error: function (xhr, status, error) {
      displayEmptyChart();
      console.error(
        "Error fetching data: " + xhr.status + " " + xhr.responseText
      );
    },
  });
};

requestCompanyRecruitments = () => {
  console.log(companyInfo.companyName);
  $.ajax({
    url: "/company/recruitment",
    type: "GET",
    dataType: "json",
    data: {
      "company-name": companyInfo.companyName,
    },
    success: function (response) {
      console.log(response);
      CompanyApp.companyDetails["company_recruitments"] = response.data;
      displayRecruits(response.company_recruitments);
    },
    error: function (xhr, status, error) {
      console.error(
        "Error fetching data: " + xhr.status + " " + xhr.responseText
      );
      $("#recruit-section").empty();
      var responseObj = JSON.parse(xhr.responseText);
      $("#recruit-section").text(responseObj.message);
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

  const stockDatasets = {
    labels: data.stock_info.transaction_date,
    datasets: [
      {
        label: companyInfo.companyName,
        data: data.stock_info.closing_price,
        borderColor: "purple",
        fill: false,
        tension: 0.1, // 곡선을 얼마나 부드럽게 할지 결정합니다
      },
    ],
  };

  CompanyApp.stockChart = new Chart(ctx, {
    type: "line",
    data: stockDatasets,
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

displayCompanyNews = (data) => {
  if (data.company_news.length > 0) {
    $("#news-list").empty();

    data.company_news.forEach(function (item) {
      for (let news_id in item) {
        const news = item[news_id];
        let posted_at = undefined;
        if (news.posted_at) {
          const date = new Date(news.posted_at);
          posted_at =
            date.toISOString().split("T")[0] +
            " " +
            date.toISOString().split("T")[1].slice(0, 8);
        }

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
          text: posted_at,
          style: "margin-bottom: 10px;",
        }).appendTo($anchor);

        $("<p></p>", {
          text: news.news_text,
        }).appendTo($anchor);

        $("#news-list").append($anchor);
      }
    });
  }
};

displayRecruits = (data) => {
  data.forEach(function (recruitment, index) {
    const $anchor = $("<a></a>", {
      class: "card",
      href: recruitment.recruitment_url,
      target: "_blank",
      style: "text-decoration: none",
    });

    // Create and append the h1 element for the title
    $("<h1></h1>", {
      text: recruitment.recruitment_title,
    }).appendTo($anchor);

    // Replace these placeholder texts with the actual data if available
    due_date = recruitment.due_date ? recruitment.due_date : "상시채용";
    $("<p></p>", {
      text: recruitment.career + "  " + recruitment.education + "  " + due_date,
      style: "margin-bottom: 10px;",
    }).appendTo($anchor);

    $("<p></p>", {
      text: recruitment.job_names.join(", "),
      style: "margin-bottom: 10px;",
    }).appendTo($anchor);

    $("<p></p>", {
      text: recruitment.skill_names.join(", "),
    }).appendTo($anchor);

    // Append the completed anchor element to the main div container
    $("#recruit-section").append($anchor);
  });
};

$(window).resize(resizeWordCloud);
