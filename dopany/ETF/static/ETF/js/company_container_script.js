document.addEventListener("DOMContentLoaded", function () {
  const mainContainer = document.getElementById("company-grid-section");
  mainContainer.innerHTML = "";

  // for (let i = 0; i < 10; i++) {
  //   const lineContainer = document.createElement("div");
  //   lineContainer.className = "line-container"; // Ensuring unique ID for each line-container
  for (let i = 0; i < 5; i++) {
    const companyContainer = document.createElement("button");
    companyContainer.className = "company-container";
    companyContainer.style.zIndex = "10";
    companyContainer.innerHTML = `
            <div class="company-icon-section">
              <div style="width: 50%;">
                <img src="/static/ETF/images/Dopany.svg" alt="icon SVG" style="max-width: 100%; height: auto;">
              </div>
            </div>
            <div class="company-content-section">
                <div id="company-title-article">
                  회사명
                </div>
                <div>
                  <ul class="company-description-article" style="margin: 0">
                    <li>산업분야</li>
                    <li>매출액</li>
                    <li>규모</li>
                  </ul>
                </div>
            </div>
        `;
    mainContainer.appendChild(companyContainer);
    // }

    // mainContainer.appendChild(lineContainer);
  }
});

// function adjustCardLayout() {
//   const screenWidth = window.innerWidth;
//   let columns;
//   if (screenWidth < 600) {
//     columns = 1; // 화면이 좁을 때는 한 행에 한 카드
//   } else if (screenWidth < 900) {
//     columns = 2; // 중간 크기 화면에서는 한 행에 두 카드
//   } else {
//     columns = 3; // 더 넓은 화면에서는 한 행에 세 카드
//   }
//   const mainContainer = document.getElementById("company-body-section");
//   mainContainer.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
// }

// window.addEventListener("resize", adjustCardLayout); // 창 크기 조정 시 레이아웃 조정
// adjustCardLayout(); // 페이지 로드 시 레이아웃 초기화
