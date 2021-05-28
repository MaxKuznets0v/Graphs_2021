from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from segmentation import segmentation
from segmentation import add_seeds

list_of_images = ['banana1-gr-320.jpg', 'banana2-gr-320.jpg', 'banana3-gr-320.jpg', 'book-gr-320.jpg', 'bool-gr-320.jpg',
                  'bush-gr-320.jpg', 'ceramic-gr-320.jpg', 'cross-gr-320.jpg', 'doll-gr-320.jpg', 'elefant-gr-320.jpg',
                  'flower-gr-320.jpg', 'fullmoon-gr-320.jpg', 'grave-gr-320.jpg', 'llama-gr-320.jpg', 'memorial-gr-320.jpg',
                  'music-gr-320.jpg', 'person1-gr-320.jpg', 'person2-gr-320.jpg', 'person3-gr-320.jpg', 'person4-gr-320.jpg',
                  'person5-gr-320.jpg', 'person6-gr-320.jpg', 'person7-gr-320.jpg', 'person8-gr-320.jpg', 'scissors-gr-320.jpg',
                  'sheep-gr-320.jpg', 'stone1-gr-320.jpg', 'stone2-gr-320.jpg', 'teddy-gr-320.jpg', 'tennis-gr-320.jpg']
obj_pixels = []
bkg_pixels = []
new_obj_pixels = []
new_bkg_pixels = []
width_image = 0
height_image = 0
# шаг, определяющий количество учитываемых соседей пикселя, на который кликнули
step = 3

def pick_obj():
    canvas.bind('<B1-Motion>', highlight_obj)

def highlight_obj(event):
    x = event.x
    y = event.y
    px_and_neighbours = []
    for i in range(-step, step+1):
        if x - 1 + i >= 0:
            for j in range(-step, step+1):
                if y - 1 + j >= 0:
                    px_and_neighbours.append([x - 1 + i, y - 1 + j])

    if x + step <= width_image and y + step <= height_image:
        for pair in px_and_neighbours:
            obj_pixels.append(pair)
        canvas.create_rectangle(x - 1 - step, y - 1 - step, x - 1 + step, y - 1 + step, fill='red', outline='red', width=0)


def pick_bkg():
    canvas.bind('<B1-Motion>', highlight_bkg)

def highlight_bkg(event):
    x = event.x
    y = event.y
    px_and_neighbours = []
    for i in range(-step, step+1):
        if x - 1 + i >= 0:
            for j in range(-step, step+1):
                if y - 1 + j >= 0:
                    px_and_neighbours.append([x - 1 + i, y - 1 + j])

    if x + step <= width_image and y + step <= height_image:
        for pair in px_and_neighbours:
            bkg_pixels.append(pair)
        canvas.create_rectangle(x - 1 - step, y - 1 - step, x - 1 + step, y - 1 + step, fill='blue', outline='blue', width=0)

def choose_image():
    # global image
    global width_image, height_image
    lbl_image_name.configure(text=combo_list.get())
    lbl_image_name.pack()
    pilImage = Image.open("images-320\\" + combo_list.get())
    width_image = pilImage.size[0]
    height_image = pilImage.size[1]
    canvas.configure(height=height_image, width=width_image)
    image = ImageTk.PhotoImage(pilImage)
    image_c = canvas.create_image(0, 0, anchor='nw', image=image)
    canvas.pack()
    btn_obj.pack()
    btn_bkg.pack()
    btn_segmentation.pack()
    panel.configure(image=image)
    panel.image = image
    # panel.pack()


def open_result(path):
    img_window = Toplevel(root)
    Label(img_window, text='Результат сегментации').pack()
    img_w_image = ImageTk.PhotoImage(Image.open(path))
    img_w_panel = Label(img_window, image=img_w_image)
    img_w_panel.image = img_w_image
    img_w_panel.pack(fill="both", expand="yes")

def start_segmentation():
    unique_obj_pixels = []
    unique_bkg_pixels = []
    for pair in obj_pixels:
        if pair not in unique_obj_pixels:
            unique_obj_pixels.append(pair)
    for pair in bkg_pixels:
        if pair not in unique_bkg_pixels:
            unique_bkg_pixels.append(pair)
    img_path = segmentation(combo_list.get(), unique_obj_pixels, unique_bkg_pixels)
    open_result(img_path)

    btn_obj["state"] = "disabled"
    btn_bkg["state"] = "disabled"
    btn_segmentation["state"] = "disabled"
    btn_add_obj.pack()
    btn_add_bkg.pack()
    btn_add_seeds.pack()


def add_obj_pixels():
    global new_obj_pixels
    new_obj_pixels = []
    canvas.bind('<B1-Motion>', highlight_new_obj)

def highlight_new_obj(event):
    x = event.x
    y = event.y
    px_and_neighbours = []
    for i in range(-step, step+1):
        if x - 1 + i >= 0:
            for j in range(-step, step+1):
                if y - 1 + j >= 0:
                    px_and_neighbours.append([x - 1 + i, y - 1 + j])

    if x + step <= width_image and y + step <= height_image:
        for pair in px_and_neighbours:
            new_obj_pixels.append(pair)
        canvas.create_rectangle(x - 1 - step, y - 1 - step, x - 1 + step, y - 1 + step, fill='red', outline='red', width=0)


def add_bkg_pixels():
    global new_bkg_pixels
    new_bkg_pixels = []
    canvas.bind('<B1-Motion>', highlight_new_bkg)

def highlight_new_bkg(event):
    x = event.x
    y = event.y
    px_and_neighbours = []
    for i in range(-step, step+1):
        if x - 1 + i >= 0:
            for j in range(-step, step+1):
                if y - 1 + j >= 0:
                    px_and_neighbours.append([x - 1 + i, y - 1 + j])

    if x + step <= width_image and y + step <= height_image:
        for pair in px_and_neighbours:
            new_bkg_pixels.append(pair)
        canvas.create_rectangle(x - 1 - step, y - 1 - step, x - 1 + step, y - 1 + step, fill='blue', outline='blue', width=0)

def start_new_segmentation():
    unique_obj_pixels = []
    unique_bkg_pixels = []
    for pair in new_obj_pixels:
        if pair not in unique_obj_pixels:
            unique_obj_pixels.append(pair)
    for pair in new_bkg_pixels:
        if pair not in unique_bkg_pixels:
            unique_bkg_pixels.append(pair)
    img_path = add_seeds(combo_list.get(), unique_obj_pixels, unique_bkg_pixels)
    open_result(img_path)


root = Tk()
root.geometry('500x700')
root.title('Сегментация изображения')

lbl_choose_image = Label(root, text='Выберите изображение:')
lbl_choose_image.pack()
combo_list = Combobox(root)
combo_list['values'] = list_of_images
combo_list.pack()
btn_choose_image = Button(root, text='Выбрать', command=choose_image)
btn_choose_image.pack()

lbl_image_name = Label(root, text='')
panel = Label(root)
canvas = Canvas(root, height=450, width=320)
obj_pixels_str = "Пиксели объекта: "
bkg_pixels_str = "Пиксели фона: "
btn_obj = Button(root, text="Выделить объект", command=pick_obj)
btn_bkg = Button(root, text="Выделить фон", command=pick_bkg)
btn_segmentation = Button(root, text="Начать сегментацию", command=start_segmentation)
btn_add_obj = Button(root, text="Добавить пиксели объекта", command=add_obj_pixels)
btn_add_bkg = Button(root, text="Добавить пиксели фона", command=add_bkg_pixels)
btn_add_seeds = Button(root, text="Скорректировать сегментацию", command=start_new_segmentation)

root.mainloop()
