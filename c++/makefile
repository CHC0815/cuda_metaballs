CC = g++
INCLUDES = -I. -I./src -I./SDL/include/SDL2 -I./SDL_Image/include/SDL2
# LDFLAGS = -L./SDL/lib -L./SDL_Image/lib -lSDL2main -lSDL2 -lSDL2_image
LDFLAGS = -lSDL2main -lSDL2 -lSDL2_image
CFLAGS = -Wall -std=gnu++17  $(INCLUDES)

SRC = $(wildcard src/*.cpp)
OBJ = $(patsubst %.cpp,%.o,$(SRC))
DEPS = $(wildcard src/*.hpp)

%.o: %.cpp $(DEPS)
	$(CC) $(CFLAGS) -o $@ -c $<

main: $(OBJ)
	$(CC) $^ $(LDFLAGS) -o bin/$@

crun: clean main
	./bin/main

run:
	./bin/main

.PHONY: clean
clean:
	rm -f src/*.o bin/main