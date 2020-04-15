#ifndef ENABLE_DXL
#define ENABLE_DXL

#include <stdlib.h>
#include <wirish/wirish.h>
#include <terminal.h>
#include <main.h>
#include <servos.h>


TERMINAL_PARAMETER_INT(angle, "Variable angle", 0);

TERMINAL_COMMAND(hello, "Prints hello world")
{
  terminal_io()->println("Hello world");
}

uint8_t aze; 
/**
 * Setup function
 */
void setup() {
  
  terminal_init(&SerialUSB);
  angle = 0;
  aze = servos_register(3, (char*)"aze");
  servos_init();
  servos_enable(aze);
  
}

/**
 * Loop function
 */
void loop() {
  

  servos_command(aze, angle);
  terminal_tick();
}

#endif
