# HackerOne Program Fetcher

A Python tool to fetch and filter HackerOne programs using the HackerOne API.

## Prerequisites

- Python 3.x
- A HackerOne account with an API identifier and token.

## Installation

1.  Clone this repository or download the files.
2.  Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

**RECOMMENDED: Run with Python directly**
To avoid issues with file permissions or line endings on Windows/WSL, run the script using the `python` command:

```bash
python hackerone_fetcher.py <USERNAME> <API_KEY> [OPTIONS]
```

### Arguments

-   `username`: Your HackerOne API identifier.
-   `api_key`: Your HackerOne API token.

### Options

-   `--type {all,bounty,vdp}`: Filter programs by type.
    -   `all`: Fetch all programs (default).
    -   `bounty`: Fetch only programs that offer bounties.
    -   `vdp`: Fetch only programs that do not offer bounties (Vulnerability Disclosure Programs).
-   `--output OUTPUT`: Specify the output JSON filename (default: `programs.json`).
-   `-h, --help`: Show this help message and exit.

### Examples

**Fetch all programs:**
```bash
python hackerone_fetcher.py my_username my_api_key
```

**Fetch only Bug Bounty programs:**
```bash
python hackerone_fetcher.py my_username my_api_key --type bounty
```

**Fetch only VDPs and save to `my_vdps.json`:**
```bash
python hackerone_fetcher.py my_username my_api_key --type vdp --output my_vdps.json
```

## Output

The script generates a JSON file (default `programs.json`) containing the list of programs that match your criteria. It also prints a summary of the fetch operation to the console.
