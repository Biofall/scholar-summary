def generate_summary_report(summary, articles):
    # Convert the summary to a markdown file and save it.
    # Include citations (e.g., "[Article 1](URL)") in the summary.
    output_path = "output_summary.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Summary of Google Scholar Alerts\n\n")
        f.write(summary)
    return output_path