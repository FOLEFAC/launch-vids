import csv
import math

def split_csv(input_file, output_prefix, num_parts=100):
    

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    rows_per_part = math.ceil(len(rows) / num_parts)
    for i in range(num_parts):
        start_index = i * rows_per_part
        end_index = min((i + 1) * rows_per_part, len(rows))
        output_file = f"{output_prefix}_{i+1}.csv"

        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            if i>0:
                writer.writerows([['', 'channel']]+rows[start_index:end_index])
            else:
                writer.writerows(rows[start_index:end_index])

if __name__ == "__main__":
    input_file = "overall.csv"#"output_csv/output_part_0.csv"#
    output_prefix = "./output_csv/output_part"
    num_parts = 5000

    split_csv(input_file, output_prefix, num_parts)