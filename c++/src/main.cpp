#include <iostream>

#include "program.hpp"

Program *program = nullptr;

static int WIDTH = 1000;
static int HEIGHT = 1000;

int main()
{
    const float FPS = 60;
    const float frameDelay = 1000.0f / FPS;

    Uint32 frameStart;
    int frameTime;

    program = new Program();
    program->init("CUDA METABALLS", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WIDTH, HEIGHT, false);
    while(program->running())
    {
        frameStart = SDL_GetTicks();

        program->handleEvents();
        program->update();
        program->render();

        frameTime = SDL_GetTicks() - frameStart;
        if (frameDelay > frameTime)
        {
            SDL_Delay(frameDelay - frameTime);
        }
        program->deltaTime = (float)((SDL_GetTicks() - frameStart) / 1000.0f);
    }

    program->clean();
    free(program);
    return 0;
}