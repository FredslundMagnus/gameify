type BallGame
# SETUP
let ball be Ball((70, 120), 30.2)

let platforms_1 be Platform(20, 300, 100, 20)
let platforms_2 be Platform(220, 300, 100, 20)
let platforms_3 be Platform(420, 300, 100, 20)


# SOLUTION
wait 60 frames
set ball.speed.x to 1.9