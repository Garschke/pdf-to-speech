import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from google.cloud import texttospeech

# Load environment variables
load_dotenv()


class PDFToSpeechConverter:
    def __init__(self):
        # Initialize Google Cloud client
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"
        self.client = texttospeech.TextToSpeechClient()

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        print(f"Extracting text from {pdf_path}...")
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def split_text(self, text, max_chars=5000):
        """
        Split text into chunks that are small enough for the API.
        Google Text-to-Speech has a limit of 5000 characters per
        request.
        """
        chunks = []
        while len(text) > max_chars:
            # Find the last space within the limit
            split_at = text.rfind(' ', 0, max_chars)
            if split_at == -1:
                split_at = max_chars
            chunks.append(text[:split_at])
            text = text[split_at:].lstrip()
        chunks.append(text)
        return chunks

    def text_to_speech(self, text, output_file="output.mp3"):
        """
        Convert text to speech using Google Cloud Text-to-Speech API.
        """
        print("Converting text to speech...")

        # Split text into manageable chunks
        text_chunks = self.split_text(text)
        audio_content = bytearray()

        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i+1}/{len(text_chunks)}...")

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

        # Save the complete audio to file
        with open(output_file, "wb") as out:
            out.write(audio_content)
            print(f"Audio content written to file '{output_file}'")

    def convert_pdf_to_speech(self, pdf_path, output_file="output.mp3"):
        """
        Full pipeline: PDF -> Text -> Speech
        """
        text = self.extract_text_from_pdf(pdf_path)
        print(f"\nExtraxted text:\n\n{text}")
        print(
            f"Text length: {len(text)} characters, " +
            f"{len(text.split())} words"
            )
        self.text_to_speech(text, output_file)


if __name__ == "__main__":
    converter = PDFToSpeechConverter()
    pdf_file = input("Enter the path to your PDF file: ")
    output_file = input(
        "Enter the output MP3 file name (default: output.mp3): "
        ) or "output.mp3"
    converter.convert_pdf_to_speech(pdf_file, output_file)
