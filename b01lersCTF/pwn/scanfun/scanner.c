#include <stdio.h>
#include <stdlib.h>

void scan() {
    char scanner[0x50] = {0};
    while (1) {
        fprintf(stdout, "What do you want to scan?\n");
        scanf("%50s\n", scanner);
        scanf(scanner);
        
    }
}


int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("Welcome to The Scanner (TM)!!!\n");
    printf("A hint for you. Just a byte, no more [0x%hhx]\n", (((unsigned long)stdout) >> 16) & 0xFF);
    scan();
}