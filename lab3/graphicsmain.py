from gamemodel import *
from graphics import *


class GameGraphics:
    def __init__(self, game):
        self.game = game

        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
       
        line = Line(Point(-110,0),Point(110,0)).draw(self.win)
        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]
        

    def drawCanon(self, playerNr):
        player = self.game.getPlayers()[playerNr]
        x = player.getX()
        size = self.game.getCannonSize()
        
        cannon = Rectangle(Point(x - size / 2, 0), Point(x + size / 2, size))
        cannon.setFill(player.getColor())  
        cannon.draw(self.win)
        return cannon


    def drawScore(self,playerNr):
   
        player = self.game.getPlayers()[playerNr]  
        score_text =f"Score: {player.getScore()}"  
        score_position = Point(player.getX(), -4)  

        text = Text(score_position, score_text)
        text.draw(self.win)

        return text
      
    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)

        if self.draw_projs[self.game.getCurrentPlayerNumber()] is not None:  
            self.draw_projs[self.game.getCurrentPlayerNumber()].undraw()

        circle = Circle(Point(proj.getX(), proj.getY()), self.game.getBallSize())
        circle.setFill(player.getColor())
        circle.draw(self.win)

        self.draw_projs[self.game.getCurrentPlayerNumber()] = circle

        while proj.isMoving():
            proj.update(1/50)
            circle.move(proj.getX() - circle.getCenter().getX(), proj.getY() - circle.getCenter().getY())
            update(50)

        return proj
    


    def updateScore(self,playerNr): 
        
        if self.draw_scores[playerNr] is not None:  
            self.draw_scores[playerNr].undraw()
            
        score_text = f"Score: {self.game.getPlayers()[playerNr].getScore()}"

        score_position = Point(self.game.getPlayers()[playerNr].getX(), -4)
        self.draw_scores[playerNr] = Text(score_position, score_text)
        self.draw_scores[playerNr].draw(self.win)


    def explode(self, proj,color):
        radius=self.game.getBallSize()

        while radius< 2*self.game.getCannonSize() :
            explosion_ring = Circle(Point(proj.getX(), proj.getY()), radius)
            explosion_ring.setFill(color)
            explosion_ring.draw(self.win)
            update(50)
            radius+=1
            explosion_ring.undraw()
    
    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind)
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()
            
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.explode(proj,player.getColor())
                self.game.newRound()

            self.game.nextPlayer()










class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
