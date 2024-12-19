# Makefile for GatorTicketMaster

# Python interpreter
PYTHON = python

# Source file
SRC = final_gatorTicketMaster.py

# Input files
INPUT_FILES = example1.txt example2.txt test1.txt test2.txt test3.txt

# Phony targets
.PHONY: all run clean

# Default target
all: $(INPUT_FILES:.txt=_output_file.txt)

# Rule to run the program for each input file
%_output_file.txt: %.txt
	$(PYTHON) $(SRC) $<

# Run all test cases
run: all

# Clean up generated output files
clean:
	rm -f *_output_file.txt

# Run a specific test case
test1: test1_output_file.txt
test2: test2_output_file.txt
test3: test3_output_file.txt
example1: example1_output_file.txt
example2: example2_output_file.txt