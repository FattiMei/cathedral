CXX = g++
WARNINGS = -Wall -Wextra -Wpedantic


target = test


all: $(target)


$(target): src/main.cpp
	$(CXX) $(WARNINGS) -o $@ $^


run: $(target)
	./$^ | python3 ./plot.py
