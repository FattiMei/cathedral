#ifndef __WINDOW_H__
#define __WINDOW_H__


#include <GLFW/glfw3.h>
#include <vector>
#include <string>


namespace Window {
	extern GLFWwindow *handle;
	int  create(const std::string &title, int width, int height);
	void set_hints(const std::vector<std::pair<int,int>> &hints);
	void set_callbacks();
	void swap_buffers();
	void poll_events();
	bool should_close();
	void close();
};


#endif
