import cv2
import numpy as np

def track_ping_pong_ball():
	
	# Initialize camera
	camera = cv2.VideoCapture(0)

	# Run until ESC key has been pressed:
	while cv2.waitKey(1) is not 27:

		# Get video feed
		_, frame = camera.read()

		# Create color HSV color range for orange
		lower_range = np.array([5, 130, 110])
		upper_range = np.array([30, 255, 255])

		# Get HSV values from frame
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Find intersections among hvs and our color range
		mask = cv2.inRange(hsv, lower_range, upper_range)

		# Draw circles around detected circles in mask
		# with_circles = add_border_to_circles(frame, mask)
		# cv2.imshow("Detected Circles", with_circles)

		cv2.imshow("Detected Orange", mask)

	# Shut camera and close out all created windows
	camera.release()
	cv2.destroyAllWindows()

def calibrate_color_mask():

	# Initialize camera
	camera = cv2.VideoCapture(0)

	# Create trackbars to alter the HSV values:
	cv2.namedWindow('Trackbars')
	cv2.createTrackbar("L - H", "Trackbars", 0, 255, lambda x: None)
	cv2.createTrackbar("L - S", "Trackbars", 0, 255, lambda x: None)
	cv2.createTrackbar("L - V", "Trackbars", 0, 225, lambda x: None)
	cv2.createTrackbar("U - H", "Trackbars", 255, 255, lambda x: None)
	cv2.createTrackbar("U - S", "Trackbars", 255, 255, lambda x: None)
	cv2.createTrackbar("U - V", "Trackbars", 255, 255, lambda x: None)

	# Run until ESC key has been pressed
	while cv2.waitKey(1) is not 27:

		# Get video feed
		_, frame = camera.read()
		
		# Read HSV values from trackbar positions:
		l_h = cv2.getTrackbarPos("L - H", "Trackbars")
		l_s = cv2.getTrackbarPos("L - S", "Trackbars")
		l_v = cv2.getTrackbarPos("L - V", "Trackbars")
		u_h = cv2.getTrackbarPos("U - H", "Trackbars")
		u_s = cv2.getTrackbarPos("U - S", "Trackbars")
		u_v = cv2.getTrackbarPos("U - V", "Trackbars")

		# Use trackbar HSV values to create color range for image mask:
		lower_range = np.array([l_h, l_s, l_v])
		upper_range = np.array([u_h, u_s, u_v])

		# Get HSV values from frame:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Create and display masked frame:
		mask = cv2.inRange(hsv, lower_range, upper_range)
		cv2.imshow("Masked", mask)

	# Shut camera and close out created windows
	camera.release()
	cv2.destroyAllWindows()

def add_border_to_circles(og_frame, output_frame):

	# Make copy of original frame
	with_circles = output_frame.copy()

	# Convert to black and white
	bw_frame = cv2.cvtColor(og_frame, cv2.COLOR_BGR2GRAY)

	# Detect circles in b&w frame
	circles = cv2.HoughCircles(bw_frame, cv2.HOUGH_GRADIENT, 1.2, 100)

	# If circles have been detected
	if circles is not None:
		circles = np.round(circles[0, :]).astype('int')

		# Add circle bounds to frame
		for (x, y, r) in circles:
			cv2.circle(
				with_circles,  # The image to draw the circle on
				(x, y),  # The coordinates of the center of the circle
				r,       # The radius of the circle
				(17, 202, 190),  # The HSV color values of drawn circle, I went with orange
				4        # The thickness of drawn circle
			)
	
	return np.hstack([output_frame, with_circles])



if __name__ == '__main__':
	track_ping_pong_ball()
