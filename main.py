from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


WATERMARK = "your copyright text"
FONTSIZE = 50
OPACITY = 30
COLOR = (255, 255, 255)


# --------------- FUNCTIONALITY --------------- #
def get_main_img():
    global main_image
    filename = filedialog.askopenfilename(
        initialdir='/',
        title="Upload Main Image",
        filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("png files", "*.png"))
    )

    if filename != "":
        Label(window, text="Main Image Uploaded").grid(row=4, column=0)
        main_image = filename


def get_wtm_img():
    global wtm_image
    filename = filedialog.askopenfilename(
        initialdir='/',
        title="Upload Watermark Image",
        filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("png files", "*.png"))
    )

    if filename != "":
        Label(window, text="Secondary Image Uploaded").grid(row=4, column=1)
        wtm_image = filename


def add_logo(main_img, wtm_img):
    if main_img is not None and wtm_img is not None:
        main = Image.open(main_img)
        wtm = Image.open(wtm_img)
        wtm = wtm.resize((50, 50), Image.ANTIALIAS)
        wtm.putalpha(200)
        main = main.resize(main.size, Image.ANTIALIAS)
        main.paste(wtm, (main.width - 70, main.height - 70), wtm)
        filename = filedialog.asksaveasfilename(title="Save Image", initialdir='/')

        if filename != "":
            main.save(filename, quality=95)
            file_save_label = Label(window, text="Image Saved")
            file_save_label.grid(row=4, column=2)
            print(main.size)


main_image = None
wtm_image = None


def add_wtm_text(main_img):
    if main_image is not None:
        main = Image.open(main_img)
        width, height = main.size

        txt = Image.new('RGBA', main.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        text = watermark_entry.get()
        font = ImageFont.truetype('arial.ttf', 40)
        textwidth, textheight = draw.textsize(text, font)

        # calculate the x,y coordinates of the text
        margin = 15
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 35))
        combined = Image.alpha_composite(main, txt)
        filename = filedialog.asksaveasfilename(title="Save Image", initialdir='/')
        if filename != "":
            combined.save(filename, quality=95)
            file_save_label = Label(window, text="Image Saved")
            file_save_label.grid(row=6, column=2)
            print(main.size)


# --------------- UI --------------- #
window = Tk()
window.title("Imager")
window.config(padx=100, pady=100)
window.iconbitmap("film-editor1.ico")

title_label = Label(window, text="Imager\n Watermark Any Image", font="Arial")
title_label.grid(row=0, column=1, pady=20)

canvas = Canvas(height=250, width=250)
logo_img = PhotoImage(file='film-editor.png')
canvas.create_image(125, 125, image=logo_img)
canvas.grid(row=1, column=1)


# --------------- BUTTONS --------------- #
upload_btn_main = Button(window, text="Get Main Image", command=get_main_img)
upload_btn_main.grid(row=3, column=0, pady=10)

upload_btn_wtm = Button(window, text="Get Logo Image", command=get_wtm_img)
upload_btn_wtm.grid(row=3, column=1)

edit_save_btn = Button(window, text="Edit & Save", command=lambda: add_logo(main_image, wtm_image))
edit_save_btn.grid(row=3, column=2, pady=20)

add_watermark_btn = Button(window, text="Add Text & Save", width=15, command=lambda: add_wtm_text(main_img=main_image))
add_watermark_btn.grid(row=5, column=2, pady=20)

# --------------- ENTRY --------------- #
watermark_entry = Entry(window, bd=0.5, width=35, insertwidth=1)
watermark_entry.grid(row=5, column=1,  pady=20)

window.mainloop()
