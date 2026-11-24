import csv
import json

import requests

csv_file_path = "./db.csv"


def main():
    request_output = requests.get("https://ringsdb.com/api/public/cards/", {})
    # request_output = requests.get("https://ringsdb.com/api/public/card/01001", {})

    # Maps the table column names to the JSON keys of the request output.
    output_map = {
        "Card Type": "type_name",
        "Sphere": "sphere_name",
        "Name": "name",
        "Traits": "traits",
        "Text": "text",
        # "Flavor Text": "flavor",
        "Unique?": "is_unique",
        "Threat": "threat",
        "Willpower": "willpower",
        "Attack": "attack",
        "Defense": "defense",
        "Health": "health",
        "Card Count": "quantity",
        "Packs": "packs",
    }

    # List of packs to filter by that you own.
    # Pack codes can be found using get_packs.py
    owned_packs = [
        "Core",
        "RevCore",
        "HfG",
        "CatC",
        "JtR",
        "HoEM",
        "TDM",
        "RtM",
        "KD",
        "HoN",
        "TLR",
        "WoE",
        "EfMG",
        "AtE",
        "ToR",
        "BoCD",
        "TDR",
        "TWoR",
        "TWH",
        "RAR",
        "FitN",
        "TGoF",
        "MG",
        "TFoW",
        "TBR",
        "TRD",
        "ToS",
        "LoS",
        "FotW",
        "MoF",
    ]

    output = {key: [] for key in output_map}

    # print(request_output.text)

    for item in request_output.json():
        # print(item["type_name"])
        is_owned = False
        card_count = 0
        packs = ""

        for pack in item["packs"]:
            if pack["pack_code"] in owned_packs:
                is_owned = True
                card_count += int(pack["quantity"])
                packs += f"{pack['pack_name']}, "

        item["quantity"] = card_count
        item["packs"] = packs.strip(", ")

        # Remove the bold from the text field
        item["text"] = (
            item["text"]
            .replace("<b>", " ")
            .replace("</b>", " ")
            .replace("<i>", " ")
            .replace("</i>", " ")
            .replace("  ", " ")
        )

        if is_owned:
            for key, value in output_map.items():
                try:
                    output[key].append(item[value])
                except KeyError as e:
                    output[key].append("N/A")
                    print(f"KeyError: {e} for item {item['name']}")

    # Write the output to a CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output.keys())
        writer.writerows(zip(*output.values()))


if __name__ == "__main__":
    main()
