#pragma once
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <vector>

class Program
{
public:
    Program();
    ~Program();

    void init(const char* title, int xpos, int ypos, int width, int height, bool fullscreen);

    void handleEvents();
    void update();
    void render();
    void clean();

    bool running()
    {
        return isRunning;
    }

    static SDL_Renderer *renderer;
    static SDL_Event event;
    static int mouse_x;
    static int mouse_y;
    static float deltaTime;

private:
    int count = 0;
    bool isRunning;
    SDL_Window *window;
};