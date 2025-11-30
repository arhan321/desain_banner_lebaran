from PIL import Image, ImageDraw, ImageFont
import random

# ================================
# PENGATURAN YANG MUDAH DIUBAH
# ================================

# Ukuran gambar (pixel) – sesuaikan dengan kebutuhan
WIDTH, HEIGHT = 3000, 1000

# Teks utama banner (tetap seperti sebelumnya)
LINE1 = "Kami keluarga Sri Yunari mengucapkan"
LINE2 = "SELAMAT DATANG"
LINE3 = "KELUARGA BESAR"
LINE4 = "R. MARTO WISASTRO"
FOOTER = "HALAL BIHALAL 1447 H / 2026"

# Nama file output
OUTPUT_FILE = "banner_halal_bihalal_sri_yunari_marto_wisastro_rame.png"

# Warna (R, G, B) – nuansa biru emas seperti contoh
TOP_COLOR = (7, 37, 89)        # biru gelap (atas)
BOTTOM_COLOR = (16, 104, 164)  # biru lebih terang (bawah)

TEXT_LIGHT = (255, 249, 233)   # krem hampir putih
GOLD = (230, 190, 80)          # emas
SHADOW = (0, 30, 60)           # bayangan teks

MOSQUE_DARK = (5, 45, 90)      # biru gelap masjid
MOSQUE_MED = (8, 60, 120)
MOSQUE_LIGHT = (15, 80, 150)

STAR_COLOR = (250, 240, 200)
KETUPAT_LIGHT = (144, 227, 84)
KETUPAT_DARK = (61, 153, 59)

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


# def draw_bokeh_and_pattern(draw, width, height):
#     """
#     Bikin pattern halus di background: lingkaran lembut + pattern titik.
#     """
#     # Lingkaran bokeh
#     for _ in range(40):
#         radius = random.randint(40, 120)
#         x = random.randint(-50, width + 50)
#         y = random.randint(-50, int(height * 0.7))
#         opacity = random.randint(20, 60)
#         color = (255, 255, 255, opacity)

#         # Pakai image terpisah dengan alpha agar transparan
#         circle_img = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
#         circle_draw = ImageDraw.Draw(circle_img)
#         circle_draw.ellipse((0, 0, radius * 2, radius * 2), fill=color)
#         draw_image = draw.im  # PIL hack: akses base image
#         draw_image.paste(circle_img, (x - radius, y - radius), circle_img)

#     # Pattern titik kecil di sisi kanan seperti motif islami
#     spacing = 60
#     for y in range(80, height - 200, spacing):
#         for x in range(int(width * 0.6), width - 80, spacing):
#             draw.ellipse(
#                 (x - 3, y - 3, x + 3, y + 3),
#                 fill=(200, 220, 250)
#             )
def draw_bokeh_and_pattern(draw, img, width, height):
    """
    Bikin pattern halus di background: lingkaran lembut + pattern titik.
    """

    # Lingkaran bokeh
    for _ in range(40):
        radius = random.randint(40, 120)
        x = random.randint(-50, width + 50)
        y = random.randint(-50, int(height * 0.7))
        opacity = random.randint(20, 60)
        color = (255, 255, 255, opacity)

        # gunakan layer RGBA transparan
        circle_img = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        circle_draw.ellipse((0, 0, radius * 2, radius * 2), fill=color)

        # tempel ke image utama
        img.paste(circle_img, (x - radius, y - radius), circle_img)

    # Pattern titik kecil
    spacing = 60
    for y2 in range(80, height - 200, spacing):
        for x2 in range(int(width * 0.6), width - 80, spacing):
            draw.ellipse(
                (x2 - 3, y2 - 3, x2 + 3, y2 + 3),
                fill=(200, 220, 250)
            )


def draw_lantern(draw, x, y, size, body_color, glow_color, line_color):
    """
    Gambar lentera sederhana di posisi x, y.
    """
    # tali
    draw.line((x, 0, x, y), fill=line_color, width=4)

    body_width = size * 0.5
    body_height = size * 0.7
    left = x - body_width / 2
    top = y
    right = x + body_width / 2
    bottom = y + body_height

    # badan luar
    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=int(size * 0.18),
        outline=glow_color,
        width=4,
        fill=body_color,
    )

    # jendela dalam
    inner_margin = size * 0.15
    draw.rounded_rectangle(
        (left + inner_margin, top + inner_margin,
         right - inner_margin, bottom - inner_margin),
        radius=int(size * 0.12),
        outline=glow_color,
        width=3,
        fill=None,
    )

    # lingkar glow di bawah
    glow_r = int(size * 0.18)
    gx = x
    gy = bottom + glow_r // 2
    draw.ellipse(
        (gx - glow_r, gy - glow_r, gx + glow_r, gy + glow_r),
        outline=glow_color,
        width=2,
    )


def draw_crescent_moon(draw, cx, cy, radius, color, bg_color):
    """
    Gambar bulan sabit dengan dua lingkaran.
    """
    # lingkaran besar (bulan)
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill=color
    )
    # lingkaran pemotong (warna mendekati langit)
    offset = radius * 0.4
    draw.ellipse(
        (cx - radius + offset, cy - radius,
         cx + radius + offset, cy + radius),
        fill=bg_color
    )

    # bintang dekat bulan
    for dx, dy, r in [(-radius * 1.5, -radius * 0.6, 6),
                      (radius * 1.2, -radius * 0.4, 5),
                      (radius * 0.3, radius * 0.8, 4)]:
        x = cx + dx
        y = cy + dy
        draw.ellipse(
            (x - r, y - r, x + r, y + r),
            fill=STAR_COLOR
        )


