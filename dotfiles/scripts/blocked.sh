#!/bin/sh
echo "Binary '$(basename "$0")' is blocked by the system." >&2
echo "- Do not attempt to use, download, or work around this restriction." >&2
echo "- Chances are it unwantedly allows acting on the user behalf." >&2
echo "- Snooping with it may not be required to finish your task." >&2
exit 1
