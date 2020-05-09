from minesweeper import Application

from yaml import Loader, load

with open('config.yaml', 'r') as f:
	config = load(f, Loader = Loader)
	

app = Application(config['square_size'], config['num_bombs'])
app.mainloop()