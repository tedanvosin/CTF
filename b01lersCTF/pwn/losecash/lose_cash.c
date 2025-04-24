#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <stdint.h>
#include <string.h>

#include <unistd.h>


/* x**31 + x**3 + 1.  */
#define	TYPE_3		3
#define	BREAK_3		128
#define	DEG_3		31
#define	SEP_3		3


size_t is_cached[32] = {0};
size_t *cards_cache[32] = {0};
char player_name[32];
int32_t randstate[DEG_3 + 1];

char* hand;
int money;
int high_score;
char choice[8];
char card_chars[] = "A234567890JQK";



int draw_cards() {
    size_t hand_int = *(size_t*)hand;
    
    int greatest_match = 0;
    int index = 0;

    size_t cards = 0;

    // rand is expensive don't do it if we don't have to
    if (cards_cache[hand_int % 32] != NULL) {
        if (strcmp(hand, (char*)cards_cache[hand_int % 32]) == 0) {
            cards = cards_cache[hand_int % 32][1];
        }
    } else {
        cards_cache[hand_int % 32] = malloc(16);
        is_cached[hand_int % 32] = 1;
    }

    if (cards <= 0 || cards > (1 << 31)) {
        cards = rand();
    }

    // Already allocated earlier so we don't need to check.
    cards_cache[hand_int % 32][0] = hand_int;
    cards_cache[hand_int % 32][1] = cards;

    while (cards > 0) {
        int card = cards % 13;
        printf("%c\n", card_chars[card]);
        
        if (hand[index %  5] == card_chars[card]) {
            index += 1;
        } else {
            index = 0;
        }

        if (index > greatest_match) {
            greatest_match = index;
        }

        cards = cards / 13;
    }
    return greatest_match;
}

// Random seeds
void* seeds[4] = {
    0x44444444, // chosen by random dice roll
    draw_cards,
    rand,
    0,
};

int main() {
    hand = malloc(0x10);
    memset(hand, 0, 0x10);
    seeds[3] = hand;

    // ASLR is random, so this is secure from attacks.
    char* oldstate = initstate(((size_t) hand) >> 12, (char *)randstate, BREAK_3);
    
    money = 50;
    high_score = money;

    printf("Match as many cards as possible! Get as much money as your longest streak!\n");
    printf("get $5,000,000,000 for the grand prize!\n");
    printf("Buy in is $1\n");
    while (true) {
        printf("Current money: $%d\n > ", money);
        fflush(stdout);
        
        read(0, hand, 7);
        money -= 5;
        printf("$1 spent. Hand: %s\n", hand);

        printf("Shuffling deck...\n");
        
        int winnings = (1 << draw_cards());
        printf("You won $%d\n", winnings);
        money += winnings;

        if (money > high_score)
            high_score = money;

        if (money < 0) {
            setstate((char *)oldstate);

            printf("You Lose! Highest amount of money was %d\n", high_score);
            printf("Input name for your high score! > ");
            fflush(stdout);
            
            player_name[read(0, player_name, 32)] = '\x00';

            printf("Play again? [Y/n] > ");
            fflush(stdout);
            scanf("%1s", choice);
            
            money = 50;
            
            if (choice[0] == 'n') {
                printf("goodbye.\n");
                free(hand);
                exit(0);
            }

            // Reset cache
            for (int i = 0; i < 32; i++) {
                if (is_cached[i] != 0) {
                    free(cards_cache[i]);
                }
                
                is_cached[i] = 0;
            }
            

            void* seed = seeds[rand() % 4];

            randstate[1] = (((size_t) seed) >> (12));
            setstate((char *)randstate);
        }
    }

}
