# -*- coding: utf-8 -*-
"""Assignment Code
Question 1
"""

def calculate_name_length(first_name, last_name):
    return len(first_name) + len(last_name)

# Take input from user
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# Calculate total length of first and last name
total_name_length = calculate_name_length(first_name, last_name)

# Convert first name and last name to uppercase
first_name_upper = first_name.upper()
last_name_lower = last_name.lower()

print(f"First name (upper): {first_name_upper}")
print(f"Last name (lower): {last_name_lower}")
print(f"Total length of first and last name: {total_name_length}")


"""Question 2"""

def calculate_circle_area(radius):
    return 3.14 * radius**2

def calculate_rectangle_area(length, width):
    return length * width

def calculate_square_area(side):
    return side**2

def calculate_triangle_area(base, height):
    return 0.5 * base * height


# Display options for shapes
print("Select the shape to calculate its area:")
print("1. Circle")
print("2. Rectangle")
print("3. Square")
print("4. Triangle")

while True:
    # Take user input for shape selection
    shape_choice = int(input("Enter the number corresponding to the shape: "))

    # Calculate and print the area based on the selected shape
    if shape_choice == 1:
        radius = float(input("Enter the radius of the circle: "))
        print("Area of the circle is:", calculate_circle_area(radius))
    elif shape_choice == 2:
        length = float(input("Enter the length of the rectangle: "))
        width = float(input("Enter the width of the rectangle: "))
        print("Area of the rectangle is:", calculate_rectangle_area(length, width))
    elif shape_choice == 3:
        side = float(input("Enter the side length of the square: "))
        print("Area of the square is:", calculate_square_area(side))
    elif shape_choice == 4:
        base = float(input("Enter the base of the triangle: "))
        height = float(input("Enter the height of the triangle: "))
        print("Area of the triangle is:", calculate_triangle_area(base, height))
    else:
        print("Invalid input. Please enter a valid shape number.")
        break


"""Task 3"""

import random
color_palette = ["red", "blue", "green", "yellow", "orange", "purple"]
random_index = random.randint(0, len(color_palette) - 1)
chosen_color = color_palette[random_index]
generated_password = chosen_color[::-1]

print("Chosen color:", chosen_color)
print("Generated password:", generated_password)
