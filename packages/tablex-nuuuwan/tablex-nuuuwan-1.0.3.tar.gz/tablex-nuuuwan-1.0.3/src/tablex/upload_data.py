"""Uploaded data to nuuuwan/tablex:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/tablex.test.txt')
    os.system('echo "# tablex" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
