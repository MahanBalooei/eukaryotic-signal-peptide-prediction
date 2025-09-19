# LB2_project_Group_7
The table of our result

data = [
    ["Category", "Total", "Filtered"],
    ["Positive", "2949", "2932"],
    ["Negative", "20615", "20615"]
]

# Print as Markdown table
print("| " + " | ".join(data[0]) + " |")
print("| " + " | ".join(["---"] * len(data[0])) + " |")
for row in data[1:]:
    print("| " + " | ".join(row) + " |")
