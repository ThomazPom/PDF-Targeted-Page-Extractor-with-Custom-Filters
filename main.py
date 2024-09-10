import os
import shutil
import argparse
import logging
from tqdm import tqdm
import fitz  # PyMuPDF library for handling PDFs

def contains_unwanted_phrases(text, unwanted_phrases):
    for phrase in unwanted_phrases:
        if phrase.lower() in text.lower():
            return True
    return False

def extract_pages(input_pdf, output_dir, search_string, pages_before, pages_after, unwanted_phrases, filename_prefix):
    # Check if the output directory exists; if yes, delete it
    if os.path.exists(output_dir):
        logging.info(f"Output directory '{output_dir}' exists, removing it.")
        shutil.rmtree(output_dir)
    # Create a new output directory
    logging.info(f"Creating output directory '{output_dir}'.")
    os.makedirs(output_dir)

    # Open the input PDF using PyMuPDF for robust handling
    doc = fitz.open(input_pdf)
    total_pages = doc.page_count
    logging.info(f"Opened PDF '{input_pdf}' with {total_pages} pages.")

    extract_count = 0  # Counter to number extracted files

    # Progress bar for page processing
    for i in tqdm(range(total_pages), desc="Processing pages"):
        page_text = doc[i].get_text()
        if search_string.lower() in page_text.lower():
            start_page = max(i - pages_before, 0)
            end_page = min(i + pages_after + 1, total_pages)

            # Check unwanted phrases in the before and after pages
            skip_extraction = False
            for j in range(start_page, end_page):
                if j != i:  # Skip the page with the search string itself
                    surrounding_page_text = doc[j].get_text()
                    if contains_unwanted_phrases(surrounding_page_text, unwanted_phrases):
                        skip_extraction = True
                        logging.info(
                            f"Skipping extraction for pages {start_page + 1}-{end_page} due to unwanted phrases.")
                        break

            if not skip_extraction:
                # Create a new PDF document to write the extracted pages
                output_pdf = fitz.open()  # New PDF document

                for j in range(start_page, end_page):
                    output_pdf.insert_pdf(doc, from_page=j, to_page=j)

                extract_count += 1  # Increment the counter for each valid extraction
                padded_number = f"{extract_count:07}"
                output_pdf_filename = f"{filename_prefix}{padded_number}.pdf"
                output_pdf_path = os.path.join(output_dir, output_pdf_filename)

                output_pdf.save(output_pdf_path)
                output_pdf.close()

                logging.info(f"Extracted pages {start_page + 1}-{end_page} to '{output_pdf_filename}'.")

    # Close the input document
    doc.close()

def main():
    parser = argparse.ArgumentParser(description="Extract pages from a PDF containing a specific string.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_dir", help="Directory to store the extracted PDF files.")
    parser.add_argument("search_string", help="String to search for in the PDF.")
    parser.add_argument("--before", type=int, default=0, help="Number of pages to include before the matching page.")
    parser.add_argument("--after", type=int, default=0, help="Number of pages to include after the matching page.")
    parser.add_argument("--unwanted_phrases", nargs='+', default=[],
                        help="Phrases that, if found in the surrounding pages, will prevent extraction.")
    parser.add_argument("--filename_prefix", default="extracted_",
                        help="Prefix for the output PDF filenames. Default is 'extracted_'.")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting PDF extraction process.")
    extract_pages(args.input_pdf, args.output_dir, args.search_string, args.before, args.after, args.unwanted_phrases,
                  args.filename_prefix)
    logging.info("PDF extraction process completed.")

if __name__ == "__main__":
    main()
