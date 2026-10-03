import zlib
import struct

INF = 99999

def floyd_warshall(graph):
    v_count = len(graph)
    dist = [row[:] for row in graph]
    history = [(0, [row[:] for row in dist], [])]

    for k in range(v_count):
        updated = []
        for i in range(v_count):
            for j in range(v_count):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    updated.append((i, j))
        history.append((k + 1, [row[:] for row in dist], updated))
    return dist, history

def write_ppm(history, filename="temp.ppm"):
    cell_w, cell_h = 60, 40
    cols = 4
    margin = 25
    total_w = len(history) * (cols * cell_w + margin) + margin
    total_h = cols * cell_h + 80
    
    img = [[[255, 255, 255] for _ in range(total_w)] for _ in range(total_h)]

    for idx, (step, mat, updated) in enumerate(history):
        start_x = margin + idx * (cols * cell_w + margin)
        start_y = 50

        for r in range(cols):
            for c in range(cols):
                is_upd = (r, c) in updated
                is_pivot = (step > 0) and (r == step - 1 or c == step - 1)
                
                bg = [200, 230, 201] if is_upd else ([240, 240, 240] if is_pivot else [255, 255, 255])
                
                for y in range(start_y + r * cell_h, start_y + (r + 1) * cell_h):
                    for x in range(start_x + c * cell_w, start_x + (c + 1) * cell_w):
                        if y == start_y + r * cell_h or x == start_x + c * cell_w:
                            img[y][x] = [180, 180, 180]
                        else:
                            img[y][x] = bg

    with open(filename, "wb") as f:
        f.write(f"P6\n{total_w} {total_h}\n255\n".encode())
        for row in img:
            for pixel in row:
                f.write(bytes(pixel))

def ppm_to_png(ppm_path, png_path):
    with open(ppm_path, "rb") as f:
        _ = f.readline()
        dims = f.readline().decode().strip().split()
        _ = f.readline()
        w, h = int(dims[0]), int(dims[1])
        data = f.read()

    raw_data = bytearray()
    idx = 0
    for _ in range(h):
        raw_data.append(0)
        raw_data.extend(data[idx:idx + w * 3])
        idx += w * 3

    compressed = zlib.compress(raw_data)
    
    def chunk(tag, content):
        return struct.pack(">I", len(content)) + tag + content + struct.pack(">I", zlib.crc32(tag + content) & 0xffffffff)

    png_bytes = b"\x89PNG\r\n\x1a\n"
    png_bytes += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png_bytes += chunk(b"IDAT", compressed)
    png_bytes += chunk(b"IEND", b"")

    with open(png_path, "wb") as f:
        f.write(png_bytes)

if __name__ == "__main__":
    graph = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0]
    ]
    _, history = floyd_warshall(graph)
    write_ppm(history, "temp.ppm")
    ppm_to_png("temp.ppm", "Visualization.png")
    import os
    if os.path.exists("temp.ppm"):
        os.remove("temp.ppm")
    print("[OK] Generated Visualization.png without external libraries.")
