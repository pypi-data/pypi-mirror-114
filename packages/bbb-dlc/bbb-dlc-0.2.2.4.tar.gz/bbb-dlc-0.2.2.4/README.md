# Big Blue Button (BBB) Converter & Downloader

Downloads a BBB lesson as MP4 video, including presentation, audio, webcam and screenshare.

### Setup
1. Install [Python](https://www.python.org/) >=3.7
2. Install [ffmpeg](https://www.ffmpeg.org/)
3. Run: `pip install bbb-dlc` as administrator

### Usage

```
usage: bbb-dlc [-h] [-aw] [-aa] [-kt] [-v] [-ncc] [--version] [--encoder ENCODER] [--audiocodec AUDIOCODEC] [-f FILENAME] URL

Big Blue Button Downloader that downloads a BBB lesson as MP4 video

positional arguments:
  URL                   URL of a BBB lesson

optional arguments:
  -h, --help            show this help message and exit
  -aw, --add-webcam     add the webcam video as an overlay to the final video
  -aa, --add-annotations
                        add the annotations of the professor to the final video
  -kt, --keep-tmp-files
                        keep the temporary files after finish
  -v, --verbose         print more verbose debug informations
  -ncc, --no-check-certificate
                        Suppress HTTPS certificate validation
  --version             Print program version and exit
  --encoder ENCODER     Optional encoder to pass to ffmpeg (default libx264)
  --audiocodec AUDIOCODEC
                        Optional audiocodec to pass to ffmpeg (default copy the codec from the original source)
  -f FILENAME, --filename FILENAME
                        Optional output filename
```


### License
This project is licensed under the terms of the *GNU General Public License v2.0*. For further information, please look [here](http://choosealicense.com/licenses/gpl-2.0/) or [here<sup>(DE)</sup>](http://www.gnu.org/licenses/old-licenses/gpl-2.0.de.html).

This project is based on the work of [CreateWebinar.com](https://github.com/createwebinar/bbb-download), [Stefan Wallentowitz](https://github.com/wallento/bbb-scrape), [Olivier Berger](https://github.com/ytdl-org/youtube-dl/pull/25092) and [Daniel Vogt](https://github.com/C0D3D3V/bbb-dl).
Parts of this code have already been published under MIT license and public domain. These parts are re-released in this project under the GPL-2.0 License.