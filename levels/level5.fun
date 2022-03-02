type BallGame

# SETUP
let ball_1 be Ball((50, 340), 10, color=Colors.orange, weight=0.1)
let ball_2 be Ball((160, 300), 30, color=Colors.orange)
let ball_3 be Ball((460, 180), 30, color=Colors.orange)

let platforms_1 be Platform(0, 400, 700, 20)
let platforms_2 be Platform(100, 300, 20, 100)
let platforms_3 be Platform(200, 300, 20, 100)
let platforms_4 be Platform(400, 200, 20, 200)
let platforms_5 be Platform(500, 200, 20, 200)

set ball_1.speed.y to 5

let goal be Goal(580, 30, 50, 50)

# SOLUTION
wait 200 frames
set ball_1.speed.x to 5
