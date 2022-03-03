# Defining a function
make something(n) {
    # The function does not return imidiately because it has to wait
    wait n frames
    return n
}

# We run the function
let future0 be something(3)
# future0=Future(done=False)
wait 1 frames
# future0=Future(done=False)
wait 1 frames
# future0=Future(done=False)
wait 1 frames
# future0=Future(done=True, value=3)
wait 1 frames
# future0=Future(done=True, value=3)
wait 1 frames
# future0=Future(done=True, value=3)

# We could now simply redefine future to be the value like this:
let future0 be future0.value
# future0=3

# But we need to make sure this will work for all n so for this we need a loop


let future1 be something(3)
# future1=Future(done=False)
loop {
    if future1.done {
        # future1=Future(done=True, value=3)
        let future1 be future1.value
        # future1=3
        break
    }
    # future1=Future(done=False)
    wait 1 frames
}
# future1=3

# So we basically just wait until it is done and then overwrite the value
# Since this is to much code to write each time most languages have a keyword "await" which does exacly this
# So lets try to replicate what we just did with this new syntax.


let future2 be something(3)
# future2=Future(done=False)
await future2
# future2=3

# Wow that was a lot simpler! And this way is also a fair approach, we had to define the future above, and then wait for it afterwards
# We want to do something like this
await something(3)
# But then we wont have any way to get the result. However if we are not interested in the result this is the solution we should use.
# But if we are interested in the solution, the language give us a way to get that:
await something(3) as value
# value=3

# Conclusion
# We see that we now basiacally have removed our need to hande the futeres and have gotten 2 simple approaches:
# We want to wait until something finishes:
await something(3)
# We want to wait until something finishes and get the result
await something(3) as result
# result=3