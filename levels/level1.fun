type BallGame

# SETUP
let ball_1 be Ball((140, 120), 30.2)
let ball_2 be Ball((240, 120), 30)

let platforms_1 be Platform(0, 300, 400, 20)
let platforms_2 be Platform(40, 50, 20, 400)
let platforms_3 be Platform(340, 50, 20, 400)


set ball_1.speed.x to 1
set ball_2.speed.x to -1

# SOLUTION
wait 30 frames
set ball_1.speed.x to 10
