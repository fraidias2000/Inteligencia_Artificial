from Tkinter import *
import tkMessageBox
from connect4game import Connect4Game, eval_board
from players import MinimaxPlayer, AlphabetaPlayer, RandomPlayer


class Connect4World:

	def __init__(self, rows=6, cols=7, player1=None, player2=None):
		
		self.game = Connect4Game(rows, cols)
		self.player_agents = {'R': player1, 'B': player2}
		self.player_names = {'R': 'RED', 'B': 'BLUE'}
		self.player_colors = {'R': 'red', 'B': 'blue'}
		
		self.rows = rows
		self.cols = cols
		self.width = 40 + 80 * cols
		self.height = 120 + 80 * rows
		
		self.window = Tk()
		self.window.resizable(False, False)
		self.window.title("4 in a line")
		self.canvas = Canvas(self.window, width=self.width, height=self.height, bg='#ffffcc')
		red_image = PhotoImage(file="img/red.gif")
		blue_image = PhotoImage(file="img/blue.gif")
		empty_image = PhotoImage(file="img/empty.gif")
		self.arrow_image = PhotoImage(file="img/arrow.gif")
		self.images = {'R': red_image, 'B': blue_image, ' ': empty_image}
		
		self.buttons = []
		for i in range(self.cols):
			b = Button(self.window, image=self.arrow_image, command=lambda col=i: self.next_action(col))
			b.place(x=20 + 80 * i, y=60, anchor=NW, width=80, height=30)
			self.buttons.append(b)
			
		self.l_turn = Label(self.window, text="Current player: ", font=("Helvetica", 16), bg='#ffffcc')
		self.l_turn.place(x=20, y=20)
		
		self.l_player = Label(self.window, text="", font=("Helvetica", 16), bg='#ffffcc', fg="red")
		self.l_player.place(x=170, y=20)
			
		self.canvas.pack()
		
		current_player = self.current_player_agent()
		if current_player:
			action = current_player.get_next_action(self.game)
			self.next_action(action)
		
		self.draw()
		self.window.mainloop()
		
	def current_player_agent(self):
		return self.player_agents[self.game.current_player]
		
	# NEXT STEP IN THE GAME
	def next_action(self, col):
		
		for b in self.buttons:
			b.config(state=DISABLED)
		self.canvas.update()
		
		row = 0
		while row < self.rows and self.game.board[row][col] == ' ':
			self.game.board[row][col] = self.game.current_player
			if row > 0:
				self.game.board[row - 1][col] = ' '
			self.draw()
			self.canvas.after(40)
			row += 1
			
		if row > 0:
			game_over = self.game.check_win(row - 1, col)
	
			if game_over:
				if self.game.current_player == 'R':
					tkMessageBox.showinfo("Finished!", "RED player won! :)")
					return
				else:
					tkMessageBox.showinfo("Finished!", "BLUE player won! :)")
					return
					
			elif not self.game.possible_actions():
				tkMessageBox.showinfo("Finished!", "There is a draw!")
				return
					
			else:
				
				self.game.next_player()
				self.draw()
				
				current_player = self.current_player_agent()
				if current_player:
					action = current_player.get_next_action(self.game)
					self.next_action(action)
				else:
					for i in range(len(self.buttons)):
						if self.game.board[0][i] == ' ':
							self.buttons[i].config(state=NORMAL)
					self.draw()
		
		
	# DRAWS THE SCENARIO
	def draw(self):
		
		self.canvas.delete(ALL)
		
		player_name = self.player_names[self.game.current_player]
		player_color = self.player_colors[self.game.current_player]
		if self.current_player_agent():
			player_name += " (thinking...)"
		self.l_player.config(text=player_name, fg=player_color)
		
		for i in range(self.rows):
			for j in range(self.cols):
				x = 20 + 80 * j
				y = 100 + 80 * i 
				img = self.images[self.game.board[i][j]]
				self.canvas.create_image(x, y, image=img, anchor=NW)
		self.canvas.update()




# Main program: START THE GAME!

if __name__ == "__main__":
	random_player = RandomPlayer()
	minimax_player = MinimaxPlayer(3)
	alphabeta_player = AlphabetaPlayer(3, eval_board)
	world = Connect4World(6, 7, player1=None,player2=alphabeta_player)
