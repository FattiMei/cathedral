#include "render.h"
#include "shader.h"
#include <GLFW/glfw3.h>
#include <algorithm>


GLint  program;
GLuint point_buffer;
GLint  npoints;


static const char* vertex_shader_src = R"a(
	attribute vec2 vposition;
	uniform float min;
	uniform float max;

	void main() {
		float normalized = 2.0 * (vposition.y - min) / (max - min) - 1.0;
		gl_Position = vec4(vposition.x, normalized, 0.0, 1.0);
	}
)a";


static const char* fragment_shader_src = R"a(
	precision mediump float;
	uniform vec3 color;

	void main() {
		gl_FragColor = vec4(color, 1.0);
	}
)a";


void render_init(int width, int height) {
	glGenBuffers(1, &point_buffer);
	program = program_load(vertex_shader_src, fragment_shader_src);

	glUseProgram(program);
	glUniform3f(glGetUniformLocation(program, "color"), 1.0, 0.0, 0.0);

	glViewport(0, 0, width, height);
}


void render_resize(int width, int height) {
	glViewport(0, 0, width, height);
}


void render_present() {
	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT);

	glUseProgram(program);
	glDrawArrays(GL_LINE_STRIP, 0, npoints);
}


void render_cleanup() {
	glDeleteBuffers(1, &point_buffer);
}


void render_send_points(const std::vector<double> &T) {
	std::vector<float> local_buffer(2 * T.size());

	// problematic when min == max, but rare
	const float min = *std::min_element(T.begin(), T.end());
	const float max = *std::max_element(T.begin(), T.end());

	for (size_t i = 0; i < T.size(); ++i) {
		local_buffer[2*i    ] = -1.0f + 2.0f * static_cast<float>(i) / static_cast<float>(T.size() - 1);
		local_buffer[2*i + 1] = static_cast<float>(T[i]);
	}

	glUseProgram(program);
	glUniform1f(glGetUniformLocation(program, "min"), min);
	glUniform1f(glGetUniformLocation(program, "max"), max);

	// @TODO: exists a sizeof(std::vector) ??
	glBindBuffer(GL_ARRAY_BUFFER, point_buffer);
	glBufferData(GL_ARRAY_BUFFER, local_buffer.size() * sizeof(float), local_buffer.data(), GL_DYNAMIC_DRAW);

	glBindAttribLocation(program, 0, "vposition");
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);

	npoints = T.size();
}
