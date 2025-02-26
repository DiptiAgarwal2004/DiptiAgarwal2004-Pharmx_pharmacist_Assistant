function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function () {
        var preview = document.getElementById("preview");
        preview.src = reader.result;
        preview.style.display = "block"; // Show the image
    };
    reader.readAsDataURL(event.target.files[0]);
}

function uploadImage() {
    let fileInput = document.getElementById("imageInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image!");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    // Send request to Flask
    fetch("/predict_tablet", { 
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        let resultDiv = document.getElementById("result");

        if (data.error) {
            resultDiv.innerHTML = `<span style="color: red;">❌ ${data.error}</span>`;
        } else if (data.tablet === "No Tablet detected") {
            resultDiv.innerHTML = `<span style="color: orange;">⚠️ No Tablet detected.</span>`;
        } else {
            resultDiv.innerHTML = `<b>✅ Tablet</b>`;
              document.getElementById("drug").value = data.tablet;
            document.getElementById("confidence").value = `${data.confidence}%`

            // Update preview to display the processed image
            document.getElementById("preview").src = data.image_url;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Check console for details.");
    });
}
