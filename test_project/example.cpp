#include <stdio.h>

// This would typically go into .h files:
struct ButtonController {
public:
	void on_button_pressed();
};

struct LedController {
public:
	void toggle_led();

	LedController();
};



// This would typically go into .cpp files:
ButtonController *button_controller;
LedController *led_controller;

// This function is meant to be automatically
// called whenever a button is pressed.
void ButtonController::on_button_pressed() {
	/* ~ZMIJA.GENERATOR:
	def declare(variables):
		# Declare a new list called "on_button_pressed".
		# This list will contain calls to callback functions
		# in string form.
		variables["on_button_pressed"] = []
		
	def init(variables):
		# Nothing to do. This function can safely be removed.
		pass
		
	def generate(variables):
		# Return a string containing all callback calls,
		# separated by a newline character.
		return "\n".join(variables["on_button_pressed"])
	*/// ~ZMIJA.GENERATED_CODE:
	led_controller->toggle_led();
	// ~ZMIJA.END
}


void LedController::toggle_led() {
	printf("LED toggled.\n");
}

LedController::LedController() {
	/* ~ZMIJA.GENERATOR:
	def declare(variables):
		# Nothing to do. This function can safely be removed.
		pass
	
	def init(variables):
		# Add a callback call in string form.
		# This string will be added to the ButtonController's 
		# generated code.
		variables["on_button_pressed"].append("led_controller->toggle_led();")
		
	def generate(variables):
		# Nothing to do. This function can safely be removed.
		return ''
	*/// ~ZMIJA.GENERATED_CODE:
	
	// ~ZMIJA.END
}

int main() {
	button_controller = new ButtonController();
	led_controller = new LedController();

	button_controller->on_button_pressed();

	return 0;
}