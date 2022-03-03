# Normal function
make fib(n) {
    if n == 1 or n == 2 {
        return 1
    } else {
        return fib(n-1) + fib(n-2)
    }
}

# fib(10)=55


# Use Futures
make fib_async(n) {
    wait 1 frames
    if n == 1 or n == 2 {
        return 1
    } else {
        await fib_async(n-1) as fib1
        await fib_async(n-2) as fib2
        return fib1 + fib2
    }
}

await fib_async(10) as result
# result=55