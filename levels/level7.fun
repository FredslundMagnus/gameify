type BallGame

# SETUP
let ball be Ball((70, 120), 30.2)

let platforms_1 be Platform(50, 300, 40, 20)
let platforms_2 be Platform(250, 300, 40, 20)
let platforms_3 be Platform(450, 300, 40, 20)

let goal be Goal(550, 110, 50, 50)

set platforms_1.speed.x to 1
set platforms_2.speed.x to 1
set platforms_3.speed.x to 1

every 100 frames {
    set platforms_1.speed.x to -platforms_1.speed.x
    set platforms_2.speed.x to -platforms_2.speed.x
    set platforms_3.speed.x to -platforms_3.speed.x
}
# SOLUTION
