import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in km

# Example Usage
lat1, lon1 = 28.6139, 77.2090  # New Delhi
lat2, lon2 = 28.6200, 77.2200  # Pharmacy 1

distance = haversine(lat1, lon1, lat2, lon2)
print(f"Distance: {distance:.2f} km")