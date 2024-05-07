var EtfApp = EtfApp || {}; // Namespace

EtfApp.currDomainName = "IT";
EtfApp.currTimeUnit = "day";
EtfApp.etfsGraphColors = {};
EtfApp.etfChart = null;

$(document).ready(function () {
  requestETFByTime("", EtfApp.currTimeUnit);
  document.querySelector(".dropdown__text").textContent = "IT";
  setSelectDomainBtn();
  setSelectTimeBtn();
  requestCompaniesByDomain();
});

setSelectDomainBtn = () => {
  EtfApp.etfsGraphColors = {};

  const buttons = document.querySelectorAll(".domain-select-btn");
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      document.querySelector(".dropdown__text").textContent = this.textContent;
      document.getElementById("dropdown").checked = false;
      EtfApp.currDomainName = this.textContent;
      setSelectDay();
      requestETFByTime(EtfApp.currDomainName, EtfApp.currTimeUnit);
      requestCompaniesByDomain(EtfApp.currDomainName);
    });

    button.onmouseover = function () {
      this.style.backgroundColor = "rgba(255, 255, 255, 0.3)";
    };
    button.onmouseout = function () {
      this.style.backgroundColor = "#f39189";
    };
    button.onmousedown = function () {
      this.style.backgroundColor = "#d3857f";
    };
    button.onmouseup = function () {
      this.style.backgroundColor = "#f39189";
    };
  });
};

setSelectDay = () => {
  const slider = document.querySelector(".slider");
  slider.style.left = "2px"; // 왼쪽
  slider.textContent = "일";

  EtfApp.currTimeUnit = "day";
};

setSelectWeek = () => {
  const slider = document.querySelector(".slider");
  slider.style.left = "30px"; // 중간
  slider.textContent = "주";

  EtfApp.currTimeUnit = "week";
};

setSelectMonth = () => {
  const slider = document.querySelector(".slider");
  slider.style.left = "58px"; // 오른쪽
  slider.textContent = "월";

  EtfApp.currTimeUnit = "month";
};

setSelectTimeBtn = () => {
  const switchContainer = document.querySelector(".switch");

  switchContainer.addEventListener("click", function (event) {
    const switchRect = this.getBoundingClientRect();
    const clickX = event.clientX - switchRect.left; // 클릭 위치 계산
    const switchWidth = switchRect.width;

    if (clickX < switchWidth / 3) {
      setSelectDay();
      requestETFByTime(EtfApp.currDomainName, EtfApp.currTimeUnit);
    } else if (clickX < (2 * switchWidth) / 3) {
      setSelectWeek();
      requestETFByTime(EtfApp.currDomainName, EtfApp.currTimeUnit);
    } else {
      setSelectMonth();
      requestETFByTime(EtfApp.currDomainName, EtfApp.currTimeUnit);
    }
  });
};

requestETFByTime = (domainName, timeUnit) => {
  $.ajax({
    url: "/etf/get_ETF",
    type: "GET",
    dataType: "json",
    data: {
      "domain-name": domainName || "IT",
      "time-unit": timeUnit || "day",
    },
    success: function (response) {
      console.log(response);
      displayETFChart(response);
      displayETFDesc(response);
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
  const canvas = $("#etf-chart")[0]; // DOM 요소로 접근
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

displayETFChart = (data) => {
  const canvas = $("#etf-chart").get(0); // DOM 요소로 접근
  const ctx = canvas.getContext("2d"); // 2D 컨텍스트 가져오기

  if (EtfApp.etfChart) {
    EtfApp.etfChart.destroy();
  }

  const etfDatasets = data.etf_info.map((etf) => {
    console.log(etf);
    return {
      label: etf.etf_name,
      data: etf.closing_price.map((price, index) => ({
        x: etf.transaction_date[index],
        y: price,
      })),
      fill: false,
      borderColor: getRandomColor(etf.etf_name), // 각 선의 색상을 랜덤으로 생성
      tension: 0.1,
    };
  });

  // 랜덤 색상 생성 함수
  function getRandomColor(etf_name) {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    EtfApp.etfsGraphColors[etf_name] = color;
    return color;
  }

  EtfApp.etfChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: etfDatasets,
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            unit: data.time_unit, // 'day', 'week', or 'month'
          },
        },
      },
      maintainAspectRatio: false, // 그래프 비율을 유지
      responsive: true, // 반응형 디자인을 활성화
    },
  });
};

displayETFDesc = (data) => {
  var infoDiv = $("#etf-info");
  infoDiv.empty(); // Clear previous contents

  data.etf_info.forEach(function (etf, index) {
    var circle = $("<span></span>").css({
      display: "inline-block",
      width: "10px",
      height: "10px",
      "border-radius": "50%",
      "background-color": EtfApp.etfsGraphColors[etf.etf_name],
      "margin-right": "5px",
    });
    var itemHTML = $("<li></li>")
      .append(circle)
      .append(etf.etf_name + "   " + etf.etf_major_company.join(", "));
    infoDiv.append(itemHTML);
  });
};

requestCompaniesByDomain = (domainName) => {
  $.ajax({
    url: "/etf/get_company",
    type: "GET",
    dataType: "json",
    data: {
      "domain-name": domainName || "IT",
    },
    success: function (response) {
      displayCompanies(response);
    },
    error: function (xhr, status, error) {
      console.error(
        "Error fetching data: " + xhr.status + " " + xhr.responseText
      );
    },
  });
};

displayCompanies = (data) => {
  const mainContainer = document.getElementById("company-grid-section");
  mainContainer.innerHTML = ""; // 기존 내용 초기화

  data.domain_companies_info.forEach((company) => {
    const companyContainer = document.createElement("div");
    companyContainer.className = "company-container";
    companyContainer.style.zIndex = "10";

    const maxLength = 10; // 최대 길이 설정
    const truncatedName =
      String(company.company_name).length > maxLength
        ? String(company.company_name).substring(0, maxLength) + "..."
        : company.company_name;

    companyContainer.innerHTML = `
          <div class="company-icon-section">
            <div style="width: 50%;">
            <img src="${
              company.company_img_url || "/static/ETF/images/Dopany.svg"
            }" alt="icon SVG" style="max-width: 100%; height: auto;">
            </div>
          </div>
          <div class="company-content-section">
              <div class="company-title-article">
                ${truncatedName}
              </div>
              <div class="company-description-article">
                <ul>
                  <li>${company.industry_name.split(">")[0]}</li>
                  <li>${company.industry_name.split(">")[1]}</li>
                  <li>${company.company_sales ? company.company_sales : ""}</li>
                  <li>${company.company_size ? company.company_size : ""}</li>
                </ul>
              </div>
          </div>
      `;

    mainContainer.appendChild(companyContainer);
  });
};
