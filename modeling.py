import tkinter as tk
import numpy as np

from queue import Queue
from tkinter import *
from PIL import ImageTk
from PIL import Image
from PIL import ImageGrab
from tkinterdnd2 import DND_FILES, TkinterDnD

def replace_text(widget, e):
   widget.delete(0, tk.END)
   widget.insert(0, e.data)

def openImage(name):
   if len(name) > 2 and name[0] != '/':
      name = name[1:len(name)-1]
   return Image.open(name)

class Application:
   def __init__(self):
      self.root = TkinterDnD.Tk()
      self.root.title('City modelling')

      self.mode = 'single_file'  # multi_file
      self.init_params()
      self.have_data = False
      self.save_counter = 0

      self.frame_enter = Frame(
         self.root,
         padx = 10,
         pady = 10,
         width = 200,
         height = 200
      )
      self.frame_enter.pack(anchor = NW, side = LEFT)

      self.frame_exit = Frame(
         self.root,
         padx = 10,
         pady = 1
      )
      self.frame_exit.pack(expand = True, anchor = CENTER, side = LEFT)

      self.button_change_mode = Button(
         self.frame_enter,
         text="change mode",
         command=self.change_mode
      )
      self.button_change_mode.grid(row=1, column=2)

      self.text1_lb_single = Label(
         self.frame_enter,
         text="City map",
         width=20, height=4
      )

      self.file_drop_1_single = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_1_single.insert(1, "drop file here")
      self.file_drop_1_single.drop_target_register(DND_FILES)
      self.file_drop_1_single.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_1_single, e))

      self.text1_lb = Label(
         self.frame_enter,
         text="City development",
         width=20, height=4
      )

      self.text2_lb = Label(
         self.frame_enter,
         text="Restricted areas",
         width=20, height=4
      )

      self.text3_lb = Label(
         self.frame_enter,
         text="Roads",
         width=20, height=4
      )

      self.text4_lb = Label(
         self.frame_enter,
         text="Amenities",
         width=20, height=4
      )

      self.text5_lb = Label(
         self.frame_enter,
         text="Public transport",
         width=20, height=4
      )

      self.file_drop_1 = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_1.insert(1, "drop file here")
      self.file_drop_1.drop_target_register(DND_FILES)
      self.file_drop_1.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_1, e))

      self.file_drop_2 = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_2.insert(1, "drop file here")
      self.file_drop_2.drop_target_register(DND_FILES)
      self.file_drop_2.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_2, e))

      self.file_drop_3 = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_3.insert(1, "drop file here")
      self.file_drop_3.drop_target_register(DND_FILES)
      self.file_drop_3.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_3, e))

      self.file_drop_4 = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_4.insert(1, "drop file here")
      self.file_drop_4.drop_target_register(DND_FILES)
      self.file_drop_4.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_4, e))

      self.file_drop_5 = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_5.insert(1, "drop file here")
      self.file_drop_5.drop_target_register(DND_FILES)
      self.file_drop_5.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_5, e))

      self.text_r_x = Label(
         self.frame_enter,
         text="r_x",
         width=4, height=2
      )
      self.text_r_x.grid(row=7, column=1)

      self.text_entry_r_x = Entry(
         self.frame_enter,
         width=4
      )
      self.text_entry_r_x.grid(row=7, column=2)
      self.text_entry_r_x.insert(1, "3")

      self.text_r_y = Label(
         self.frame_enter,
         text="r_y",
         width=4, height=2
      )
      self.text_r_y.grid(row=8, column=1)

      self.text_entry_r_y = Entry(
         self.frame_enter,
         width=4
      )
      self.text_entry_r_y.grid(row=8, column=2)
      self.text_entry_r_y.insert(1, "3")

      self.text_N = Label(
         self.frame_enter,
         text="N",
         width=4, height=2
      )
      self.text_N.grid(row=9, column=1)

      self.text_entry_N = Entry(
         self.frame_enter,
         width=4
      )
      self.text_entry_N.grid(row=9, column=2)
      self.text_entry_N.insert(1, "5")

      self.button_read = Button(
         self.frame_enter,
         text="read images",
         command=self.read_data
      )
      self.button_read.grid(row=10, column=2)

      self.canvas = Canvas(
         self.frame_exit,
         bg="white", width=self.width, height=self.height
      )

      self.button_next = Button(
         self.frame_enter,
         text="next step",
         command=self.next_step
      )
      self.button_next.grid(row=11, column=2)

      self.show_visible()

      self.root.geometry(str(self.root.winfo_screenwidth()) + 'x' + str(self.root.winfo_screenheight()))
      self.root.mainloop()

   def coords_for_rectangle_to_fill(self, x, y):
      x = x * self.x_grid // self.width
      y = y * self.y_grid // self.height
      return x, y
   
   def change_mode(self):
      if self.mode == 'multi_file':
         self.mode = 'single_file'
      else:
         self.mode = 'multi_file'
      self.show_visible()
      self.hide_invisible()

   def show_visible(self):
      if self.mode == 'multi_file':
         self.text1_lb.grid(row=2, column=1)
         self.text2_lb.grid(row=3, column=1)
         self.text3_lb.grid(row=4, column=1)
         self.text4_lb.grid(row=5, column=1)
         self.text5_lb.grid(row=6, column=1)
         self.file_drop_1.grid(row=2, column=2)
         self.file_drop_2.grid(row=3, column=2)
         self.file_drop_3.grid(row=4, column=2)
         self.file_drop_4.grid(row=5, column=2)
         self.file_drop_5.grid(row=6, column=2)
      else:
         self.text1_lb_single.grid(row=2, column=1)
         self.file_drop_1_single.grid(row=2, column=2)
   
   def hide_invisible(self):
      if self.mode == 'single_file':
         self.text1_lb.grid_forget()
         self.text2_lb.grid_forget()
         self.text3_lb.grid_forget()
         self.text4_lb.grid_forget()
         self.text5_lb.grid_forget()
         self.file_drop_1.grid_forget()
         self.file_drop_2.grid_forget()
         self.file_drop_3.grid_forget()
         self.file_drop_4.grid_forget()
         self.file_drop_5.grid_forget()
      else:
         self.text1_lb_single.grid_forget()
         self.file_drop_1_single.grid_forget()

   def create_rectangle(self,x,y,a,b,**options):
      if 'alpha' in options:
         alpha = int(options.pop('alpha') * 255)
         fill = options.pop('fill')
         fill = self.root.winfo_rgb(fill) + (alpha,)
         image = Image.new('RGBA', (a-x, b-y), fill)
         self.images.append(ImageTk.PhotoImage(image))
         self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')
         self.canvas.create_rectangle(x, y,a,b, **options)
   
   def read_data(self):
      self.fixed_mode = self.mode
      self.init_params()
      self.read_params()
      self.read_file()
      self.have_data = True
      self.next_step()

   def next_step(self):
      self.read_params()
      if self.x_grid * self.r_x * 4 < self.width and self.y_grid * self.r_y * 4 < self.height and self.have_data:
         self.previous_grids.append((self.x_grid, self.y_grid))
         self.x_grid *= self.r_x 
         self.y_grid *= self.r_y

         self.canvas.delete('all')
         self.canvas.grid(row=1, column=1)
         self.images = []

         self.density = np.array([[[0,0,self.x_grid+self.y_grid,self.x_grid+self.y_grid,self.x_grid+self.y_grid] \
                                   for i in range(self.x_grid)] for j in range(self.y_grid)])
         self.prev_score = self.score
         self.score = np.array([[[0, 0] for i in range(self.x_grid)] for j in range(self.y_grid)])

         self.add_buildings()
         self.add_restrictions()
         self.add_roads()
         self.add_amenities()
         self.add_transport()

         self.calc_scores()

         self.print_canvas()
   
   def init_params(self):
      self.x_grid = 1
      self.y_grid = 1
      self.previous_grids = []
      self.pixel_buffer = 5
      self.width = 1000 
      self.height = 1000
      self.density = np.array([[[0,0,0,0,0] for i in range(self.x_grid)] for j in range(self.y_grid)])
      self.images = []
      self.score = [[[1,1]]]
      self.add_restrictions_bool = True
      self.add_roads_bool = True
      self.add_amenities_bool = True
      self.add_transport_bool = True

   def read_params(self):
      self.r_x = int(self.text_entry_r_x.get())
      self.r_y = int(self.text_entry_r_y.get())
      self.N = int(self.text_entry_N.get())

   def read_file(self):
      if self.fixed_mode == 'single_file':
         file_name = self.file_drop_1_single.get()
         self.img_single = openImage(file_name)

         self.width, self.height = self.img_single.size
         resize_ratio = min((self.root.winfo_screenwidth()-220)/self.width, self.root.winfo_screenheight()/self.height) * 0.85
         self.img_single = self.img_single.resize([int(resize_ratio * s) for s in self.img_single.size])
         self.width, self.height = self.img_single.size

         pb = self.pixel_buffer
         self.canvas = Canvas(
            self.frame_exit,
            bg="white", width=self.width+pb, height=self.height+pb
         )

         self.img_single_bg = ImageTk.PhotoImage(self.img_single)
         self.img_np_array = np.array(self.img_single.getdata())
         self.img_np_array = np.reshape(self.img_np_array, (self.height, self.width, 4))
      else:
         file_name = self.file_drop_1.get()
         self.img_housing = openImage(file_name)

         self.width, self.height = self.img_housing.size
         resize_ratio = min((self.root.winfo_screenwidth()-220)/self.width, self.root.winfo_screenheight()/self.height) * 0.85
         self.img_housing = self.img_housing.resize([int(resize_ratio * s) for s in self.img_housing.size])
         self.width, self.height = self.img_housing.size

         pb = self.pixel_buffer
         self.canvas = Canvas(
            self.frame_exit,
            bg="white", width=self.width+pb, height=self.height+pb
         )

         self.img_single_bg = ImageTk.PhotoImage(self.img_single)
         self.img_np_array_housing = np.array(self.img_housing.getdata())
         self.img_np_array_housing = np.reshape(self.img_np_array_housing, (self.height, self.width, 4))

         file_name = self.file_drop_2.get()
         self.img_restrictions = openImage(file_name)
         self.img_restrictions = self.img_restrictions.resize([self.width, self.height])
         self.img_np_array_restrictions = np.array(self.img_restrictions.getdata())
         self.img_np_array_restrictions = np.reshape(self.img_np_array_restrictions, (self.width, self.height, 4))

         file_name = self.file_drop_3.get()
         self.img_roads = openImage(file_name)
         self.img_roads = self.img_roads.resize([self.width, self.height])
         self.img_np_array_roads = np.array(self.img_roads.getdata())
         self.img_np_array_roads = np.reshape(self.img_np_array_roads, (self.width, self.height, 4))

         file_name = self.file_drop_4.get()
         self.img_amenities = openImage(file_name)
         self.img_amenities = self.img_amenities.resize([self.width, self.height])
         self.img_np_array_amenities = np.array(self.img_amenities.getdata())
         self.img_np_array_amenities = np.reshape(self.img_np_array_amenities, (self.width, self.height, 4))

         file_name = self.file_drop_5.get()
         self.img_public_transport = openImage(file_name)
         self.img_public_transport = self.img_public_transport.resize([self.width, self.height])
         self.img_np_array_public_transport = np.array(self.img_public_transport.getdata())
         self.img_np_array_public_transport = np.reshape(self.img_np_array_public_transport, (self.width, self.height, 4))

   def calc_scores(self):
      grid_width = self.width / self.x_grid
      grid_height = self.height / self.y_grid
      eps = grid_height * grid_width / 100
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            for i in range(-2, 2):
               for j in range(-2, 2):
                  if i != 0 or j != 0:
                     if y+j >= 0 and y+j < self.y_grid and x+i >= 0 and x+i < self.x_grid:
                        if self.density[y+j][x+i][0] > eps:
                           self.score[y][x][0] = self.score[y][x][0] + 1
            if self.density[y][x][0] > eps:
               self.score[y][x][0] = self.score[y][x][0] + 1
               self.score[y][x][1] = 1
            if self.add_restrictions_bool and self.density[y][x][1] > eps and self.density[y][x][1] > self.density[y][x][0]:
               self.score[y][x][1] = 2
            if self.add_roads_bool:
               self.score[y][x][0] = 100 * self.score[y][x][0] / (self.density[y][x][2]+1)
            if self.add_amenities_bool:
               self.score[y][x][0] = 50 * self.score[y][x][0] / (self.density[y][x][3]+1)
            if self.add_transport_bool:
               self.score[y][x][0] = 50 * self.score[y][x][0] / (self.density[y][x][4]+1)
      
      prev_x_grid = self.previous_grids[-1][0]
      prev_y_grid = self.previous_grids[-1][1]
      for prev_y in range(0, prev_y_grid):
         for prev_x in range(0, prev_x_grid):
            if self.prev_score[prev_y][prev_x][1] == 1:
               c = 0
               cand = []
               for y in range(prev_y * self.r_y, (prev_y+1) * self.r_y):
                  for x in range(prev_x * self.r_x, (prev_x+1) * self.r_x):
                     if self.score[y][x][1] == 1:
                        c += 1
                     elif self.score[y][x][1] == 0:
                        cand.append((self.score[y][x][0], (x, y)))
               cand.sort(reverse = True)
               for i in range(min(self.N - c, len(cand))):
                  self.score[cand[i][1][1]][cand[i][1][0]][1] = 1
   
   def print_canvas(self):
      pb = self.pixel_buffer
      grid_width = self.width / self.x_grid
      grid_height = self.height / self.y_grid
      eps = grid_height * grid_width / 100
      self.canvas.create_image(pb, pb, anchor=NW, image=self.img_single_bg)

      color = "black"
      for i in range(0, self.x_grid+1):
         self.canvas.create_line(int(i * self.width / self.x_grid) + pb, pb, \
                                 int(i * self.width / self.x_grid) + pb, self.height + pb, fill = color)
      for i in range(0, self.y_grid+1):
         self.canvas.create_line(pb, int(i * self.height / self.y_grid) + pb, self.width + pb, \
                                 int(i * self.height / self.y_grid) + pb, fill = color)
         
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.score[y][x][1] == 1:
               if self.density[y][x][0] > eps:
                  self.create_rectangle(int(x   * self.width / self.x_grid) + pb, int(y     * self.height / self.y_grid) + pb, \
                                       int((x+1) * self.width / self.x_grid) + pb, int((y+1) * self.height / self.y_grid) + pb, \
                                       fill="black", alpha = 0.5)
               else:
                  self.create_rectangle(int(x   * self.width / self.x_grid) + pb, int(y     * self.height / self.y_grid) + pb, \
                                       int((x+1) * self.width / self.x_grid) + pb, int((y+1) * self.height / self.y_grid) + pb, \
                                       fill="green", alpha = 0.5)

   def add_buildings(self):
      if self.fixed_mode == 'single_file':
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if (self.img_np_array[y][x] == [150, 150, 150, 255]).all():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][0] = self.density[rectangle_y][rectangle_x][0] + 1
      else:
         for y in range(self.img_np_array_housing.shape[0]):
            for x in range(self.img_np_array_housing.shape[1]):
               if (self.img_np_array_housing[y][x] != [0, 0, 0, 255]).any():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][0] = self.density[rectangle_y][rectangle_x][0] + 1

   def add_restrictions(self):
      if self.fixed_mode == 'single_file':
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if (self.img_np_array[y][x] == [55, 126, 184, 255]).all():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][1] = self.density[rectangle_y][rectangle_x][1] + 1
      else:
         for y in range(self.img_np_array_restrictions.shape[0]):
            for x in range(self.img_np_array_restrictions.shape[1]):
               if (self.img_np_array_restrictions[y][x] != [0, 0, 0, 255]).any():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][1] = self.density[rectangle_y][rectangle_x][1] + 1

   def add_roads(self):
      if self.fixed_mode == 'single_file':
         queue = Queue()
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if (self.img_np_array[y][x] == [255, 96, 17, 255]).all():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][2] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][2] + 1 < self.density[y][x][2]:
                           self.density[rectangle_y][rectangle_x][2] = self.density[rectangle_y][rectangle_x][2] + 1
                           queue.put((x, y))
      else:
         queue = Queue()
         for y in range(self.img_np_array_roads.shape[0]):
            for x in range(self.img_np_array_roads.shape[1]):
               if (self.img_np_array_roads[y][x] != [0, 0, 0, 255]).any():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][2] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][2] + 1 < self.density[y][x][2]:
                           self.density[rectangle_y][rectangle_x][2] = self.density[rectangle_y][rectangle_x][2] + 1
                           queue.put((x, y))

   def add_amenities(self):
      if self.fixed_mode == 'single_file':
         queue = Queue()
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if (self.img_np_array[y][x] == [77, 175, 74, 255]).all():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][3] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][3] + 1 < self.density[y][x][3]:
                           self.density[rectangle_y][rectangle_x][3] = self.density[rectangle_y][rectangle_x][3] + 1
                           queue.put((x, y))
      else:
         queue = Queue()
         for y in range(self.img_np_array_amenities.shape[0]):
            for x in range(self.img_np_array_amenities.shape[1]):
               if (self.img_np_array_amenities[y][x] != [0, 0, 0, 255]).any():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][3] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][3] + 1 < self.density[y][x][3]:
                           self.density[rectangle_y][rectangle_x][3] = self.density[rectangle_y][rectangle_x][3] + 1
                           queue.put((x, y))

   def add_transport(self):
      if self.fixed_mode == 'single_file':
         queue = Queue()
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if (self.img_np_array[y][x] == [255, 96, 17, 255]).all():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][4] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][4] + 1 < self.density[y][x][4]:
                           self.density[rectangle_y][rectangle_x][4] = self.density[rectangle_y][rectangle_x][4] + 1
                           queue.put((x, y))
      else:
         queue = Queue()
         for y in range(self.img_np_array_public_transport.shape[0]):
            for x in range(self.img_np_array_public_transport.shape[1]):
               if (self.img_np_array_public_transport[y][x] != [0, 0, 0, 255]).any():
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y)
                  self.density[rectangle_y][rectangle_x][4] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            for i in range(-1, 1):
               for j in range(-1, 1):
                  if i != 0 or j != 0:
                     x = pos[0] + i
                     y = pos[1] + j
                     if x >= 0 and y >= 0 and x < self.x_grid and y < self.y_grid:
                        if self.density[rectangle_y][rectangle_x][4] + 1 < self.density[y][x][4]:
                           self.density[rectangle_y][rectangle_x][4] = self.density[rectangle_y][rectangle_x][4] + 1
                           queue.put((x, y))
               
stuff = Application()