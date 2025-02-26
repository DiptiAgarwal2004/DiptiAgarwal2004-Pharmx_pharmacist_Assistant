function uploadImage() {
    let formData = new FormData();
    let imageFile = document.getElementById("imageInput").files[0];

    if (!imageFile) {
        alert("Please select an image.");
        return;
    }

    formData.append("image", imageFile);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("uploadedImage").src = "/static/uploads/" + imageFile.name;
        document.getElementById("uploadedImage").style.display = "block";

        document.getElementById("name").value = data.name || "";
        document.getElementById("age").value = data.age || "";
        document.getElementById("sex").value = data.sex || "";
        document.getElementById("medical_facility").value = data.medical_facility || "";
        document.getElementById("expire_date").value = data.expire_date || "";
        document.getElementById("contact").value = data.contact || "";
        document.getElementById("weight").value = data.weight || "";
        document.getElementById("doctor_reg").value = data.doctor_reg || "";

        let medicinesContainer = document.getElementById("medicines");
        medicinesContainer.innerHTML = "";

        (data.medicine_names || []).forEach((medicine, index) => {
            let medicineDiv = document.createElement("div");
            medicineDiv.classList.add("medicine-container");

            medicineDiv.innerHTML = `
                <label>Medicine ${index + 1}:</label>
                <input type="text" value="${medicine}" readonly>
                <button onclick="fetchMedicineInfo('${medicine}', ${index})">Info</button>
                <p id="info-${index}"></p>
                <div id="medicineDetailsContainer-${index}"></div>
            `;

            medicinesContainer.appendChild(medicineDiv);
        });
    })
    .catch(error => console.error("Error:", error));
}
function fetchMedicineInfo(medicineName, index) {
    console.log("Requested Medicine Name:", medicineName);

    fetch("/get_medicine_info", {
        method: "POST",
        body: JSON.stringify({ medicine_name: medicineName }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Raw API Response:", data);

        if (!data || typeof data !== "object") {
            console.error("Invalid response format or null data.");
            alert("Error: No valid data received.");
            return;
        }

        if (data.error) {
            console.log(`Error: ${data.error}`);
            alert(`Error: ${data.error}`);
            return;
        }

        // Get the specific container using the dynamic index
        const container = document.getElementById(`medicineDetailsContainer-${index}`);
        if (!container) {
            console.error(`Container medicineDetailsContainer-${index} not found!`);
            return;
        }

        container.innerHTML = ""; // Clear previous results

        // Create a label and input for the medicine name
        // const nameLabel = document.createElement("label");
        // nameLabel.textContent = "Medicine Name:";
        // const nameInput = document.createElement("input");
        // nameInput.type = "text";
        // nameInput.value = data.medicine_name || "Unknown";
        // nameInput.readOnly = true;

        // container.appendChild(nameLabel);
        // container.appendChild(nameInput);
        // container.appendChild(document.createElement("br"));

        // Populate additional details
        // if (data.info && typeof data.info === "object" && Object.keys(data.info).length > 0) {
        //     Object.entries(data.info).forEach(([key, value]) => {
        //         const label = document.createElement("label");
        //         label.textContent = `${key}:`;

        //         const input = document.createElement("input");
        //         input.type = "text";
        //         input.value = value;
        //         input.readOnly = true;

        //         container.appendChild(label);
        //         container.appendChild(input);
        //         container.appendChild(document.createElement("br"));
        //     });
        // } 
        
        if (data.info && typeof data.info === "object" && Object.keys(data.info).length > 0) {
            const medicineWrapper = document.createElement("div");
            medicineWrapper.classList.add("medicine-wrapper");
        
            let row = document.createElement("div");
            row.classList.add("medicine-row");
        
            Object.entries(data.info).forEach(([key, value], index) => {
                const label = document.createElement("label");
                label.textContent = `${key}:`;
                label.classList.add("medicine-label");
        
                const input = document.createElement("input");
                input.type = "text";
                input.value = value;
                input.readOnly = true;
                input.classList.add("medicine-input");
        
                const fieldWrapper = document.createElement("div");
                fieldWrapper.classList.add("medicine-field");
                fieldWrapper.appendChild(label);
                fieldWrapper.appendChild(input);
        
                row.appendChild(fieldWrapper);
        
                // Add first 3 elements in the first row and next 2 in the second row
                if (index === 2 || index === Object.entries(data.info).length - 1) {
                    medicineWrapper.appendChild(row);
                    row = document.createElement("div");
                    row.classList.add("medicine-row");
                }
            });
        
            container.appendChild(medicineWrapper);
        }else {
            container.innerHTML += "<p>No additional info available.</p>";
        }
    })
    .catch(error => {
        console.error("Error fetching medicine info:", error);
        alert("Error fetching medicine info. Please try again.");
    });
}



// function fetchMedicineInfo(medicineName) {
//     console.log("Requested Medicine Name:", medicineName);

//     fetch("/get_medicine_info", {
//         method: "POST",
//         body: JSON.stringify({ medicine_name: medicineName }),
//         headers: { "Content-Type": "application/json" }
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log("Raw API Response:", data);

//         if (!data || typeof data !== "object") {
//             console.error("Invalid response format or null data.");
//             alert("Error: No valid data received.");
//             return;
//         }

//         if (data.error) {
//             console.log(`Error: ${data.error}`)
//             alert(`Error: ${data.error}`);
//             return;
//         }

//         let medicineDetails = `Medicine Name: ${data.medicine_name || "Unknown"}\n\n`;

//         if (data.info && typeof data.info === "object") {
//             medicineDetails += Object.entries(data.info)
//                 .map(([key, value]) => `${key}: ${value}`)
//                 .join("\n");
//         } else {
//             medicineDetails += "No additional info available.";
//         }

//         console.log("Formatted Medicine Details:\n", medicineDetails);
//         alert(`Medicine Details:\n${medicineDetails}`);
//     })
//     .catch(error => {
//         console.error("Error fetching medicine info:", error);
//         alert("Error fetching medicine info. Please try again.");
//     });
// }





