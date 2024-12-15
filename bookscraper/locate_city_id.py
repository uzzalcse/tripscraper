import json
import os

# Define file paths
input_file_path = os.path.join("spiders/hotels_combined_data.json")  # Adjust file path
output_file_path = os.path.join("output.json")

# Step 1: Read JSON data from the input file
try:
    with open(input_file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Input file not found: {input_file_path}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

# Step 2: Extract IDs from inboundHotels and outboundHotels
inbound_ids = [hotel["id"] for hotel in json_data.get("inboundHotels", [])]
outbound_ids = [hotel["id"] for hotel in json_data.get("outboundHotels", [])]

# Step 3: Create a new JSON structure with only the extracted IDs
output_data = {
    "inboundCities": inbound_ids,
    "outboundCities": outbound_ids
}

# Step 4: Write the output JSON data to a file
try:
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4)
    print(f"IDs extracted and written to {output_file_path}")
except IOError as e:
    print(f"Error writing to file: {e}")
    exit(1)
