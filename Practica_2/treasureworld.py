from Tkinter import *
import tkMessageBox
from agents import *

class TreasureWorld:
    
    def __init__(self, agent, rows=4, cols=6):
        
        self.agent = agent
        
        self.board = [['carretera' for i in range(cols)] for j in range(rows)]
        self.visible = [[False for i in range(cols)] for j in range(rows)]
        self.visible[0][0] = True
        
        self.casa_position = [3, 3]
        
        self.board[0][4] = 'coronavirus'
        self.board[2][1] = 'coronavirus'
        
        self.rows = rows
        self.cols = cols
        self.width = 250 + 152 * cols
        self.height = 40 + 152 * rows
        
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("LLega a casa sin infectarte de coronavirus!")
        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg='#ffffcc')
        fraidias_image = PhotoImage(file="img/fraidias.gif")
        casa_image = PhotoImage(file="img/casa.gif")
        coronavirus_image = PhotoImage(file="img/coronavirus.gif")
        carretera_image = PhotoImage(file="img/carretera.gif")
        personas_image = PhotoImage(file="img/personas.gif")
        darkness_image = PhotoImage(file="img/darkness.gif")
        self.images = {'fraidias': fraidias_image, 'casa': casa_image, 
                       'coronavirus': coronavirus_image, 'carretera': carretera_image, 
                       'personas': personas_image, 'darkness': darkness_image}
        
        self.b_next = Button(self.window, text="Next Step", command=self.next_step, font=("Helvetica", 20))
        self.b_next.place(x=(20 + 152 * cols + 115), y=200, anchor=CENTER)
        self.l_player = Label(self.window, text="", font=("Helvetica", 20), bg='#ffffcc', fg="blue")
        self.l_player.place(x=(20 + 152 * cols + 115), y=280, anchor=CENTER)
        
        self.canvas.pack()
        self.draw()
        self.window.mainloop()


    def next_step(self):
        personas = self.near_pit(self.agent.x, self.agent.y)
        glitter = [self.agent.x, self.agent.y] == self.casa_position
        percept = (personas, glitter)
        
        self.l_player.config(text='...')
        self.canvas.update()
        action = self.agent.program(percept)
        self.l_player.config(text=action)
        self.canvas.update()

        self.fraidias_position = [self.agent.x, self.agent.y]
        self.visible[self.agent.x][self.agent.y] = True
        self.draw()
        
        if self.board[self.agent.x][self.agent.y] == 'coronavirus':
            self.b_next.config(state=DISABLED)
            self.canvas.update()
            self.canvas.after(500)
            self.agent.x, self.agent.y = -1, -1
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'coronavirus':
                        self.visible[i][j] = True
            self.visible[self.casa_position[0]][self.casa_position[1]] = True
            self.draw()
            tkMessageBox.showerror("GAME OVER", "Has sido infectado por coronavirus...")
            return
        elif ([self.agent.x, self.agent.y] == self.casa_position) and action == 'Grab':
            self.b_next.config(state=DISABLED)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'coronavirus':
                        self.visible[i][j] = True
            self.draw()
            tkMessageBox.showinfo("Has ganado!", "Has llegado a casa sano y salvo!!")
            return
        elif action == 'GetOut':
            self.b_next.config(state=DISABLED)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'coronavirus':
                        self.visible[i][j] = True
            self.visible[self.casa_position[0]][self.casa_position[1]] = True
            self.draw()
            tkMessageBox.showinfo("Fraidias no ha conseguido llegar a casa...")
            return

    def draw(self):
        
        self.canvas.delete(ALL)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x = 20 + 152 * j
                y = 20 + 152 * i 
                if self.visible[i][j]:
                    img = self.images[self.board[i][j]]
                    self.canvas.create_image(x, y, image=img, anchor=NW)
                    if [i, j] == [self.agent.x, self.agent.y]:
                        self.canvas.create_image(x, y, image=self.images['fraidias'], anchor=NW)
                    if self.near_pit(i, j) and self.board[i][j] != 'coronavirus':
                        self.canvas.create_image(x, y, image=self.images['personas'], anchor=NW)
                    if [i, j] == self.casa_position:
                        self.canvas.create_image(x, y, image=self.images['casa'], anchor=NW)
                else:
                    img = self.images['darkness']
                    self.canvas.create_image(x, y, image=img, anchor=NW)
        self.canvas.update()

    def near_pit(self, x, y):
        for (i, j) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= i < self.rows and 0 <= j < self.cols:
                if self.board[i][j] == 'coronavirus':
                    return True
        return False

if __name__ == "__main__":
    rows = 4
    cols = 6
    agent = RandomTreasureAgent(rows, cols)
    #agent = PLTreasureAgent(rows, cols)
    world = TreasureWorld(agent, rows, cols)
    