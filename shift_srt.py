import sys
import re
from datetime import timedelta

def parse_time(time_str):
    """Convert SRT time string 'HH:MM:SS,mmm' to timedelta."""
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds)
    )

def format_time(td):
    """Convert timedelta back to SRT time string."""
    total_seconds = int(td.total_seconds())
    millis = int(td.microseconds / 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def shift_srt(input_path, output_path, shift_ms):
    """Shift subtitle times by given milliseconds."""
    shift = timedelta(milliseconds=shift_ms)
    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            match = time_pattern.match(line)
            if match:
                start_time = parse_time(match.group(1)) + shift
                end_time = parse_time(match.group(2)) + shift

                # prevent negative times
                if start_time.total_seconds() < 0:
                    start_time = timedelta(0)
                if end_time.total_seconds() < 0:
                    end_time = timedelta(0)

                outfile.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            else:
                outfile.write(line)

    print(f"✅ Subtitles shifted by {shift_ms} ms and saved to '{output_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python shift_srt.py input.srt output.srt shift_ms")
        print("Example: python shift_srt.py movie.srt movie_shifted.srt -1500")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    shift_ms = int(sys.argv[3])

    shift_srt(input_file, output_file, shift_ms)
