type BallGame

# SETUP
let ball be Ball((30, 320), 10)

let platforms_1 be Platform(0, 350, 50, 20)
let platforms_2 be Platform(100, 300, 50, 20)
let platforms_3 be Platform(200, 250, 50, 20)
let platforms_4 be Platform(300, 200, 50, 20)
let platforms_5 be Platform(400, 150, 50, 20)
let platforms_6 be Platform(100, 35, 20, 200)
set ball.speed.y to 4
set ball.speed.x to 2
let goal be Goal(550, 110, 50, 50)


# SOLUTION