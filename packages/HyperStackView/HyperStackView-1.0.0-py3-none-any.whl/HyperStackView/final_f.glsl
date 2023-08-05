#version 330 core
/*
 * HyperStackView -- application for rendering 3D raster images
 * Copyright (C) 2021  Jiří Wolker
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

varying vec4 vTexCoord;

uniform float sampleSz;

uniform float brightnessMax;
uniform float contrastMax;
uniform float gammaMax;

uniform float brightnessAvg;
uniform float contrastAvg;
uniform float gammaAvg;

uniform int binaryEnabled;
uniform float binarySampleSize;
uniform float binaryContrast;
uniform float binarySmoothness;

uniform vec3 colorMax;
uniform vec3 colorAvg;
uniform vec3 binaryObjectColor;

uniform sampler2D tMax;
uniform sampler2D tSum;
uniform sampler2D tNbz;

float color_correction(float value, float brightness, float contrast, float gamma) {
    return clamp(pow(value, gamma) * contrast + brightness, 0, 1);
}

void main() {
    // Inputs from the flattening (intermediate) stage
    float rayMaximum, raySum, nearestBinaryDistance, shadedBinary;

    // Locally calculated values
    float rayAverage;
    vec3 pxColor;

    // Get inputs
    rayMaximum = texture(tMax, vTexCoord.xy).r;
    raySum = texture(tSum, vTexCoord.xy).r;
    nearestBinaryDistance = texture(tNbz, vTexCoord.xy).r;

    // Calculate average from sum
    rayAverage = raySum * sampleSz;

    // Shading of binary data
    shadedBinary = 0;
    if (nearestBinaryDistance > -900 && binaryEnabled > 0) {
        for (float x = 0.01; x < 1; x += binarySampleSize)
            for (float y = 0.01; y < 1; y += binarySampleSize) {
                vec2 offset = vec2(x, y) * binarySmoothness;
                float distance1 = texture(tNbz, vTexCoord.xy + offset).r;
                float distance2 = texture(tNbz, vTexCoord.xy - offset).r;

                shadedBinary += distance2 * .5/(length(offset));
                shadedBinary -= distance1 * .5/(length(offset));
            }
        shadedBinary *= binarySampleSize * binarySampleSize;
        shadedBinary = atan(shadedBinary);
        shadedBinary *= binaryContrast * .5;
        shadedBinary += .5;

        pxColor = shadedBinary * binaryObjectColor;
    }
    else {
        pxColor =
            colorMax * color_correction(rayMaximum, brightnessMax, contrastMax, gammaMax)
        +
            colorAvg * color_correction(rayAverage, brightnessAvg, contrastAvg, gammaAvg)
        ;
    }

    gl_FragColor = vec4(pxColor, 100.);
}
