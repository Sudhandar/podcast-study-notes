#!/usr/bin/env python3
"""
Validation script for podcast study notes
Checks that study-notes.md meets all structural requirements
"""

import pathlib
import re
import sys


def validate_notes():
    """Validate study notes structure and content"""
    
    notes_file = pathlib.Path("study-notes.md")
    
    # Check file exists
    if not notes_file.exists():
        print("❌ FAIL: study-notes.md not found")
        return False
    
    content = notes_file.read_text()
    errors = []
    warnings = []
    
    # ===== SECTION EXISTENCE CHECKS =====
    required_sections = {
        "Title (H1)": r'^# .+',
        "Executive Summary": r'## Executive Summary',
        "Key Points": r'## Key Points',
        "Notable Quotes": r'## Notable Quotes',
        "Key Takeaways": r'## Key Takeaways',
        "Resources Mentioned": r'## Resources Mentioned'
    }
    
    for section_name, pattern in required_sections.items():
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"Missing required section: {section_name}")
    
    if errors:
        print("❌ FAIL: Missing required sections")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # ===== METADATA CHECKS =====
    metadata_patterns = {
        "Podcast name": r'\*\*Podcast:\*\*',
        "Duration": r'\*\*Duration:\*\*',
        "Date": r'\*\*Date:\*\*'
    }
    
    for meta_name, pattern in metadata_patterns.items():
        if not re.search(pattern, content):
            warnings.append(f"Missing metadata: {meta_name}")
    
    # ===== EXECUTIVE SUMMARY CHECKS =====
    summary_match = re.search(
        r'## Executive Summary\s+(.+?)(?=\n##|\Z)', 
        content, 
        re.DOTALL
    )
    if summary_match:
        summary_text = summary_match.group(1).strip()
        sentence_count = len(re.findall(r'[.!?]+', summary_text))
        if sentence_count < 2:
            warnings.append(f"Executive Summary seems short ({sentence_count} sentences)")
    
    # ===== KEY POINTS CHECKS =====
    key_points_match = re.search(
        r'## Key Points\s+(.+?)(?=\n## |\Z)', 
        content, 
        re.DOTALL
    )
    
    if key_points_match:
        key_points_section = key_points_match.group(1)
        
        # Count topics (H3 headers)
        topics = re.findall(r'### .+', key_points_section)
        topic_count = len(topics)
        
        if topic_count < 3:
            errors.append(f"Found {topic_count} topics, need at least 3")
        elif topic_count > 7:
            warnings.append(f"Found {topic_count} topics, recommended max is 7")
        
        # Check for timestamps in Key Points
        timestamps = re.findall(
            r'\*\*\[?\d{1,2}:\d{2}\]?\*\*|\*\*Timestamp:?\s*\d{1,2}:\d{2}\*\*',
            key_points_section
        )
        timestamp_count = len(timestamps)
        
        if timestamp_count < 5:
            errors.append(f"Found {timestamp_count} timestamps in Key Points, need at least 5")
        
        # Check topics aren't generic
        generic_topics = [t for t in topics if re.search(r'Topic \d+|Section \d+|Part \d+', t, re.IGNORECASE)]
        if generic_topics:
            warnings.append(f"Found generic topic names: {generic_topics}")
    
    # ===== QUOTES CHECKS =====
    quotes_match = re.search(
        r'## Notable Quotes\s+(.+?)(?=\n## |\Z)', 
        content, 
        re.DOTALL
    )
    
    if quotes_match:
        quotes_section = quotes_match.group(1)
        
        # Count blockquotes
        quotes = re.findall(r'^> ".+?"', quotes_section, re.MULTILINE)
        quote_count = len(quotes)
        
        if quote_count < 3:
            errors.append(f"Found {quote_count} quotes, need at least 3")
        elif quote_count > 5:
            warnings.append(f"Found {quote_count} quotes, recommended max is 5")
        
        # Check for timestamp attribution
        quote_timestamps = re.findall(
            r'\*Timestamp:?\s*\d{1,2}:\d{2}\*',
            quotes_section
        )
        if len(quote_timestamps) < quote_count:
            warnings.append("Not all quotes have timestamp attribution")
    
    # ===== TAKEAWAYS CHECKS =====
    takeaways_match = re.search(
        r'## Key Takeaways\s+(.+?)(?=\n## |\Z)', 
        content, 
        re.DOTALL
    )
    
    if takeaways_match:
        takeaways_section = takeaways_match.group(1)
        
        # Count bullet points
        takeaway_bullets = re.findall(r'^\s*- .+', takeaways_section, re.MULTILINE)
        takeaway_count = len(takeaway_bullets)
        
        if takeaway_count < 3:
            errors.append(f"Found {takeaway_count} takeaways, need at least 3")
        elif takeaway_count > 5:
            warnings.append(f"Found {takeaway_count} takeaways, recommended max is 5")
    
    # ===== RESOURCES CHECKS =====
    resources_match = re.search(
        r'## Resources Mentioned\s+(.+?)(?=\Z)', 
        content, 
        re.DOTALL
    )
    
    if resources_match:
        resources_section = resources_match.group(1).strip()
        if not resources_section or len(resources_section) < 10:
            warnings.append("Resources section seems empty")
    
    # ===== FINAL REPORT =====
    if errors:
        print("❌ FAIL: Validation errors found")
        for error in errors:
            print(f"  ❌ {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        return False
    
    # Success!
    print("✅ PASS: All validation checks passed!")
    print(f"\nStats:")
    print(f"  📝 Topics: {topic_count}")
    print(f"  ⏱️  Timestamps: {timestamp_count}")
    print(f"  💬 Quotes: {quote_count}")
    print(f"  🎯 Takeaways: {takeaway_count}")
    
    if warnings:
        print("\n⚠️  Warnings (non-blocking):")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("\n✨ study-notes.md is ready!")
    return True


if __name__ == "__main__":
    success = validate_notes()
    sys.exit(0 if success else 1)