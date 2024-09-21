import time

# define the disks
disk_1b = [10, 13, 10, 2, 15, 23, 19, 3, 2, 3, 27, 20, 11, 27, 10, 19]
disk_2b = [24, 10, 9, 22, 9, 5, 10, 5, 1, 24, 2, 10, 9, 7, 3, 12]
disk_2o = [17, 2, 2, 10, 15, 6, 9, 16]
disk_3b = [14, 5, 5, 7, 8, 24, 8, 3, 6, 15, 22, 6, 1, 1, 11, 27]
disk_3o = [2, 17, 15, 14, 5, 10, 2, 22]
disk_4b = [6, 10, 4, 1, 5, 5, 4, 8, 6, 3, 1, 6, 10, 6, 10, 2]
disk_4o = [3, 3, 6, 10, 10, 10, 6, 13]


# attached disks are:
# disk_2o with disk_3b
# disk_3o with disk_4b


# disk offets from base (range from 0 to 15)
disk_2_offset = 0
disk_3_offset = 0
disk_4_offset = 0


# inflate overlay disks with 0s where there are cutouts
for overlay_list in [disk_2o, disk_3o, disk_4o]:
    index = 8
    while index > 0:
        overlay_list.insert(index, 0)
        index -= 1


# enable logging
LOG_TRIES = False



counter = 0
max_equal = 0

print(f"Looking for combination... (can take up to {16**4} tries)")

start_time = time.time()

# brute-force the combination
for disk_2_offset in range(16):
    for disk_3_offset in range(16):
        for disk_4_offset in range(16):
            segment_sum = 0
            for segment_no in range(16):
                disk_1_value = disk_1b[segment_no]
                disk_2_value = (disk_2b[segment_no] if disk_2o[(segment_no + disk_2_offset) % 16] == 0 else disk_2o[(segment_no + disk_2_offset) % 16])
                disk_3_value = (disk_3b[(segment_no + disk_2_offset) % 16] if disk_3o[(segment_no + disk_3_offset) % 16] == 0 else disk_3o[(segment_no + disk_3_offset) % 16])
                disk_4_value = (disk_4b[(segment_no + disk_3_offset) % 16] if disk_4o[(segment_no + disk_4_offset) % 16] == 0 else disk_4o[(segment_no + disk_4_offset) % 16])

                this_segment_sum = disk_1_value + disk_2_value + disk_3_value + disk_4_value

                if LOG_TRIES:
                    print(f"[{disk_2_offset}, {disk_3_offset}, {disk_4_offset}] Sum of segment {segment_no} with ({disk_1_value}, {disk_2_value}, {disk_3_value}, {disk_4_value}) is {this_segment_sum}")
                counter += 1

                if segment_sum == 0 or this_segment_sum == segment_sum:
                    segment_sum = this_segment_sum
                    if segment_no == 15:
                        if LOG_TRIES:
                            print("\n\n")
                        print(f"FOUND COMBINATION ({counter} tries)")
                        print(f"TOOK {time.time() - start_time} SECONDS!")
                        print("Disk Offset:", (disk_2_offset, disk_3_offset, disk_4_offset), "\n")
                        print("Disk Value Combinations (Segments):")
                        for n in range(16):
                            disk_1_value = disk_1b[n]
                            disk_2_value = (disk_2b[n] if disk_2o[(n + disk_2_offset) % 16] == 0 else disk_2o[(n + disk_2_offset) % 16])
                            disk_3_value = (disk_3b[(n + disk_2_offset) % 16] if disk_3o[(n + disk_3_offset) % 16] == 0 else disk_3o[(n + disk_3_offset) % 16])
                            disk_4_value = (disk_4b[(n + disk_3_offset) % 16] if disk_4o[(n + disk_4_offset) % 16] == 0 else disk_4o[(n + disk_4_offset) % 16])
                            print((disk_1_value, disk_2_value, disk_3_value, disk_4_value))
                        exit()
                    if segment_no > max_equal:
                        max_equal = segment_no
                else:
                    if LOG_TRIES:
                        print(f"[{disk_2_offset}, {disk_3_offset}, {disk_4_offset}] Sum of segment {segment_no} differs. BREAKING")
                    break

print("TRIES:", counter)
print("MAX AMOUNT OF EQUAL SEGMENTS:",max_equal)



