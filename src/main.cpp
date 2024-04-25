#include <iostream>
#include <algorithm>
#include <random>
#include <vector>
#include <cassert>
#include "window.h"
#include "render.h"


// @TODO: experiment better with std::array, I couldn't compile this code


double compute_mean(const std::vector<double> &track) {
	double sum{0};

	for (auto sample : track) {
		sum += sample;
	}

	return sum / static_cast<double>(track.size());
}


void center(std::vector<double> &track) {
	const double mean = compute_mean(track);

	for (auto &sample : track) {
		sample = sample - mean;
	}
}


void apply_delay(std::vector<double> &track, size_t tau, double pan) {
	assert(pan >= 0.0 and pan <= 1.0);

	for (size_t i = tau; i < track.size(); ++i) {
		track[i] = pan * track[i - tau] + (1.0 - pan) * track[i];
	}

	center(track);
}


double cross_correlation(const std::vector<double> &track, size_t phi) {
	double result{0};

	for (size_t i = 0; i < track.size(); ++i) {
		result += track[i] * track[(i + phi) % track.size()];
	}

	return result;
}


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

	window_close();

#if 0
	std::default_random_engine gen(0);
	std::uniform_real_distribution<double> uniform(-1.0, 1.0);
	std::vector<double> example;


	for (int i = 0; i < 1000; ++i) {
		example.push_back(uniform(gen));
	}


	apply_delay(example, 300, 0.5);


	for (size_t i = 0; i < example.size(); ++i) {
		std::cout << cross_correlation(example, i) << std::endl;
	}
#endif

	return 0;
}
