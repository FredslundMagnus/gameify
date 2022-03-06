type BallGame

# SETUP
let ball be Ball((20, 290), 30.2)
let random_weight be random() * 3 + 0.5
let ball2 be Ball((220, 420), 30.2, color=Colors.deepOrange, weight=random_weight)
let platforms_1 be Platform(-20, 320, 100, 20)
let platforms_2 be Platform(170, 450, 100, 20)
set ball.speed.x to 3
let goal be Goal(550, 240, 50, 50)
wait 70 frames
let random_speed be random()*8 + 2
set ball2.speed.y to random_speed


# SOLUTION