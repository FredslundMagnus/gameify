type BallGame

# SETUP
let ball1 be Ball((100, 41), 10)
let ball2 be Ball((130, 41), 10)
let ball3 be Ball((160, 41), 10)
let ball4 be Ball((190, 41), 10)
let ball5 be Ball((220, 41), 10)
let ball6 be Ball((250, 41), 10)
let ball7 be Ball((280, 41), 10)
set ball1.speed.x to 1
set ball2.speed.x to 1
set ball3.speed.x to 1
set ball4.speed.x to 1
set ball5.speed.x to 1
set ball6.speed.x to 1
set ball7.speed.x to 1
let platforms_1 be Platform(0, 50, 550, 20)
let platforms_2 be Platform(100, 150, 550, 20)
let platforms_3 be Platform(0, 250, 550, 20)
let platforms_4 be Platform(100, 450, 550, 20)
let goal be Goal(100, 300, 50, 50, balls=7)


# do print(go_right)

make turns(ball) {
    if ball.center.x > 570 or ball.center.x < 90 {
        set ball.speed.x to -ball.speed.x
    }
}
every 10 frames {
    do turns(ball1)
    do turns(ball2)
    do turns(ball3)
    do turns(ball4)
    do turns(ball5)
    do turns(ball6)
    do turns(ball7)
}

