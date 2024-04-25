#include "render.h"
#include <GLFW/glfw3.h>


void render_init(int width, int height) {
	glViewport(0, 0, width, height);
}


void render_resize(int width, int height) {
	glViewport(0, 0, width, height);
}


void render_present() {
	glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT);
}
