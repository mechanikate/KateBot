import datetime

# tuple corresponds to top, left, right, bottom
TILE_TYPES = {(1,0,1,1): "├", (0,1,1,0): "─", (0,1,1,1): "┬", (0,0,1,1): "┌", (1,0,1,0): "└", (0,0,0,0): " "}

PRETEXTS = {
    "default": [(1,0,1,1), (0,1,1,0), "datetime", (0,0,0,0)],
    "start": [(0,1,1,1), (0,1,1,0), "datetime", (0,0,0,0)],
    "end": [(1,0,1,0), (0,1,1,0), "datetime", (0,0,0,0)]
}
def printt(text, pretext=[(1,0,1,1), (0,1,1,0), "datetime", (0,0,0,0)]):
    TILE_TYPES["datetime"] = f"[{datetime.datetime.now().isoformat()}]"
    print(f"{''.join([TILE_TYPES[char_id] for char_id in pretext])}{text}")


