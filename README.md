![Zmija](logo/logo.svg "Zmija")

<br>

<p align=center>
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/adrian-samoticha/zmija?style=plastic">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/adrian-samoticha/zmija?style=plastic">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/adrian-samoticha/zmija?style=plastic">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/adrian-samoticha/zmija?style=plastic">
<img alt="GitHub" src="https://img.shields.io/github/license/adrian-samoticha/zmija?style=plastic">
</p>

<br>

# Żmija
**Żmija** is a simple universal code generation tool. It is intended to be used as a means to generate code that is both efficient and easily maintainable.

It is intended to be used in embedded systems with limited resources, however it can be used anywhere else as well.

<br>

# Usage
**Żmija** lets you define sections in your code where code is generated automatically in accordance to a Python script that you provide. Such a section typically looks like this:

```Python
/* ~ZMIJA.GENERATOR:
def declare(variables):
	pass
	
def init(variables):
	pass
	
def generate(variables):
	return ""
*/// ~ZMIJA.GENERATED_CODE:

// ~ZMIJA.END
```

The section is defined inside a multi-line comment as to not affect the compilation of the code it is located in. **Żmija** supports any languge, including those that have non C-style comment styles (hence it is universal).

This is what the same section might look like inside a Lua script, for example:
```Python
--[[ ~ZMIJA.GENERATOR:
def declare(variables):
	pass
	
def init(variables):
	pass
	
def generate(variables):
	return ""
]]-- ~ZMIJA.GENERATED_CODE:

-- ~ZMIJA.END
```

Each section consists of a `declare`-function, an `init`-function and a `generate`-function.

The `declare`-function is executed first. It is meant for variable declaration and should only reference its own variables.

The `init`-function is meant to initialize variables, including those of other sections. It is executed only after the `declare`-function has been executed for all sections in the project.

The `generate`-function returns the generated code for the section it is located in. It is executed only after the `declare` and `init`-functions of all sections have been executed.

*Note:* Empty functions can safely be removed.

<br>

Run `python3 src/zmija.py /path/to/your/project/directory/` to perform the code generation. The generated code will be placed between the `~ZMIJA.GENERATED_CODE:` and the `~ZMIJA.END` lines.

<br>

# Help output
```
Zmija. Simple universal code generation.

Usage:
	zmija.py path
	zmija.py path -d | --delete
	zmija.py path -c | --check-only
	zmija.py -h | --help
	
Options:
	-h --help         Show this screen.
	-d --delete       Delete all generated code.
	-c --check-only   Check Python code for syntax and runtime errors without writing the changes to file.
	-u --unsafe       Skip the test pass. May cause data loss if the Python code raises exceptions, but offers better performance. Use with caution.
```

<br>

# Example
Say you have two modules, a ButtonController and a LedController. You would like to implement the observer pattern to allow the ButtonController to communicate with the LedController without depending on it.

The following C++ code implements this. It is a simple example where pressing the button toggles the LED.
```C++
#include <stdio.h>
#include <vector>
#include <functional>

// This would typically go into .h files:
struct ButtonController {
private:
    // Callbacks are functions that will be called
    // when the button is pressed. Notice how the
    // vector is constructed at runtime and held in
    // RAM.
    std::vector<std::function<void()>> callbacks;

public:
    void on_button_pressed();
    void register_callback(std::function<void()> cb);
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
    // call all registered callbacks
    for (auto &cb : callbacks) cb();
}

// This function is meant to be called by other
// modules that would like to react to button
// presses.
void ButtonController::register_callback(std::function<void()> cb) {
    callbacks.push_back(cb);
}


void LedController::toggle_led() {
    printf("LED toggled.\n");
}

LedController::LedController() {
    // Registering a new callback consumes precious RAM.
    button_controller->register_callback([this]() {
        toggle_led();
    });
}

int main() {
    button_controller = new ButtonController();
    led_controller = new LedController();

    button_controller->on_button_pressed();

    return 0;
}
```

Calling the `main()` function will print `LED toggled.` to the console, as intended.

However, the ButtonController's `callbacks` vector is built during runtime and held in RAM. This causes an unnecessary overhead regarding both memory usage and execution speed.

Since the registered callbacks do not change after they have been registered, it may be beneficial to register them during compile time instead.

<br>

The following C++ code attempts to achieve this by using **Żmija** to generate the callbacks during compile time:

```C++
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
```

<br>

Let's run **Żmija**:
```console
python3 src/zmija.py /path/to/your/project/directory/
```

<br>

This is what our newly generated .cpp file looks now:

```C++
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
```

As you can see, **Żmija** has generated the `led_controller->toggle_led();`-line, just as intended.

<br>

# ROADMAP
* ☑ Basic functionality
* ☑ Command line arguments
* ☐ Config file
* ☐ Proper testing

<br>

# WARNING
This project is still WIP. Do not use this in production.