#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int  main() {
    setbuf(stdout, NULL);
    char first_shot[5];
    long s1, d1, d2, s2;
    puts("The prophet Eminem famously said you only have one shot, one opportunity.");
    printf("First shot...");
    scanf("%5s", first_shot);
    printf("\nPalms are sweaty, knees weak, arms are heavy "); 
    printf(first_shot);
    printf("\n");

    printf("He opens his mouth but the words don't come out... ");
    scanf("%ld %ld", &s1, &d1);
    printf("\nHe's chokin how, everbody's jokin now... ");
    scanf("%ld %ld", &s2, &d2);
    
    *(long *) s1 = d1;
    *(long *) s2 = d2;
    
    printf("Clock's run out, time's up, over, blaow");
    exit(0);
}
