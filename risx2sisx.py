#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("representation_index", help="The representation "
		"index to convert (generally a .sidx file).")
	parser.add_argument("--template", "-t", help="Template for segment index "
		"files. {n} will be replaced with the segment number.",
		default="segment-{n}.sidx")

	args = parser.parse_args()
