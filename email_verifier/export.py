from tkinter import filedialog
import json
import csv

def export_results(results):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w') as file:
            if file_path.endswith('.json'):
                json.dump(results, file, indent=4)
            elif file_path.endswith('.csv'):
                writer = csv.writer(file)
                writer.writerow(["Email", "Status"])
                for email in results["valid"]:
                    writer.writerow([email, "Valid"])
                # for email in results["invalid"]:
                #     writer.writerow([email, "Invalid"])
            else:
                for email in results["valid"]:
                    file.write(f"{email}\n")
                # for email in results["invalid"]:
                #     file.write(f"{email}: Invalid\n")
