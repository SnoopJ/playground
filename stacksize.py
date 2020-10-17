"""
Based on a question in Freenode #python on March 6th, 2019 about computing the
effect of code on the size of the stack
"""
import dis
from pprint import pprint
from codetransformer import Code

def example(arg):
    try:
        arg.x
    except:
        return

print(dis.code_info(example))
instr = list(dis.get_instructions(example))
sfx = [dis.stack_effect(op.opcode, op.arg) for op in instr]

for i, s in zip(instr, sfx):
    opline = '\t'.join([f"{thing:<15}" for thing in ('>>' if i.is_jump_target else '', i.offset, i.opname, i.argrepr, f'{s:>5d}')])
    print(opline)

c = Code.from_pyfunc(example)
