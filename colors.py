import streamlit as st
from PIL import Image, ImageDraw
from colormath.color_objects import LCHabColor, sRGBColor
from colormath.color_conversions import convert_color

# --- FUNKCJE ---
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def lch_to_rgb(l, c, h):
    lch = LCHabColor(l, c, h)
    rgb = convert_color(lch, sRGBColor)
    # Ograniczamy do 0-1 i przeskalowujemy na 0-255
    r = min(max(int(rgb.clamped_rgb_r * 255),0),255)
    g = min(max(int(rgb.clamped_rgb_g * 255),0),255)
    b = min(max(int(rgb.clamped_rgb_b * 255),0),255)
    return (r,g,b)

def generate_lch_grid(hex_color, c_min=10, step_l=5, step_c=5):
    rgb = hex_to_rgb(hex_color)
    lch = convert_color(sRGBColor(*(v/255 for v in rgb)), LCHabColor)
    L0, C0, H0 = lch.lch_l, lch.lch_c, lch.lch_h

    # Przygotowanie siatki
    cols_right = int((100 - L0)/step_l)
    cols_left = int(L0/step_l)
    rows = int((C0 - c_min)/step_c) + 1

    cell_size = 40
    width = (cols_left + cols_right + 1) * cell_size
    height = rows * cell_size

    img = Image.new("RGB", (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(img)

    for r in range(rows):
        C = C0 - r*step_c
        for i in range(-cols_left, cols_right+1):
            L = L0 + i*step_l
            L = max(0, min(100,L))
            color_rgb = lch_to_rgb(L,C,H0)
            x0 = (i+cols_left)*cell_size
            y0 = r*cell_size
            draw.rectangle([x0,y0,x0+cell_size,y0+cell_size], fill=color_rgb)

    return img

# --- STREAMLIT INTERFEJS ---
st.title("Siatka kolorów LCH")
hex_input = st.text_input("Podaj kolor bazowy HEX (np. #FFFF00)", "#FFFF00")
c_min_input = st.number_input("Minimalna saturacja C", min_value=0, max_value=100, value=10, step=5)

if st.button("Generuj siatkę PNG"):
    img = generate_lch_grid(hex_input, c_min=c_min_input)
    st.image(img, caption="Siatka kolorów LCH", use_column_width=True)
    img.save("siatka.png")
    st.success("Gotowe! Plik 'siatka.png' zapisany lokalnie (jeśli używasz Streamlit lokalnie).")
