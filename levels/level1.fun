type BallGame

# SETUP
let ball_1 be Ball((150, 120), 50)

let platforms_1 be Platform(0, 300, 400, 20)
let platforms_2 be Platform(40, 50, 20, 400)
let platforms_3 be Platform(340, 50, 20, 400)
let platforms_4 be Platform(0, 50, 400, 20)


set ball_1.speed.x to 2

# SOLUTION
set ball_1.speed.x to 10
set ball_1.speed.y to -10