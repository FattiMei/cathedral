#include <iostream>
#include <algorithm>
#include <random>
#include <vector>
#include <cassert>
#include "window.h"
#include "render.h"


int main() {
	int width = 800;
	int height = 600;

	if (window_init("cathedral", width, height) != 0) {
		window_close();
		exit(EXIT_FAILURE);
	}

	render_init(width, height);
	window_set_callbacks();

	while (!window_should_close()) {
		render_present();

		window_swap_buffers();
		window_poll_events();
	}

	render_cleanup();
	window_close();

	return 0;
}