def draw_random_stars(draw, width, height, count=80):
    """
    Bintang-bintang kecil di langit.
    """
    for _ in range(count):
        x = random.randint(20, width - 20)
        y = random.randint(20, int(height * 0.5))
        r = random.randint(2, 4)
        draw.ellipse(
            (x - r, y - r, x + r, y + r),
            fill=STAR_COLOR
        )


def draw_ketupat(draw, cx, cy, size, color_light, color_dark):
    """
    Gambar ketupat (wajik) dengan motif diagonal & pita.
    """
    half = size / 2

    # diamond luar
    diamond = [
        (cx, cy - half),
        (cx + half, cy),
        (cx, cy + half),
        (cx - half, cy),
    ]
    draw.polygon(diamond, fill=color_dark)

    # garis kotak diagonal dalam (grid)
    step = size / 4
    for i in range(-2, 3):
        # garis miring kiri-atas ke kanan-bawah
        x1 = cx - size
        y1 = cy + i * step
        x2 = cx + size
        y2 = cy + (i + 4) * step
        draw.line((x1, y1, x2, y2), fill=color_light, width=2)

        # garis miring kanan-atas ke kiri-bawah
        x1b = cx - size
        y1b = cy + (i + 4) * step
        x2b = cx + size
        y2b = cy + i * step
        draw.line((x1b, y1b, x2b, y2b), fill=color_light, width=2)

    # pita bawah (2 helai)
    ribbon_len = size * 0.8
    ribbon_width = size * 0.18

    for offset in (-ribbon_width * 0.8, ribbon_width * 0.8):
        x1 = cx + offset
        y1 = cy + half
        x2 = x1
        y2 = y1 + ribbon_len
        draw.rectangle(
            (x1 - ribbon_width / 2, y1,
             x2 + ribbon_width / 2, y2),
            fill=color_light
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

    # Background gradasi biru
    draw_vertical_gradient(img, TOP_COLOR, BOTTOM_COLOR)

    # Pattern bokeh & motif titik di kanan
    # draw_bokeh_and_pattern(draw, WIDTH, HEIGHT)
    draw_bokeh_and_pattern(draw, img, WIDTH, HEIGHT)


    # Bintang-bintang
    draw_random_stars(draw, WIDTH, HEIGHT, count=70)

    # Bulan sabit di kiri atas
    moon_radius = 90
    draw_crescent_moon(
        draw,
        cx=int(WIDTH * 0.12),
        cy=140,
        radius=moon_radius,
        color=GOLD,
        bg_color=TOP_COLOR,
    )

    # Lentera di kanan atas (2–3 buah)
    lantern_size = 160
    draw_lantern(
        draw,
        int(WIDTH * 0.78),
        80,
        lantern_size,
        body_color=(20, 70, 130),
        glow_color=GOLD,
        line_color=TEXT_LIGHT,
    )
    draw_lantern(
        draw,
        int(WIDTH * 0.90),
        120,
        int(lantern_size * 0.8),
        body_color=(25, 80, 145),
        glow_color=GOLD,
        line_color=TEXT_LIGHT,
    )

    # Garis tali diagonal di pojok kanan atas
    draw.line(
        (int(WIDTH * 0.65), 0, WIDTH - 40, 120),
        fill=TEXT_LIGHT,
        width=3
    )

    # Ketupat di kanan tengah
    ketupat_size = 220
    draw_ketupat(
        draw,
        cx=int(WIDTH * 0.72),
        cy=int(HEIGHT * 0.55),
        size=ketupat_size,
        color_light=KETUPAT_LIGHT,
        color_dark=KETUPAT_DARK,
    )
    draw_ketupat(
        draw,
        cx=int(WIDTH * 0.82),
        cy=int(HEIGHT * 0.47),
        size=int(ketupat_size * 0.75),
        color_light=KETUPAT_LIGHT,
        color_dark=KETUPAT_DARK,
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
    font_bigger = load_font(150, bold=True)

    # Posisi teks dari atas ke bawah (lebih turun sedikit)
    current_y = 170

    # Baris 1: kecil (pembuka)
    h = draw_centered_text(
        draw, LINE1, current_y, font_small,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )
    current_y += h + 40

    # Baris 2: SELAMAT DATANG (paling besar)
    h = draw_centered_text(
        draw, LINE2, current_y, font_bigger,
        WIDTH,
        fill=GOLD,
        shadow_color=SHADOW
    )
    current_y += h + 10

    # Baris 3: KELUARGA BESAR
    h = draw_centered_text(
        draw, LINE3, current_y, font_big,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )
    current_y += h + 10

    # Baris 4: R. MARTO WISASTRO
    h = draw_centered_text(
        draw, LINE4, current_y, font_big,
        WIDTH,
        fill=TEXT_LIGHT,
        shadow_color=SHADOW
    )

    # Footer dekat bagian masjid
    event_y = int(HEIGHT * 0.76)
    draw_centered_text(
        draw, FOOTER, event_y, font_medium,
        WIDTH,
        fill=GOLD,
        shadow_color=SHADOW
    )

    # Simpan gambar
    img.save(OUTPUT_FILE)
    print(f"Banner tersimpan sebagai: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
