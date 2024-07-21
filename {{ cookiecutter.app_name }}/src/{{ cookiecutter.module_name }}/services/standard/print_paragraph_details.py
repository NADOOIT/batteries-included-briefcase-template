

def print_paragraph_details(paragraph):
    print("This is one paragraph:")
    if paragraph.text:
        print(f"Text: {paragraph.text}")
    if paragraph.style:
        print(f"Style: {paragraph.style.name}")
    if paragraph.alignment:
        print(f"Alignment: {paragraph.alignment}")
    if paragraph.contains_page_break:
        print(f"Contains page break: {paragraph.contains_page_break}")
    if paragraph.hyperlinks:
        print(f"Hyperlinks: {paragraph.hyperlinks}")
    if paragraph.paragraph_format:
        print("Paragraph format details:")
        format = paragraph.paragraph_format
        if format.alignment:
            print(f"    Alignment: {format.alignment}")
        if format.keep_together:
            print(f"    Keep together: {format.keep_together}")
        if format.keep_with_next:
            print(f"    Keep with next: {format.keep_with_next}")
        if format.left_indent:
            print(f"    Left indent: {format.left_indent}")
        if format.line_spacing:
            print(f"    Line spacing: {format.line_spacing}")
        if format.line_spacing_rule:
            print(f"    Line spacing rule: {format.line_spacing_rule}")
        if format.page_break_before:
            print(f"    Page break before: {format.page_break_before}")
        if format.right_indent:
            print(f"    Right indent: {format.right_indent}")
        if format.space_after:
            print(f"    Space after: {format.space_after}")
        if format.space_before:
            print(f"    Space before: {format.space_before}")
        if format.tab_stops:
            print("    Tab stops:")
            for tabstop in format.tab_stops:
                print(f"        Alignment: {tabstop.alignment}")
                print(f"        Leader: {tabstop.leader}")
                print(f"        Position: {tabstop.position}")
        if format.widow_control:
            print(f"    Widow control: {format.widow_control}")
    if paragraph.runs:
        print("Runs:")
        for run in paragraph.runs:
            if run.text:
                print(f"    Text: {run.text}")
            if run.bold:
                print(f"    Bold: {run.bold}")
            if run.italic:
                print(f"    Italic: {run.italic}")
            if run.underline:
                print(f"    Underline: {run.underline}")
            if run.font:
                if run.font.name:
                    print(f"    Font name: {run.font.name}")
                if run.font.size:
                    print(f"    Font size: {run.font.size}")