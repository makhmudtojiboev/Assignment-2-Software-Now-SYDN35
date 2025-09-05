# Makhmud Tojiboev - s395965
# Mohammed Abir Chowdhury - s397008

import turtle

def draw_fractal_edge(t, length, depth):
    """
    A recursive function to draw a single edge of the geometric pattern with an
    inward-pointing indentation.

    Args:
        t (turtle.Turtle): The turtle object used for drawing.
        length (float): The length of the current edge.
        depth (int): The current recursion depth.
    """
    # Base case: If the depth is 0, just draw a straight line.
    if depth == 0:
        t.forward(length)
    else:
        # Recursive step:
        # Divide the edge into three equal segments and replace the middle
        # with two sides of an equilateral triangle pointing inward.
        segment = length / 3
        
        # Segment 1
        draw_fractal_edge(t, segment, depth - 1)
        
        # Segment 2 (Inward pointing side of the equilateral triangle)
        t.right(60)
        draw_fractal_edge(t, segment, depth - 1)
        
        # Segment 3 (The other inward pointing side)
        t.left(120)
        draw_fractal_edge(t, segment, depth - 1)
        
        # Segment 4
        t.right(60)
        draw_fractal_edge(t, segment, depth - 1)

def main():
    """
    Main function to get user input and initiate the drawing process.
    """
    try:
        # Get user input for drawing parameters
        num_sides = int(input("Enter the number of sides: "))
        side_length = float(input("Enter the side length: "))
        recursion_depth = int(input("Enter the recursion depth: "))
        
        # Set up the turtle screen and object
        screen = turtle.Screen()
        screen.title("Recursive Geometric Pattern")
        t = turtle.Turtle()
        t.speed("fastest")
        t.penup()
        
        # Position the turtle to center the drawing
        initial_angle = (180 * (num_sides - 2)) / num_sides
        start_pos_x = -side_length / 2
        
        t.goto(start_pos_x, 0)
        t.pendown()
        
        # Draw the polygon with the fractal edges
        for _ in range(num_sides):
            draw_fractal_edge(t, side_length, recursion_depth)
            t.right(360 / num_sides)
            
        t.hideturtle()
        screen.exitonclick()
        
    except ValueError:
        print("Invalid input. Please enter valid numeric values for all parameters.")

if __name__ == "__main__":
    main()
