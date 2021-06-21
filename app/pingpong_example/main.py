from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.graphics import Color, Rectangle
import random
import datetime

class Robot():
    def __init__(self, stableness: float=0.8):  #stableness =1.0 always catchs, < 1, has chance to lose ball
        random.seed(datetime.datetime.now().timestamp)
        if (stableness > 1.0):
            raise RuntimeError('stableness cannot be > 1.0')
        self.stableness = stableness
        self.landing_point = 0
        self.playground_width = 0
        self.playground_height = 0
        self.player_width = 0
        self.player_length = 0

    def set_playground(self, playground_width, playground_height, player_width, player_length):
        self.playground_width = playground_width
        self.playground_height = playground_height
        self.player_width = player_width
        self.player_length = player_length

    def reset(self, landing_point):
        print(landing_point)
        self.landing_point = landing_point
        
    def feed(self, init_vx, init_vy, init_x, init_y):
        if init_vx < 0: 
            return
        bouncing_times = abs(init_y +(self.playground_width-self.player_width-init_x)/init_vx*init_vy)//self.playground_height
        self.landing_point = ((init_y + (self.playground_width-self.player_width-init_x)/init_vx*init_vy)%self.playground_height * ( -1 if (bouncing_times%2==1) else 1) + self.playground_height)%self.playground_height
        # print(self.landing_point)
        self.landing_point += (1-self.stableness)*(2*random.random()-1)*self.player_length
        # print(self.landing_point)
        if self.landing_point > self.playground_width:
            self.landing_point = self.playground_width
        if self.landing_point < 0:
            self.landing_point = 0
        # print(self.landing_point)
        # print(self.playground_height)
        # print('___')

    def get_landing_point(self):
        return self.landing_point



class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    win_label = ObjectProperty(None)
    start_button = ObjectProperty(None)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    score = NumericProperty(0)
    color = ListProperty([1,1,0,0])
    def bounce_ball(self, ball, robot_player:Robot):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height/2)
            bounced = Vector(-1*vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset*1.5
            #heading toward robot player 2
            if(ball.velocity[0] > 0):
                robot_player.feed(ball.velocity[0],ball.velocity[1], ball.center_x, ball.center_y)

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    WIN_SCORE = 5
    game_stop = False
    player2_robot = Robot(stableness=0.3)
    
    def serve_ball(self, vel=(-4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.player1.color = [0.8,0.9,0.15,0.59]
        self.player2.color = [0.15,0.9,0.15,0.59]
        # print(self.center_y)
        #print(self.player1.center_y)
        #self.player2_robot.reset(self.center_y)
        if self.ball.velocity[0]> 0:
            self.feed_robot()

    def update(self, dt):
        if self.game_stop:
            return

        if self.player1.score >= self.WIN_SCORE:
            self.win_ending(1)
            return
        if self.player2.score >= self.WIN_SCORE:
            self.win_ending(2)
            return

        

        #call ball move
        self.ball.move()

        self.player2_robot.set_playground(self.width,self.height,self.player2.width,self.player2.height)
        self.move_robot_player2()
        
        #player bounce ball 
        self.player1.bounce_ball(self.ball, self.player2_robot)
        self.player2.bounce_ball(self.ball, self.player2_robot)

        #bounce the ball at bottom or top
        if(self.ball.y< self.y) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        
        #went out of side if miss (player bounce failed), and score up on the other player
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(-4,0))
        
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))

    def feed_robot(self):
        self.player2_robot.feed(self.ball.velocity[0], self.ball.velocity[1], self.ball.center_x, self.ball.center_y)

    def move_robot_player2(self):
        if self.ball.velocity[0] > 0:
            #slowly approchs when player 1 bounce the ball
            self.player2.center_y = self.ball.center_x/self.width*(self.player2_robot.get_landing_point()-self.player2.center_y) + self.player2.center_y 
            #self.player2.center_y = self.player2_robot.get_landing_point()

    def win_ending(self, player_number):
        
        self.win_label = Label(text='Winner Is Player{} !!!'.format(player_number), font_size='36sp', halign='center', valign='middle')
        self.win_label.center_x = self.center_x
        self.win_label.center_y = self.center_y
        self.win_label.texture_update()
        with self.win_label.canvas:
            text_size_x,text_size_y = self.win_label.texture_size
            Color(1,1,0,0.5)
            Rectangle(pos=(self.win_label.center_x - text_size_x/2, self.win_label.center_y - text_size_y/2), size=self.win_label.texture_size)
        self.add_widget(self.win_label)
        
        self.start_button = Button(text='Press Start')
        self.start_button.bind(on_release = self.start_new_game)
        with self.start_button.canvas:
            self.start_button.background_color = [0,1,1,1]
            self.start_button.size = (180, 60)
            # self.start_button.background_normal='./press_start.png'
            self.start_button.pos = (self.center_x-self.start_button.size[0]/2, self.height-self.start_button.size[1])
        self.add_widget(self.start_button)


        self.game_stop = True
        # self.remove_widget(self.ball)
        # self.remove_widget(self.player1)
        # self.remove_widget(self.player2)

    def start_new_game(self, instance):
        self.remove_widget(self.start_button)
        self.remove_widget(self.win_label)
        self.player1.score = 0
        self.player2.score = 0
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y
        self.serve_ball((-4,0))
        self.game_stop = False

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width*2/3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
