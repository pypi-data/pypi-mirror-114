#include <stdio.h>

#define PIXEL_MIN 0
#define PIXEL_MAX 255

// Helper functions to control minimum and maximum pixel values
int Minimum(int input1, int input2) {
    return input1 < input2 ? input1 : input2;
}

int Maximum(int input1, int input2) {
    return input1 > input2 ? input1 : input2;
}

// Blending functions for multiple images
void AdditionBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = Minimum(image1[i] + image2[i], PIXEL_MAX);
    }
}

void SubtractionBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = Maximum(image1[i] - image2[i], PIXEL_MIN);
    }
}

void MultiplicationBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = (image1[i] * image2[i] / PIXEL_MAX) + 0.5f;
    }
}

void ScreenBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        //result[i] = (1 - (1 - image1[i]) * (1 - image2[i])) / PIXEL_MAX; // This is the first attempt
        //result[i] = PIXEL_MAX - ((image1[i] * image2[i] / PIXEL_MAX) + 0.5f); // Second attempt
        //result[i] = ((1.0f - (1.0f - (float)image1[i] / 255.0f) * (1.0f - (float)image2[i] / 255.0f)) * 255.0f) + 0.5f; // THIS WORKS
        result[i] = ((1.0f - (1.0f - image1[i] / (float)PIXEL_MAX) * (1.0f - image2[i] / (float)PIXEL_MAX)) * (float)PIXEL_MAX) + 0.5f;
    }
}

void RedChannelBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i+= 3) {
        result[i] = Minimum(image1[i] * 3 + image2[i], PIXEL_MAX);
    }
}

void GreenChannelBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 1; i < size; i+= 3) {
        result[i] = Minimum(image1[i] * 3 + image2[i], PIXEL_MAX);
    }
}

void BlueChannelBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 2; i < size; i+= 3) {
        result[i] = Minimum(image1[i] * 3 + image2[i], PIXEL_MAX);
    }
}

void OpacityBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = 0.5 * image1[i] + (1 - 0.5) * image2[i];
    }
}

void OverlayBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        if (image2[i] / (float)PIXEL_MAX <= 0.5f) {
            result[i] = (2.0f * (image1[i] * image2[i] / PIXEL_MAX)) + 0.5f;
        }
        else {
            result[i] = ((1.0f - 2.0f * (1.0f - image1[i] / (float)PIXEL_MAX) * (1.0f - image2[i] / (float)PIXEL_MAX)) * (float)PIXEL_MAX) + 0.5f;
        }
    }
}

void LightenBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        //get lighter of two colors (higher value is lighter)
        result[i] = Maximum(image1[i], image2[i]);
    }
}

void DarkenBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        //get darker of two colors (lower value is darker)
        result[i] = Minimum(image1[i], image2[i]);
    }
}

void ColorDodgeBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        // Check for potential zero division
        if (image1[i] < PIXEL_MAX) {
            //result[i] = ((image2[i] / (PIXEL_MAX - image1[i])) * PIXEL_MAX) + 0.5f;
            result[i] = Minimum((((image2[i] / (float)PIXEL_MAX) / (1.0f - image1[i] / (float)PIXEL_MAX)) * (float)PIXEL_MAX) + 0.5f, PIXEL_MAX);
        }
        else {
            result[i] = PIXEL_MAX;
        }
    }
}

void ColorBurnBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        // Check for potential zero division
        if (image1[i] > PIXEL_MIN) {
            //result[i] = (PIXEL_MAX - ((PIXEL_MAX - image2[i]) / image1[i])) + 0.5f;
            result[i] = Maximum((1.0f - (1.0f - image2[i] / (float)PIXEL_MAX) / (image1[i] / (float)PIXEL_MAX)) * (float)PIXEL_MAX + 0.5f, PIXEL_MIN);
        }
        else {
            result[i] = PIXEL_MIN;
        }
    }
}