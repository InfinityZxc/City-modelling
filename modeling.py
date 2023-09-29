import tkinter as tk
from tkinter import *
from tokenize import Double
import numpy as np
import math
from queue import Queue
from tkinter.ttk import Combobox
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

def mu_number(n_input, n_limit, type):
   return min(1, n_input/n_limit)

def mu_diversity(t_input, t_threshold, t_limit, type):
   if type == "daily":
      if t_input <= t_threshold: 
         return 1
      elif t_input <= t_limit:
         return 0.5
      else:
         return 0
   elif type == "weekly":
      if t_input <= t_threshold: 
         return min(1, max(1-t_input/(t_threshold*2), 0))
      else:
         return min(1, max(0.5-(t_input-t_threshold)/(t_limit - t_threshold), 0))

def mu_distance(d_input, d_threshold, d_limit, type):
   if type == "daily":
      if d_input <= d_threshold: 
         return min(1, max(1-d_input/(d_threshold*2), 0))
      else:
         return min(1, max(0.5-(d_input-d_threshold)/(d_limit - d_threshold), 0))
   elif type == "weekly":
      return min(1, max(1-d_input/d_limit, 0))
   
def coord_distance(x_1, y_1, x_2, y_2):
   return ((x_1-x_2) ** 2 + (y_1-y_2) ** 2) ** (0.5)

