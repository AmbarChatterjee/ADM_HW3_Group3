#!/bin/bash

# Delete merged_courses.tsv if it exists
rm -f merged_courses.tsv

# First take the header from the first file
head -n 1 folderTSV/course_1.tsv > merged_courses.tsv

# Now loop over all the files from 1 to 6000, and append the contents to the merge file.
# We start from file number 2 because we already took the header from file 1.
for i in {2..6000}
do
    # Use awk to print all lines except the first one (which is the header)
    awk 'FNR > 1' folderTSV/course_${i}.tsv >> merged_courses.tsv
done

echo "Which country offers the most Master's Degrees?"
# For country
cut -f11 merged_courses.tsv | sort | uniq -c | sort -nr | awk '{print $2,$3}' | head -n1

echo "Which city?"
# For city
cut -f10 merged_courses.tsv | sort | uniq -c | sort -nr | awk '{print $2}' | head -n1

echo "How many colleges offer Part-Time education?"
# For Part-Time
cut -f4 merged_courses.tsv | grep -i 'Part time' | wc -l 

echo "Print the percentage of courses in Engineering (the word "Engineer" is contained in the course's name)."
# Count total number of lines (subtracting 1 for the header)
total_lines=$(($(wc -l < merged_courses.tsv) - 1))

# Count the number of lines containing the word "Engineer"
engineer_lines=$(cut -f1 merged_courses.tsv | grep -i 'Engineer' | wc -l)

# Calculate the percentage
engineer_percentage=$(awk "BEGIN {print ($engineer_lines / $total_lines) * 100}")
echo "$engineer_percentage%"