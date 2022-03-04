type MazeGame

# SETUP
let maze be Maze(2)
let player be maze.player
set player.speed to 5

# SOLUTION
loop 2 times {
    await player.up()
}
loop 4 times {
    await player.right()
}
loop 4 times {
    await player.up()
}
loop 10 times {
    await player.right()
}
loop 4 times {
    await player.up()
}
