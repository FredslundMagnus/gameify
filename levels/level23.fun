type MazeGame

# SETUP
let maze be Maze(4)
let player be maze.player
set player.speed to 5

# SOLUTION
make move(operation) {
    make function(n) {
        loop n times {
            await operation()
        }
    }
    return function
}

let up be move(player.up)
let down be move(player.down)
let left be move(player.left)
let right be move(player.right)

await up(2)
await right(2)
await up(2)
await right(6)
await up(2)
await right(2)
await up(2)
await right(4)
await up(2)