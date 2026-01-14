# Git LFS Setup for Large Data Files

## Overview

This repository uses Git LFS (Large File Storage) to track large data files (primarily Parquet files) without bloating the Git repository.

## Setup

Git LFS is already initialized in this repository. The `.gitattributes` file configures which files are tracked by Git LFS.

## What's Tracked

- `*.parquet` files - All Parquet data files are tracked with Git LFS
- `*.csv` files - Large CSV files (if any) are also tracked

## What's NOT Tracked

- Cache files in `artifacts/data/cache/` - These are ignored and should not be committed
- Other artifacts in `artifacts/` - Generated outputs are generally ignored

## Usage

### Adding Large Files

When you add a large Parquet file, Git LFS will automatically handle it:

```bash
# Add the file normally - Git LFS will intercept it
git add artifacts/data/stooq_daily.parquet

# Commit as usual
git commit -m "Add bulk market data"

# Push - Git LFS will upload the file to LFS storage
git push
```

### Checking LFS Status

```bash
# See which files are tracked by LFS
git lfs ls-files

# See LFS file sizes
git lfs ls-files --long
```

### Cloning with LFS Files

When cloning the repository, LFS files are automatically downloaded:

```bash
git clone <repository-url>
```

If you need to download LFS files after cloning:

```bash
git lfs pull
```

### Skipping LFS Files (for faster clones)

If you don't need the data files immediately:

```bash
# Clone without LFS files
GIT_LFS_SKIP_SMUDGE=1 git clone <repository-url>

# Download LFS files later if needed
git lfs pull
```

## File Size Considerations

- **Cache files**: Should remain in `.gitignore` - they're regenerated from source
- **Main data files**: Tracked with Git LFS - these are the canonical datasets
- **Golden test files**: Small CSV files can be tracked normally (not LFS)

## Troubleshooting

### LFS files not downloading

```bash
# Reinstall LFS hooks
git lfs install

# Pull LFS files manually
git lfs pull
```

### Check if LFS is working

```bash
# Verify LFS is installed
git lfs version

# Check LFS tracking status
git lfs track
```

## GitHub Limits

GitHub provides:
- 1 GB storage for Git LFS (free tier)
- 1 GB bandwidth per month (free tier)

For larger datasets, consider:
- Using external storage (S3, etc.) and downloading via script
- Storing only metadata in Git, with download instructions
- Using Git LFS hosting services for larger quotas
