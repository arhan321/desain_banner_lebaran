from PIL import Image, ImageDraw, ImageFont

# ================================
# PENGATURAN YANG MUDAH DIUBAH
# ================================

# Ukuran gambar (pixel) – sesuaikan dengan kebutuhan
WIDTH, HEIGHT = 3000, 1000

# Teks utama banner
LINE1 = "Kami keluarga Sri Yunari mengucapkan"
LINE2 = "SELAMAT DATANG"
LINE3 = "KELUARGA BESAR"
LINE4 = "R. MARTO WISASTRO"
FOOTER = "HALAL BIHALAL 1447 H / 2026"

# Nama file output
OUTPUT_FILE = "banner_halal_bihalal_sri_yunari_marto_wisastro.png"

# Warna (R, G, B)
TOP_COLOR = (11, 122, 75)       # hijau tua (atas)
BOTTOM_COLOR = (61, 190, 122)   # hijau lebih muda (bawah)
TEXT_LIGHT = (255, 249, 233)    # krem hampir putih
GOLD = (212, 175, 55)           # emas
SHADOW = (0, 60, 40)            # bayangan teks
MOSQUE_DARK = (5, 70, 45)       # hijau gelap masjid
MOSQUE_MED = (4, 90, 55)
MOSQUE_LIGHT = (4, 110, 70)

# ================================
# FUNGSI UTIL
# ================================

def load_font(size, bold=False):
    """
    Coba load font DejaVuSans (biasanya ada di banyak sistem Linux).
    Kalau tidak ada, pakai font default.
    """
    try:
        if bold:
            return ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size
            )
        else:
            return ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size
            )
    except:
        return ImageFont.load_default()


def draw_vertical_gradient(img, top_color, bottom_color):
    """
    Bikin background gradasi vertikal dari top_color ke bottom_color.
    """
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        ratio = y / (height - 1)
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        for x in range(width):
            pixels[x, y] = (r, g, b)


def draw_lantern(draw, x, y, size, text_color, gold_color):
    """
    Gambar lentera sederhana di posisi x, y.
    """
    # tali
    draw.line((x, 0, x, y), fill=text_color, width=4)

    body_width = size * 0.5
    body_height = size * 0.7
    left = x - body_width / 2
    top = y
    right = x + body_width / 2
    bottom = y + body_height

    # badan luar
    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=int(size * 0.15),
        outline=gold_color,
        width=4,
        fill=None,
    )

    # bagian dalam
    inner_margin = size * 0.12
    draw.rounded_rectangle(
        (left + inner_margin, top + inner_margin,
         right - inner_margin, bottom - inner_margin),
        radius=int(size * 0.1),
        outline=text_color,
        width=2,
        fill=None,
    )


def draw_mosque_silhouette(draw, width, height,
                           dark, med, light):
    """
    Gambar siluet masjid di bagian bawah banner.
    """
    base_height = int(height * 0.28)
    base_top = height - base_height

    # lantai panjang
    draw.rectangle(
        (0, base_top + base_height * 0.35, width, height),
        fill=dark
    )

    # bangunan tengah
    center_width = int(width * 0.32)
    center_left = (width - center_width) // 2
    center_top = base_top
    center_right = center_left + center_width
    draw.rectangle(
        (center_left, center_top + base_height * 0.18, center_right, height),
        fill=med
    )

    # kubah utama
    dome_width = int(center_width * 0.9)
    dome_height = int(base_height * 0.55)
    dome_left = (width - dome_width) // 2
    dome_top = center_top - int(dome_height * 0.15)
    dome_right = dome_left + dome_width
    dome_bottom = dome_top + dome_height
    draw.ellipse(
        (dome_left, dome_top, dome_right, dome_bottom),
        fill=light
    )

    # menara kiri & kanan
    min_w = int(width * 0.04)
    min_h = int(base_height * 0.9)
    offset = int(width * 0.19)
    for side in (-1, 1):
        cx = width // 2 + side * offset
        min_left = cx - min_w // 2
        min_right = cx + min_w // 2
        min_top = base_top

        # badan menara
        draw.rectangle(
            (min_left, min_top, min_right, min_top + min_h),
            fill=med
        )

        # kubah kecil di atas menara
        top_dome_h = int(min_h * 0.35)
        draw.ellipse(
            (min_left - 5, min_top - top_dome_h // 2,
             min_right + 5, min_top + top_dome_h // 2),
            fill=light
        )


def draw_centered_text(draw, text, y, font,
                       width,
                       fill=(255, 255, 255),
                       shadow_color=(0, 0, 0),
                       shadow_offset=3):
    """
    Gambar teks rata tengah di posisi y, dengan bayangan.
    Return: tinggi teks (untuk bantu ngatur jarak ke bawah).
    Kompatibel dengan Pillow versi baru (pakai textbbox).
    """
    # Hitung bounding box text
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (width - w) // 2

    # bayangan
    if shadow_color is not None and shadow_offset:
        draw.text((x + shadow_offset, y + shadow_offset),
                  text, font=font, fill=shadow_color)

    # teks utama
    draw.text((x, y), text, font=font, fill=fill)
    return h

# ================================
# BAGIAN UTAMA PROGRAM
# ================================

def main():
    # Buat gambar kosong
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Background gradasi hijau
    draw_vertical_gradient(img, TOP_COLOR, BOTTOM_COLOR)

    # Lentera di kiri-kanan atas
    lantern_size = 160
    draw_lantern(
        draw,
        int(WIDTH * 0.12),
        80,
        lantern_size,
        TEXT_LIGHT,
        GOLD
    )
    draw_lantern(
        draw,
        int(WIDTH * 0.88),
        80,
        lantern_size,
        TEXT_LIGHT,
        GOLD
    )

    # Siluet masjid di bawah
    draw_mosque_silhouette(
        draw, WIDTH, HEIGHT,
        MOSQUE_DARK, MOSQUE_MED, MOSQUE_LIGHT
    )

    # Font
    font_small = load_font(60, bold=False)
    font_medium = load_font(90, bold=True)
    font_big = load_font(120, bold=True)
    font_bigger = load_font(140, bold=True)

    # Posisi teks dari atas ke bawah
    current_y = 120

    # Baris 1: kecil (pembuka)
    h = draw_centered_text(
        draw, LINE1, current_y, font_small,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )
    current_y += h + 40

    # Baris 2: SELAMAT DATANG
    h = draw_centered_text(
        draw, LINE2, current_y, font_bigger,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )
    current_y += h + 20

    # Baris 3: KELUARGA BESAR
    h = draw_centered_text(
        draw, LINE3, current_y, font_big,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )
    current_y += h + 20

    # Baris 4: R. MARTO WISASTRO
    h = draw_centered_text(
        draw, LINE4, current_y, font_big,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )

    # Footer dekat bagian masjid
    event_y = int(HEIGHT * 0.7)
    draw_centered_text(
        draw, FOOTER, event_y, font_medium,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )

    # Simpan gambar
    img.save(OUTPUT_FILE)
    print(f"Banner tersimpan sebagai: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
