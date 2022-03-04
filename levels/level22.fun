type MazeGame

# SETUP
let maze be Maze(3)
let player be maze.player

# SOLUTION
make up(n) {
    loop n times {
        await player.up()
    }
}

make down(n) {
    loop n times {
        await player.down()
    }
}

make right(n) {
    loop n times {
        await player.right()
    }
}

make left(n) {
    loop n times {
        await player.left()
    }
}

await right(2)
await up(4)
await right(2)
await up(4)
await right(4)
await up(2)
await right(6)