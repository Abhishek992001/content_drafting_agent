import csv

def read_recipients(csv_path):
    recipients = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            recipients.append({
                "name": row["name"],
                "email": row["email"],
                "key_points": [
                    kp.strip() for kp in row["key_points"].split(";")
                ]
            })

    return recipients
