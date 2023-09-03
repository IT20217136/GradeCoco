import cv2
import numpy as np

def calculate_color_and_size(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection to find edges
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    
    # Perform dilation to make lines thicker and easier to detect
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Find contours in the dilated image for color detection
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculate the number of black lines (contours)
    num_lines = len(contours)
    
    # Determine the color grade based on the number of lines
    if num_lines > 20:
        color_grade = 'A'
    elif num_lines < 5:
        color_grade = 'C'
    else:
        color_grade = 'B'
    
    # Convert the image to grayscale for size detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the image to separate the objects from the background
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Find the contours of the objects in the image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate the area of the largest object for size detection
    area = cv2.contourArea(largest_contour)

    # Categorize the size based on the area value
    if area < 95000:
        size = "L"
    elif 95000 <= area < 190000:
        size = "M"
    else:
        size = "S"

    return color_grade, size

def map_to_final_grade(color_grade, size_grade):
    final_grade_map = {
        ('A', 'S'): 'B',
        ('A', 'M'): 'A',
        ('A', 'L'): 'A',
        ('B', 'S'): 'B',
        ('B', 'M'): 'B',
        ('B', 'L'): 'A',
        ('C', 'S'): 'C',
        ('C', 'M'): 'C',
        ('C', 'L'): 'C'
    }
    return final_grade_map.get((color_grade, size_grade), 'N/A')

# Example usage
if __name__ == "__main__":
    image_path = 'test4.jpg'  # Replace with the path to your image
    result_color, result_size = calculate_color_and_size(image_path)
    final_grade = map_to_final_grade(result_color, result_size)
    print(f"Color Grade: {result_color}")
    print(f"Size Grade: {result_size}")
    print(f"Final Grade: {final_grade}")
