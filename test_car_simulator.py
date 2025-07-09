# test_car_simulator.py

import unittest
from car_simulator import simulate_single_car, simulate_multiple_cars

class TestAutoDrivingCar(unittest.TestCase):
    """
    Unit tests for the auto-driving car simulator.
    """

    def test_part1_sample(self) -> None:
        """Tests final output for Part 1 sample input."""
        result = simulate_single_car(10, 10, 1, 2, 'N', 'FFRFFFRRLF')
        self.assertEqual(result, (4, 3, 'S'))

    def test_part2_sample_collision(self) -> None:
        """Tests collision detection for Part 2 sample input."""
        cars = [
            ('A', (1, 2, 'N'), 'FFRFFFFRRL'),
            ('B', (7, 8, 'W'), 'FFLFFFFFFF'),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'A B\n5 4\n7')

    def test_part2_no_collision(self) -> None:
        """Tests that no collision is correctly reported."""
        cars = [
            ('A', (0, 0, 'N'), 'FF'),
            ('B', (9, 9, 'S'), 'FF'),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'no collision')

    def test_boundary_ignored(self) -> None:
        """Tests that out-of-bound forward moves are ignored."""
        result = simulate_single_car(5, 5, 0, 0, 'S', 'F')
        self.assertEqual(result, (0, 0, 'S'))

    def test_rotate_wraparound(self) -> None:
        """Tests that four right turns return to original direction."""
        result = simulate_single_car(5, 5, 2, 2, 'N', 'RRRR')
        self.assertEqual(result, (2, 2, 'N'))

    def test_full_turn_left(self) -> None:
        """Tests that four left turns return to original direction."""
        result = simulate_single_car(5, 5, 2, 2, 'E', 'LLLL')
        self.assertEqual(result, (2, 2, 'E'))

    def test_single_car_long_path(self) -> None:
        """Tests a long, looping movement path."""
        commands = 'FFRFFRFFRFF'
        result = simulate_single_car(10, 10, 0, 0, 'N', commands)
        self.assertEqual(result, (0, 0, 'W'))

    def test_collision_on_start(self) -> None:
        """Tests collision at initial position (step 0)."""
        cars = [
            ('A', (2, 2, 'N'), ''),
            ('B', (2, 2, 'S'), ''),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'A B\n2 2\n0')

    def test_collision_due_to_sync_move(self) -> None:
        """Tests collision from two cars moving into the same tile at same step."""
        cars = [
            ('A', (0, 0, 'E'), 'FF'),
            ('B', (2, 0, 'W'), 'FF'),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'A B\n1 0\n1')

    def test_path_overlap_no_collision(self) -> None:
        """Tests cars crossing paths at different times (no collision)."""
        cars = [
            ('A', (0, 0, 'E'), 'FFF'),
            ('B', (3, 0, 'W'), 'FFF'),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'no collision')

    def test_different_command_lengths(self) -> None:
        """Tests collision detection with unequal command lengths."""
        cars = [
            ('A', (0, 0, 'N'), 'FFFFFFFF'),
            ('B', (0, 4, 'S'), 'F'),
        ]
        result = simulate_multiple_cars(10, 10, cars)
        self.assertEqual(result, 'A B\n0 3\n3')

    def test_corner_blocked(self) -> None:
        """Tests movement ignored at upper boundary."""
        result = simulate_single_car(3, 3, 2, 2, 'N', 'F')
        self.assertEqual(result, (2, 2, 'N'))

if __name__ == "__main__":
    unittest.main()
