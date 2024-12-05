from concurrent.futures import ThreadPoolExecutor
import time
from ratelimit import limits, sleep_and_retry
import threading

# Rate limit constants
MAX_CALLS = 15  # Max 15 API calls
REFILL_RATE = 60  # In seconds (1 minute)

# Mock data
pages = [{"image_prompt": f"Image {i}"} for i in range(20)]
characters = [{"character_name": "Hero", "character_features": "Tall, strong"}]

# Lock for thread safety
lock = threading.Lock()

# Mocking the DALL-E image generation (using sleep to simulate API delay)
@sleep_and_retry
@limits(calls=MAX_CALLS, period=REFILL_RATE)
def generate_image(page, characters, image_style):
    start_time = time.time()
    print(f"Generating image for page: {page['image_prompt']}")

    # Simulating image generation delay
    time.sleep(2)

    # Mock the image generation (pretend it works)
    image_url = f"https://mock_image_url/{page['image_prompt']}.png"
    page["image_url"] = image_url

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Image generated for {page['image_prompt']} in {time_taken:.2f} seconds.")

    return page

def generate_images_for_picture_book(image_style="default"):
    start_time = time.time()
    print("Starting image generation...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(generate_image, page, characters, image_style) for page in pages]

        # Collect results
        for i, future in enumerate(futures):
            try:
                result = future.result()
                #print(f"Result for page {i}: {result}")
            except Exception as e:
                print(f"Failed to generate image for page {i}: {str(e)}")

    end_time = time.time()
    total_time_taken = end_time - start_time
    print(f"All images generated in {total_time_taken:.2f} seconds.")

# Run the function to test
generate_images_for_picture_book()