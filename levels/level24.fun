type MazeGame

# SETUP
let maze be Maze()
let player be maze.player

# SOLUTION
let visited be {player.position}
let stack be []

loop {
    let could_go_to_new_place be False
    loop 1 times {
        if player.position.up not in visited and maze.is_free(player.position.up) {
            await player.up()
            do stack.append(player.down)
            do visited.add(player.position)
            let could_go_to_new_place be True
            break
        } 
        if player.position.right not in visited and maze.is_free(player.position.right) {
            await player.right()
            do stack.append(player.left)
            do visited.add(player.position)
            let could_go_to_new_place be True
            break
        }
        if player.position.down not in visited and maze.is_free(player.position.down) {
            await player.down()
            do stack.append(player.up)
            do visited.add(player.position)
            let could_go_to_new_place be True
            break
        }  
        if player.position.left not in visited and maze.is_free(player.position.left) {
            await player.left()
            do stack.append(player.right)
            do visited.add(player.position)
            let could_go_to_new_place be True
        }
    }
    if not could_go_to_new_place {
        let go_back be stack.pop()
        await go_back()
    }
}