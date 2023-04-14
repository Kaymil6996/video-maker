import os
import json
import random
import textwrap
from moviepy.editor import *

def get_quotes_from_json(file_path):
    with open(file_path, 'r') as file:
        quotes_data = json.load(file)
    return quotes_data


def create_video(quote, background_video, output_file):
    max_duration = 20  # Define the maximum duration for the text overlay

    # Load background video and get its duration
    video = VideoFileClip(background_video)
    video_duration = video.duration

    # Adjust font size and wrap text based on the length of the quote
    if len(quote) <= 50:
        fontsize = 40
        wrap_length = 25
    elif len(quote) <= 80:
        fontsize = 30
        wrap_length = 30
    else:
        fontsize = 20
        wrap_length = 40

    wrapped_quote = "\n".join(textwrap.wrap(quote, wrap_length))

    # Create a TextClip with the given quote
    text_duration = min(video_duration, max_duration)
    text = TextClip(wrapped_quote, fontsize=fontsize, color='white', font='Arial').set_duration(text_duration).fadein(1)

    # Overlay the text on the video
    result = CompositeVideoClip([video, text.set_position(("center", "center"))])

    # Add logo and 'Check out bio' text
    logo = ImageClip('logo.png').set_duration(text_duration).resize(height=150).set_position(("center", video.h * 0.15)).fadein(1)
    logo_position = ("center", video.h - logo.h + 100)  # Calculate the position of the logo
    check_bio = TextClip("Check out bio", fontsize=34, color="white", font="Arial").set_duration(text_duration).set_position(("center", logo_position[1] - 200)).fadein(1)

    # Overlay the logo and 'Check out bio' text on the video
    result = CompositeVideoClip([result, logo, check_bio])

    # Write the video to a file
    result.write_videofile(output_file, codec='libx264', fps=30)





def main():
    # Load quotes from JSON file
    quotes = get_quotes_from_json('quotes.json')

    # Get list of background videos
    background_videos = [f for f in os.listdir('videos') if f.endswith('.mp4')]

    # Prompt user for the number of videos to generate
    num_videos = int(input("Enter the number of videos to generate: "))

    for i in range(num_videos):
        # Randomly select a quote and background video
        quote = random.choice(quotes)
        background_video = random.choice(background_videos)

        # Generate output video filename
        output_filename = f'output_{i + 1}.mp4'

        # Create and save the video
        create_video(quote, os.path.join('videos', background_video), output_filename)
        print(f"Generated video: {output_filename}")

if __name__ == "__main__":
    main()
