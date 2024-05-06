document.addEventListener("DOMContentLoaded", function () {
  const mainContainer = document.getElementById("company-body-section");

  for (let i = 0; i < 10; i++) {
    const lineContainer = document.createElement("div");
    lineContainer.className = "line-container"; // Ensuring unique ID for each line-container
    for (let i = 0; i < 5; i++) {
      const companyContainer = document.createElement("div");
      companyContainer.id = "company-container";
      companyContainer.style.zIndex = "10";
      companyContainer.innerHTML = `
            <div id="company-icon-section"></div>
            <div id="company-content-section">
                <div id="title-article"></div>
                <div id="description-article"></div>
            </div>
        `;
      lineContainer.appendChild(companyContainer);
    }

    mainContainer.appendChild(lineContainer);
  }
});

// document.addEventListener("DOMContentLoaded", function () {
//   const mainContainer = document.getElementById("company-body-section");

//   if (!mainContainer) {
//     console.error("The main container element does not exist!");
//     return;
//   }

//   function createCompanyContainer() {
//     const companyContainer = document.createElement("div");
//     companyContainer.className = "company-container";
//     companyContainer.style.zIndex = "10";
//     companyContainer.innerHTML = `
//           <div class="company-icon-section"></div>
//           <div class="company-content-section">
//               <div class="title-article"></div>
//               <div class="description-article"></div>
//           </div>
//       `;

//     return companyContainer;
//   }

//   for (let i = 0; i < 10; i++) {
//     const lineContainer = document.createElement("div");
//     lineContainer.className = "line-container";
//     lineContainer.style.zIndex = "1";

//     for (let j = 0; j < 5; j++) {
//       lineContainer.appendChild(createCompanyContainer());
//     }

//     mainContainer.appendChild(lineContainer);
//   }
// });
