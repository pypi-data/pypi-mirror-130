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

uniform mat4 uM;
uniform sampler3D tTex;
uniform isampler3D tBinary;
uniform float uNear;
uniform float uFar;
uniform int uZSamples;
uniform float uInputOffset;
uniform float uInputMultiplier;
uniform int uObjectFilter;
uniform int uObjectFilterMode;

layout (location = 0) out vec4 oMax;
layout (location = 1) out vec4 oSum;
layout (location = 2) out float oNbz;

void main() {
    float z, sampleSz, maxProjectionResult, avgProjectionResult, weightedProjectionResult, binaryZResult, vxValue, binaryValue;
    vec4 vxCoord;
    bool objectFilterMatch;

    maxProjectionResult = 0;
    avgProjectionResult = 0;
    weightedProjectionResult = 0;
    binaryZResult = -1000.;

    sampleSz = abs(uFar - uNear) / uZSamples;
    for (z = uFar; z < uNear; z += sampleSz) {
        vxCoord = (vTexCoord + vec4(0.0, 0.0, z, 0.0)) * uM;
        vxCoord = vxCoord / vxCoord.w;
        objectFilterMatch = texture(tBinary, vxCoord.xyz).r == (uObjectFilter + 0.0);
        if (uObjectFilterMode != 1 || objectFilterMatch) {
            vxValue = texture(tTex, vxCoord.xyz).r;
            vxValue += uInputOffset;
            vxValue *= uInputMultiplier;

            if (uObjectFilterMode != 2 || objectFilterMatch) {
                binaryZResult = (texture(tBinary, vxCoord.xyz).r != 0.0) ? z : binaryZResult;
            }

            maxProjectionResult = max(maxProjectionResult, vxValue);
            avgProjectionResult += vxValue;
            weightedProjectionResult = .12 * vxValue / (5 + z * z / 2)
            + (1 - .12 * vxValue / (5 + z * z / 2)) * weightedProjectionResult;
        }
    }

    oSum = vec4(avgProjectionResult);
    oMax = vec4(maxProjectionResult);
    oNbz = binaryZResult;
}
