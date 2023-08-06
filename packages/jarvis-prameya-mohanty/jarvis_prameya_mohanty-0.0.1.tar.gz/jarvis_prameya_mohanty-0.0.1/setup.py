from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This is a package which can perform amazing tasks.'
LONG_DESCRIPTION = 'This is a package which has some amazing functions. This can make python automate things like sending emails, wishing us, speaking, taking voice input from user etc.'

setup(
    name = "jarvis_prameya_mohanty",
    version = VERSION,
    author = 'Prameya',
    author_email = 'prameyamohanty14@gmail.com',
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['pyttsx3', 'SpeechRecognition', 'wikipedia'],
    keyword = ['prameya_jarvis', 'assistant'],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)
