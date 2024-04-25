CXX = g++
WARNINGS = -Wall -Wextra -Wpedantic


target = test


all: $(target)


$(target): main.cpp
	$(CXX) $(WARNINGS) -o $@ $^


run: $(target)
	./$^ | python3 ./plot.py
