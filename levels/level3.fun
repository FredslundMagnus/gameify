type BallGame

# SETUP
let ball be Ball((70, 120), 30.2)

let platforms_1 be Platform(20, 300, 100, 20)
let platforms_2 be Platform(220, 300, 100, 20)
let platforms_3 be Platform(420, 300, 100, 20)

let goal be Goal(550, 110, 50, 50)

every 50 frames {
    set platforms_1.speed.x to -platforms_1.speed.x
}

# SOLUTION
make change_x_direction(obj) {
    set obj.speed.x to -obj.speed.x
}

after 75 frames {
    change_x_direction(platforms_1)
}

print(3)

make fib(n) {
    if n == 1 or n == 2{
        return 1
    } else {
        return fib(n-1) + fib(n-2)
    }
}

loop 2 times {
    print(fib(5))
}


print(fib(1))
print(fib(2))
print(fib(3))
print(fib(4))
print(fib(5))

set ball_1.speed.x to 10


"(?<=(make |call ))([a-z]+[a-z_0-9]*)"

"match": "([a-z]+[a-z_0-9]*)(?=\\(.*\\))"