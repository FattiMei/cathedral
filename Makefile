CXX = g++
INCLUDE  = -I ./include
WARNINGS = -Wall -Wextra -Wpedantic
DEFINES  = -DUSE_OPENGLES2
LIBS     = -lglfw -lGL


target = test


all: $(target)


$(target): build/main.o build/window.o
	$(CXX) -o $@ $^ $(LIBS)


build/%.o: src/%.cpp
	$(CXX) -c $(INCLUDE) $(WARNINGS) $(DEFINES) -o $@ $^


run: $(target)
	./$^ | python3 ./plot.py


.PHONY: clean
clean:
	rm -f $(target) build/*.o