class Application:
   def __init__(self):
      self.root = TkinterDnD.Tk()
      self.root.title('City modelling')

      self.mode = 'hide_params'  # show_params
      self.file_name = None
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
         text="Show parameters",
         command=self.change_mode
      )
      self.button_change_mode.grid(row=1, column=2)

      self.button_read = Button(
         self.frame_enter,
         text="read images",
         command=self.read_data
      )
      self.button_read.grid(row=2, column=2)

      self.button_next = Button(
         self.frame_enter,
         text="next step",
         command=self.next_step
      )
      self.button_next.grid(row=3, column=2)

      self.button_reset = Button(
         self.frame_enter,
         text="reset model",
         command=self.reset_model
      )
      self.button_reset.grid(row=4, column=2)

      self.text1_lb_single = Label(
         self.frame_enter,
         text="City map",
         width=20, height=4
      )
      self.text1_lb_single.grid(row=5, column=1)

      self.file_drop_1_single = Entry(
         self.frame_enter,
         width=30
      )
      self.file_drop_1_single.grid(row=5, column=2)
      self.file_drop_1_single.insert(1, "drop file here")
      self.file_drop_1_single.drop_target_register(DND_FILES)
      self.file_drop_1_single.dnd_bind('<<Drop>>', lambda e: replace_text(self.file_drop_1_single, e))

      self.text_r_x = Label(
         self.frame_enter,
         text="r_x",
         width=20, height=1
      )
      self.text_entry_r_x = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_r_x.insert(1, "3")

      self.text_r_y = Label(
         self.frame_enter,
         text="r_y",
         width=20, height=1
      )
      self.text_entry_r_y = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_r_y.insert(1, "3")

      self.text_N = Label(
         self.frame_enter,
         text="N",
         width=20, height=1
      )
      self.text_entry_N = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_N.insert(1, "5")

      self.build_new_value = BooleanVar()
      self.build_new_check = Checkbutton(
         self.frame_enter,
         text="Build new",
         variable=self.build_new_value
      )

      self.text_width_meters = Label(
         self.frame_enter,
         text="Region width",
         width=20, height=1
      )
      self.text_entry_width_meters = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_width_meters.insert(1, "4246")

      self.text_cluster_size_meters = Label(
         self.frame_enter,
         text="Cluster size",
         width=20, height=1
      )
      self.text_entry_cluster_size_meters = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_cluster_size_meters.insert(1, "200")

      self.text_walking_distance = Label(
         self.frame_enter,
         text="Walking distance",
         width=20, height=1
      )
      self.text_entry_walking_distance = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_walking_distance.insert(1, "400")

      self.text_cycling_distance = Label(
         self.frame_enter,
         text="Cycling distance",
         width=20, height=1
      )
      self.text_entry_cycling_distance = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_cycling_distance.insert(1, "2000")

      self.text_built_eps_mod = Label(
         self.frame_enter,
         text="Built eps",
         width=20, height=1
      )
      self.text_entry_built_eps_mod = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_built_eps_mod.insert(1, "0.01")

      self.text_daily_number_limit = Label(
         self.frame_enter,
         text="Daily number limit",
         width=20, height=1
      )
      self.text_entry_daily_number_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_daily_number_limit.insert(1, "3")

      self.text_weekly_number_limit = Label(
         self.frame_enter,
         text="Weekly number limit",
         width=20, height=1
      )
      self.text_entry_weekly_number_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_weekly_number_limit.insert(1, "15")

      self.text_daily_diversity_threshold = Label(
         self.frame_enter,
         text="Daily diversity threshold",
         width=20, height=1
      )
      self.text_entry_daily_diversity_threshold = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_daily_diversity_threshold.insert(1, "1")

      self.text_daily_diversity_limit = Label(
         self.frame_enter,
         text="Daily diversity limit",
         width=20, height=1
      )
      self.text_entry_daily_diversity_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_daily_diversity_limit.insert(1, "2")

      self.text_weekly_diversity_threshold = Label(
         self.frame_enter,
         text="Weekly diversity threshold",
         width=20, height=1
      )
      self.text_entry_weekly_diversity_threshold = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_weekly_diversity_threshold.insert(1, "8")

      self.text_weekly_diversity_limit = Label(
         self.frame_enter,
         text="Weekly diversity limit",
         width=20, height=1
      )
      self.text_entry_weekly_diversity_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_weekly_diversity_limit.insert(1, "12")

      self.text_daily_distance_threshold = Label(
         self.frame_enter,
         text="Daily distance threshold",
         width=20, height=1
      )
      self.text_entry_daily_distance_threshold = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_daily_distance_threshold.insert(1, "200")

      self.text_daily_distance_limit = Label(
         self.frame_enter,
         text="Daily distance limit",
         width=20, height=1
      )
      self.text_entry_daily_distance_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_daily_distance_limit.insert(1, "600")

      self.text_weekly_distance_limit = Label(
         self.frame_enter,
         text="Weekly distance limit",
         width=20, height=1
      )
      self.text_entry_weekly_distance_limit = Entry(
         self.frame_enter,
         width=10
      )
      self.text_entry_weekly_distance_limit.insert(1, "4000")

      self.canvas = Canvas(
         self.frame_exit,
         bg="white", 
         width=self.width, 
         height=self.height
      )

      self.single_touch_type = IntVar() # 0 - Inspect, 1 - Change, 2 - Add points
      self.single_touch_type.set(0)
      self.Radiobutton_I = Radiobutton(self.frame_enter, text="Inspect cell", variable=self.single_touch_type, value=0)
      self.Radiobutton_C = Radiobutton(self.frame_enter, text="Change cell", variable=self.single_touch_type, value=1)
      self.Radiobutton_A = Radiobutton(self.frame_enter, text="Add points of intrest", variable=self.single_touch_type, value=2)
      self.Radiobutton_I.grid(row=24, column=1)
      self.Radiobutton_C.grid(row=25, column=1)
      self.Radiobutton_A.grid(row=26, column=1)

      self.touch_dropout_list_node = Combobox(
         self.frame_enter,
         values = self.touch_dropout_list_options
      )
      self.touch_dropout_list_node.grid(row=26, column=2)
      
      self.exit_text = tk.Text(
         self.frame_enter,
         height=10,
         width=40,
      )
      self.exit_text.configure(state=tk.DISABLED)
      self.exit_text.grid(row=27, column=2)

      self.show_visible()

      self.root.geometry(str(self.root.winfo_screenwidth()) + 'x' + str(self.root.winfo_screenheight()))
      self.root.mainloop()

   def write_result(self, text):
      self.exit_text.configure(state=tk.NORMAL)
      self.exit_text.delete("1.0", END)
      self.exit_text.insert(tk.END, text)
      self.exit_text.configure(state=tk.DISABLED)

   def gamma(self, x_index, y_index, cluster, type):
      mu_number_res = mu_number(len(cluster["points"]), self.n_limit[type], type)

      point_types = set()
      for point in cluster["points"]:
         point_types.add(point[2])
      mu_diversity_res = mu_diversity(len(point_types), self.t_threshold[type], self.t_limit[type], type)

      x, y = self.coords_rectangle_center(x_index, y_index)
      distance = coord_distance(cluster["center"][0], cluster["center"][1], x, y)
      mu_distance_res = mu_distance(distance, self.d_threshold[type], self.d_limit[type], type)

      res = (((mu_number_res**mu_diversity_res) * mu_distance_res)**(1-mu_distance_res)) * \
      ((1 - (1-mu_number_res**mu_diversity_res) * (1-mu_distance_res))**(mu_distance_res))
      return res

   def phi(self, x, y, type):
      prod = 0
      if len(self.clusters) > 0:
         prod = 1
      for cluster in self.clusters:
         if cluster["type"] == type or type == "both":
            prod = prod * (1 - self.gamma(x, y, cluster, cluster["type"]))
      return 1 - prod

   def road_proximity(self, cell_distance):
      cell_size = (self.width / self.x_grid) * (self.width_meters / self.width)
      if cell_size > 500:
         return min(1, max(0, 1 - (cell_distance - 1)))
      elif cell_size > 200:
         return min(1, max(0, 1 - 0.5 * (cell_distance - 1)))
      elif cell_size > 50:
         return min(1, max(0, 1 - (1/3) * (cell_distance - 1)))
      elif cell_size > 20:
         return min(1, max(0, 1 - 0.25 * (cell_distance - 1)))
      else:
         return min(1, max(0, 1 - 0.2 * (cell_distance - 1)))

   def coords_rectangle_center(self, x_index, y_index):
      pb = self.pixel_buffer
      x = int((x_index+0.5) * self.width / self.x_grid) + pb
      y = int((y_index+0.5) * self.height / self.y_grid) + pb
      return x, y

   def coords_for_rectangle_to_fill(self, x, y, subtract_buffer = True):
      rectangle_x = (x-(self.pixel_buffer if subtract_buffer else 0)) * self.x_grid // self.width
      rectangle_y = (y-(self.pixel_buffer if subtract_buffer else 0)) * self.y_grid // self.height
      return int(rectangle_x), int(rectangle_y)
   
   def change_mode(self):
      if self.mode == 'show_params':
         self.mode = 'hide_params'
      else:
         self.mode = 'show_params'
      self.show_visible()
      self.hide_invisible()

   def show_visible(self):
      if self.mode == 'show_params':
         self.text_r_x.grid(row=6, column=1)
         self.text_entry_r_x.grid(row=6, column=2)
         self.text_r_y.grid(row=7, column=1)
         self.text_entry_r_y.grid(row=7, column=2)
         self.text_N.grid(row=8, column=1)
         self.text_entry_N.grid(row=8, column=2)
         self.build_new_check.grid(row=9, column=2)
         self.text_width_meters.grid(row=10, column=1)
         self.text_entry_width_meters.grid(row=10, column=2)
         self.text_cluster_size_meters.grid(row=11, column=1)
         self.text_entry_cluster_size_meters.grid(row=11, column=2)
         self.text_walking_distance.grid(row=12, column=1)
         self.text_entry_walking_distance.grid(row=12, column=2)
         self.text_cycling_distance.grid(row=13, column=1)
         self.text_entry_cycling_distance.grid(row=13, column=2)
         self.text_built_eps_mod.grid(row=14, column=1)
         self.text_entry_built_eps_mod.grid(row=14, column=2)
         self.text_daily_number_limit.grid(row=15, column=1)
         self.text_entry_daily_number_limit.grid(row=15, column=2)
         self.text_weekly_number_limit.grid(row=16, column=1)
         self.text_entry_weekly_number_limit.grid(row=16, column=2)
         self.text_daily_diversity_threshold.grid(row=17, column=1)
         self.text_entry_daily_diversity_threshold.grid(row=17, column=2)
         self.text_daily_diversity_limit.grid(row=18, column=1)
         self.text_entry_daily_diversity_limit.grid(row=18, column=2)
         self.text_weekly_diversity_threshold.grid(row=19, column=1)
         self.text_entry_weekly_diversity_threshold.grid(row=19, column=2)
         self.text_weekly_diversity_limit.grid(row=20, column=1)
         self.text_entry_weekly_diversity_limit.grid(row=20, column=2)
         self.text_daily_distance_threshold.grid(row=21, column=1)
         self.text_entry_daily_distance_threshold.grid(row=21, column=2)
         self.text_daily_distance_limit.grid(row=22, column=1)
         self.text_entry_daily_distance_limit.grid(row=22, column=2)
         self.text_weekly_distance_limit.grid(row=23, column=1)
         self.text_entry_weekly_distance_limit.grid(row=23, column=2)
   
   def hide_invisible(self):
      if self.mode == 'hide_params':
         self.text_r_x.grid_forget()
         self.text_entry_r_x.grid_forget()
         self.text_r_y.grid_forget()
         self.text_entry_r_y.grid_forget()
         self.text_N.grid_forget()
         self.text_entry_N.grid_forget()
         self.build_new_check.grid_forget()
         self.text_width_meters.grid_forget()
         self.text_entry_width_meters.grid_forget()
         self.text_cluster_size_meters.grid_forget()
         self.text_entry_cluster_size_meters.grid_forget()
         self.text_walking_distance.grid_forget()
         self.text_entry_walking_distance.grid_forget()
         self.text_cycling_distance.grid_forget()
         self.text_entry_cycling_distance.grid_forget()
         self.text_built_eps_mod.grid_forget()
         self.text_entry_built_eps_mod.grid_forget()
         self.text_daily_number_limit.grid_forget()
         self.text_entry_daily_number_limit.grid_forget()
         self.text_weekly_number_limit.grid_forget()
         self.text_entry_weekly_number_limit.grid_forget()
         self.text_daily_diversity_threshold.grid_forget()
         self.text_entry_daily_diversity_threshold.grid_forget()
         self.text_daily_diversity_limit.grid_forget()
         self.text_entry_daily_diversity_limit.grid_forget()
         self.text_weekly_diversity_threshold.grid_forget()
         self.text_entry_weekly_diversity_threshold.grid_forget()
         self.text_weekly_diversity_limit.grid_forget()
         self.text_entry_weekly_diversity_limit.grid_forget()
         self.text_daily_distance_threshold.grid_forget()
         self.text_entry_daily_distance_threshold.grid_forget()
         self.text_daily_distance_limit.grid_forget()
         self.text_entry_daily_distance_limit.grid_forget()
         self.text_weekly_distance_limit.grid_forget()
         self.text_entry_weekly_distance_limit.grid_forget()

   def create_rectangle(self, x_index, y_index, **options):
      if 'alpha' in options:
         pb = self.pixel_buffer
         x = int(x_index * self.width / self.x_grid) + pb
         y = int(y_index * self.height / self.y_grid) + pb
         a = int((x_index+1) * self.width / self.x_grid) + pb
         b = int((y_index+1) * self.height / self.y_grid) + pb
         alpha = int(options.pop('alpha') * 255)
         fill = options.pop('fill')
         fill = self.root.winfo_rgb(fill) + (alpha,)
         self.rectangle_img_list[y_index][x_index][0] = ImageTk.PhotoImage(Image.new('RGBA', (a-x, b-y), fill))
         self.rectangle_img_list[y_index][x_index][1] = self.canvas.create_image(x, y, image=self.rectangle_img_list[y_index][x_index][0], anchor='nw')
         self.canvas.create_rectangle(x, y, a, b, **options)

   def create_circle(self, x, y, color = "red", r = 6, outline = "black"):
      x0 = x - r
      y0 = y - r
      x1 = x + r
      y1 = y + r
      return self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline=outline)
   
   def read_data(self):
      self.file_name = None
      self.init_params()
      self.read_file()
      self.read_params()
      self.have_data = True
      self.next_step()

   def reset_model(self):
      if self.have_data:
         self.init_params()
         self.read_file()
         self.read_params()
         self.next_step()

   def next_step(self):
      self.cancel_inspect()
      self.read_params()
      if self.x_grid * self.r_x * 2 < self.width and self.y_grid * self.r_y * 2 < self.height and self.have_data:
         self.previous_grids.append((self.x_grid, self.y_grid))
         self.x_grid *= self.r_x 
         self.y_grid *= self.r_y

         self.canvas.delete('all')
         self.canvas.grid(row=0, column=0)
         self.scroll_x.grid(row=1, column=0, sticky="ew")
         self.scroll_y.grid(row=0, column=1, sticky="ns")

         self.density = np.array([[[0,0,self.x_grid+self.y_grid] for i in range(self.x_grid)] for j in range(self.y_grid)])
         self.prev_score = self.score
         self.post_res_scores = np.array([[[0,0,0,0,0,0] for i in range(self.x_grid)] for j in range(self.y_grid)])
         self.score = np.array([[[0, 0] for i in range(self.x_grid)] for j in range(self.y_grid)])
         self.built_neighbours = np.array([[[0, 0] for i in range(self.x_grid)] for j in range(self.y_grid)]) # built neighbours, free spaces around built neighbours
         self.score_rules_res = np.array([[{"mean" : 0, "openness" : 0, "daily" : 0, "weekly": 0, "roads" : 0} for i in range(self.x_grid)] for j in range(self.y_grid)])
         self.rectangle_img_list = [[[None, None] for i in range(self.x_grid)] for j in range(self.y_grid)] # image, canvas_id

         self.add_buildings()
         self.add_restrictions()
         self.add_roads()

         self.calc_scores()
         self.calc_post_res_scores()

         self.print_canvas()
   
   def init_params(self):
      self.x_grid = 1
      self.y_grid = 1
      self.r_x = 3
      self.r_y = 3
      self.N_max = 5
      self.N_obs = 0
      self.previous_grids = []
      self.pixel_buffer = 5
      self.width = 1000 
      self.height = 1000
      self.width_meters = 4246
      self.walking_distance = 400
      self.cycling_distance = 2000
      self.cluster_size_meters = 200
      self.cluster_size = 200
      self.built_eps_mod = 0.01
      self.inspected_coords = (-1,-1)
      self.neighbour_type = "Moore" # "Moore" 
      self.fixed_mode = 'single_file'

      self.density = np.array([[[0,0,0,0,0] for i in range(self.x_grid)] for j in range(self.y_grid)])

      self.avaliable_colors = ["red", "green", "blue", "yellow", "brown", "orange", "lime", "gold", "tan", "aquamarine", "turquoise", "plum", "coral", "tomato",
                               "chocolate", "steelblue", "khaki", "limegreen", "sienna"]
      if not self.file_name:
         self.touch_dropout_list_options = []
         self.points_lists_coords = {pos_type : [] for pos_type in self.touch_dropout_list_options}
         self.points_colors = {self.touch_dropout_list_options[i] : self.avaliable_colors[i] for i in range(len(self.touch_dropout_list_options))}
         self.clusters = []

      self.inspected_cell_border = []

      self.n_limit = {"daily" : 3, "weekly" : 15}
      self.t_threshold = {"daily" : 1, "weekly" : 8}
      self.t_limit = {"daily" : 2, "weekly" : 12}
      self.d_threshold = {"daily" : 200, "weekly" : 0}
      self.d_limit = {"daily" : 600, "weekly" : 4000}

      self.score = [[[1,1]]]
      self.score_rules_res = []
      self.built_neighbours = []
      self.post_res_scores = []
      self.add_restrictions_bool = True

   def read_params(self):
      self.r_x = int(self.text_entry_r_x.get())
      self.r_y = int(self.text_entry_r_y.get())
      self.N_max = int(self.text_entry_N.get())

      self.width_meters = int(self.text_entry_width_meters.get())
      self.cluster_size_meters = int(self.text_entry_cluster_size_meters.get())
      self.walking_distance = int(self.text_entry_walking_distance.get())
      self.cycling_distance = int(self.text_entry_cycling_distance.get())
      self.built_eps_mod = float(self.text_entry_built_eps_mod.get())
      self.n_limit["daily"] = int(self.text_entry_daily_number_limit.get())
      self.n_limit["weekly"] = int(self.text_entry_weekly_number_limit.get())
      self.t_threshold["daily"] = int(self.text_entry_daily_diversity_threshold.get())
      self.t_limit["daily"] = int(self.text_entry_daily_diversity_limit.get())
      self.t_threshold["daily"] = int(self.text_entry_weekly_diversity_threshold.get())
      self.t_limit["weekly"] = int(self.text_entry_weekly_diversity_limit.get())
      self.d_threshold["daily"] = int(self.text_entry_daily_distance_threshold.get())
      self.d_limit["daily"] = int(self.text_entry_daily_distance_limit.get())
      self.d_limit["weekly"] = int(self.text_entry_weekly_distance_limit.get())

      m_to_pix_mod = (self.width / self.width_meters)
      self.cluster_size = self.cluster_size_meters * m_to_pix_mod
      self.d_threshold["daily"] = self.d_threshold["daily"] * m_to_pix_mod
      self.d_limit["daily"] = self.d_limit["daily"] * m_to_pix_mod
      self.d_limit["weekly"] = self.d_limit["weekly"] * m_to_pix_mod

   def event_canvas_press(self, event):
      touch_x = self.scroll_x.get()[0]*(self.width+self.pixel_buffer*2) + event.x
      touch_y = self.scroll_y.get()[0]*(self.height+self.pixel_buffer*2) + event.y
      if self.single_touch_type.get() == 2:
         dropout_option = self.touch_dropout_list_node.get()
         if dropout_option != "":
            point_type = dropout_option[-1]
            if point_type == "1" or point_type == "2":
               if dropout_option in self.touch_dropout_list_options:
                  id = self.create_circle(touch_x, touch_y, self.points_colors[dropout_option])
                  self.points_lists_coords[dropout_option].append([touch_x, touch_y, id])
               else:
                  self.touch_dropout_list_options = self.touch_dropout_list_options + [dropout_option]
                  self.touch_dropout_list_node["values"] = self.touch_dropout_list_options
                  self.points_lists_coords[dropout_option] = []
                  self.points_colors[dropout_option] = self.avaliable_colors[min(len(self.points_lists_coords), len(self.avaliable_colors))-1]
                  id = self.create_circle(touch_x, touch_y, self.points_colors[dropout_option])
                  self.points_lists_coords[dropout_option].append([touch_x, touch_y, id])

               if point_type == "1":
                  point_type = "daily"
               elif point_type == "2":
                  point_type = "weekly"
               nearest_cluster = -1
               smallest_dist = self.cluster_size + 1
               for cluster_i in range(len(self.clusters)):
                  cluster_center = self.clusters[cluster_i]["center"]
                  dist_to_cluster = coord_distance(cluster_center[0], cluster_center[1], touch_x, touch_y)
                  if dist_to_cluster <= self.cluster_size and dist_to_cluster < smallest_dist and self.clusters[cluster_i]["type"] == point_type:
                     nearest_cluster = cluster_i
                     smallest_dist = dist_to_cluster
                  
               if nearest_cluster != -1:
                     self.clusters[cluster_i]["points"].append((touch_x, touch_y, dropout_option))
                     new_center_x = 0
                     new_center_y = 0
                     for coords in self.clusters[cluster_i]["points"]:
                        new_center_x = new_center_x + coords[0]
                        new_center_y = new_center_y + coords[1]
                     new_center_x = new_center_x / len(self.clusters[cluster_i]["points"])
                     new_center_y = new_center_y / len(self.clusters[cluster_i]["points"])
                     self.clusters[cluster_i]["center"] = (new_center_x, new_center_y)
               else:
                  self.clusters.append({"center" : (touch_x, touch_y), "points" : [(touch_x, touch_y, dropout_option)], "type" : point_type})
      elif self.single_touch_type.get() == 1:
         rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(touch_x, touch_y)
         if rectangle_x >= 0 and rectangle_x < self.x_grid and rectangle_y >= 0 and rectangle_y < self.y_grid:
            self.score[rectangle_y][rectangle_x][1] = (self.score[rectangle_y][rectangle_x][1] + 1) % 3
            grid_width = self.width / self.x_grid
            grid_height = self.height / self.y_grid
            eps_minimal = grid_height * grid_width / 100
            rectangle_size = grid_height * grid_width
            if self.score[rectangle_y][rectangle_x][1] == 0:
               self.canvas.delete(self.rectangle_img_list[rectangle_y][rectangle_x][1])
               self.rectangle_img_list[rectangle_y][rectangle_x][0] = None
               self.rectangle_img_list[rectangle_y][rectangle_x][1] = None
            elif self.score[rectangle_y][rectangle_x][1] == 1:
               self.canvas.delete(self.rectangle_img_list[rectangle_y][rectangle_x][1])
               if self.density[rectangle_y][rectangle_x][0] > eps_minimal:
                  self.create_rectangle(rectangle_x, rectangle_y, fill="black", 
                                       alpha = 0.25 * self.density[rectangle_y][rectangle_x][0] / rectangle_size + 0.5)
               else:
                  self.create_rectangle(rectangle_x, rectangle_y, fill="green", 
                                     alpha = 0.25 * self.density[rectangle_y][rectangle_x][0] / rectangle_size + 0.5)
            elif self.score[rectangle_y][rectangle_x][1] == 2:
               self.canvas.delete(self.rectangle_img_list[rectangle_y][rectangle_x][1])
               self.rectangle_img_list[rectangle_y][rectangle_x][0] = None
               self.rectangle_img_list[rectangle_y][rectangle_x][1] = None
      elif self.single_touch_type.get() == 0:
         rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(touch_x, touch_y)
         if rectangle_y >= 0 and rectangle_y < self.y_grid and rectangle_x >= 0 and rectangle_x < self.x_grid:
            if self.inspected_coords == (rectangle_x, rectangle_y):
               self.cancel_inspect()
               self.write_post_res_score()
               return
            self.cancel_inspect()
            self.inspected_coords = (rectangle_x, rectangle_y)
            color = "red"
            x_1 = int(rectangle_x * self.width / self.x_grid) + self.pixel_buffer
            y_1 = int(rectangle_y * self.height / self.y_grid) + self.pixel_buffer
            x_2 = int((rectangle_x+1) * self.width / self.x_grid) + self.pixel_buffer
            y_2 = int((rectangle_y+1) * self.height / self.y_grid) + self.pixel_buffer
            self.inspected_cell_border.append(self.canvas.create_line(x_1, y_1, x_1, y_2, fill = color, width = 5))
            self.inspected_cell_border.append(self.canvas.create_line(x_2, y_1, x_2, y_2, fill = color, width = 5))
            self.inspected_cell_border.append(self.canvas.create_line(x_1, y_1, x_2, y_1, fill = color, width = 5))
            self.inspected_cell_border.append(self.canvas.create_line(x_1, y_2, x_2, y_2, fill = color, width = 5))
            res_str = "Mean: " + str(round(self.score_rules_res[rectangle_y][rectangle_x]["mean"], 2)) + "\n" + \
               "Openness: " + str(round(self.score_rules_res[rectangle_y][rectangle_x]["openness"], 2)) + "\n" + \
               "Daily accessibility: " + str(round(self.score_rules_res[rectangle_y][rectangle_x]["daily"], 2)) + "\n" + \
               "Weekly accessibility: " + str(round(self.score_rules_res[rectangle_y][rectangle_x]["weekly"], 2)) + "\n" + \
               "Roads accessibility: " + str(round(self.score_rules_res[rectangle_y][rectangle_x]["roads"], 2)) + "\n"
            self.write_result(res_str)

   def cancel_inspect(self):
      self.inspected_coords = (-1, -1)
      for line in self.inspected_cell_border:
         self.canvas.delete(line)
      self.inspected_cell_border = []

   def read_file(self):
      if self.fixed_mode == 'single_file':
         self.file_name = self.file_drop_1_single.get()
         self.img_single = openImage(self.file_name)

         self.width, self.height = self.img_single.size
         resize_ratio = min((self.root.winfo_screenwidth()-220)/self.width, self.root.winfo_screenheight()/self.height) * 0.85

         if resize_ratio > 1:
            self.img_single = self.img_single.resize([int(resize_ratio * s) for s in self.img_single.size])
            self.width, self.height = self.img_single.size
            self.visible_width, self.visible_height = self.img_single.size
         else:
            resize_ratio = resize_ratio * 2
            self.img_single = self.img_single.resize([int(resize_ratio * s) for s in self.img_single.size])
            self.width, self.height = self.img_single.size
            self.visible_width, self.visible_height = (self.root.winfo_screenwidth()-320) * 0.80, self.root.winfo_screenheight() * 0.80

         pb = self.pixel_buffer * 2
         self.canvas.destroy()
         self.canvas = Canvas(
            self.frame_exit,
            bg="white", width=self.width+pb, height=self.height+pb, scrollregion=(0,0,self.width+pb,self.height+pb)
         )
         self.canvas.bind("<Button-1>", self.event_canvas_press)

         self.scroll_x=Scrollbar(self.frame_exit,orient=HORIZONTAL)
         self.scroll_x.config(command=self.canvas.xview)
         self.scroll_y=Scrollbar(self.frame_exit,orient=VERTICAL)
         self.scroll_y.config(command=self.canvas.yview)
         self.canvas.config(width=self.visible_width+pb,height=self.visible_height+pb)
         self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

         self.img_single_bg = ImageTk.PhotoImage(self.img_single)
         self.img_np_array = np.array(self.img_single.getdata())
         self.img_np_array = np.reshape(self.img_np_array, (self.height, self.width, 4))

   def calc_scores(self):
      grid_width = self.width / self.x_grid
      grid_height = self.height / self.y_grid
      eps = grid_height * grid_width * self.built_eps_mod
      half = grid_height * grid_width / 2
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.density[y][x][0] > eps:
               self.score[y][x][1] = 1
            if self.add_restrictions_bool and self.density[y][x][1] > half and self.density[y][x][1] > self.density[y][x][0]:
               self.score[y][x][1] = 2
      
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            for i in range(-1, 2):
               for j in range(-1, 2):
                  if self.neighbour_type == "Moore":
                     if (i != 0 or j != 0) and y+j >= 0 and y+j < self.y_grid and x+i >= 0 and x+i < self.x_grid:
                        if self.score[y+j][x+i][1] == 1:
                           self.built_neighbours[y][x][0] = self.built_neighbours[y][x][0] + 1
                           for i_2 in range(-1, 2):
                              for j_2 in range(-1, 2):
                                 if (i_2 != 0 or j_2 != 0) and y+j+j_2 >= 0 and y+j+j_2 < self.y_grid and x+i+i_2 >= 0 and x+i+i_2 < self.x_grid:
                                    if self.score[y+j+j_2][x+i+i_2][1] != 1:
                                       self.built_neighbours[y][x][1] = self.built_neighbours[y][x][1] + 1

      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.score[y][x][1] == 0:
               if self.built_neighbours[y][x][0] == 8:
                  self.score[y][x][1] = 2
               if self.neighbour_type == "Moore":
                  for i in range(-1, 2):
                     for j in range(-1, 2):
                        if (i != 0 or j != 0) and y+j >= 0 and y+j < self.y_grid and x+i >= 0 and x+i < self.x_grid:
                           if self.built_neighbours[y+j][x+i][0] == 7:
                              self.score[y][x][1] = 2

      if self.build_new_value.get():
         prev_x_grid = self.previous_grids[-1][0]
         prev_y_grid = self.previous_grids[-1][1]
         for prev_y in range(0, prev_y_grid):
            for prev_x in range(0, prev_x_grid):
               if self.prev_score[prev_y][prev_x][1] == 1:
                  count = 0
                  cand = []
                  for y in range(prev_y * self.r_y, (prev_y+1) * self.r_y):
                     for x in range(prev_x * self.r_x, (prev_x+1) * self.r_x):
                        if self.score[y][x][1] == 1:
                           count += 1
                        elif self.score[y][x][1] == 0:
                           self.score_rules_res[y][x]["openness"] = self.built_neighbours[y][x][1] / 34
                           self.score_rules_res[y][x]["daily"] = self.phi(x, y, "daily")
                           self.score_rules_res[y][x]["weekly"] = self.phi(x, y, "weekly")
                           self.score_rules_res[y][x]["roads"] = self.road_proximity(self.density[y][x][2])
                           self.score_rules_res[y][x]["mean"] = (self.score_rules_res[y][x]["openness"] + self.score_rules_res[y][x]["daily"] + \
                                                               self.score_rules_res[y][x]["weekly"] + self.score_rules_res[y][x]["roads"]) / 4
                           cand.append((self.score_rules_res[y][x]["mean"], (x, y)))
                  cand.sort(reverse = True)
                  for candidate in range(len(cand)):
                     if count >= self.N_max:
                        break
                     x = cand[candidate][1][0]
                     y = cand[candidate][1][1]
                     can_be_built = True
                     for i in range(-1, 2):
                        for j in range(-1, 2):
                           if (i != 0 or j != 0) and y+j >= 0 and y+j < self.y_grid and x+i >= 0 and x+i < self.x_grid:
                              built_count = 0
                              for i_2 in range(-1, 2):
                                 for j_2 in range(-1, 2):
                                    if (i_2 != 0 or j_2 != 0) and y+j+j_2 >= 0 and y+j+j_2 < self.y_grid and x+i+i_2 >= 0 and x+i+i_2 < self.x_grid:
                                       if self.score[y+j+j_2][x+i+i_2][1] == 1:
                                          built_count = built_count + 1
                              self.built_neighbours[y+j][x+i][0] = built_count
                              if self.score[y+j][x+i][1] == 1 and self.built_neighbours[y+j][x+i][0] >= 7:
                                 self.score[y][x][1] = 2
                                 can_be_built = False
                     if can_be_built:
                        count = count + 1
                        self.score[y][x][0] = cand[candidate][0]
                        self.score[y][x][1] = 1

   def calc_post_res_scores(self):
      prev_x_grid = self.previous_grids[-1][0]
      prev_y_grid = self.previous_grids[-1][1]
      self.N_obs = 0
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.score[y][x][1] == 1:
               self.N_obs = self.N_obs + 1
      self.N_obs = self.N_obs/(prev_x_grid*prev_y_grid)

      self.post_res_score_0 = 0
      self.post_res_score_1 = 0
      self.post_res_score_2 = 0
      self.post_res_score_3 = 0
      self.post_res_score_4 = 0
      self.post_res_score_5 = 0

      count_built = 0
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.score[y][x][1] == 1:
               count_built = count_built + 1
               x_cent, y_cent = self.coords_rectangle_center(x, y)

               min_dist = -1
               for dropout_option in self.touch_dropout_list_options:
                  if dropout_option[-1] == "1":
                     for coords in self.points_lists_coords[dropout_option]:
                        distance = coord_distance(x_cent, y_cent, coords[0], coords[1])
                        if distance < min_dist or min_dist == -1:
                           min_dist = distance
               self.post_res_scores[y][x][0] = min_dist * (self.width_meters / self.width)
               self.post_res_score_0 = self.post_res_score_0 + self.post_res_scores[y][x][0]

               min_dist = -1
               for dropout_option in self.touch_dropout_list_options:
                  if dropout_option[-1] == "2":
                     for coords in self.points_lists_coords[dropout_option]:
                        distance = coord_distance(x_cent, y_cent, coords[0], coords[1])
                        if distance < min_dist or min_dist == -1:
                           min_dist = distance
               self.post_res_scores[y][x][1] = min_dist * (self.width_meters / self.width)
               self.post_res_score_1 = self.post_res_score_1 + self.post_res_scores[y][x][1]

               count = 0
               for dropout_option in self.touch_dropout_list_options:
                  if dropout_option[-1] == "1":
                     for coords in self.points_lists_coords[dropout_option]:
                        distance = coord_distance(x_cent, y_cent, coords[0], coords[1])
                        if distance * (self.width_meters / self.width) <= self.walking_distance:
                           count = count + 1
               self.post_res_scores[y][x][2] = count
               self.post_res_score_2 = self.post_res_score_2 + self.post_res_scores[y][x][2]

               count = 0
               for dropout_option in self.touch_dropout_list_options:
                  if dropout_option[-1] == "2":
                     for coords in self.points_lists_coords[dropout_option]:
                        distance = coord_distance(x_cent, y_cent, coords[0], coords[1])
                        if distance * (self.width_meters / self.width) <= self.cycling_distance:
                           count = count + 1
               self.post_res_scores[y][x][3] = count
               self.post_res_score_3 = self.post_res_score_3 + self.post_res_scores[y][x][3]

               self.post_res_scores[y][x][4] = (1 if self.built_neighbours[y][x][0] != 8 else 0)
               self.post_res_score_4 = self.post_res_score_4 + self.post_res_scores[y][x][4]

               self.post_res_scores[y][x][5] = 8 - self.built_neighbours[y][x][0]
               self.post_res_score_5 = self.post_res_score_5 + self.post_res_scores[y][x][5]

      if count_built != 0:
         self.post_res_score_0 = self.post_res_score_0 / count_built
         self.post_res_score_1 = self.post_res_score_1 / count_built
         self.post_res_score_2 = self.post_res_score_2 / count_built
         self.post_res_score_3 = self.post_res_score_3 / count_built
         self.post_res_score_4 = self.post_res_score_4 / count_built
         self.post_res_score_5 = self.post_res_score_5 / count_built

      self.write_post_res_score()

   def write_post_res_score(self):
      res_str = "N observable: " + str(self.N_obs) + "\n" + \
            "Avg daily distance: " + str(round(self.post_res_score_0, 2)) + "\n" + \
            "Avg close daily amount: " + str(round(self.post_res_score_2, 2)) + "\n" + \
            "Avg weekly distance: " + str(round(self.post_res_score_1, 2)) + "\n" + \
            "Avg close weekly amount: " + str(round(self.post_res_score_3, 2)) + "\n" + \
            "Fraction of cells adjacent with adjacent free cells: " + str(round(self.post_res_score_4, 2)) + "\n" + \
            "Avg adjacent free cells: " + str(round(self.post_res_score_5, 2)) + "\n"
      self.write_result(res_str)

   def print_canvas(self):
      pb = self.pixel_buffer
      grid_width = (self.width-self.pixel_buffer) / self.x_grid
      grid_height = (self.height-self.pixel_buffer) / self.y_grid
      eps_minimal = grid_height * grid_width * self.built_eps_mod
      self.canvas.create_image(pb, pb, anchor=NW, image=self.img_single_bg)

      color = "black"
      for i in range(0, self.x_grid+1):
         self.canvas.create_line(int(i * self.width / self.x_grid) + pb, pb, \
                                 int(i * self.width / self.x_grid) + pb, self.height + pb, fill = color)
      for i in range(0, self.y_grid+1):
         self.canvas.create_line(pb, int(i * self.height / self.y_grid) + pb, self.width + pb, \
                                 int(i * self.height / self.y_grid) + pb, fill = color)
         
      rectangle_size = grid_height * grid_width
      
      for y in range(0, self.y_grid):
         for x in range(0, self.x_grid):
            if self.score[y][x][1] == 1:
               if self.density[y][x][0] > eps_minimal:
                  self.create_rectangle(x, y, fill="black", alpha = 0.25 * self.density[y][x][0] / rectangle_size + 0.5)
               else:
                  self.create_rectangle(x, y, fill="green", alpha = 0.25 * self.density[y][x][0] / rectangle_size + 0.5)
                  
      for option in self.touch_dropout_list_options:
         for point in range(len(self.points_lists_coords[option])):
            self.points_lists_coords[option][point][2] = self.create_circle(self.points_lists_coords[option][point][0], 
                                                                            self.points_lists_coords[option][point][1],
                                                                            self.points_colors[option])

   def rgb_distance(self, target, compare, max_dist):
      dist = abs(target[0]-compare[0]) + abs(target[1]-compare[1]) + abs(target[2]-compare[2])
      if dist <= max_dist:
         return True
      else:
         return False

   def add_buildings(self):
      if self.fixed_mode == 'single_file':
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if self.rgb_distance(self.img_np_array[y][x], [150, 150, 150, 255], 0):
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y, False)
                  self.density[rectangle_y][rectangle_x][0] = self.density[rectangle_y][rectangle_x][0] + 1

   def add_restrictions(self):
      if self.fixed_mode == 'single_file':
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if self.rgb_distance(self.img_np_array[y][x], [55, 126, 184, 255], 20):
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y, False)
                  self.density[rectangle_y][rectangle_x][1] = self.density[rectangle_y][rectangle_x][1] + 1

   def add_roads(self):
      if self.fixed_mode == 'single_file':
         queue = Queue()
         for y in range(self.img_np_array.shape[0]):
            for x in range(self.img_np_array.shape[1]):
               if self.rgb_distance(self.img_np_array[y][x], [255, 96, 17, 255], 200):
                  rectangle_x, rectangle_y = self.coords_for_rectangle_to_fill(x, y, False)
                  self.density[rectangle_y][rectangle_x][2] = 0
                  queue.put((rectangle_x, rectangle_y))
         while not queue.empty():
            pos = queue.get()
            rectangle_x, rectangle_y = pos
            for i in range(-1, 2):
               for j in range(-1, 2):
                  rectangle_x_new = pos[0] + i
                  rectangle_y_new = pos[1] + j
                  if (i != 0 or j != 0) and rectangle_x_new >= 0 and rectangle_y_new >= 0 and rectangle_x_new < self.x_grid and rectangle_y_new < self.y_grid:
                     if self.density[rectangle_y][rectangle_x][2] + 1 < self.density[rectangle_y_new][rectangle_x_new][2]:
                        self.density[rectangle_y_new][rectangle_x_new][2] = self.density[rectangle_y][rectangle_x][2] + 1
                        queue.put((rectangle_x_new, rectangle_y_new))
               
stuff = Application()