type MazeGame

# SETUP
let maze be Maze()
let player be maze.player

# SOLUTION
let visited be {player.position}
let stack be []

make is_new(position) {
    return position not in visited and maze.is_free(position)
}

loop {
    if is_new(player.position.right) {
        await player.right()
        do stack.append(player.left)
        do visited.add(player.position)
        continue
    }
    if is_new(player.position.up) {
        await player.up()
        do stack.append(player.down)
        do visited.add(player.position)
        continue
    } 
    if is_new(player.position.down) {
        await player.down()
        do stack.append(player.up)
        do visited.add(player.position)
        continue
    }  
    if is_new(player.position.left) {
        await player.left()
        do stack.append(player.right)
        do visited.add(player.position)
        continue
    }
    let go_back be stack.pop()
    await go_back()
}