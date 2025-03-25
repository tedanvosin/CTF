#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>

// Matrix structure for the challenge
typedef struct {
    size_t rows;
    size_t cols;
    int64_t* data;
} Matrix;

// Function prototypes
void init_matrix(Matrix* matrix, size_t rows, size_t cols);
void free_matrix(Matrix* matrix);
bool get_matrix_element(Matrix* matrix, size_t row, size_t col, int64_t* result);
bool set_matrix_element(Matrix* matrix, size_t row, size_t col, int64_t value);
bool multiply_matrices(Matrix* matrix_a, Matrix* matrix_b, Matrix* result);
size_t string_length(const char* str);
void xor_decrypt(const char* input);
void print_fail_message();
void check_timing_and_print_flag(char* input);

// Initialize matrix (function at 0x1820)
void init_matrix(Matrix* matrix, size_t rows, size_t cols) {
    matrix->rows = rows;
    matrix->cols = cols;
    matrix->data = (int64_t*)calloc(rows * cols, sizeof(int64_t));
}

// Free matrix memory (function at 0x1b00)
void free_matrix(Matrix* matrix) {
    if (matrix->data) {
        free(matrix->data);
        matrix->data = NULL;
    }
}

// Get value from matrix (function at 0x1ca0)
bool get_matrix_element(Matrix* matrix, size_t row, size_t col, int64_t* result) {
    if (row >= matrix->rows || col >= matrix->cols) {
        return false;
    }
    
    size_t index = row * matrix->cols + col;
    *result = matrix->data[index];
    return true;
}

// Set value in matrix (function at 0x2180)
bool set_matrix_element(Matrix* matrix, size_t row, size_t col, int64_t value) {
    if (row >= matrix->rows || col >= matrix->cols) {
        return false;
    }
    
    size_t index = row * matrix->cols + col;
    matrix->data[index] = value;
    return true;
}

// Matrix multiplication (function at 0x2630)
bool multiply_matrices(Matrix* matrix_a, Matrix* matrix_b, Matrix* result) {
    // Check compatibility for multiplication
    if (matrix_a->cols != matrix_b->rows || 
        result->rows != matrix_a->rows || 
        result->cols != matrix_b->cols) {
        return false;
    }
    
    for (size_t i = 0; i < matrix_a->rows; i++) {
        for (size_t j = 0; j < matrix_b->cols; j++) {
            int64_t sum = 0;
            for (size_t k = 0; k < matrix_a->cols; k++) {
                int64_t a_val = 0, b_val = 0;
                get_matrix_element(matrix_a, i, k, &a_val);
                get_matrix_element(matrix_b, k, j, &b_val);
                sum += a_val * b_val;
            }
            set_matrix_element(result, i, j, sum);
        }
    }
    
    return true;
}

// Calculate string length (function at 0x3690)
size_t string_length(const char* str) {
    size_t len = 0;
    while (*str++) {
        len++;
    }
    return len;
}

// XOR decryption function (function at 0x38a0)
void xor_decrypt(const char* input) {
    // Hard-coded key from assembly at 0x38a0
    unsigned char key[] = {
        0x0a, 0x12, 0x01, 0x3d, 0x59, 0x75, 0x7a, 0x15,
        0x21, 0x78, 0x20, 0x03, 0x14, 0x34, 0x1d, 0x10,
        0x6d, 0x6b, 0x2c
    };
    
    unsigned char result[19];
    
    // XOR each byte of input with corresponding byte of key
    for (int i = 0; i < 0x12; i++) {
        result[i] = input[i] ^ key[i];
    }
    result[0x12] = '\0';
    
    puts((char*)result);
}

// Print failure message (function at 0x3ea0)
void print_fail_message() {
    puts("Invalid input. Try again.");
}

// Check timing and print flag (function at 0x3fc0)
void check_timing_and_print_flag(char* input) {
    puts("Checking...");
    
    // In the original assembly this has a timing check with rdtsc
    // but we'll simplify and just decrypt the flag
    xor_decrypt(input);
    
    printf("Flag revealed!\n");
}

