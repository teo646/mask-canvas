from setuptools import setup

setup(
    name='mask-canvas',
    version='0.1',
    description='Library for maskable canvas',
    author='Tae Young Choi',
    author_email='tyul0529@naver.com',
    packages=['maskCanvas'],
    install_requires=['numpy', 'opencv-python', 'scipy', 'aioconsole', 'perlin_noise', 'matplotlib', 'scipy', 'aioconsole', 'perlin_noise', 'pyaxidraw @ https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip'],
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
