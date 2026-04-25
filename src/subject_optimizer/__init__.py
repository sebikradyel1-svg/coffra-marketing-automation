"""
Coffra Subject Line Optimizer

A Claude-powered tool that generates and critiques email subject line variants
for the Coffra marketing automation system.

Modules:
    config:    Persona definitions and brand voice rules
    prompts:   Prompt templates for Claude API
    generator: Generates subject line variants
    critic:    Scores variants on multiple dimensions
    cache:     JSON-based response caching for cost efficiency
"""

__version__ = "1.0.0"
__author__ = "Sebastian Kradyel"
