#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    // Character that store the read
    // character

    char ch = 'c';

    // Opening file in reading mode
    FILE *fptr = fopen(argv[1], "r");

    // Reading file character by character
    while (fgetc(fptr) != EOF);
        
    // Closing the file
    fclose(fptr);
    return 0;
}