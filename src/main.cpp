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

	Track T = generate_centered_track(1000);
	apply_delay(T, 240, 0.5);
	std::vector<double> auto_correlation(T.size());

	for (size_t i = 0; i < T.size(); ++i) {
		auto_correlation[i] = cross_correlation(T, i);
	}

	render_send_points(auto_correlation);


	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGuiIO& io = ImGui::GetIO(); (void)io;
	ImGui::StyleColorsDark();
	ImGui_ImplGlfw_InitForOpenGL(window, true);
	ImGui_ImplOpenGL3_Init("#version 100");

	while (!window_should_close()) {
		window_poll_events();

		render_present();

		ImGui_ImplOpenGL3_NewFrame();
		ImGui_ImplGlfw_NewFrame();
		ImGui::NewFrame();
		ImGui::ShowDemoWindow(NULL);

		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

		window_swap_buffers();
	}

	render_cleanup();
	window_close();

	return 0;
}
