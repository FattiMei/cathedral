CXX      = g++
INCLUDE  = -I ./include
WARNINGS = -Wall -Wextra -Wpedantic
DEFINES  = -DUSE_OPENGLES2
LIBS     = -lglfw -lGL


src      = $(wildcard src/*.cpp)
obj      = $(patsubst src/%.cpp,build/%.o,$(src))
target   = test


all: $(target)


$(target): $(obj)
	$(CXX) -o $@ $^ $(LIBS)


build/%.o: src/%.cpp
	$(CXX) -c $(INCLUDE) $(WARNINGS) $(DEFINES) -o $@ $^


run: $(target)
	./$^


.PHONY: clean
clean:
	rm -f $(target) build/*.o
