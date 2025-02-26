document.addEventListener("DOMContentLoaded", function () {
    let searchLat = null;
    let searchLng = null;
    var map = L.map("map").setView([28.6330, 77.2190], 13); // Set initial view to main location

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var locations = [
        { name: "New Delhi (Main Location)", lat: 28.6330, lng: 77.2190, color: "blue" },
        { name: "Apollo Pharmacy", lat: 28.6201, lng: 77.2150, color: "red" },
        { name: "MedPlus Pharmacy", lat: 28.6215, lng: 77.2255, color: "red" },
        { name: "Guardian Pharmacy", lat: 28.6223, lng: 77.2102, color: "red" },
        { name: "Fortis HealthWorld", lat: 28.6237, lng: 77.2055, color: "red" },
        { name: "Wellness Forever", lat: 28.6245, lng: 77.2300, color: "red" },
        { name: "Sanjivani Pharmacy", lat: 28.6250, lng: 77.2020, color: "red" },
        { name: "Medcity Pharmacy", lat: 28.6267, lng: 77.2170, color: "red" },
        { name: "Cure & Care Pharmacy", lat: 28.6279, lng: 77.2215, color: "red" },
        { name: "Health Plus Pharmacy", lat: 28.6290, lng: 77.2060, color: "red" },
        { name: "Lifeline Pharmacy", lat: 28.6305, lng: 77.2123, color: "red" },
        { name: "Aster Pharmacy", lat: 28.6312, lng: 77.2280, color: "red" },
        { name: "Green Cross Pharmacy", lat: 28.6320, lng: 77.2075, color: "red" },
        { name: "Urban Medicos", lat: 28.6337, lng: 77.2235, color: "red" },
        { name: "Max Pharmacy", lat: 28.6349, lng: 77.2158, color: "red" },
        { name: "Global Health Pharmacy", lat: 28.6358, lng: 77.2005, color: "red" },
        { name: "Reliable Pharmacy", lat: 28.6370, lng: 77.2207, color: "red" },
        { name: "Sun Pharma Store", lat: 28.6385, lng: 77.2250, color: "red" },
        { name: "Healthy Life Pharmacy", lat: 28.6398, lng: 77.2080, color: "red" },
        { name: "Om Sai Pharmacy", lat: 28.6409, lng: 77.2195, color: "red" },
        { name: "SureCare Pharmacy", lat: 28.6423, lng: 77.2050, color: "red" }
    ];

    var blueIcon = L.icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        iconSize: [32, 32]
    });

    var redIcon = L.icon({
        iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
        iconSize: [32, 32]
    });

    var markerGroup = L.featureGroup();
    var mainLocation = locations[0];

    // Function to initially display only the main location
    function displayMainLocation() {
        var marker = L.marker([mainLocation.lat, mainLocation.lng], { icon: blueIcon })
            .bindPopup(mainLocation.name);
        markerGroup.addLayer(marker);
        markerGroup.addTo(map);
    }

    // Function to update the map with all pharmacies
    function updateMap() {
        markerGroup.clearLayers(); // Clear previous markers
        // Add the main location back to the map
        var marker = L.marker([mainLocation.lat, mainLocation.lng], { icon: blueIcon })
            .bindPopup(mainLocation.name);
        markerGroup.addLayer(marker);

        // Add all pharmacies as red markers
        locations.forEach(function (location) {
            if (location.name !== mainLocation.name) { // Exclude the main location
                var marker = L.marker([location.lat, location.lng], { icon: redIcon }).bindPopup(location.name);
                markerGroup.addLayer(marker);
            }
        });
        markerGroup.addTo(map);
        map.fitBounds(markerGroup.getBounds()); // Adjust map view to fit markers
    }

    displayMainLocation(); // Initially display the main location only

    window.searchLocation = function () {
        var searchInput = document.getElementById("searchInput").value.toLowerCase();
    
        var foundLocation = locations.find(loc => loc.name.toLowerCase().includes(searchInput));
    
        if (foundLocation) {
            // Update the main location with the found location
            mainLocation = foundLocation;
    
            // Call the function to update the map (assuming it still exists)
            updateMap();
            searchLat = foundLocation.lat;
            searchLng = foundLocation.lng;
            // Fetch the sorted pharmacy list based on the new location
            fetch(`/list?lat=${foundLocation.lat}&lng=${foundLocation.lng}`)
                .then(response => response.text())
                .then(html => {
                    // Update your page content with the new pharmacy list
                    document.getElementById("pharmacyList").innerHTML = html;
                })
                .catch(error => {
                    console.error("Error fetching pharmacy list:", error);
                });
            // window.location.href = `/list?lat=${mainLocation.lat}&lng=${mainLocation.lng}`;
        } else {
            alert("Location not found!");
        }
    };
    window.redirectToPharmacyList = function() {
        // Redirect to /list with the lat and lng parameters only when this function is called
        if (searchLat !== null && searchLng !== null) {
            window.location.href = `/list?lat=${searchLat}&lng=${searchLng}`;
        } else {
            alert("Please search for a location first!");
        }
    };
});