// Main function (at 0x43e0)
int main() {
    // Stack buffer setup
    char input[0x210] = {0};         // Input buffer
    char processed[0x110] = {0};      // Processed input storage
    bool valid = true;
    
    // Matrix setup
    Matrix matrix_a, matrix_b, matrix_c;
    
    // Initialize matrices (4x4)
    init_matrix(&matrix_a, 4, 4);
    init_matrix(&matrix_b, 4, 4);
    init_matrix(&matrix_c, 4, 4);
    
    // Initialize matrix_a with specific values from the binary
    set_matrix_element(&matrix_a, 0, 0, 0x58);
    set_matrix_element(&matrix_a, 0, 1, 0xffffffffffffffef);
    set_matrix_element(&matrix_a, 0, 2, 0x13);
    set_matrix_element(&matrix_a, 0, 3, 0xffffffffffffffc7);
    set_matrix_element(&matrix_a, 1, 0, 0x2d);
    set_matrix_element(&matrix_a, 1, 1, 0xfffffffffffffff7);
    set_matrix_element(&matrix_a, 1, 2, 0xa);
    set_matrix_element(&matrix_a, 1, 3, 0xffffffffffffffe3);
    set_matrix_element(&matrix_a, 2, 0, 0xffffffffffffffc8);
    set_matrix_element(&matrix_a, 2, 1, 0xb);
    set_matrix_element(&matrix_a, 2, 2, 0xfffffffffffffff4);
    set_matrix_element(&matrix_a, 2, 3, 0x24);
    set_matrix_element(&matrix_a, 3, 0, 0xffffffffffffffd8);
    set_matrix_element(&matrix_a, 3, 1, 0x8);
    set_matrix_element(&matrix_a, 3, 2, 0xfffffffffffffff7);
    set_matrix_element(&matrix_a, 3, 3, 0x1a);
    
    // Print welcome messages
    puts("Welcome to the Matrix Challenge!");
    puts("Enter the correct key to unlock the flag:");
    puts("");
    
    printf("> ");
    
    // Read user input
    int bytes_read = read(0, input, 0x100);
    
    // Remove newline if present
    if (bytes_read > 0) {
        if (input[bytes_read - 1] == '\n') {
            input[bytes_read - 1] = '\0';
        }
    }
    
    // Check input length
    if (string_length(input) != 0x13) { // Must be 19 characters
        print_fail_message();
        return 0;
    }
    
    // Process and validate input
    valid = true;
    int processed_index = 0;
    
    for (int i = 0; i < 0x13; i++) {
        // Check for dash characters at every 5th position
        if (i % 5 == 4) {
            if (input[i] == '-' && valid) {
                valid = true;
            } else {
                valid = false;
            }
        }
        
        // Store character in processed buffer
        processed[processed_index++] = input[i];
        
        // Check if character is uppercase letter (A-Z)
        if (input[i] > '@' && input[i] <= 'Z') {
            // Keep valid as true
        } else {
            valid = false;
        }
    }
    
    if (!valid) {
        print_fail_message();
        return 0;
    }
    
    // Fill matrix_b based on processed input
    for (int i = 0; i <= 3; i++) {
        for (int j = 0; j <= 3; j++) {
            // Calculate matrix element based on character code and position
            char c = processed[i*4 + j];
            int val = (c - 'A') - (i * j);
            set_matrix_element(&matrix_b, i, j, val);
        }
    }
    
    // Multiply matrices to get result matrix_c
    valid = true;
    multiply_matrices(&matrix_a, &matrix_b, &matrix_c);
    
    // Check if result is identity matrix (1s on diagonal, 0s elsewhere)
    for (int i = 0; i <= 3; i++) {
        for (int j = 0; j <= 3; j++) {
            int64_t val;
            get_matrix_element(&matrix_c, i, j, &val);
            
            if (i == j) {
                valid = valid && (val == 1);
            } else {
                valid = valid && (val == 0);
            }
        }
    }
    
    if (!valid) {
        print_fail_message();
        return 0;
    }
    
    // If all checks pass, reveal the flag
    check_timing_and_print_flag(input);
    
    // Clean up resources
    free_matrix(&matrix_a);
    free_matrix(&matrix_b);
    free_matrix(&matrix_c);
    
    return 0;
}