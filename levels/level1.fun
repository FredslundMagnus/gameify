type BallGame

# SETUP
let ball_1 be Ball((50, 250), 20, weight=1)
let platforms_1 be Platform(-20, 400, 200, 20)
let platforms_2 be Platform(400, 400, 300, 20)
let platforms_3 be Platform(0, 0, 20, 420)
let platforms_4 be Platform(620, 0, 20, 420)
let goal be Goal(500, 250, 50, 50)

# # SOLUTION TEMPLATE
set ball_1.speed.x to 0 # Skriv her et tal mellem -5 og 5 i stedet for 0, der løser banen

# # SOLUTION
# set ball_1.speed.x to -3