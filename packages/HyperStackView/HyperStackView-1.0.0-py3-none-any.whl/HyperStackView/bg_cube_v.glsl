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

attribute vec3 aPos;
attribute vec3 aNormal;

varying float vDiffuseComponent;

uniform mat4 uMRotate;
uniform mat4 uM;

const vec4 LIGHT_DIRECTION = vec4(-.5, 1, -10, 0);

void main() {
	vec3 diffuseComponent;
	float lightAngleCos;

    gl_Position = vec4(aPos, 1.0) * uM;

	lightAngleCos = dot(normalize(LIGHT_DIRECTION).xyz, normalize(vec4(aNormal, 0.0) * uMRotate).xyz);
	vDiffuseComponent = max(0, -lightAngleCos);
}
