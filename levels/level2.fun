type BallGame

# SETUP
let ball_1 be Ball((50, 450), 20, weight=1)
let platforms_1 be Platform(420, 100, 200, 20)
let platforms_2 be Platform(420, 55, 20, 50)
let goal be Goal(500, 50, 50, 50)

# SOLUTION
set ball_1.speed.x to 3
set ball_1.speed.y to -10