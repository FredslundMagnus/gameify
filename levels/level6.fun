type BallGame

# SETUP
let ball_1 be Ball((550, 360), 30, color=Colors.purple)
let ball_2 be Ball((50, 300), 30, color=Colors.orange)


let platforms_1 be Platform(0, 400, 700, 20)
let platforms_2 be Platform(0, 0, 20, 400)
let platforms_3 be Platform(620, 0, 20, 400)
set ball_2.speed.x to 6

let goal be Goal(300, 30, 50, 50)

# SOLUTION
set ball_1.weight to 100