import argparse


def main():
    """
    The Carpentries command line tool.
    """
    parser = argparse.ArgumentParser(description="""
    A toolkit for The Carpentries.
    """)
    from thecarpentries import values


if __name__ == "__main__":
    main()
