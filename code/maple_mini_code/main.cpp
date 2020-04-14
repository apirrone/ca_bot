#include <stdlib.h>
#include <wirish/wirish.h>
#include <terminal.h>
#include <main.h>

TERMINAL_PARAMETER_INT(t, "Variable t", 0);

TERMINAL_COMMAND(hello, "Prints hello world")
{
    terminal_io()->println("Hello world");
}

/**
 * Setup function
 */
void setup()
{
    terminal_init(&SerialUSB);
    t = 123;
}

/**
 * Loop function
 */
void loop()
{
    terminal_tick();
}
