
#include "Life.h"

Cell::Cell() { 
	state = SUSCEPTIBLE; 
}

CELL_STATE Cell::getState() const { 
	return state;
}

void Cell::setState(CELL_STATE newState) { 
	state = newState; 
}

Life::Life() {
	window.create(
		sf::VideoMode(
			WINDOW_WIDTH_IN_CELLS * SIDE_SIZE_PX, WINDOW_HEIGHT_IN_CELLS * SIDE_SIZE_PX
		),
		WINDOW_TITLE,
		sf::Style::Titlebar);
	window.setPosition(sf::Vector2i(WINDOW_POSITION_X, WINDOW_POSITION_Y));
	initCells();
	std::srand(std::time(nullptr));
}

void Life::handle() {
	sf::Event event;
	while (window.pollEvent(event)) {
		if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Escape) {
			window.close();
		} else if (event.type == sf::Event::MouseButtonPressed && numbersOfStartCellsCounter != 0) {
			isClick = true;
			mousePosition = sf::Mouse::getPosition(window);
		}
	}
}

void Life::update() {
	if (numbersOfStartCellsCounter != 0) {
		std::string title = WINDOW_TITLE;
		title.append(": ");
		title.append(std::to_string(numbersOfStartCellsCounter));
		window.setTitle(title);
	} else {
		window.setTitle(WINDOW_TITLE);
	}

	if (getIsUpdateStart() == false && 
		animationClock.getElapsedTime().asMilliseconds() > ANIMATION_SPEED_IN_MILLISECONDS) {
		updateInfection();
	}

	for (Cell& cell : cells) {
		switch (cell.getState()) {
			case SUSCEPTIBLE:
				cell.setFillColor(sf::Color(SUSCEPTIBLE_CELL_FILL_COLOR_RGBA));
				break;
			case INFECTED:
				cell.setFillColor(sf::Color(INFECTED_CELL_FILL_COLOR_RGBA));
				break;
			case RECOVERED:
				cell.setFillColor(sf::Color(RECOVERED_CELL_FILL_COLOR_RGBA));
				break;
		}
	}
}

void Life::render() {
	window.clear(sf::Color(WINDOW_BACKGROUND_RGBA));

	for (Cell& cell : cells) {
		window.draw(cell);
	}

	window.display();
}

void Life::initCells() {
	for (int i = 0; i < WINDOW_HEIGHT_IN_CELLS; i++) {
		for (int j = 0; j < WINDOW_WIDTH_IN_CELLS; j++) {
			Cell cell;
			cell.setPosition(j * SIDE_SIZE_PX, i * SIDE_SIZE_PX);
			cell.setSize(sf::Vector2f(SIDE_SIZE_PX, SIDE_SIZE_PX));
			cell.setFillColor(sf::Color(SUSCEPTIBLE_CELL_FILL_COLOR_RGBA));
			cell.setOutlineThickness(-WINDOW_GRID_THICKNESS_IN_PX / 2.0);
			cell.setOutlineColor(sf::Color(WINDOW_GRID_RGBA));
			cells.push_back(cell);
		}
	}
}

bool Life::getIsUpdateStart() {
	if (numbersOfStartCellsCounter == 0) {
		return false;
	}
	if (isClick) {
		for (Cell& cell : cells) {
			if (cell.getGlobalBounds().contains(mousePosition.x, mousePosition.y) && cell.getState() != INFECTED) {
				cell.setState(INFECTED);
				isClick = false;
				numbersOfStartCellsCounter--;
			} else if (cell.getGlobalBounds().contains(mousePosition.x, mousePosition.y) && cell.getState() == INFECTED) {
				cell.setState(SUSCEPTIBLE);
				isClick = false;
				numbersOfStartCellsCounter++;
			}
		}
	}
	animationClock.restart();
	for (Cell& cell : cells) {
		cell.timer.restart();
	}
	return true;
}

void Life::updateInfection() {
	for (int i = 0; i < cells.size(); i++) {
		if (cells[i].getState() == SUSCEPTIBLE) {
			int numberOfNearInfectedCells = getNumOfNearInfectedCells(i);
			if (numberOfNearInfectedCells > 0) {
				infectWithProbability(cells[i], numberOfNearInfectedCells, i);
			}
		}
		if (cells[i].getState() == INFECTED && cells[i].timer.getElapsedTime().asSeconds() > T_RECOVER_IN_SECONDS) {
			cells[i].setState(RECOVERED);
		}
	}
	for (int i = 0; i < bufferInfectionedCells.size(); i++) {
		cells[bufferInfectionedCells[i]].setState(INFECTED);
		cells[bufferInfectionedCells[i]].timer.restart();
	}
	bufferInfectionedCells.clear();
	animationClock.restart();
}

void Life::infectWithProbability(Cell& cell, int& numberOfNearInfectedCells, int& cellIndex) {
	float probabilityOfInfection = 1 - pow(1 - P_INFECT, numberOfNearInfectedCells);
	float randFloatZeroToOne = float(std::rand()) / RAND_MAX;
	if (randFloatZeroToOne < P_INFECT) {
		bufferInfectionedCells.push_back(cellIndex);
	}
}

int Life::getNumOfNearInfectedCells(int& cellIndex) {
	int infectedCounter = 0;
	std::vector<int> neighbors;
	neighbors.push_back(cellIndex - WINDOW_WIDTH_IN_CELLS - 1);
	neighbors.push_back(cellIndex - WINDOW_WIDTH_IN_CELLS);
	neighbors.push_back(cellIndex - WINDOW_WIDTH_IN_CELLS + 1);
	neighbors.push_back(cellIndex + WINDOW_WIDTH_IN_CELLS - 1);
	neighbors.push_back(cellIndex + WINDOW_WIDTH_IN_CELLS);
	neighbors.push_back(cellIndex + WINDOW_WIDTH_IN_CELLS + 1);
	neighbors.push_back(cellIndex - 1);
	neighbors.push_back(cellIndex + 1);
	for (int& neighborIndex : neighbors) {
		if (neighborIndex >= 0 && neighborIndex < cells.size()) {
			if (cells[neighborIndex].getState() == INFECTED) {
				infectedCounter++;
			}
		}
	}
	return infectedCounter;
}



