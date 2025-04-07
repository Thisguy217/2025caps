# Bioinformatics Capstone Project

## Overview
This project is an extension and, more specifically, an early attempt at utilizing 3-dimensional protein information and graph clustering methods to identify binding pockets of proteins.

Proteins are a building block of life, with extensible configuration and design to accomplish a myriad of tasks. However, interestingly, despite the vast morphology that proteins can theoretically experience, they limit themselves. This discovery came along with an understanding that proteins require specific functional components or folds for function to be derived. If either a fold or an incorporated amino acid is incorrect, the protein will not function and may be fatal to the organism. To protect against this, proteins often have corrective mechanisms and selective pressures that ensure that important amino acids remain unchanged in the protein sequence. By identifying these amino acids and combining the information with 3-dimensional structures, we believe we can identify where metabolites or other invariant ligands bind.

## Features
- **Optimized Algorithms**: With the previous projects that have built much of the precursors, we have sought to adjust and build a much faster and more accurate method of identifying binding pockets with orthologous protein sequence information.
- **Benchmarking Suite**: For proper testing, we encourage known orthologies and identified conserved residues to be tested, and we even provide our test set for verification.
- **Parallel Processing**: Along with more advanced algorithms, some of the processes have now leveraged parallel processing and allow for larger data sets to be worked through.
- **Code Refactoring**: Though our focus is on optimization, we sought to also create a "plug-and-plAcademic Free License v3.0ay" design to encourage further development and improvements.

## Installation
- **Google Colab**: We designed our pipeline to run inside a Google Colab notebook. This means translating it to other notebooks software (VSCode, Jupyter, etc.). However, this may break some imports *if* they are not previously installed on the system. We include a `requirements.txt` for these cases.

## Project Structure
- **Plug-And-Play**: As mentioned before, we looked for a more simplified approach to usage and designed it to simply be installed on a notebook and provide the inputs for it to run and finalize. However, we will walk briefly here through the structure of the project, which will be detailed more heavily in the notebook.
1. Project Import...
2. etc...

## Dependencies
- Python 3.11.11 (the current version installed on Google Colab)
  - Biopython, os, subprocess, etc.

## Contributing
If you would like to contribute, please fork the repository and submit a pull request with your improvements.

## License
[Specify your license, e.g., MIT License]

## Acknowledgments
- We want to acknowledge the work of Dr. Sam Payne in assisting in designing and improving our project, as well as being the instructor for the course, which made this project a reality.

