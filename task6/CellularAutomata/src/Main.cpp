
#include "Life.h"

int main() {

	Life life;

	while (life.window.isOpen()) {
		life.handle();
		life.update();
		life.render();
	}

	return 0;
}




