
#pragma once

#include <SFML/Graphics.hpp>

#include <iostream>

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

// Window styles

#define WINDOW_TITLE "Cellular Automata"
#define WINDOW_WIDTH_IN_CELLS 75
#define WINDOW_HEIGHT_IN_CELLS 40
#define WINDOW_POSITION_X 100
#define WINDOW_POSITION_Y 50
#define WINDOW_BACKGROUND_RGBA 255, 255, 255, 255
#define WINDOW_GRID_RGBA 0, 0, 0, 255
#define WINDOW_GRID_THICKNESS_IN_PX 1

// Cells styles

#define SIDE_SIZE_PX 20
#define SUSCEPTIBLE_CELL_FILL_COLOR_RGBA 0, 0, 0, 0
#define INFECTED_CELL_FILL_COLOR_RGBA 0, 0, 0, 255
#define RECOVERED_CELL_FILL_COLOR_RGBA 0, 0, 0, 255 / 2


// Cells parameters

enum CELL_STATE {SUSCEPTIBLE, INFECTED, RECOVERED};

#define P_INFECT 0.02
#define T_RECOVER_IN_SECONDS 2

#define NUMBERS_OF_START_CELLS 5
#define ANIMATION_SPEED_IN_MILLISECONDS 20

////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

class Cell : public sf::RectangleShape {
private:
	CELL_STATE state;
public:
	Cell();
	void setState(CELL_STATE state);
	CELL_STATE getState() const;
	sf::Clock timer;
};

class Life {
public:
	Life();
	void handle();
	void update();
	void render();
	sf::RenderWindow window;

private:
	std::vector<Cell> cells;
	void initCells();
	int numbersOfStartCellsCounter = NUMBERS_OF_START_CELLS;
	bool isClick = false;
	bool isStart = false;
	sf::Vector2i mousePosition;
	bool getIsUpdateStart();
	void updateInfection();
	int getNumOfNearInfectedCells(int&);
	void infectWithProbability(Cell&, int&, int&);
	sf::Clock animationClock;
	std::vector<int> bufferInfectionedCells;
};



