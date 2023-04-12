# Run a test message ticker
import time

from display.display import Display
from display.display_content import DisplayContent


display: Display = Display()
test_message: str = "Hello this is a test message. The weather is fantastic today in MTL! 16081990."
print(test_message)

for i in range(len(test_message) - 4):
    time.sleep(0.3)
    excerpt: str = test_message[i:i + 4]
    print(excerpt)
    display_content: DisplayContent = DisplayContent(excerpt)
    print(display_content)
    display.set_content(display_content)

time.sleep(0.3)
display.set_content(None)
