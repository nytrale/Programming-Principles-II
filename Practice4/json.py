import json

def load_data(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def collect_rows(data):
    rows = []
    for item in data.get("imdata", []):
        attrs = item.get("l1PhysIf", {}).get("attributes", {})
        dn = attrs.get("dn", "")
        descr = attrs.get("descr", "")
        speed = attrs.get("speed", "")
        mtu = attrs.get("mtu", "")
        rows.append((dn, descr, speed, mtu))
    return rows

def print_table(rows):
    print("Interface Status")
    print("=" * 75)

    dn_w = max(len("DN"), *(len(r[0]) for r in rows)) if rows else len("DN")
    descr_w = max(len("Description"), *(len(r[1]) for r in rows)) if rows else len("Description")
    speed_w = max(len("Speed"), *(len(r[2]) for r in rows)) if rows else len("Speed")
    mtu_w = max(len("MTU"), *(len(str(r[3])) for r in rows)) if rows else len("MTU")

    header = f"{'DN':<{dn_w}}  {'Description':<{descr_w}}  {'Speed':<{speed_w}}  {'MTU':<{mtu_w}}"
    print(header)
    print("-" * (dn_w + descr_w + speed_w + mtu_w + 6))

    for dn, descr, speed, mtu in rows:
        print(f"{dn:<{dn_w}}  {descr:<{descr_w}}  {speed:<{speed_w}}  {mtu:<{mtu_w}}")

def main():
    filename = "sample-data.json"
    data = load_data(filename)
    rows = collect_rows(data)
    print_table(rows)

if __name__ == "__main__":
    main()