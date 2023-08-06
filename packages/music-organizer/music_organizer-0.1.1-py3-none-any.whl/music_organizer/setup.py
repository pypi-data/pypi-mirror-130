
from distutils.core import setup
setup(
    name='music_organizer',         # How you named your package folder (MyLib)
    packages=['music_organizer'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Organize music of a filepath',
    author='JavierOramas',                   # Type in your name
    author_email='javiale2000@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/JavierOramas/Music_Library_Organizer.git',
    # package_dir=    # I explain this later on
    download_url='https://github.com/JavierOramas/Music_Library_Organizer/archive/refs/tags/fisrtbuild.zip',
    # Keywords that define your package best
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[            # I get to this in a second
        'audio_metadata',
        'typer'

    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
