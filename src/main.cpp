#include <iostream>
#include <vector>
#include "window.h"
#include "render.h"
#include "processing.h"
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"


int main() {
	int width = 800;
	int height = 600;

	if (window_init("cathedral", width, height) != 0) {
		window_close();
		exit(EXIT_FAILURE);
	}

	render_init(width, height);

	Track original = generate_centered_track(1000);
	Track delayed(original.size());
	std::vector<double> auto_correlation(original.size() / 2);




	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGuiIO& io = ImGui::GetIO(); (void)io;
	ImGui::StyleColorsDark();
	ImGui_ImplGlfw_InitForOpenGL(window, true);
	ImGui_ImplOpenGL3_Init("#version 100");

	float old_pan = 0.5f;
	float new_pan = old_pan;

	int old_delay = 200;
	int new_delay = old_delay;

	apply_delay(original, delayed, new_delay, 0.5);

	for (size_t i = 0; i < auto_correlation.size(); ++i) {
		auto_correlation[i] = cross_correlation(delayed, i);
	}

	render_send_points(auto_correlation);

	while (!window_should_close()) {
		window_poll_events();

		int display_w, display_h;
		glfwGetFramebufferSize(window, &display_w, &display_h);

		render_resize(display_w, display_h);
		render_present();

		ImGui_ImplOpenGL3_NewFrame();
		ImGui_ImplGlfw_NewFrame();
		ImGui::NewFrame();

		ImGui::SliderFloat("pan controls", &new_pan, 0.0f, 1.0f, "pan = %.3f");
		ImGui::SliderInt("slider int", &new_delay, 0, original.size() - 1);

		if (old_pan != new_pan or old_delay != new_delay) {
			old_pan = new_pan;

			apply_delay(original, delayed, new_delay, new_pan);

			for (size_t i = 0; i < auto_correlation.size(); ++i) {
				auto_correlation[i] = cross_correlation(delayed, i);
			}

			render_send_points(auto_correlation);
		}

		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

		window_swap_buffers();
	}

	render_cleanup();
	window_close();

	return 0;
}
