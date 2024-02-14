import moviepy.editor as mp
import os
import speech_recognition as sr

def download_youtube_video(video_url):
    from pytube import YouTube

    # Download the YouTube video
    yt = YouTube(video_url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    video.download(filename="youtube_video.mp4")

def split_and_save_audio(input_audio_path, output_dir, segment_length=20):
    # Load the audio file
    try:
        audio = mp.AudioFileClip(input_audio_path)
    except Exception as e:
        print(f"Error loading audio file {input_audio_path}: {e}")
        return

    # Get the total duration of the audio file
    total_duration = audio.duration

    # Calculate the number of segments
    num_segments = int(total_duration // segment_length) + 1

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract and save each segment
    for i in range(num_segments):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, total_duration)
        segment = audio.subclip(start_time, end_time)
        output_path = os.path.join(output_dir, f"segment_{i}.wav")
        segment.write_audiofile(output_path, codec='pcm_s16le')  # Save as WAV
        print(f"Segment {i} saved to {output_path}")

    # Close the audio clip
    audio.close()

def transcribe_audio_files(audio_dir, output_file):
    # Initialize a recognizer
    recognizer = sr.Recognizer()

    # Open the output file in append mode
    with open(output_file, "a") as file:
        # Iterate through each audio file in the directory
        for filename in sorted(os.listdir(audio_dir)):
            if filename.endswith(".wav"):  # Change the extension to .wav
                audio_path = os.path.join(audio_dir, filename)

                # Load the audio file
                try:
                    with sr.AudioFile(audio_path) as source:
                        # Perform speech recognition
                        audio_data = recognizer.record(source)
                        transcribed_text = recognizer.recognize_google(audio_data)

                        # Write the transcribed text to the output file
                        file.write(f"Transcription for {filename}:\n")
                        file.write(transcribed_text + "\n\n")
                except Exception as e:
                    print(f"Error transcribing audio file {audio_path}: {e}")

if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=2Ae6MZ878yc"  # Replace with your YouTube video URL
    download_youtube_video(video_url)

    input_audio_path = "youtube_video.mp4"  # Replace with your audio file path
    output_dir = "output_segments"  # Output directory for segments
    output_file = "transcribed_text.txt"  # Output file for transcriptions

    # Get the total duration of the audio file
    audio = mp.AudioFileClip(input_audio_path)
    total_duration = audio.duration
    audio.close()

    # Split and save audio with segments of 20 seconds
    split_and_save_audio(input_audio_path, output_dir)

    # Transcribe audio segments
    transcribe_audio_files(output_dir, output_file)
