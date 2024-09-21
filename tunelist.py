import os

def find_music_files(directory):
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                metadata = extract_metadata(file_path)
                music_files.append({
                    'artist': metadata['artist'],
                    'title': metadata['title'],
                    'genre': metadata['genre'],
                    'bpm': metadata['bpm']
                })
    return music_files

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.asf import ASF
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TPE1, TBPM

def extract_metadata(file_path):
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=ID3)
            artist = audio.get('TPE1', 'Unknown Artist')
            title = audio.get('TIT2', 'Unknown Title')
            genre = audio.get('TCON', ['Unknown Genre'])[0]
            # Kontrollera om TBPM är ett numeriskt värde, och omvandla om nödvändigt
            bpm_tag = audio.get('TBPM', None)
            if bpm_tag:
                bpm = round(float(bpm_tag.text[0])) if bpm_tag and bpm_tag.text else 0
            else:
                bpm = 0
        elif file_path.endswith('.flac'):
            audio = FLAC(file_path)
            artist = audio.get('artist', 'Unknown Artist')
            title = audio.get('title', 'Unknown Title')
            genre = audio.get('genre', 'Unknown Genre')
            bpm = audio.get('bpm', 0)
        elif file_path.endswith('.m4a') or file_path.endswith('.mp4'):
            audio = MP4(file_path)
            artist = audio.get('\xa9ART', ['Unknown Artist'])[0]
            title = audio.get('\xa9nam', ['Unknown Title'])[0]
            genre = audio.get('\xa9gen', ['Unknown Genre'])[0]
            bpm = round(float(audio.get('tmpo', [0])[0]))
        elif file_path.endswith('.asf') or file_path.endswith('.wma'):
            audio = ASF(file_path)
            artist = audio.get('Author', ['Unknown Artist'])[0]
            title = audio.get('Title', ['Unknown Title'])[0]
            genre = audio.get('WM/Genre', ['Unknown Genre'])[0]
            bpm = 0  # ASF-formatet stöder inte BPM så bra
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
            artist = audio.get('artist', 'Unknown Artist')
            title = audio.get('title', 'Unknown Title')
            genre = audio.get('genre', 'Unknown Genre')
            bpm = audio.get('bpm', 0)
        else:
            return {
                'artist': 'Unsupported Format',
                'title': 'Unsupported Format',
                'genre': 'Unsupported Format',
                'bpm': 0
            }

        return {
            'artist': str(artist),
            'title': str(title),
            'genre': str(genre),
            'bpm': int(bpm) if bpm else 0
        }

    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return {
            'artist': 'Unknown',
            'title': 'Unknown',
            'genre': 'Unknown',
            'bpm': 0
        }

def write_music_metadata_to_html(directory, html_filename):
    music_files = find_music_files(directory)
    
    # Skapa HTML-tabell
    with open(html_filename, 'w') as file:
        file.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Linköping Dancing Team - Musikbiblioteket</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    cursor: pointer;
                }
            </style>
        </head>
        <body>

        <h2>Linköping Dancing Teams musikbibliotek</h2>
        <table id="musicTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Artist</th>
                    <th onclick="sortTable(1)">Title</th>
                    <th onclick="sortTable(2)">Genre</th>
                    <th onclick="sortTable(3)">BPM</th>
                </tr>
            </thead>
            <tbody>
        """)

        for file_info in music_files:
            file.write(f"""
            <tr>
                <td>{file_info['artist']}</td>
                <td>{file_info['title']}</td>
                <td>{file_info['genre']}</td>
                <td>{file_info['bpm']}</td>
            </tr>
            """)

        file.write("""
            </tbody>
        </table>

        <script>
        // Sorterbar tabell
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("musicTable");
            switching = true;
            dir = "asc"; // Sortera stigande
            while (switching) {
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {
                        if (n == 3) { // Sortera BPM som nummer
                            if (parseInt(x.innerHTML) > parseInt(y.innerHTML)) {
                                shouldSwitch = true;
                                break;
                            }
                        } else {
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    } else if (dir == "desc") {
                        if (n == 3) { // Sortera BPM som nummer
                            if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {
                                shouldSwitch = true;
                                break;
                            }
                        } else {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }
        </script>

        </body>
        </html>
        """)

import argparse

def main():
    # Skapa en parser för att hämta katalogvägen från kommandoraden
    parser = argparse.ArgumentParser(description='Generate HTML table from music metadata')
    parser.add_argument('directory', type=str, help='Directory to scan for music files')
    args = parser.parse_args()

    # Använd den angivna katalogen för att skriva HTML-filen
    directory_to_scan = args.directory
    html_output_file = 'music_metadata.html'
    
    # Kör funktionen för att generera HTML från den angivna katalogen
    write_music_metadata_to_html(directory_to_scan, html_output_file)
    print(f"HTML file written to {html_output_file}")

if __name__ == "__main__":
    main()