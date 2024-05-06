document.addEventListener("DOMContentLoaded", function () {
  const mainContainer = document.getElementById("company-grid-section");
  mainContainer.innerHTML = "";

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
  }
});
