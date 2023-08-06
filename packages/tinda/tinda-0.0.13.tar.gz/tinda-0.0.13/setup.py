from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = "BUGGY ALPHA STAGE-'Daddy Wrapper'"
LONG_DESCRIPTION = """
                    It contains a few useful wrapper functions,
                    setup to be used as you may.
                    They are essentially plug and play.
                    All the required dependencies should install automatically.
                    PORT AUDIO MIGHT SHOW ERROR WHICH MIGHT REQUIRE TROUBLESHOOTING
                    Check version for more details.
                    """

# Setting up
setup(
    name="tinda",
    version=VERSION,
    author="(Hank Singh)",
    author_email="<hanksingh07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'argparse', 'wave', 'pyautogui', 'twine', 'pyttsx3', 'transformers', 'pyaudio', 'speedtest-cli', 'pynput', 'datetime', 'mediapipe', 'opencv-python', 'tqdm', 'bs4', 'SpeechRecognition'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
