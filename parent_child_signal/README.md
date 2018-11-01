### Forwarding `KeyboardInterrupt` (or other signals) to a child process

This demonstrates a parent/child process structure, where the child does some
work (here just a `print()`) and then waits for a signal from the parent.
