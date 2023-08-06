# append-zip

Appends a file to a zip file, overwriting the existing file there if necessary

## Performance
Not efficient; extracts all the files in the zip, copies over the new file, and compresses a brand new zip replacing the original one. You will need enough disk space to duplicate the zip file.

## Caveats
for some reason, windows has a different file length after unzipping (by 10-20 bytes). So beware how this works on windows