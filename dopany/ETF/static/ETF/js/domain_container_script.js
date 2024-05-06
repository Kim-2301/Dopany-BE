let currDomainName = "";
let currTimeUnit = "day";

$(document).ready(function () {
  currDomainName = requestETFByTime(currTimeUnit);
  setSelectDomainBtn();
  setSelectTimeBtn();
  requestCompaniesByDomain();
});

setSelectDomainBtn = () => {
  const buttons = document.querySelectorAll(".domain-select-btn");
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      document.querySelector(".dropdown__text").textContent = this.textContent;
      document.getElementById("dropdown").checked = false;
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

setSelectTimeBtn = () => {
  const slider = document.querySelector(".slider");
  const switchContainer = document.querySelector(".switch");

  switchContainer.addEventListener("click", function (event) {
    const switchRect = this.getBoundingClientRect();
    const clickX = event.clientX - switchRect.left; // 클릭 위치 계산
    const switchWidth = switchRect.width;

    if (clickX < switchWidth / 3) {
      slider.style.left = "2px"; // 왼쪽
      slider.textContent = "일";

      requestETFByTime("day");
    } else if (clickX < (2 * switchWidth) / 3) {
      slider.style.left = "30px"; // 중간
      slider.textContent = "주";

      requestETFByTime("week");
    } else {
      slider.style.left = "58px"; // 오른쪽
      slider.textContent = "월";

      requestETFByTime("month");
    }
  });
};

requestETFByTime = (timeUnit) => {
  var domainName = currDomainName; // 도메인 이름 예시로 설정

  $.ajax({
    url: "/app_name?domain-name=" + domainName + "&time-unit=" + timeUnit,
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      displayETFChart(response);
      displayETFDesc(response);
      return data.etf_info[0].etf_name;
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
  const canvas = $("#etf-chart")[0]; // DOM 요소로 접근
  const ctx = canvas.getContext("2d"); // 2D 컨텍스트 가져오기

  const etfDatasets = data.etf_info.map((etf) => {
    return {
      label: etf.etf_name,
      data: etf.closing_price.map((price, index) => ({
        x: etf.transaction_date[index],
        y: parseFloat(price.replace("원", "")),
      })),
      fill: false,
      borderColor: getRandomColor(), // 각 선의 색상을 랜덤으로 생성
      tension: 0.1,
    };
  });

  // 랜덤 색상 생성 함수
  function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  const chart = new Chart(ctx, {
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
      "background-color": index % 2 === 0 ? "#ff6384" : "#ffcd56",
      "margin-right": "5px",
    });
    var itemHTML = $("<li></li>")
      .append(circle)
      .append(etf.etf_name + "   " + etf.etf_major_company.join(", "));
    list.append(itemHTML);
  });
};

requestCompaniesByDomain = () => {
  let domainName = currDomainName;

  $.ajax({
    url: "/app_name?domain-name=" + domainName,
    type: "GET",
    dataType: "json",
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
  const mainContainer = document.getElementById("company-body-section");
  mainContainer.innerHTML = ""; // 기존 내용 초기화

  data.domain_companies_info.forEach((company) => {
    const companyContainer = document.createElement("div");
    companyContainer.className = "company-container";
    companyContainer.style.zIndex = "10";
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
                ${company.company_name}
              </div>
              <div>
                <ul class="company-description-article" style="margin: 0">
                  <li>${company.industry_name}</li>
                  <li>${company.company_sales}</li>
                  <li>${company.company_size}</li>
                </ul>
              </div>
          </div>
      `;

    mainContainer.appendChild(companyContainer);
  });
};

function adjustCardLayout() {
  const screenWidth = window.innerWidth;
  let columns;
  if (screenWidth < 600) {
    columns = 1; // 화면이 좁을 때는 한 행에 한 카드
  } else if (screenWidth < 900) {
    columns = 2; // 중간 크기 화면에서는 한 행에 두 카드
  } else {
    columns = 3; // 더 넓은 화면에서는 한 행에 세 카드
  }
  const mainContainer = document.getElementById("company-body-section");
  mainContainer.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
}

window.addEventListener("resize", adjustCardLayout); // 창 크기 조정 시 레이아웃 조정
adjustCardLayout(); // 페이지 로드 시 레이아웃 초기화
