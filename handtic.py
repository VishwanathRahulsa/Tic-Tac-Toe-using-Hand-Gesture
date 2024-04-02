import cv2
import pyautogui

# Tic Tac Toe game variables
board = [' '] * 9
player = 'X'

# Open the webcam
cap = cv2.VideoCapture(0)

def check_winner():
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] != ' ':
            return board[i*3]  # Return the winner (X or O)
        if board[i] == board[i+3] == board[i+6] != ' ':
            return board[i]    # Return the winner (X or O)
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]
    return None  # No winner yet

while True:
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply a Gaussian blur to reduce noise and improve accuracy
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use the Canny edge detection algorithm
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge map
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour (assuming it's the hand)
        max_contour = max(contours, key=cv2.contourArea)
        
        # Get the centroid of the largest contour
        M = cv2.moments(max_contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # Determine the cell based on the centroid's position
        row = cy // 100
        col = cx // 100
        
        # Make a move in the Tic Tac Toe game
        if 0 <= row < 3 and 0 <= col < 3 and board[row * 3 + col] == ' ':
            board[row * 3 + col] = player
            player = 'X' if player == 'O' else 'O'
        
    # Draw the Tic Tac Toe board on the frame
    for i in range(1, 3):
        cv2.line(frame, (0, i * 100), (300, i * 100), (0, 0, 255), 2)
        cv2.line(frame, (i * 100, 0), (i * 100, 300), (0, 0, 255), 2)
    
    for i in range(3):
        for j in range(3):
            if board[i * 3 + j] != ' ':
                cv2.putText(frame, board[i * 3 + j], (j * 100 + 30, i * 100 + 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                
       # Check for a winner
    winner = check_winner()
    if winner:
        print(f"Player {winner} wins!")
        break
    
    cv2.imshow("Hand Gesture and Tic Tac Toe", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
