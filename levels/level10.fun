type BallGame

# SETUP
let ball be Ball((60, 41), 10)
let ball2 be Ball((80, 41), 10)
let ball3 be Ball((100, 41), 10)
let ball4 be Ball((120, 41), 10)
set ball.speed.x to 1
let platforms_1 be Platform(0, 50, 550, 20)
let platforms_2 be Platform(100, 150, 550, 20)
let platforms_3 be Platform(0, 250, 550, 20)
let platforms_4 be Platform(100, 350, 250, 20)
let platforms_5 be Platform(450, 350, 250, 20)
let platforms_6 be Platform(350, 450, 100, 20)
let platforms_7 be Platform(330, 350, 20, 100)
let platforms_8 be Platform(450, 350, 20, 100)


# do print(go_right)

make complete(ball) {
    every 200 frames {
        set ball.speed.x to -ball.speed.x
    }
}

do complete(ball4)