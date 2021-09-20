#!/usr/bin/env python3
"""
A program that deletes itself
"""
from pathlib import Path

if __name__ == "__main__":
    print(f"Deleting self: {__file__}")
    Path(__file__).unlink()
