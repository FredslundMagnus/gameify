make something(n) {
    wait n frames
    return n
}

let future be something(3)
do print(future, "before1")
wait 1 frames
do print(future, "before2")
wait 1 frames
do print(future, "before3")
wait 1 frames
do print(future, "before4")
wait 1 frames
do print(future, "before5")

let future1 be something(3)
loop {
    if future1.done {
        let future1 be future1.value
        break
    }
    wait 1 frames
}
do print(future1, "after 1")


let future2 be something(3)
await future2
do print(future2, "after 2")

await something(3) as future3
do print(future3, "after 3")