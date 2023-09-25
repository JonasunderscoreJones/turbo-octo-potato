def convert_time_to_seconds(time_str):
    # Split the time string into hours, minutes, and seconds
    time_parts = time_str.split(':')
    print(time_parts)
    # Convert each part to an integer
    minutes = int(time_parts[0])
    seconds = int(time_parts[1])

    # Calculate the total time in seconds
    total_seconds = minutes * 60 + seconds

    return total_seconds


input_file = 'data.txt'
total_product = 0

with open(input_file, 'r') as file:
    for line in file:
        line_parts = line.strip().split(':::')
        print(line_parts)

        # Extract the relevant information
        avg_track_length = line_parts[6]
        play_count = int(line_parts[3])

        if avg_track_length == 'NaN:NaN':
            # Use 3 minutes and 30 seconds (3:30) as the default track length
            track_length_seconds = convert_time_to_seconds('0:03:30')
        else:
            # Convert average track length to seconds
            track_length_seconds = convert_time_to_seconds(avg_track_length)

        # Calculate the product and add it to the total
        product = track_length_seconds * play_count
        total_product += product

print(f"Sum of (Average Track Length * Play Count): {total_product}")