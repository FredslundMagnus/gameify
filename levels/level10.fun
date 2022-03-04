type BallGame

# SETUP
let ball be Ball((320, 120), 30.2)
let goal be Goal(550, 410, 50, 50)

let goal_location be random() < 0.5

if goal_location {
    let goal be Goal(550, 410, 50, 50)
    else
    let goal be Goal(50, 410, 50, 50)
}


# SOLUTION
if goal_location {
    set ball.speed.x to -3
} else {
    set ball.speed.x to 3
}