type BallGame

# SETUP
let ball_1 be Ball((70, 120), 30.2, color=Colors.green)

let platforms_1 be Platform(50, 300, 50, 20)
let platforms_2 be Platform(250, 300, 50, 20)
let platforms_3 be Platform(450, 300, 50, 20)

let goal be Goal(550, 110, 50, 50)

# SOLUTION
wait 60 frames
set ball_1.speed.x to 2

