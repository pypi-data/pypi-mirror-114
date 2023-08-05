from distutils.core import setup
setup(
  name = 'harbinger',
  packages = ['harbinger'],
  version = '0.5',
  license='MIT',
  description = 'A python tool that simplifies automating tasks across multiple servers.',
  author = 'protosam',
  author_email = 'sam.igknighted@gmail.com',
  url = 'https://github.com/protosam/harbinger',
  download_url = 'https://github.com/protosam/harbinger/archive/refs/tags/v0.5.zip',
  keywords = ['ssh', 'easy', 'automation', 'administration', 'orchestration', 'devops', 'linux', 'servers', 'cloud', 'infrastructure'],
  install_requires=[
          'jinja2',
          'paramiko',
          'pyyaml',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: System :: Installation/Setup',
    'Topic :: System :: Systems Administration',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',
  ],
)