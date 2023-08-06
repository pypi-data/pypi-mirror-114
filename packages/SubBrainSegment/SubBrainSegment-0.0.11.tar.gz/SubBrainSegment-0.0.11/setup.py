from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6',
    'Environment :: GPU :: NVIDIA CUDA :: 10.0',
    'License :: OSI Approved :: MIT License'
]

setup(
     name='SubBrainSegment',
     version='0.0.11',
     description='Package for subcortical brain segmentation',
     long_description_content_type='text/x-rst',
     url='https://github.com/JENNSHIUAN',
     author='JENNSHIUAN',
     author_email='danny092608@gmail.com',
     License='MIT',
     classifiers=classifiers,
     keywords='subcortical brain segmentation',
     package=find_packages(),
     include_package_data=True,
     py_modules=["SubBrainSegment"],
     python_requires='>=3.6',
     install_requires=[
             'numpy',
             'nibabel',
             'nilearn',
             'SimpleITK',
             'tables'
         ]
)
