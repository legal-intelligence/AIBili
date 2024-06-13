import argparse
import json
from .AIBili import UPSearch, UPDownloader


def main():
    parser = argparse.ArgumentParser(description="Bilibili UP user search and download tool")
    subparsers = parser.add_subparsers(dest="command")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for UP users")
    search_parser.add_argument("keyword", help="Keyword to search for UP users")
    search_parser.add_argument("--order", default="fans", help="Order of results (default: fans)")
    search_parser.add_argument("--followers", type=int, default=0, help="Minimum number of followers")
    search_parser.add_argument("--count", type=int, default=12, help="Number of results to return")
    search_parser.add_argument("--page", type=int, default=1, help="Number of pages to search")
    search_parser.add_argument("--data_dir", required=True, help="Directory to save intermediate data")
    search_parser.add_argument("--download_dir", required=True, help="Directory to save downloaded audio files")
    search_parser.add_argument("--intermediate", action="store_true", help="Save intermediate data")
    search_parser.add_argument("--struct", action="store_true", help="Save data in structured format")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download videos and audio of a UP user")
    download_parser.add_argument("mid", help="MID of the UP user", nargs="+")
    download_parser.add_argument("--data_dir", required=True, help="Directory to save intermediate data")
    download_parser.add_argument("--download_dir", required=True, help="Directory to save downloaded audio files")
    download_parser.add_argument("--intermediate", action="store_true", help="Save intermediate data")
    download_parser.add_argument("--struct", action="store_true", help="Save data in structured format")

    args = parser.parse_args()

    if args.command == "search":
        searcher = UPSearch(
            key_word=args.keyword,
            order=args.order,
            followers=args.followers,
            count=args.count,
            page=args.page,
            data_dir=args.data_dir,
            download_dir=args.download_dir,
            intermediate=args.intermediate,
            struct=args.struct,
        )
        result = searcher.search()
        print(result)

    elif args.command == "download":
        downloader = UPDownloader(
            mid=args.mid,
            data_dir=args.data_dir,
            download_dir=args.download_dir,
            intermediate=args.intermediate,
            struct=args.struct,
        )
        downloader.download()
        print("Download completed.")


if __name__ == "__main__":
    main()
