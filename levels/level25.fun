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

let reverse be {player.up: player.down, player.down: player.up, player.right: player.left, player.left: player.right}

make move(action) {
    await action()
    do stack.append(reverse[action])
    do visited.add(player.position)
}

loop {
    if is_new(player.position.right) {
        await move(player.right)
        continue
    }
    if is_new(player.position.up) {
        await move(player.up)
        continue
    } 
    if is_new(player.position.down) {
        await move(player.down)
        continue
    }  
    if is_new(player.position.left) {
        await move(player.left)
        continue
    }
    let go_back be stack.pop()
    await go_back()
}