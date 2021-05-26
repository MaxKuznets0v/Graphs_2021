from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from segmentation import segmentation

list_of_images = ['banana1-gr-320.jpg', 'banana2-gr-320.jpg', 'banana3-gr-320.jpg', 'book-gr-320.jpg', 'bool-gr-320.jpg',
                  'bush-gr-320.jpg', 'ceramic-gr-320.jpg', 'cross-gr-320.jpg', 'doll-gr-320.jpg', 'elefant-gr-320.jpg',
                  'flower-gr-320.jpg', 'fullmoon-gr-320.jpg', 'grave-gr-320.jpg', 'llama-gr-320.jpg', 'memorial-gr-320.jpg',
                  'music-gr-320.jpg', 'person1-gr-320.jpg', 'person2-gr-320.jpg', 'person3-gr-320.jpg', 'person4-gr-320.jpg',
                  'person5-gr-320.jpg', 'person6-gr-320.jpg', 'person7-gr-320.jpg', 'person8-gr-320.jpg', 'scissors-gr-320.jpg',
                  'sheep-gr-320.jpg', 'stone1-gr-320.jpg', 'stone2-gr-320.jpg', 'teddy-gr-320.jpg', 'tennis-gr-320.jpg']
obj_pixels = []
bkg_pixels = []
width_image = 0
height_image = 0

def pick_obj():
    canvas.bind('<Button-1>', click_obj)

def click_obj(event):
    global obj_pixels_str
    x = event.x
    y = event.y
    if x <= width_image and y <= height_image:
        obj_pixels_str = obj_pixels_str + '(' + str(x) + ', ' + str(y) + '), '
        lbl_obj_pixels.configure(text=obj_pixels_str)
        obj_pixels.append([x-1, y-1])

def pick_bkg():
    canvas.bind('<Button-1>', click_bkg)

def click_bkg(event):
    global bkg_pixels_str
    x = event.x
    y = event.y
    if x <= width_image and y <= height_image:
        bkg_pixels_str = bkg_pixels_str + '(' + str(x) + ', ' + str(y) + '), '
        lbl_bkg_pixels.configure(text=bkg_pixels_str)
        bkg_pixels.append([x-1, y-1])

def choose_image():
    # global image
    global width_image, height_image
    lbl_image_name.configure(text=combo_list.get())
    # lbl.grid(row=3, column=1)
    lbl_image_name.pack()
    pilImage = Image.open("images-320\\" + combo_list.get())
    width_image = pilImage.size[0]
    height_image = pilImage.size[1]
    print(width_image, height_image)
    image = ImageTk.PhotoImage(pilImage)
    image_c = canvas.create_image(0, 0, anchor='nw', image=image)
    # # canvas.grid(row=3, column=3)
    canvas.pack()
    # btn_obj = Button(root, text="Выделить объект")
    # btn_bkg = Button(root, text="Выделить фон")
    btn_obj.pack()
    btn_bkg.pack()
    lbl_obj_pixels.pack()
    lbl_bkg_pixels.pack()
    btn_segmentation.pack()
    # canvas.bind('<Button-1>', click)
    panel.configure(image=image)
    panel.image = image
    # panel.pack()


def start_segmentation():
    segmentation(combo_list.get(), obj_pixels, bkg_pixels)


root = Tk()
root.geometry('800x800')
root.title('Сегментация изображения')

# frame = Frame(root)
# frame.grid()

lbl_choose_image = Label(root, text='Выберите изображение:')
# lbl_choose_image.grid(row=1, column=1)
lbl_choose_image.pack()
combo_list = Combobox(root)
combo_list['values'] = list_of_images
# combo_list.grid(row=2, column=1)
combo_list.pack()
btn_choose_image = Button(root, text='Выбрать', command=choose_image)
# btn_choose_image.grid(row=2, column=2)
btn_choose_image.pack()

lbl_image_name = Label(root, text='')
panel = Label(root)
canvas = Canvas(root, height=450, width=320)
obj_pixels_str = "Пиксели объекта: "
bkg_pixels_str = "Пиксели фона: "
btn_obj = Button(root, text="Выделить объект", command=pick_obj)
btn_bkg = Button(root, text="Выделить фон", command=pick_bkg)
lbl_obj_pixels = Label(root, text="Пиксели объекта: ")
lbl_bkg_pixels = Label(root, text="Пиксели фона: ")
btn_segmentation = Button(root, text="Начать сегментацию", command=start_segmentation)

root.mainloop()
