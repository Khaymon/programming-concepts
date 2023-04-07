## Assembler and virtual machine

This task consists assembler, which translates handwritten code into the byte-code, and virtual machine translator of the byte-code

### Instructions supported
- _FBEG function_number_ -- defines a function with numerical number _function_number_ which must be positive integer
- _FEND_ -- defines the end of a function
- _PUSH value_ -- puts the _value_ into the stack
- _POP_ -- deletes a top number from the stack
- _CALL function_number_ -- calls the function with name _function_number_
- _TOP destination_ -- copies the top value from the stack to the register with address _destination_
- _SUB destination source_ -- subtract _source_ value from _destination_ value and writes result to the _destination_
- _ADD destination source_ -- adds _destination_ value and _source_ value and writes result to the _destination_
- _ASSIGN destination value_ -- places _value_ to the register with address _destination_
- _PUSHREG source_ -- places value of the register with address _source_ into the stack
- _PUTC character_number_ prints symbol with ordinal _character_number_
- _JUMP address_ -- moves IP to the _address_
- _MOV destination source_ -- copies value from _source_ to _destination_
- _STOP_ -- stops the program
- _READ destination_ -- reads the value entered into a terminal
- _PRINT source_ -- prints the value of a register with the address _source_


### Examples
Examples are located in the `examples` folder.
