# run_simulation.py

from car_simulator import simulate_single_car, simulate_multiple_cars

def main() -> None:
    """
    Demonstrates the use of simulate_single_car and simulate_multiple_cars
    using hardcoded sample inputs.
    """
    # Part 1: Single Car
    print("Single Car Simulation Result:")
    print(simulate_single_car(10, 10, 1, 2, 'N', 'FFRFFFRRLF'))

    # Part 2: Multiple Cars
    print("\nMultiple Car Simulation Result:")
    cars = [
        ('A', (1, 2, 'N'), 'FFRFFFFRRL'),
        ('B', (7, 8, 'W'), 'FFLFFFFFFF'),
    ]
    print(simulate_multiple_cars(10, 10, cars))

if __name__ == "__main__":
    main()
