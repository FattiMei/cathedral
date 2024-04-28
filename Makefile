CXX          = g++
INCLUDE      = -I ./include -I ./imgui/include
WARNINGS     = -Wall -Wextra -Wpedantic
IMGUI_CONFIG = -DIMGUI_IMPL_OPENGL_ES2
DEFINES      = -DUSE_OPENGLES2
LIBS         = -lglfw -lGL -ldl


imgui_src = $(wildcard imgui/src/*.cpp)
src       = $(wildcard src/*.cpp)
obj      += $(patsubst src/%.cpp,build/%.o,$(src))
obj      += build/imgui.so


target    = test


all: $(target)


$(target): $(obj)
	$(CXX) -o $@ $^ $(LIBS)


build/%.o: src/%.cpp
	$(CXX) -c $(INCLUDE) $(WARNINGS) $(DEFINES) -o $@ $^


build/imgui.so: $(imgui_src)
	$(CXX) -shared $(IMGUI_CONFIG) $(INCLUDE) -o $@ $^


run: $(target)
	./$^


.PHONY: clean fullclean
clean:
	rm -f $(target) $(obj)


fullclean: clean
	rm -f build/imgui.o
