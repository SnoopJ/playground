## Description

Based on a question asked in `#python` on Libera.chat on 10 Dec 2022 about
debugging a program that reads from `stdin`, meaning that normal usage of `pdb`
gets mixed up with the program's input.

Ideally, the program could be re-written to take its input from a file, freeing
up `stdin` for `pdb`'s usage, or the user could rely on a debugging tool with a
"remote debugging" feature (e.g. [pudb](https://documen.tician.de/pudb/starting.html#remote-debugging),
my personal preference). But the question got me curious how `pdb` could be
cajoled into taking its input from somewhere other than `sys.stdin`

With kudos to StackOverflow user dmoreno for an answer that got me started:
https://stackoverflow.com/a/26975795



## Usage

To run this sample, place this file somewhere where it can be imported and
set the environment variable `PYTHONBREAKPOINT=FIFOPdb.set_trace` before
running the target program. When the debugger is invoked, a message will tell
you the name of the FIFO where it will be expecting its input. This FIFO will
be used for all debugger input for the lifetime of the debugger

![Screenshot showing the operation of this sample, showing two terminals, one
for the main program and pdb output, one for the pdb input](example.png)

