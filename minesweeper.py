 #!/usr/bin/env python

import tkinter as tk
from functools import partial
from random import shuffle
import sys



class MinefieldButton(tk.Button):
	
	def __init__(self, master, row, col, bomb, **kwargs):
		super().__init__(master, **kwargs)
		
		assert isinstance(row, int)
		assert row >= 0
		self.row = row
		
		assert isinstance(col, int)
		assert col >= 0
		self.col = col

		self.is_bomb = bomb
		self.flagged = False
		self.revealed = False
		
		self.bomb_neighbours = None
		
	def text_to_(self, x):
		self['text'] = str(x)
		
	def set_flagged(self):
		self.text_to_('F')
		self.flagged = True
		self['fg'] = 'red'
	
	def set_unflagged(self):
		self.text_to_('')
		self.flagged = False
		self['fg'] = 'black'
		
	def reset(self):
		self.text_to_('')
		self.revealed = False
		self.set_unflagged()
		
		
		
class Application(tk.Tk):

	def __init__(
			self, 
			square_size,
			num_bombs):
			
		super().__init__()
		
		assert isinstance(square_size, int)
		assert square_size > 0
		self.square_size = square_size
		
		assert isinstance(num_bombs, int)
		assert num_bombs < (square_size)**2 - 1
		self.num_bombs = num_bombs
		
		self.buttons = {}
								
		self.create_content()
		
	def get_bomb_order(self):
		bombs = [True]*self.num_bombs
		empties = [False]*(self.square_size**2-self.num_bombs)
		order = (bombs + empties)
		shuffle(order)
		return order
		
	def create_content(self):
		self.create_dashboard()
		self.create_field()
	
	def create_dashboard(self):
	
		dashboard = tk.Frame(self)
		
		reset_button = tk.Button(
								dashboard,
								text="RESET",
								bg="black",
								fg="white",
								command = partial(self.reset, self.buttons)
							)
							
							
		flag_button = tk.Button(
								dashboard,
								text="Flag",
								fg="black",
								font=('Helvetica', '15'),
								command = self.toggle_flagging
							)
							
		reset_button.grid(row = 0, column = 2, sticky =tk.E)
		flag_button.grid(row = 0, column = 1, pady=10, padx = self.square_size*10)
		
		self.flag_button = flag_button
		
		bomb_counter = tk.Label(dashboard,
								font = ('Helvetica', '15'),
								fg = 'white',
								bg = 'black'
						)
								
		bomb_counter.grid(row = 0, column = 0, sticky = tk.W)
		self.bomb_counter = bomb_counter
		
		
		dashboard.grid(row = 0, column = 0)
		
	def set_flagging(self):
		self.flag_button['text'] = 'Flagging'
		self.flagging = True
		self.flag_button['fg'] = 'red'	
		
	def set_not_flagging(self):
		self.flag_button['text'] = 'Flag'
		self.flagging = False
		self.flag_button['fg'] = 'black'
	
	def toggle_flagging(self):
		if self.flagging:
			self.set_not_flagging()
		else:
			self.set_flagging()
	


	def calculate_all_bomb_neighbours(self):
		for i in range(self.square_size):
			for j in range(self.square_size):
				
				self.buttons[f'{i}-{j}'].bomb_neighbours = self.calculate_bomb_neighbours(self.buttons[f'{i}-{j}'])
					
	
	def set_start_point(self):
		self.bombs = []
		self.bomb_order = self.get_bomb_order()
		self.flags = self.num_bombs
		self.bomb_counter['text'] = f'{self.flags}'
		self.set_not_flagging()
		self.dead = False
	
	def reset(self, buttons):

		self.set_start_point()
		count = 0
		for key, button in buttons.items():
				button.is_bomb = self.bomb_order[count]
				button.reset()
				
				if self.bomb_order[count]:
					self.bombs.append(key)
					
				count += 1
				
		self.calculate_all_bomb_neighbours()

				
	def create_field(self):
		field = tk.Frame(self)
		field.grid(row = 1, column = 0)
		
		
		self.set_start_point()

		count = 0
		for i in range(self.square_size):
			for j in range(self.square_size):
			
				button = MinefieldButton(
							field, i, j, bomb = self.bomb_order[count],
							width = int(80/self.square_size),
							height = int(40/self.square_size),
							text = ''
						)
				
				button['command'] = partial(
										self.clicked_button,
										button
									)
										
				button.grid(row = button.row,
							column = button.col)
							
				self.buttons[f'{i}-{j}'] = button
				
				if self.bomb_order[count]:
					self.bombs.append(f'{i}-{j}')
				count += 1
		
		self.calculate_all_bomb_neighbours()

	def all_to_bombs(self):
		for bomb in self.bombs:
			self.buttons[bomb]['fg'] = 'black'
			self.buttons[bomb].text_to_('X')
		
	def clicked_button(self, button):
		if self.dead:
			pass
		elif button.revealed:
			pass
		
		elif self.flagging:
			if button.flagged:
				button.set_unflagged()
				self.flags += 1
				self.bomb_counter['text'] = self.flags
				
			elif  self.flags > 0:
				button.set_flagged()
				self.flags -= 1
				self.bomb_counter['text'] = self.flags

		elif button.flagged:
			pass

		elif button.is_bomb:
			pass
			button.text_to_('X')
			
			self.dead = True
			self.all_to_bombs()

			
		else:
			self.recursion_level = 0
			self.clear_zeros(button)

			
			
	def calculate_bomb_neighbours(self, cell):
		row = cell.row
		col = cell.col
			
		index = [-1,0,1]
		
		total = 0
		for i in index:
			for j in index:
				if (i == 0) & (j == 0):
					continue

				neighbour = self.buttons.get(f'{i+row}-{j+col}')
				if neighbour:
					if neighbour.is_bomb:
						total += 1
					
		return total	
		
		
	def clear_zeros(self, button):
		self.recursion_level += 1
		button.text_to_(f'{button.bomb_neighbours}')
		button.revealed = True
		
		print(button.bomb_neighbours)
		if button.bomb_neighbours == 0:
			
			row = button.row
			col = button.col
				
			index = [-1,0,1]
			
			total = 0
			for i in index:
				for j in index:
					if (i == 0) & (j == 0):
						continue

					neighbour = self.buttons.get(f'{i+row}-{j+col}')
					
					if neighbour:
						if neighbour.revealed == True:
							continue
						if self.recursion_level < sys.getrecursionlimit():
							self.clear_zeros(neighbour)
						else:
							neighbour.text_to_(f'{neighbour.bomb_neighbours}')
							neighbour.revealed = True
					
		
	
		
