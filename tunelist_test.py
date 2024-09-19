import unittest
from unittest.mock import patch
import os

from tunelist import find_music_files, extract_metadata

class TestMusicFileFinder(unittest.TestCase):

    @patch('os.walk')
    @patch('tunelist.extract_metadata')
    def test_find_single_mp3_file(self, mock_metadata, mock_walk):
        # Mocka os.walk för att returnera en katalogstruktur
        mock_walk.return_value = [
            ('/music', ('subdir',), ('song1.mp3',))
        ]

        mock_metadata.return_value = {'artist': 'Unknown', 'title': 'Unknown', 'bpm': 130}

        result = find_music_files('/music')

        expected_result = [
            {'file': os.path.join('/music', 'song1.mp3'), 'artist': 'Unknown', 'title': 'Unknown', 'bpm': 130}
        ]
        self.assertEqual(result, expected_result)

    @patch('os.walk')
    @patch('tunelist.extract_metadata')
    def test_find_multiple_files_with_different_extensions(self, mock_metadata, mock_walk):
        # Mocka os.walk för att returnera en blandning av filer
        mock_walk.return_value = [
            ('/music', ('subdir',), ('song1.mp3', 'song2.wav', 'song3.mp3'))
        ]

        # Dummy-metadata för mp3-filerna
        mock_metadata.return_value = {'artist': 'Unknown', 'title': 'Unknown', 'bpm': 110}

        expected_files = [
            {'file': os.path.join('/music', 'song1.mp3'), 'artist': 'Unknown', 'title': 'Unknown', 'bpm': 110},
            {'file': os.path.join('/music', 'song3.mp3'), 'artist': 'Unknown', 'title': 'Unknown', 'bpm': 110}
        ]

        result = find_music_files('/music')
        self.assertEqual(result, expected_files)

    @patch('os.walk')
    @patch('tunelist.extract_metadata')  # Mocka funktionen som läser metadata
    def test_extract_metadata_for_single_file(self, mock_metadata, mock_walk):
        # Mocka os.walk för att returnera en katalogstruktur med en fil
        mock_walk.return_value = [
            ('/music', ('subdir',), ('song1.mp3',))
        ]

        # Mocka metadata för att returnera artist och låttitel
        mock_metadata.return_value = {'artist': 'Artist1', 'title': 'Song1', 'bpm': 100}

        result = find_music_files('/music')
        
        # Förväntat resultat är filnamn och dess metadata
        expected_result = [
            {'file': os.path.join('/music', 'song1.mp3'), 'artist': 'Artist1', 'title': 'Song1', 'bpm': 100}    
        ]

        self.assertEqual(result, expected_result)

    @patch('os.walk')
    @patch('tunelist.extract_metadata')
    def test_extract_metadata_with_bpm(self, mock_metadata, mock_walk):
        # Mocka os.walk för att returnera en katalogstruktur med en fil
        mock_walk.return_value = [
            ('/music', ('subdir',), ('song1.mp3',))
        ]

        # Mocka metadata för att inkludera BPM
        mock_metadata.return_value = {'artist': 'Artist1', 'title': 'Song1', 'bpm': 120}

        result = find_music_files('/music')

        # Förvänta att BPM också returneras
        expected_result = [
            {'file': os.path.join('/music', 'song1.mp3'), 'artist': 'Artist1', 'title': 'Song1', 'bpm': 120}
        ]

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
