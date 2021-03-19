
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
  servos_init();
  aze = servos_register(3, (char*)"aze");

  servos_enable_all();
  // servos_enable(aze);
  // servos_reset(aze);
}

/**
 * Loop function
 */
void loop() {
  // terminal_io()->println(servos_count());
  servos_command(aze, angle);
  // servos_flush();
  terminal_tick();
}
