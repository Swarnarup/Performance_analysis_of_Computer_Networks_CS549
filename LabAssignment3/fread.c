#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    // Character that store the read
    // character

    int buff[100];

    // Opening file in reading mode
    FILE *fptr = fopen(argv[1], "r");

    // Reading file character by character
    while (fread(&buff, sizeof(buff), 1, fptr));
        
    // Closing the file
    fclose(fptr);
    return 0;
}
