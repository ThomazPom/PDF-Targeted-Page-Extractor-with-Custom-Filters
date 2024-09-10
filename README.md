# PDF Page Extractor

PDF Page Extractor is a Python script that searches for specific strings within a PDF document and extracts the pages containing the string, along with a specified number of pages before and after the found page. It also includes options to avoid extraction if certain unwanted phrases are present in the vicinity of the found page.

## Features

- **Search String**: Extract pages that contain a specific string.
- **Context Pages**: Include pages before and after the found page in the extraction.
- **Unwanted Phrases**: Skip extraction if specified phrases are found in the context pages.
- **Custom Filename Prefix**: Customize the prefix for the output filenames.
- **Logging**: Detailed logging of the process.
- **Progress Bar**: Visual progress bar during the processing.

## Prerequisites

Before running this script, ensure you have Python installed on your system. Additionally, you'll need to install the following Python libraries:

- `PyPDF2`
- `tqdm`

You can install these dependencies using pip:

```bash
pip install PyPDF2 tqdm
```
## Usage

To use the script, follow the syntax below from the command line:

```bash
python pdf_extractor.py <input_pdf> <output_dir> "<search_string>" --before <n> --after <n> --unwanted_phrases "<phrase1>" "<phrase2>" --filename_prefix "<prefix>"
```
Parameters

    input_pdf: Path to the input PDF file.
    output_dir: Directory to store the extracted PDF files. If it exists, it will be removed and recreated.
    search_string: The text string to search for within the PDF.
    --before: Optional. Number of pages to include before the matching page. Default is 0.
    --after: Optional. Number of pages to include after the matching page. Default is 0.
    --unwanted_phrases: Optional. A list of phrases that, if found in the context pages, will prevent the extraction of that section.
    --filename_prefix: Optional. Prefix for the output PDF filenames. Default is 'extracted_'.

## Example

Here is an example of how to run the script:

```bash
python pdf_extractor.py example.pdf output "confidential" --before 2 --after 3 --unwanted_phrases "classified" "restricted" --filename_prefix "doc_"
```
This command will extract pages containing the word "confidential", including 2 pages before and 3 pages after each occurrence, unless the pages contain the words "classified" or "restricted". The extracted pages will be saved in the output directory with filenames starting with doc_.
Logging

The script provides detailed logs during execution, including actions taken, pages processed, and any pages skipped due to unwanted phrases. These logs help in monitoring the script's operation and troubleshooting if needed.
Progress Bar

A progress bar is displayed on the command line, showing the percentage of pages processed. This feature provides a visual indication of the script's progress, enhancing user interaction.