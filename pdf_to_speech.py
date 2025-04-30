import os
from modules.logger import get_logger
from logging import DEBUG, INFO
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from google.cloud import texttospeech
# from time import sleep

# Load environment variables
load_dotenv()


class PDFToSpeechConverter:
    def __init__(self) -> None:
        # Initialize Google Cloud client
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"
        self.client = texttospeech.TextToSpeechClient()

    def extract_text_from_pdf(self, pdf_path) -> str:
        """Extract text from a PDF file."""
        log.debug(f"Extracting text from {pdf_path}...")
        text = ""
        # Open the PDF file
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def split_text(self, text, max_chars=4950) -> list:
        """
        Split text into chunks that are small enough for the API.
        Google Text-to-Speech has a limit of 5000 characters per
        request.
        (found errors when using 5000 characters so reduced to 4950)
        """
        log.debug(f"Splitting text into chuncks of {max_chars} charaters")
        chunks = []
        while len(text) > max_chars:
            # Find the last space within the limit
            split_at = text.rfind(' ', 0, max_chars)
            log.debug(f"Splitting text at {split_at} characters.")
            if split_at == -1:
                split_at = max_chars
                log.debug(f"Splitting at max_chars: {max_chars} characters.")
            chunks.append(text[:split_at])
            text = text[split_at:].lstrip()
        chunks.append(text)
        return chunks

    def text_to_speech(self, text, output_file="output/output.mp3") -> None:
        """
        Convert text to speech using Google Cloud Text-to-Speech API.
        """
        log.debug("Converting text to Speech...")
        # Split text into manageable chunks
        text_chunks = self.split_text(text)
        audio_content = bytearray()

        for i, chunk in enumerate(text_chunks):
            log.info(f"Processing chunk {i+1}/{len(text_chunks)}...")
            log.debug(f"Chunk length: {len(chunk)} characters, " +
                      f"{len(chunk.split())} words")
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=chunk)

            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Standard-F",  # Female voice
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Concatenate the audio chunks
            audio_content.extend(response.audio_content)

            # Pause for a short duration to avoid hitting API limits
            # sleep(0.1)
            log.debug(f"Chunk {i+1} processed.")

        log.debug("All chnunks processed.")
        log.debug(f"Total audio length: {len(audio_content)} bytes")

        # Save the complete audio to file
        log.debug(f"Writing audio content to file '{output_file}'...")
        with open(output_file, "wb") as out:
            out.write(audio_content)
            log.info(f"Audio content written to file '{output_file}'")

    def convert_pdf_to_speech(self, pdf_path: str,
                              output_file="output.mp3") -> None:
        """
        Full pipeline: PDF -> Text -> Speech
        """
        text = self.extract_text_from_pdf(pdf_path)
        log.debug(f"\nExtraxted text:\n\n{text}\n")
        log.debug(
            f"Text length: {len(text)} characters, " +
            f"{len(text.split())} words"
            )
        self.text_to_speech(text, output_file)


def is_valid_pdf(file_path: str) -> bool:
    """
    Check if the file exists and has a valid .pdf extension.
    Args:
        file_path (str): The path to the file to be checked.
    Returns:
        bool: True if the file exists and has a .pdf extension,
        False otherwise.
    """
    # Check if the path exists and is a file (not a directory)
    if not os.path.isfile(file_path):
        log.info(f"Error: Path '{file_path}' does not exist or is not a file.")
        return False
    # Check if the file has a .pdf extension (case insensitive)
    if not file_path.lower().endswith('.pdf'):
        log.info(f"Error: File '{file_path}' does not have a .pdf extension.")
        return False
    return True


def get_valid_pdf_path(default_path: str) -> str:
    """
    Prompt the user for a file path until a valid PDF file is provided.
    Returns:
        str: The valid PDF file path.
    """
    while True:
        # Ask the user for a file path
        file_path = input(
            "Please enter path to PDF file (default: " +
            f"{default_path}): ").strip()
        # Check if the path is empty and set a default value
        if not file_path:
            file_path = default_path
            log.debug(f"No PDF file path provided so default {file_path} used")
        # Check if the path is valid and has PDF extension
        if is_valid_pdf(file_path):
            log.debug("Valid PDF file found!")
            return file_path
        # If not valid, explain what's needed and try again
        print("\nThe provided path must:")
        print("- Point to an existing file (not a directory)")
        print("- Have a '.pdf' extension (case doesn't matter)")
        print("Please try again.\n")


def main() -> None:
    """
    Main function to run the PDF to speech conversion.
    """
    pdf_file = get_valid_pdf_path("input/test.pdf")
    log.debug(f"File '{pdf_file}' exists and is a PDF file.")
    output_file = input(
        "Enter the output MP3 file name (default: output/output.mp3): "
        ) or "output/output.mp3"
    log.debug(f"Output file name: {output_file}")
    log.debug("Starting conversion...")
    converter = PDFToSpeechConverter()
    converter.convert_pdf_to_speech(pdf_file, output_file)


if __name__ == "__main__":
    log = get_logger("pdf_to_speech_app", DEBUG)
    log.debug("Starting PDF to Speech conversion app")
    main()
    log.debug("PDF to Speech conversion app finished")
