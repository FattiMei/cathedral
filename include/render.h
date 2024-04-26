#ifndef __RENDER_H__
#define __RENDER_H__


#include "processing.h"


void render_init(int width, int height);
void render_resize(int width, int height);
void render_present();
void render_cleanup();


void render_send_points(const Track &T);


#endif
