type BallGame

# SETUP
let ball be Ball((60, 120), 30.2)

let platforms_0 be Platform(-180, 300, 40, 20)
let platforms_1 be Platform(20, 300, 40, 20)
let platforms_2 be Platform(220, 300, 40, 20)
let platforms_3 be Platform(420, 300, 40, 20)
let platforms_4 be Platform(620, 300, 40, 20)
let platforms_5 be Platform(820, 300, 40, 20)

let goal be Goal(550, 110, 50, 50)

let go_right be random() < 0.5

let speed be 1 if go_right else -1

make set_speed(speed) {
    set platforms_0.speed.x to speed
    set platforms_1.speed.x to speed
    set platforms_2.speed.x to speed
    set platforms_3.speed.x to speed
    set platforms_4.speed.x to speed
    set platforms_5.speed.x to speed
}

do set_speed(speed)
every 200 frames {
    do set_speed(-speed*199)
    wait 1 frames
    do set_speed(speed)
}

# SOLUTION

# Du skal bruge go_right i din løsning
do print(go_right)

if go_right {
    wait 20 frames
    set ball.speed.x to 1
} else {
    set ball.speed.x to 2
    wait 60 frames
    set ball.speed.x to 0.8
}