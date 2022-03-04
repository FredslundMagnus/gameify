type MazeGame

# SETUP
let maze be Maze()
let player be maze.player
set player.speed to 5

# SOLUTION
let visited be {player.position}
let stack be []

make try_move(position, move, go_back, could_do_previous) {
    if position not in visited and maze.is_free(position) and not could_do_previous {
        await move()
        do stack.append(go_back)
        do visited.add(player.position)
        return True
    }
    wait 0 frames
    return could_do_previous
}

loop {
    await try_move(player.position.up, player.up, player.down, False) as could_move
    await try_move(player.position.right, player.right, player.left, could_move) as could_move
    await try_move(player.position.down, player.down, player.up, could_move) as could_move
    await try_move(player.position.left, player.left, player.right, could_move) as could_move
    if not could_move {
        let go_back be stack.pop()
        await go_back()
    }    
}