from math import sin,cos,radians
import random


""" This is the model of the game"""
class Game:
    """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """
    def __init__(self, cannonSize, ballSize):
        # HINT: This constructor needs to create two players according to the rules specified in the assignment text
        self.cannonSize=cannonSize
        self.ballSize=ballSize
       
        self.players=[Player(self,False,-90,"blue"), Player(self,True,90,"red")]
   
        self.currentPlayerIndex = 0 
        self.wind = 0
        

    """ A list containing both players """
    def getPlayers(self):
        return self.players 

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize 

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize 

    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        if self.currentPlayerIndex==0:
            return self.players [0]
        else: return self.players [1] 

    """ The opponent of the current player """
    def getOtherPlayer(self):
        if self.currentPlayerIndex==0:
            return self.players [1]
        else: return self.players [0] 
    
    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.currentPlayerIndex 
    
    """ Switch active player """
    def nextPlayer(self):
        if self.currentPlayerIndex==0:
            self.currentPlayerIndex = 1
        else: self.currentPlayerIndex = 0

    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.wind = wind
    
    def getCurrentWind(self):
        return self.wind 
    

    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        wind = 20*random.random()-10
        self.setCurrentWind(wind)
        
        return wind
    

""" Models a player """
class Player:
   
    #HINT: It should probably take the Game that creates it as parameter and some additional properties that differ between players (like firing-direction, position and color)
    def __init__(self, game, isReversed, start_x_value, color):

        self.game = game  
        self.isReversed = isReversed  
        self.start_x_value = start_x_value 
        self.color = color 
        self.score = 0


    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        self.angle=angle
        self.velocity=velocity

        if self.isReversed:
            start_angle=180-angle
            
        else:
            start_angle=self.angle     

        starting_x=self.start_x_value 
        starting_y=0 #starting_y = self.game.getCannonSize() / 2 ? om bollen ska gå från mitten?
    
        proj=Projectile(start_angle, velocity, self.game.getCurrentWind(), starting_x, starting_y, -110, 110)
    
        # The projectile should start in the middle of the cannon of the firing player
        # HINT: Your job here is to call the constructor of Projectile with all the right values
        # Some are hard-coded, like the boundaries for x-position, others can be found in Game or Player
        return proj 

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile 
    is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj: 'Projectile'):
        #self.proj=projs
        # HINT: both self (a Player) and proj (a Projectile) have getX()-methods.
        # HINT: This method should give a negative value if the projectile missed to the left and positive if it missed to the right.
        # The distance should be how far the projectile and cannon are from touching, not the distance between their centers.
        # You probably need to use getCannonSize and getBallSize from Game to compensate for the size of cannons/cannonballs
        
        projectile_x = proj.getX() #x position för boll, hur långt hö/vä från start 
        cannon_x = self.getX() #var kanonen är
        cannon_radius = self.game.getCannonSize() / 2 #ersatte kanterna till att det blir ett fast avstånd från mitten till kant som vi använder istället för att krångla til det med bilden
        ball_radius = self.game.getBallSize()

        # Beräkna avståndet mellan kanonens centrum och projektilens centrum
        distance = projectile_x - cannon_x

        # Om projektilens y-koordinat är 0, betyder det att den har landat
        
        if abs(distance) <= (cannon_radius + ball_radius):
            return 0  #träff  vad vill vi returna?
        else:
            return distance #neg är kort och pos är för långt
        

        
    """ The current score of this player """
    def getScore(self):
        return self.score 

    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.score+=1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.color

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.start_x_value

    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return  self.angle , self.velocity



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile:
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
        wind: The wind speed value affecting this projectile
        xPos and yPos: The initial position of this projectile
        xLower and xUpper: The lowest and highest x-positions allowed
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind


    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos
