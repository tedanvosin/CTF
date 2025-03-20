#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

int main() {
    int sockfd;
    struct sockaddr_in client_addr, server_addr;
    char recv_buffer[4];
    uint32_t value_to_send = 0x32200000|1900;//htonl(0x32200000+1900);  // Convert 0x31200064 to network byte order

    // Step 1: Create a UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Step 2: Bind the client socket to a specific port
    memset(&client_addr, 0, sizeof(client_addr));
    client_addr.sin_family = AF_INET;
    client_addr.sin_addr.s_addr = INADDR_ANY;  // Bind to any available network interface
    client_addr.sin_port = htons(1900);       // Specify the port number you want to use as the source port

    if (bind(sockfd, (struct sockaddr *)&client_addr, sizeof(client_addr)) < 0) {
        perror("Bind failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Step 3: Define the server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(1337);               // Server port
    server_addr.sin_addr.s_addr = inet_addr("44.220.174.32");  // Use the provided IP address

    // Step 4: Send the data to the server
    if (sendto(sockfd, &value_to_send, sizeof(value_to_send), 0, 
            (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Send failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    printf("Sent: 0x%X \n", value_to_send);

    // Step 5: Receive 4 bytes back from the server
    socklen_t addr_len = sizeof(server_addr);
    int n = recvfrom(sockfd, recv_buffer, sizeof(recv_buffer), 0, 
                    (struct sockaddr *)&server_addr, &addr_len);
    if (n != 4) {  // Expecting exactly 4 bytes
        perror("Failed to receive the expected number of bytes");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Print the received 4 bytes in hexadecimal format
    printf("Received: 0x%02X%02X%02X%02X\n", 
        (unsigned char)recv_buffer[0], (unsigned char)recv_buffer[1], 
        (unsigned char)recv_buffer[2], (unsigned char)recv_buffer[3]);

    // Close the socket
    close(sockfd);
    return;
}
