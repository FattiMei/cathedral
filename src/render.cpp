#include "render.h"
#include "shader.h"
#include <GLFW/glfw3.h>


GLint  program;
GLuint point_buffer;


static const char* vertex_shader_src = R"a(
	attribute vec3 vposition;

	void main() {
		gl_Position = vec4(vposition, 1.0);
	}
)a";


static const char* fragment_shader_src = R"a(
	precision mediump float;
	uniform vec3 color;

	void main() {
		gl_FragColor = vec4(color, 1.0);
	}
)a";


const float vertices[] = {
	-1.0f, 0.0f,
	 0.0f, 0.5f,
	 1.0f, 0.2f
};


void render_init(int width, int height) {
	glGenBuffers(1, &point_buffer);
	glBindBuffer(GL_ARRAY_BUFFER, point_buffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_DYNAMIC_DRAW);

	program = program_load(vertex_shader_src, fragment_shader_src);

	glBindAttribLocation(program, 0, "vposition");
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);

	glUseProgram(program);
	glUniform3f(glGetUniformLocation(program, "color"), 1.0, 0.0, 0.0);

	glViewport(0, 0, width, height);
}


void render_resize(int width, int height) {
	glViewport(0, 0, width, height);
}


void render_present() {
	glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT);

	glUseProgram(program);
	glDrawArrays(GL_LINE_STRIP, 0, 3);
}


void render_cleanup() {
	glDeleteBuffers(1, &point_buffer);
}
