#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 1337
#define BUFFER_SIZE sizeof(int)

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    int received_int;
    socklen_t addr_len = sizeof(client_addr);

    // Step 1: Create a UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Step 2: Set up the server address structure
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;                // IPv4
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Bind to localhost
    server_addr.sin_port = htons(PORT);              // Bind to port 1337

    // Step 3: Bind the socket to the specified IP and port
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on 127.0.0.1:%d\n", PORT);

    // Step 4: Receive a single integer from the client
    int bytes_received = recvfrom(sockfd, &received_int, BUFFER_SIZE, 0,
                                  (struct sockaddr *)&client_addr, &addr_len);
    if (bytes_received < 0) {
        perror("recvfrom failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Print the received integer
    printf("Received integer: %hx\n", received_int);

    printf("Client's port: %x\n", client_addr.sin_port);

    // Close the socket
    close(sockfd);
    return 0;
}
