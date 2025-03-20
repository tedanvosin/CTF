#include <stdint.h>
#include <stdio.h>

int16_t do_you;
int even(){
    int ret_val = do_you & 1;
    uint32_t val = *(uint16_t *)&do_you;
    //printf("%d,%d\n",do_you,val);
    val = val>>1;
    //printf("%x\n",val);
    int64_t val_2 = *(int32_t *)&val;
    //printf("%lx\n",val_2);
    if(ret_val){
        val_2^=46080;
    }
    //printf("%d\n",val_2);
    do_you = *(int16_t *)&val_2;
    //printf("%d\n",do_you);
    return ret_val;
}
int lift_bro(){
    char inp[23] = {0xD3,0x06,0x07,0xBB,'k',0xA2,0xFD,'<','`',0xC9,'9',0x1A,0xA8,0x16,'I','2',0xA5,'5',0xD2,0xAC,'@',0xD6,')'};
    for(int i=0;i<23;i++){
        char val=0;
        for(int j=0;j<8;j++){
            val = val<<1;
            val |= even();
        }
        printf("%c",val^inp[i]);
    }
    printf("\n");
    return 0;
}
int main() {
    do_you = (int16_t)-8531;
    //even();
    lift_bro();
    return 0;
}