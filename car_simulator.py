from typing import List, Tuple, Optional, Union

DIRECTION_ORDER = ['N', 'E', 'S', 'W']
MOVES = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0)
}

class Car:
    """
    Represents a self-driving car on a bounded rectangular grid.

    Attributes:
        x (int): Current x-coordinate of the car.
        y (int): Current y-coordinate of the car.
        direction (str): Current facing direction ('N', 'E', 'S', 'W').
        name (Optional[str]): Optional name/identifier for the car.
        history (List[Tuple[int, int]]): Position history after each command.
    """

    def __init__(self, x: int, y: int, direction: str, name: Optional[str] = None):
        """
        Initializes a Car object.

        Args:
            x (int): Starting x-coordinate.
            y (int): Starting y-coordinate.
            direction (str): Starting direction ('N', 'E', 'S', 'W').
            name (Optional[str]): Optional car identifier.
        """
        self.x: int = x
        self.y: int = y
        self.direction: str = direction
        self.name: Optional[str] = name
        self.history: List[Tuple[int, int]] = [(x, y)]

    def rotate(self, turn: str) -> None:
        """
        Rotates the car 90 degrees left ('L') or right ('R').

        Args:
            turn (str): 'L' or 'R' indicating rotation direction.
        """
        idx = DIRECTION_ORDER.index(self.direction)
        if turn == 'L':
            self.direction = DIRECTION_ORDER[(idx - 1) % 4]
        elif turn == 'R':
            self.direction = DIRECTION_ORDER[(idx + 1) % 4]

    def next_position(self) -> Tuple[int, int]:
        """
        Returns the next position if the car moves forward.

        Returns:
            Tuple[int, int]: (x, y) coordinates of the next step.
        """
        dx, dy = MOVES[self.direction]
        return self.x + dx, self.y + dy

    def move_forward(self, width: int, height: int) -> None:
        """
        Moves the car forward by 1 step if within bounds.

        Args:
            width (int): Field width.
            height (int): Field height.
        """
        nx, ny = self.next_position()
        if 0 <= nx < width and 0 <= ny < height:
            self.x, self.y = nx, ny
        self.history.append((self.x, self.y))

    def execute_command_step(self, command: Optional[str], width: int, height: int) -> None:
        """
        Executes a single command ('F', 'L', 'R') for the car.

        Args:
            command (Optional[str]): Command character, or None to stay put.
            width (int): Field width.
            height (int): Field height.
        """
        if command is None:
            self.history.append((self.x, self.y))
            return
        if command in 'LR':
            self.rotate(command)
            self.history.append((self.x, self.y))
        elif command == 'F':
            self.move_forward(width, height)

    def position(self) -> Tuple[int, int, str]:
        """
        Gets the current position and direction of the car.

        Returns:
            Tuple[int, int, str]: (x, y, direction) of the car.
        """
        return self.x, self.y, self.direction


def simulate_single_car(
    width: int,
    height: int,
    x: int,
    y: int,
    direction: str,
    commands: str
) -> Tuple[int, int, str]:
    """
    Simulates a single car's movement based on commands.

    Args:
        width (int): Width of the field.
        height (int): Height of the field.
        x (int): Starting x-coordinate.
        y (int): Starting y-coordinate.
        direction (str): Starting direction ('N', 'E', 'S', 'W').
        commands (str): Sequence of commands ('F', 'L', 'R').

    Returns:
        Tuple[int, int, str]: Final position and direction of the car.
    """
    car = Car(x, y, direction)
    for cmd in commands:
        car.execute_command_step(cmd, width, height)
    return car.position()


def simulate_multiple_cars(
    width: int,
    height: int,
    cars_with_commands: List[Tuple[str, Tuple[int, int, str], str]]
) -> Union[str, Tuple[str, str, Tuple[int, int], int]]:
    """
    Simulates multiple cars moving in parallel, step-by-step.

    Detects if any two or more cars try to move to the same tile at the same step.

    Args:
        width (int): Width of the field.
        height (int): Height of the field.
        cars_with_commands (List[Tuple[str, Tuple[int, int, str], str]]): 
            List of cars with their names, start positions, directions, and commands.

    Returns:
        Union[str, Tuple[str, str, Tuple[int, int], int]]:
            - 'no collision' if all cars move safely.
            - Or string in the form:
              "<car1> <car2>\n<x> <y>\n<step>" if a collision occurs.
    """
    cars: List[Car] = []
    commands_map: dict[str, str] = {}

    max_steps = 0
    for name, (x, y, d), commands in cars_with_commands:
        car = Car(x, y, d, name)
        cars.append(car)
        commands_map[name] = commands
        max_steps = max(max_steps, len(commands))

    # Step 0: Check initial collision
    seen_positions: dict[Tuple[int, int], str] = {}
    for car in cars:
        pos = car.history[0]
        if pos in seen_positions:
            return f"{seen_positions[pos]} {car.name}\n{pos[0]} {pos[1]}\n0"
        seen_positions[pos] = car.name

    # Step 1 onward
    for step in range(1, max_steps + 1):
        future_positions: dict[Tuple[int, int], List[str]] = {}
        current_positions = {}

        for car in cars:
            current_positions[car.name] = (car.x, car.y)

        # Preview next positions
        for car in cars:
            command = commands_map[car.name][step - 1] if step - 1 < len(commands_map[car.name]) else None

            if command == 'F':
                nx, ny = car.next_position()
                if 0 <= nx < width and 0 <= ny < height:
                    future_positions.setdefault((nx, ny), []).append(car.name)
                else:
                    future_positions.setdefault((car.x, car.y), []).append(car.name)
            else:
                future_positions.setdefault((car.x, car.y), []).append(car.name)

        # Detect collisions before moving
        for pos, names in future_positions.items():
            if len(names) > 1:
                return f"{' '.join(sorted(names))}\n{pos[0]} {pos[1]}\n{step}"

        # No collision, now actually move
        for car in cars:
            command = commands_map[car.name][step - 1] if step - 1 < len(commands_map[car.name]) else None
            car.execute_command_step(command, width, height)

    return "no collision"
