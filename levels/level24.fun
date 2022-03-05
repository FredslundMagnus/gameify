type MazeGame

# SETUP
let maze be Maze()
let player be maze.player

# SOLUTION
let visited be {player.position}
let stack be []

loop {
    if player.position.right not in visited and maze.is_free(player.position.right) {
        await player.right()
        do stack.append(player.left)
        do visited.add(player.position)
        continue
    }
    if player.position.up not in visited and maze.is_free(player.position.up) {
        await player.up()
        do stack.append(player.down)
        do visited.add(player.position)
        continue
    } 
    if player.position.down not in visited and maze.is_free(player.position.down) {
        await player.down()
        do stack.append(player.up)
        do visited.add(player.position)
        continue
    }  
    if player.position.left not in visited and maze.is_free(player.position.left) {
        await player.left()
        do stack.append(player.right)
        do visited.add(player.position)
        continue
    }
    let last_action be stack.pop()
    await last_action()
}